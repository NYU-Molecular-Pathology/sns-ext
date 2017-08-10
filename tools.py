#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
General utility functions and classes for the program
'''
import logging
logger = logging.getLogger("tools")
logger.debug("loading tools module")

import sys
import os
import datetime
import csv
import json
import yaml

# ~~~~ CUSTOM CLASSES ~~~~~~ #
class Container(object):
    '''
    basic container for information
    '''
    pass


# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
def my_debugger(vars):
    '''
    starts interactive Python terminal at location in script
    very handy for debugging
    call this function with
    my_debugger(globals().copy())
    anywhere in the body of the script, or
    my_debugger(locals().copy())
    within a script function
    '''
    import readline # optional, will allow Up/Down/History in the console
    import code
    # vars = globals().copy() # in python "global" variables are actually module-level
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

def subprocess_cmd(command, return_stdout = False):
    # run a terminal command with stdout piping enabled
    import subprocess as sp
    process = sp.Popen(command,stdout=sp.PIPE, shell=True, universal_newlines=True)
     # universal_newlines=True required for Python 2 3 compatibility with stdout parsing
    proc_stdout = process.communicate()[0].strip()
    if return_stdout == True:
        return(proc_stdout)
    elif return_stdout == False:
        logger.debug(proc_stdout)

def timestamp():
    '''
    Return a timestamp string
    '''
    return('{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now()))

def print_dict(mydict):
    '''
    pretty printing for dict entries
    '''
    for key, value in mydict.items():
        logger.debug('{}: {}\n\n'.format(key, value))

def mkdirs(path, return_path=False):
    '''
    Make a directory, and all parent dir's in the path
    '''
    import sys
    import os
    import errno
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    if return_path:
        return path

def write_dicts_to_csv(dict_list, output_file):
    '''
    write a list of dicts to a CSV file
    '''
    with open(output_file, 'w') as outfile:
        fp = csv.DictWriter(outfile, dict_list[0].keys())
        fp.writeheader()
        fp.writerows(dict_list)

def backup_file(input_file, return_path=False, sys_print = False):
    '''
    backup a file by moving it to a folder called 'old' and appending a timestamp
    '''
    if os.path.isfile(input_file):
        filename, extension = os.path.splitext(input_file)
        new_filename = '{0}.{1}{2}'.format(filename, timestamp(), extension)
        new_filename = os.path.join(os.path.dirname(new_filename), "old", os.path.basename(new_filename))
        mkdirs(os.path.dirname(new_filename))
        logger.debug('\nBacking up old file:\n{0}\n\nTo location:\n{1}\n'.format(input_file, new_filename))
        if sys_print == True:
            logger.debug('''
To undo this, run the following command:\n
mv {0} {1}
'''.format(os.path.abspath(input_file), new_filename)
            )
        os.rename(input_file, new_filename)
    if return_path:
        return input_file

def print_json(object):
    '''
    Pretty printing of JSON formatted object to logger
    helps with easier viewing of heavily nested objects
    '''
    logger.debug(json.dumps(object, sort_keys=True, indent=4))

def json_dumps(object):
    '''
    Return object in JSON format
    '''
    return(json.dumps(object, sort_keys=True, indent=4))


def write_json(object, output_file):
    '''
    Write an object to JSON format
    '''
    with open(output_file,"w") as f:
        json.dump(object, f, sort_keys=True, indent=4)

def load_json(input_file):
    '''
    Load an object from JSON file
    '''
    with open(input_file,"r") as f:
        x = json.load(f)
    return(x)

def write_yaml(object, output_file):
    '''
    Write an object to YAML output formatted file
    '''
    with open(output_file, 'w') as outfile:
        yaml.dump(object, outfile, default_flow_style = False)

def load_yaml(input_file):
    '''
    Load a YAML formatted file
    '''
    with open(input_file, "r") as f:
        x = yaml.load(f)
        return(x)
