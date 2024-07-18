import logging

def setup_logging(log_file='my_log.log'):
    fmt = "%(asctime)s.%(msecs)03d|%(thread)d|%(levelname)s|%(name)s->%(funcName)s():%(lineno)d -> %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.DEBUG, 
        filename=log_file, 
        filemode='w', 
        format=fmt, 
        datefmt=datefmt
    )
    
    return logging.getLogger(__name__)
    