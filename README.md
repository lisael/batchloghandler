batchloghandler
===============

Python logging handler to log debug info only if an error occured


Usage
-----

read test.py for usage details and a dict config example.

```
>>> import logging
>>> import batchloghandler
>>> handler = batchloghandler.BatchLogHandler(logging.StreamHandler, "INFO", "ERROR")
>>> handler.setLevel(logging.DEBUG)
>>> logger = logging.getLogger()
>>> logger.setLevel(logging.DEBUG)
>>> logger.addHandler(handler)
>>> logger.info('info1')
info1
>>> logger.debug('debug1')
>>> batchloghandler.record()
>>> logger.debug('debug2')
>>> logger.info('info2')
info2
>>> logger.debug('debug3')
>>> logger.error('error1')
debug2
debug3
error1
>>> # recorded debugs are emited. From now on the logger will work as a regular debug logger
... 
>>> logger.debug('debug4')
debug4
>>> batchloghandler.stop()
>>> # back to the original behaviour: log info and do not record
... 
>>> logger.info('info3')
info3
>>> logger.debug('debug5')
>>> logger.error('error2')
error2
>>> 
```
