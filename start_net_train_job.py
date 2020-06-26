#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 17:01:34 2020

@author: briardoty
"""
import os
import json
import sys

# import pbstools (Python 3 version)
sys.path.append("/allen/programs/braintv/workgroups/nc-ophys/nick.ponvert/src/pbstools")
from pbstools import PythonJob

# path to python executable
python_executable = "/home/briar.doty/anaconda3/bin/python"

# path to data directory
data_dir = "/allen/programs/braintv/workgroups/nc-ophys/briar.doty/data/"

# params
run_params = {
    data_dir: data_dir
}

# job settings
job_settings = {
    "queue": "braintv",
    "mem": "1g",
    "walltime": "1:00:00",
    "ppn": 4
}

if __name__=="__main__":
    # prepare args
    args = [str(run_params)]
    args_string = " ".join(args)
    job_title = "test job"
    
    # kick off HPC job
    PythonJob(
        run_params["fit_script"],
        python_executable,
        python_args = args_string,
        jobname = job_title,
        jobdir = run_params["job_dir"],
        **job_settings
    ).run(dryrun=False)
