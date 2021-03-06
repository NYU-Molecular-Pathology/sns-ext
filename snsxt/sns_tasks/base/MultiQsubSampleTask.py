#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for the base MultiQsubSampleTask object class
"""
from SampleTask import SampleTask

class MultiQsubSampleTask(SampleTask):
    """
    Base class for an ``SampleTask`` operates on each sample in the analysis, and multiple qsub jobs for each.

    Notes
    -----
    This class should have a ``main`` method that returns a list of ``qsub.Job`` objects for each sample in the analysis
    """
    def __init__(self, *ars, **kwargs):
        SampleTask.__init__(self, *ars, **kwargs)

    def run(self, analysis = None, qsub_wait = True, *args, **kwargs):
        """
        Runs a task that operates on each sample in the analysis, and submits multiple qsub jobs for each.

        Parameters
        ----------
        analysis: SnsWESAnalysisOutput
            the `sns` pipeline output object to run the task on. If ``None`` is passed, ``self.analysis`` is retrieved instead.
        qsub_wait: bool
            whether the task should wait for the qsub job to finish before continuing; default is ``True``
        args: list
            a list of extra positional arguments to pass to ``self.main()``
        kwargs: dict
            a dictionary of extra positional arguments to pass to ``self.main()``

        Returns
        -------
        list or None
            a list of ``qsub.Job`` objects if ``qsub_wait`` is ``False``, otherwise returns ``None`` after waiting for all jobs to finish

        Notes
        -----
        If ``qsub_wait`` is ``True``, then qsub jobs will also be validated for completion status.

        """
        if not analysis:
            analysis = getattr(self, 'analysis', None)

        # get all the Sample objects for the analysis
        samples = analysis.get_samples()

        # empty list to hold the qsub jobs
        jobs = []

        for sample in samples:
            # run the task on each sample; should return a qsub Job object
            sample_jobs = self.main(sample = sample, *args, **kwargs)
            if sample_jobs:
                for job in sample_jobs:
                    jobs.append(job)
        self.logger.debug('Submitted jobs: {0}'.format([job.id for job in jobs]))

        # montitor the qsub jobs until they are all completed
        if qsub_wait:
            self.logger.debug('Jobs will be monitored for completion and validated')
            self.job_management.monitor_validate_jobs(jobs = jobs)
            return(None)
        else:
            return(jobs)
