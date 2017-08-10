#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Functions & items to set up the program loggers
'''

import yaml
import logging
import logging.config
import os


# ~~~~~ FUNCTIONS ~~~~~ #
def timestamp():
    '''
    Return a timestamp string
    '''
    import datetime
    return('{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))

def logpath(logfile = 'log.txt'):
    '''
    Return the path to the main log file; needed by the logging.yml
    use this for dynamic output log file paths & names
    '''
    return(logging.FileHandler(logfile))

def log_setup(config_yaml, logger_name):
    '''
    Set up the logger for the script using a YAML config file
    config = path to YAML config file
    '''
    # Config file relative to this file
    loggingConf = open(config_yaml, 'r')
    logging.config.dictConfig(yaml.load(loggingConf))
    loggingConf.close()
    return(logging.getLogger(logger_name))

def logger_filepath(logger, handler_name):
    '''
    Get the path to the filehander log file
    '''
    log_file = None
    for h in logger.__dict__['handlers']:
        if h.__class__.__name__ == 'FileHandler':
            logname = h.get_name()
            if handler_name == logname:
                log_file = h.baseFilename
    return(log_file)

def get_logger_handler(logger, handler_name, handler_type = 'FileHandler'):
    '''
    Get the filehander object from a logger
    '''
    for h in logger.__dict__['handlers']:
        if h.__class__.__name__ == handler_type:
            logname = h.get_name()
            if handler_name == logname:
                return(h)

def add_handlers(logger, handlers):
    '''
    Add filehandlers to the logger
    '''
    # handlers = None
    if handlers == None:
        return(logger)
    # handlers is assumed to be a single handler if its not a list
    if not isinstance(handlers, list):
        logger.addHandler(handlers)
    # otherwise its assumed to be a list of handlers
    else:
        for h in handlers:
            logger.addHandler(h)
    return(logger)


def build_logger(name, level = logging.DEBUG, log_format = '[%(asctime)s] (%(name)s:%(funcName)s:%(lineno)d:%(levelname)s) %(message)s'):
    '''
    Create a basic logger instance
    Only add console handler by default
    '''
    # create logger instance
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler
    consolelog = logging.StreamHandler()
    consolelog.setLevel(level)
    consolelog.set_name("console")

    # create formatter and add it to the handlers
    formatter = logging.Formatter(log_format)
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    consolelog.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(consolelog)
    # logger.addHandler(create_main_filehandler())
    return(logger)

def create_main_filehandler(log_file, name = "main", level = logging.DEBUG, log_format = '%(asctime)s:%(name)s:%(module)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s'):
    '''
    Return the 'main' file handler using globally set variables
    '''
    # global scriptdir
    # global scriptname
    # global logdir
    # file_timestamp = timestamp()
    # log_file = os.path.join(scriptdir, logdir, '{0}.{1}.log'.format(scriptname, file_timestamp))
    formatter = logging.Formatter(log_format)
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    mainhandler = logging.FileHandler(log_file)
    mainhandler.setLevel(level)
    mainhandler.set_name(name)
    mainhandler.setFormatter(formatter)
    return(mainhandler)



# ~~~~~ GLOBALS ~~~~~ #
# can also be reset by other modules
# script_timestamp = timestamp()
# scriptdir = os.path.dirname(os.path.realpath(__file__))
# scriptname = os.path.basename(__file__)
# logdir = os.path.join(scriptdir, 'logs')
#
# main_filehandler = create_main_filehandler()