import os
import logging
import logzero

from logzero import logger

if os.environ.get('ENVIRONMENT') == 'DEV':
    logzero.loglevel(logging.DEBUG)

elif os.environ.get('ENVIRONMENT') == 'PROD':
    logzero.loglevel(logging.INFO)
    logzero.logfile("./api.log")

logger = logger
