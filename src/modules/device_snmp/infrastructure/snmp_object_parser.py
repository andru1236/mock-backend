import re
from enum import Enum
from aenum import MultiValueEnum

SNMPREC = 1
SNMPWALK = 2
WALK = 3


class Validator(object):
    SNMPREC_ROW_PATTERN = r'^[0-9\.]+\|+[0-9x]+\|+[a-zA-Z0-9]{0,}'
    SNMPWALK_ROW_PATTERN = r'^[\.][0-9\.]+ = +[a-zA-Z0-9\"]'
    WALK_ROW_PATTERN = r'([a-zA-Z0-9-]+\:{2})([a-zA-Z.0-9\"]{1,})( \= )([A-Za-z0-9]{0,})(\:{0,})(.{0,})'

    def is_valid_row(self, row, pattern):
        return self.__is_valid_row(row, pattern)

    def get_row_format_pattern(self, row_value):
        if self.__is_valid_row(row_value, self.SNMPREC_ROW_PATTERN):
            return self.SNMPREC_ROW_PATTERN
        elif self.__is_valid_row(row_value, self.SNMPWALK_ROW_PATTERN):
            return self.SNMPWALK_ROW_PATTERN
        elif self.__is_valid_row(row_value, self.WALK_ROW_PATTERN):
            return self.WALK_ROW_PATTERN
        else:
            print("Format not defined")

    def __is_valid_row(self, row_value, pattern):
        p = re.compile(pattern)
        return p.match(row_value)


class SnmpType(MultiValueEnum):
    TYPE9 = '6', "STRING"
    TYPE2 = '2', "OID"
    TYPE1 = '4', "INTEGER"
    TYPE3 = '67', "Hex-STRING"
    TYPE4 = '66', "Timeticks"
    TYPE5 = '65', "Gauge32"
    TYPE6 = '70', "Counter32"
    TYPE7 = '4x', "IpAddress"
    TYPE8 = '72x', "Counter64"
    TYPE10 = '64x', "OBJECT IDENTIFIER"


class TranslatorMessages(Enum):
    OPTION_TO_PARSE_ERROR = 'you entered a unavailable option to parse.'
    TRANSLATION_DO_NOT_EXISTS = 'there are not translation for {1} value.'
    ACTION_NOT_VALID = 'the action that you entered do not exists.'
    PARAMETERS_ERROR = 'Is necessary minimum two parameters. \n action, file_path, path_to_generate_result.'


class Translator(object):
    """ FileParserClass.
    This class will parse snmp files
    """

    translation_options = ['numeric', 'literal']

    def __init__(self, snmp_oids_data={}):
        self.snmp_oids_parser = snmp_oids_data

    def translate_oid_element(self, level, oid_value, parent_value, type_to_parse):
        convert_direction = self.__get_translation_direction(type_to_parse)
        possibles = self.snmp_oids_parser.get(level)
        for possible in possibles:
            if (level == 1) or (possible.get(convert_direction[0]) == oid_value) and (
                    possible.get('parent') == parent_value):
                return [possible.get(convert_direction[1]), possible.get('literal')]
        raise ValueError(TranslatorMessages.TRANSLATION_DO_NOT_EXISTS.value.format(type_to_parse, oid_value))

    def build_complete_oid(self, oid_label):
        result_oid = []
        to_search = oid_label
        while to_search != 'iso':
            for key in self.snmp_oids_parser:
                for possible in self.snmp_oids_parser.get(key):
                    if possible.get('literal') == to_search:
                        result_oid.insert(0, possible.get('numeric'))
                        to_search = possible.get('parent')
                        break
        result_oid.insert(0, '1')
        if result_oid:
            return result_oid
        else:
            raise ValueError(TranslatorMessages.TRANSLATION_DO_NOT_EXISTS.value.format(to_search))

    def __get_translation_direction(self, type_to_parse):
        if type_to_parse in self.translation_options:
            return self.translation_options if type_to_parse == 'literal' else list(reversed(self.translation_options))
        else:
            raise ValueError(TranslatorMessages.OPTION_TO_PARSE_ERROR.value)


class SnmpObjectParser(object):
    """ FileParserClass.
    This class will parse snmp files
    """

    REC_TYPE_FORMAT = '{0}|{1}|{2}'
    """ REC TYPE FORMAT
    {0} snmp object OID.
    {1} snmp object TYPE in number value
    {2} smnp object Value
    """

    WALK_TYPE_FORMAT = '{0} = {1}: {2}'
    """ WALK TYPE FORMAT
        {0} snmp object OID.
        {1} snmp object literal TYPE
        {2} smnp object Value
    """

    IP_PATTERN = r'\"[0-9\.]{0,}\"'

    def __init__(self):
        self.validator = Validator()
        self.translator = Translator()

    def set_translator_data(self, data):
        self.translator.snmp_oids_parser = data

    def get_oid_values_parsed(self, snmp_objects_list, file_type_to_generate='snmpwalk'):
        """
        :param snmp_objects_list: valid snmp object list.
        :param file_type_to_generate: result format that you want to be generated, default is snmprec.
        :return: return a list of snmp objects with OID's values translated to value of param 'to_parse'.
        """
        parse_format = self.REC_TYPE_FORMAT if file_type_to_generate == 'snmprec' else self.WALK_TYPE_FORMAT
        translated_objects = []
        parse_pattern = self.validator.get_row_format_pattern(snmp_objects_list[0])
        regex = re.compile(parse_pattern)
        for snmp_object in snmp_objects_list:
            result = regex.match(snmp_object)
            oid = result.group(2)
            type = result.group(4) if result.group(4) != '' else 'STRING'
            value = result.group(6)
            oid = self.__parse_oid(oid)
            translated_objects.append(parse_format.format(oid, type, value))
        return translated_objects

    def get_fixed_rows(self, file_rows):
        """
        :param file_rows: File rows that have errors.
        :return: fixed list of snmp objects.
        """
        pattern = self.validator.get_row_format_pattern(file_rows[0])
        generated_file_rows = []
        for row in file_rows:
            if self.validator.is_valid_row(row, pattern):
                generated_file_rows.append(row)
            else:
                completed_row = generated_file_rows[-1] + ' {0}'.format(row)
                generated_file_rows[-1] = re.sub(' +', ' ', completed_row)
        return generated_file_rows

    def parse_rec_to_walk(self, file_rows):
        """
        :param file_rows: valid snmp file rows in rec format.
        :return: file rows translated to snmp walk rows.
        """
        generated_rows = []
        for row in file_rows:
            operator_indexes = self.__get_indexes_for(row, '|', '|')
            if len(operator_indexes) < 2:
                operator_indexes.append(operator_indexes[-1])
                snmp_object_type = 'STRING'
            else:
                snmp_object_type = row[operator_indexes[0] + 1: operator_indexes[1]].strip()
            snmp_iod_value = row[: operator_indexes[0]].strip()
            snmp_object_value = row[operator_indexes[1] + 1:].strip()
            snmp_object_type = self.__get_walk_value(snmp_object_type)
            walk_row = self.WALK_TYPE_FORMAT.format(snmp_iod_value, snmp_object_type, snmp_object_value)
            generated_rows.append(walk_row)
        return generated_rows

    def parse_walk_to_rec(self, file_rows):
        """
        :param file_rows: valid snmp file rows in walk format.
        :return: file rows translated to snmp rec rows.
        """
        generated_rows = []
        for row in file_rows:
            operator_indexes = self.__get_indexes_for(row, '=', ':')
            if len(operator_indexes) < 2:
                operator_indexes.append(operator_indexes[-1])
            else:
                snmp_object_type = row[operator_indexes[0] + 1: operator_indexes[1]].strip()
            snmp_iod_value = row[: operator_indexes[0]].strip()
            snmp_object_value = row[operator_indexes[1] + 1:].strip()
            snmp_object_type = self.__get_rec_value(snmp_object_type)
            walk_row = self.REC_TYPE_FORMAT.format(snmp_iod_value, snmp_object_type, snmp_object_value)
            generated_rows.append(walk_row)
        return generated_rows

    def get_type_of_agent_db(self, agent_db):
        file_rows = agent_db.split("\n")
        pattern = self.validator.get_row_format_pattern(file_rows[0])
        if pattern == self.validator.SNMPREC_ROW_PATTERN:
            return SNMPREC
        if pattern == self.validator.SNMPWALK_ROW_PATTERN:
            return SNMPWALK

    def __parse_oid(self, oid):
        oid_list = self.__get_splited_oid(oid)
        result = []
        for oid_element in oid_list:
            completed_oid = [oid_element]
            if not (self.__is_machine_ip(oid_element) or oid_element.isdigit()):
                completed_oid = self.translator.build_complete_oid(oid_element)
            result.extend(completed_oid)
        return '.'.join(result)

    def __is_machine_ip(self, oid):
        regex = re.compile('(\"[0-9.]{0,}\")')
        return regex.match(oid)

    def __get_splited_oid(self, oid):
        result = []
        oid_list = oid.split('.')
        parsing_ip = False
        actual_oid = ""
        for oid in oid_list:
            actual_oid = actual_oid + oid
            if '\"' in oid:
                parsing_ip = not parsing_ip
            if not parsing_ip:
                result.append(actual_oid)
                actual_oid = ""
            else:
                actual_oid = actual_oid + '.'
        return result

    def __get_separated_snmp_object(self, snmp_object, file_type):
        if file_type == 'snmprec':
            first_point, second_point = '|', '|'
        else:
            first_point, second_point = '=', ':'
        operator_indexes = self.__get_indexes_for(snmp_object, first_point, second_point)
        if len(operator_indexes) < 2:
            operator_indexes.append(operator_indexes[-1])
            snmp_object_type = 'STRING'
        else:
            snmp_object_type = snmp_object[operator_indexes[0] + 1: operator_indexes[1]].strip()
        snmp_object_oid = snmp_object[: operator_indexes[0]].strip()
        snmp_object_value = snmp_object[operator_indexes[1] + 1:].strip()
        return [snmp_object_oid, snmp_object_type, snmp_object_value]

    def __get_walk_value(self, snmp_object_type):
        enum = SnmpType(snmp_object_type)
        return SnmpType(enum).values[1]

    def __get_rec_value(self, snmp_object_type):
        enum = SnmpType(snmp_object_type)
        return SnmpType(enum).values[0]

    def __get_indexes_for(self, row, start_value, end_value):
        return [i for i, value in enumerate(row) if (value == start_value) or (value == end_value)]
