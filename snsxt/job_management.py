#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Functions for custom management of compute cluster qsub jobs
'''
# ~~~~~ LOGGING ~~~~~~ #
import os
from util import log
from util import qsub
import logging
import _exceptions as _e

logger = logging.getLogger(__name__)

# path to the script's dir
scriptdir = os.path.dirname(os.path.realpath(__file__))
scriptname = os.path.basename(__file__)
script_timestamp = log.timestamp()


# ~~~~ CUSTOM FUNCTIONS ~~~~~~ #
def monitor_validate_jobs(jobs):
    '''
    Monitor qsub jobs that were generated by tasks which did not wait for job completion

    wait for them all to complete, then check them all for their qacct completion status

    jobs = list of qsub.Job objects

    TODO: add error handling of invalid or err_jobs here
    '''
    if not jobs:
        logger.debug('No jobs were passed for monitoring')
        # TODO: what to return here?
        return()

    logger.debug('Waiting for qsub jobs to complete:\n{0}'.format([(job.id, job.name) for job in jobs]))

    completed_jobs, err_jobs = qsub.monitor_jobs(jobs = jobs)

    logger.debug('All jobs completed')

    logger.debug('Validating completion status of completed jobs...')

    valid_jobs = []
    invalid_jobs = []

    for job in completed_jobs:
        if job.validate_completion():
            valid_jobs.append(job)
        else:
            invalid_jobs.append(job)

    if invalid_jobs:
        logger.error('Some completed jobs appear invalid: {0}'.format([(job.id, job.name) for job in invalid_jobs]))

    if err_jobs:
        logger.error('Some jobs did not complete due to errors: {0}'.format([(job.id, job.name) for job in err_jobs]))

    if invalid_jobs or err_jobs:
        all_invalid_jobs = []

        if invalid_jobs:
            for job in invalid_jobs:
                all_invalid_jobs.append(job)

        if err_jobs:
            for job in err_jobs:
                all_invalid_jobs.append(job)
        err_message = 'Jobs did not complete successfully:\n\n'
        jobs_message = '\n'.join([job.completions for job in all_invalid_jobs])
        raise _e.ComputeJobInvalid(message = err_message + jobs_message, errors = '')