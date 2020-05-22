import logging


def logger():
    log = logging.basicConfig()
    log = logging.getLogger('DesafioBigData')
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("{'name':'%(name)s',\
'pid':'%(process)d',\
'time':'%(asctime)s',\
'level':'%(levelname)s',\
'message':'%(message)s'}", "%y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.propagate = False
    return log


log = None
log = logger()
