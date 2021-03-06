# batchloghandler

Python logging handler to log debug info only if an error occured


## Usage

read test.py for usage details and a dict config example.

### Vanilla python

- import

```
>>> import logging
>>> import batchloghandler
```
- intitialize the handler
  - BatchLogHndler takes at least 3 params :
    - backend handler (where the log lines are finally sent)
    - normal log level (this level and above will allways be logged directly)
    - trigger level (the log level that triggers the flush of saved log lines)
  - additionnal named parameters are passed to the backend handler's constructor  
  
the result is an instance of a Handler inheriting from BatchLogHandlerBase and the backend handler

```
>>> handler = batchloghandler.BatchLogHandler(logging.StreamHandler, "INFO", "ERROR")
```
- set the handler minimal log level
```
>>> handler.setLevel(logging.DEBUG)
```
- attach the hanlder to the logger
```
>>> logger = logging.getLogger()
>>> logger.setLevel(logging.DEBUG)
>>> logger.addHandler(handler)
```
- the logger works as expected at normal log level
```
>>> logger.info('info1')
info1
```
- and it hopefully swallows lower levels
```
>>> logger.debug('debug1')
```
- from now on, the handler will record lower level log lines
```
>>> batchloghandler.record()
```
- let's do it
```
>>> logger.debug('debug2')
>>> logger.info('info2')
info2
>>> logger.debug('debug3')
>>> logger.error('error1')
debug2
debug3
error1
```
- recorded debugs are emited. From now on the logger will work as a regular debug logger
```
>>> logger.debug('debug4')
debug4
```
- stop recording. Back to the original behaviour: log info and do not record anything
```
>>> batchloghandler.stop()
>>> logger.info('info3')
info3
>>> logger.debug('debug5')
>>> logger.error('error2')
error2
>>> 
```

### Django

Just add this in your settings (the middleware must be as near of the top as possible to handle other middlewares logs):

```python
MIDDLEWARE_CLASSES = (
    'batchloghandler.django_utils.Middleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    '...'
)

import logging
LOGGING = {
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
            # 'stream': StringIO.StringIO()
        },
    },
    'loggers': {
        # this is used internally by django, you should add this.
        'django': {
            'handlers': ['batch'],
            'level': 'DEBUG',
        },
        'my_test_app': {
            'handlers': ['batch'],
            'level': 'DEBUG',
        },
    },
}
```
