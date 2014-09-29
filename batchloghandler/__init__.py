import logging

PASSING = 0
FILTERING = 1
INACTIVE = 2


class BatchLogHandlerBase(object):
    def __init__(self, blh_bypass_level, blh_trigger_level, **kwargs):
        # TODO: backend can be a string
        super(BatchLogHandlerBase, self).__init__(**kwargs)
        # TODO: logging levels can be ints
        self.bypass_level = getattr(logging, blh_bypass_level)
        self.trigger_level = getattr(logging, blh_trigger_level)
        self.status = INACTIVE
        self.records = []

    def stop_recording(self):
        self.status = INACTIVE
        self.records = []

    def start_recording(self):
        self.status = FILTERING

    def flush_records(self):
        while self.records:
            super(BatchLogHandlerBase, self).handle(self.records.pop(0))
        self.status = PASSING

    def handle(self, record):
        if self.status == FILTERING and record.levelno >= self.trigger_level:
            self.flush_records()
        if record.levelno >= self.bypass_level or self.status == PASSING:
            return super(BatchLogHandlerBase, self).handle(record)
        if self.status == FILTERING:
            self.records.append(record)


def record(*args):
    logger = logging.getLogger(*args)
    [h.start_recording() for h in logger.handlers
        if isinstance(h, BatchLogHandlerBase)]


def stop(*args):
    logger = logging.getLogger(*args)
    [h.stop_recording() for h in logger.handlers
        if isinstance(h, BatchLogHandlerBase)]


def flush(*args):
    logger = logging.getLogger(*args)
    [h.flush_records() for h in logger.handlers
        if isinstance(h, BatchLogHandlerBase)]


def BatchLogHandler(blh_backend, blh_bypass_level,
                    blh_trigger_level, **kwargs):
    cls = type('Batch{}'.format(blh_backend.__name__),
               (BatchLogHandlerBase, blh_backend), {})
    return cls(blh_bypass_level, blh_trigger_level, **kwargs)
