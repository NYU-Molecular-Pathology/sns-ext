#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A collection of functions for submitting jobs to the NYUMC SGE compute cluster with 'qsub' from within Python, and monitoring them until completion

based on https://github.com/stevekm/pyqsub/tree/59c607d72a5b41d4804a969f9d543a89a41e39e6

modified for use with run-monitor system
'''
import logging
logger = logging.getLogger("qsub")
logger.debug("loading qsub module")

from collections import defaultdict

job_state_key = defaultdict(lambda: None)
job_state_key['Eqw'] = 'Error'
job_state_key['r'] = 'Running'
job_state_key['qw'] = 'Waiting'
job_state_key['t'] = None


# ~~~~ CUSTOM CLASSES ~~~~~~ #
class Job(object):
    '''
    A class to track a qsub job that has been submitted
    '''
    def __init__(self, id):
        global job_state_key
        self.job_state_key = job_state_key
        self.id = id
        self._update()

    def get_status(self, id, qstat_stdout = None):
        '''
        Get the status of the qsub job
        '''
        import re
        from sh import qstat
        # regex for the pattern matching https://docs.python.org/2/library/re.html
        job_id_pattern = r"^.*{0}.*\s([a-zA-Z]+)\s.*$".format(id)
        # get the qstat if it wasnt passed
        if not qstat_stdout:
            qstat_stdout = qstat()
        status = re.search(str(job_id_pattern), str(qstat_stdout), re.MULTILINE).group(1)
        return(status)

    def get_state(self, status, job_state_key):
        '''
        Get the interpretation of the job's status
        '''
        # defaultdict returns None if the key is not present
        state = job_state_key[status]
        return(state)

    def get_is_running(self, state, job_state_key):
        '''
        Check if the job is considered to be running
        '''
        is_running = False
        if state in ['Running']:
            is_running = True
        return(is_running)

    def _update(self):
        '''
        Update the object's status attributes
        '''
        self.status = self.get_status(id = self.id)
        self.state = self.get_state(status = self.status, job_state_key = self.job_state_key)
        self.is_running = self.get_is_running(state = self.state, job_state_key = self.job_state_key)

    def running(self):
        '''
        Return the most recent running state of the job
        '''
        self._update()
        return(self.is_running)



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


def get_job_ID_name(proc_stdout):
    '''
    return a tuple of the form (<id number>, <job name>)
    usage:
    proc_stdout = submit_job(return_stdout = True) # 'Your job 1245023 ("python") has been submitted'
    job_id, job_name = get_job_ID_name(proc_stdout)
    '''
    import re
    proc_stdout_list = proc_stdout.split()
    job_id = proc_stdout_list[2]
    job_name = proc_stdout_list[3]
    job_name = re.sub(r'^\("', '', str(job_name))
    job_name = re.sub(r'"\)$', '', str(job_name))
    return((job_id, job_name))


def submit_job(command = 'echo foo', params = '-j y', name = "python", stdout_log_dir = '${PWD}', stderr_log_dir = '${PWD}', return_stdout = False, verbose = False, pre_commands = 'set -x', post_commands = 'set +x'):
    '''
    Basic format for job submission to the SGE cluster with qsub
    '''
    import subprocess
    qsub_command = '''
qsub {0} -N {1} -o :{2}/ -e :{3}/ <<E0F
{4}
{5}
{6}
E0F
'''.format(
params,
name,
stdout_log_dir,
stderr_log_dir,
pre_commands,
command,
post_commands)
    if verbose == True:
        logger.debug('Command is:\n{0}'.format(qsub_command))
    proc_stdout = subprocess_cmd(command = qsub_command, return_stdout = True)
    if return_stdout == True:
        return(proc_stdout)
    elif return_stdout == False:
        logger.debug(proc_stdout)

def get_job_status(job_id, qstat_stdout = None):
    '''
    Get the status of a qsub job
    '''
    import re
    from sh import qstat
    # job_id = '2305564'
    # regex for the pattern matching https://docs.python.org/2/library/re.html
    job_id_pattern = r"^.*{0}.*\s([a-zA-Z]+)\s.*$".format(job_id)
    # get the qstat if it wasnt passed
    if not qstat_stdout:
        qstat_stdout = qstat()
    status = re.search(str(job_id_pattern), str(qstat_stdout), re.MULTILINE).group(1)
    return(status)


def check_job_status(job_id, desired_status = "r"):
    '''
    Use 'qstat' to check on the run status of a qsub job
    returns True or False if the job status matches the desired_status
    job running:
    desired_status = "r"
    job waiting:
    desired_status = "qw"
    '''
    import re
    from sh import qstat
    job_id_pattern = r"^.*{0}.*\s{1}\s.*$".format(job_id, desired_status)
    # using the 'sh' package
    qstat_stdout = qstat()
    # using the standard subprocess package
    # qstat_stdout = subprocess_cmd('qstat', return_stdout = True)
    job_match = re.findall(str(job_id_pattern), str(qstat_stdout), re.MULTILINE)
    job_status = bool(job_match)
    if job_status == True:
        status = True
        return(job_status)
    elif job_status == False:
        return(job_status)

def wait_job_start(job_id, return_True = False):
    '''
    Monitor the output of 'qstat' to determine if a job is running or not
    equivalent of
    '''
    from time import sleep
    import sys
    logger.debug('waiting for job to start')
    while check_job_status(job_id = job_id, desired_status = "r") != True:
        sys.stdout.write('.')
        sys.stdout.flush()
        sleep(3) # Time in seconds.
    if check_job_status(job_id = job_id, desired_status = "r") == True:
        logger.debug('job {0} has started'.format(job_id))
        if return_True == True:
            return(True)

def wait_all_jobs_start(job_id_list):
    '''
    Wait for every job in a list to start
    '''
    import datetime
    from time import sleep
    import sys
    jobs_started = False
    startTime = datetime.datetime.now()
    logger.debug("waiting for all jobs {0} to start...".format(job_id_list))
    while not all([check_job_status(job_id = job_id, desired_status = "r") for job_id in job_id_list]):
        sys.stdout.write('.')
        sys.stdout.flush()
        elapsed_time = datetime.datetime.now() - startTime
        # make sure the jobs did not die
        if all([check_job_absent(job_id = job_id) for job_id in job_id_list]):
            logger.debug("all jobs are now absent from 'qstat' list; elapsed time: {0}".format(elapsed_time))
            return(jobs_started)
        sleep(2) # Time in seconds.
    logger.debug("all jobs have started; elapsed time: {0}".format(elapsed_time))
    if all([check_job_status(job_id = job_id, desired_status = "r") for job_id in job_id_list]):
        jobs_started = True
    return(jobs_started)

def check_job_absent(job_id):
    '''
    Check that a single job is not in the 'qstat' list
    '''
    import re
    from sh import qstat
    qstat_stdout = qstat()
    job_id_pattern = r"^.*{0}.*$".format(job_id)
    job_match = re.findall(str(job_id_pattern), str(qstat_stdout), re.MULTILINE)
    job_status = bool(job_match)
    if job_status == True:
        return(False)
    elif job_status == False:
        return(True)


def wait_all_jobs_finished(job_id_list):
    '''
    Wait for all jobs in the list to finish
    A finished job is no longer present in the 'qstat' list
    '''
    import datetime
    from time import sleep
    import sys
    jobs_finished = False
    startTime = datetime.datetime.now()
    logger.debug("waiting for all jobs {0} to finish...".format(job_id_list))
    while not all([check_job_absent(job_id = job_id) for job_id in job_id_list]):
        sys.stdout.write('.')
        sys.stdout.flush()
        sleep(3) # Time in seconds.
    elapsed_time = datetime.datetime.now() - startTime
    logger.debug("all jobs have finished; elapsed time: {0}".format(elapsed_time))
    if all([check_job_absent(job_id = job_id) for job_id in job_id_list]):
        jobs_finished = True
    return(jobs_finished)

def demo_qsub():
    '''
    Demo the qsub code functions
    '''
    command = '''
    set -x
    cat /etc/hosts
    sleep 300
    '''
    proc_stdout = submit_job(command = command, verbose = True, return_stdout = True)
    job_id, job_name = get_job_ID_name(proc_stdout)
    logger.debug('Job ID: {0}'.format(job_id))
    logger.debug('Job Name: {0}'.format(job_name))
    wait_job_start(job_id)

def demo_multi_qsub():
    '''
    Demo the qsub code functions
    '''
    command = '''
    set -x
    cat /etc/hosts
    sleep 30
    '''
    job_id_list = []
    for i in range(5):
        proc_stdout = submit_job(command = command, verbose = True, return_stdout = True)
        job_id, job_name = get_job_ID_name(proc_stdout)
        logger.debug("Job submitted...")
        logger.debug('Job ID: {0}'.format(job_id))
        logger.debug('Job Name: {0}'.format(job_name))
        job_id_list.append(job_id)
    wait_all_jobs_start(job_id_list)
    wait_all_jobs_finished(job_id_list)


if __name__ == "__main__":
    demo_qsub()
    demo_multi_qsub()
