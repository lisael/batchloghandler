import batchloghandler

LOGGER_NAMES = []


def reset_logger_list():
    global LOGGER_NAMES
    from django.conf import settings
    loggers = settings.LOGGING.get('loggers', {})
    LOGGER_NAMES = loggers.keys()


class Middleware(object):

    def __init__(self):
        reset_logger_list()

    def process_request(self, request):
        for name in LOGGER_NAMES:
            batchloghandler.record(name)

    def process_exception(self, request, exception):
        for name in LOGGER_NAMES:
            batchloghandler.flush(name)
            batchloghandler.stop(name)

    def process_response(self, request, response):
        for name in LOGGER_NAMES:
            batchloghandler.stop(name)
        return response
