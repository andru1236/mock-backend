import os
import logging
import logzero

from logzero import logger

print('URL data base: ', os.environ.get('MONGO_CONNECTION'))
print('Data base name: ', os.environ.get('DB_NAME_MONGO'))
print('Environment', os.environ.get('ENV'))

if os.environ.get('ENV') == 'DEV':
    logzero.loglevel(logging.DEBUG)

elif os.environ.get('ENV') == 'PROD':
    logzero.loglevel(logging.INFO)
    logzero.logfile("./erp.log")

logger = logger
