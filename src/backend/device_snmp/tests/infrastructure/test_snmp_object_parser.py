import pytest
from backend.device_snmp.infrastructure.snmp_object_parser import SnmpObjectParser

parser = SnmpObjectParser()


def test_get_snmp_walk_fixed_rows():
    error_file_rows = [
        ".1.3.6.1.2.1.1.1.0 = STRING: Cisco IOS Software [Everest], Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Version 16.6.3, RELEASE SOFTWARE (fc8)",
        "Technical Support: http://www.cisco.com/techsupport",
        "Copyright (c) 1986-2018 by Cisco Systems, Inc."
    ]
    expected = [
        ".1.3.6.1.2.1.1.1.0 = STRING: Cisco IOS Software [Everest], Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Version 16.6.3, RELEASE SOFTWARE (fc8) Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2018 by Cisco Systems, Inc."]
    result = parser.get_fixed_rows(error_file_rows)

    assert expected == result


def test_get_snmp_rec_fixed_rows():
    error_rows = [
        "1.3.6.1.2.1.1.1.0|4|Cisco StarOS Software, ASR5000 Intelligent Mobile Gateway,",
        "Version 17.0.0.57028,",
        "Copyright (c) 2014 by Cisco Systems, Inc"
    ]
    expected = [
        '1.3.6.1.2.1.1.1.0|4|Cisco StarOS Software, ASR5000 Intelligent Mobile Gateway, Version 17.0.0.57028, Copyright (c) 2014 by Cisco Systems, Inc']
    result = parser.get_fixed_rows(error_rows)
    assert expected == result


def test_parse_oid_values():
    snmp_oids_parser = {
        1: [
            {'numeric': '1', 'literal': 'iso', 'parent': 'iso'},
        ],
        2: [
            {'numeric': '3', 'literal': 'org', 'parent': 'iso'}
        ],
        3: [
            {'numeric': '8802', 'literal': 'dod', 'parent': 'org'},
        ],
        4: [
            {'numeric': '1', 'literal': 'internet', 'parent': 'dod'}
        ],
        5: [
            {'numeric': '2', 'literal': 'other', 'parent': 'internet'},
            {'numeric': '1', 'literal': 'private', 'parent': 'internet'}
        ],
        6: [
            {'numeric': '1', 'literal': 'enterprises', 'parent': 'other'},
        ],
        7: [
            {'numeric': '1', 'literal': 'hrSWRunParameters', 'parent': 'enterprises'},
        ],
    }
    parser.set_translator_data(snmp_oids_parser)
    snmp_list = [
        'HOST-RESOURCES-MIB::hrSWRunParameters.6621 = "--daemon --address=10.60.35.2 --config=/etc/rsyncd-cmi.conf"',
        'HOST-RESOURCES-MIB::other.5555 = STRING: "--daemon --addresafsdss=10.60.35.2 --config=/etc/rsyncd-cmi.conf"'
    ]
    result = parser.get_oid_values_parsed(snmp_list)
    expected = ['1.3.8802.1.2.1.1.6621 = STRING: "--daemon --address=10.60.35.2 --config=/etc/rsyncd-cmi.conf"',
                '1.3.8802.1.2.5555 = STRING:  "--daemon --addresafsdss=10.60.35.2 --config=/etc/rsyncd-cmi.conf"']
    assert expected == result


def test_parse_oid_with_ips():
    snmp_oids_parser = {
        1: [
            {'numeric': '1', 'literal': 'iso', 'parent': 'iso'},
        ],
        2: [
            {'numeric': '3', 'literal': 'org', 'parent': 'iso'}
        ],
        3: [
            {'numeric': '8802', 'literal': 'dod', 'parent': 'org'},
        ],
        4: [
            {'numeric': '1', 'literal': 'internet', 'parent': 'dod'},
            {'numeric': '1', 'literal': 'ipv4', 'parent': 'dod'}
        ],
        5: [
            {'numeric': '2', 'literal': 'other', 'parent': 'internet'},
            {'numeric': '1', 'literal': 'private', 'parent': 'internet'}
        ],
        6: [
            {'numeric': '1', 'literal': 'enterprises', 'parent': 'other'},
        ],
        7: [
            {'numeric': '1', 'literal': 'ipNetToPhysicalRowStatus', 'parent': 'enterprises'},
        ],
    }
    parser.set_translator_data(snmp_oids_parser)
    snmp_list = [
        'IP-MIB::ipNetToPhysicalRowStatus.432.ipv4."10.60.35.21".432."10.60.35.21".ipv4."10.60.35.21" = INTEGER: active(1)',
        'HOST-RESOURCES-MIB::other.5555 = STRING: "--daemon --addresafsdss=10.60.35.2 --config=/etc/rsyncd-cmi.conf"'
    ]
    result = parser.get_oid_values_parsed(snmp_list)
    expected = [
        '1.3.8802.1.2.1.1.432.1.3.8802.1."10.60.35.21".432."10.60.35.21".1.3.8802.1."10.60.35.21" = INTEGER:  active(1)',
        '1.3.8802.1.2.5555 = STRING:  "--daemon --addresafsdss=10.60.35.2 --config=/etc/rsyncd-cmi.conf"']
    assert expected == result


def test_parse_snmp_rec_objects_to_walk():
    snmp_list = [
        '.1.3.6.1.2.1.1|4|Cisco StarOS Software, ASR5000 Intelligent Mobile Gateway, Version 17.0.0.57028, Copyright (c) 2014 by Cisco Systems, Inc',
        '.1.0.8802.1.1.2.1|4|topology/pod-1/node-103',
        '.1.0.8802.1.1.2.1|2|3'
        '.1.0.8802.1.1.2.1|2|3'
    ]
    result = parser.parse_rec_to_walk(snmp_list)
    expected = [
        '.1.3.6.1.2.1.1 = INTEGER: Cisco StarOS Software, ASR5000 Intelligent Mobile Gateway, Version 17.0.0.57028, Copyright (c) 2014 by Cisco Systems, Inc',
        '.1.0.8802.1.1.2.1 = INTEGER: topology/pod-1/node-103',
        '.1.0.8802.1.1.2.1 = OID: 3.1.0.8802.1.1.2.1|2|3'
    ]
    assert expected == result


def test_parse_snmp_walk_objects_to_rec():
    snmp_list = [
        '.1.3.6.1.2.1.1 = INTEGER: Cisco StarOS Software, ASR5000 Intelligent Mobile Gateway, Version 17.0.0.57028, Copyright (c) 2014 by Cisco Systems, Inc',
        '.1.0.8802.1.1.2.1 = INTEGER: topology/pod-1/node-103',
        '.1.0.8802.1.1.2.1 = OID: 3.1.0.8802.1.1.2.1|2|3'
    ]
    result = parser.parse_walk_to_rec(snmp_list)
    expected = [
        '.1.3.6.1.2.1.1|4|Cisco StarOS Software, ASR5000 Intelligent Mobile Gateway, Version 17.0.0.57028, Copyright (c) 2014 by Cisco Systems, Inc',
        '.1.0.8802.1.1.2.1|4|topology/pod-1/node-103',
        '.1.0.8802.1.1.2.1|2|3'
        '.1.0.8802.1.1.2.1|2|3'
    ]
    assert expected == result
