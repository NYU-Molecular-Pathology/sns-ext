#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Functions for cleaning up after an analysis is finished
'''
# ~~~~~ LOGGING ~~~~~~ #
import os
import sys
import shutil
import yaml
from util import tools
import logging
import config

logger = logging.getLogger(__name__)


# ~~~~~ LOAD CONFIGS ~~~~~ #
configs = config.config


# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
def save_configs(analysis_dir):
    '''
    Save the global configs to the analysis dir
    '''
    # save the configs to a YAML file
    output_config_yaml = os.path.join(analysis_dir, 'snsxt_config.yml')
    logger.debug('Saving program configs to file: {0}'.format(output_config_yaml))
    with open(output_config_yaml, 'w') as outfile:
        yaml.dump(configs, outfile, default_flow_style = False)

def analysis_complete(analysis):
    '''
    Actions to take after an analysis is done

    analysis is an SnsWESAnalysisOutput object
    '''
    analysis_dir = analysis.dir
    save_configs(analysis_dir)
