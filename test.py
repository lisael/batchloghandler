from unittest import TestCase
from logging.config import dictConfig
import logging
from StringIO import StringIO

from batchloghandler import record, stop

STREAM = StringIO()

CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'batch':{
            ## logging stuff to instanciate the handler
            '()': 'ext://batchloghandler.BatchLogHandler',
            'level':'DEBUG',
            'formatter': 'default',
            ## batchloghandler args
            # the backend handler, where to log
            'blh_backend': logging.StreamHandler,
            # logs over this level are allways emited
            'blh_bypass_level': 'INFO',
            'blh_trigger_level': 'ERROR',
            ## these keywords are passed to the backend handler constructor
            'stream': STREAM,
        },
    },
    'root': {
        'handlers': ['batch'],
        'level': 'DEBUG',
    },
}

dictConfig(CONFIG)


class TestBatchHandler(TestCase):
    def setUp(self):
        STREAM.truncate(0)
        self.logger= logging.getLogger()

    def test_bypass(self):
        self.logger.info('an info')
        self.assertEquals(STREAM.getvalue(),
                "INFO root an info\n")
        STREAM.truncate(0)
        self.logger.warning('a warning')
        self.assertEquals(STREAM.getvalue(),
                "WARNING root a warning\n")
        STREAM.truncate(0)
        self.logger.debug('a debug')
        self.assertEquals(STREAM.getvalue(),"")

    def test_recording(self):
        self.logger.debug('debug 1')
        self.assertEquals(STREAM.getvalue(), "")

        record()

        self.logger.debug('debug 2')
        self.assertEquals(STREAM.getvalue(), "")

        self.logger.info('info 1')
        self.assertEquals(STREAM.getvalue(),
                "INFO root info 1\n")

        STREAM.truncate(0)
        self.logger.debug('debug 3')
        self.assertEquals(STREAM.getvalue(), "")
        self.logger.error('error 1')
        self.assertEquals(STREAM.getvalue(),
                "DEBUG root debug 2\n" +
                "DEBUG root debug 3\n" +
                "ERROR root error 1\n"
                )

        STREAM.truncate(0)

        stop()

        self.logger.debug('debug 1')
        self.assertEquals(STREAM.getvalue(), "")

        record()

        self.logger.debug('debug 2')
        self.assertEquals(STREAM.getvalue(), "")

        self.logger.info('info 1')
        self.assertEquals(STREAM.getvalue(),
                "INFO root info 1\n")

        STREAM.truncate(0)
        self.logger.debug('debug 3')
        self.assertEquals(STREAM.getvalue(), "")
        self.logger.error('error 1')
        self.assertEquals(STREAM.getvalue(),
                "DEBUG root debug 2\n" +
                "DEBUG root debug 3\n" +
                "ERROR root error 1\n"
                )


