[![Build Status](https://travis-ci.org/NYU-Molecular-Pathology/snsxt.svg?branch=master)](https://travis-ci.org/NYU-Molecular-Pathology/snsxt)
# snsxt
Extension to the sns pipeline

# Overview

This program is meant to be an extension to the [`sns wes` pipeline](https://github.com/NYU-Molecular-Pathology/sns) for whole/target exome sequencing data analysis. 

`snsxt` is a BYOC framework (Bring Your Own Code) for running downstream analysis tasks on sns-wes pipeline output. 

Use this framework to run any extra analysis tasks you like after an `sns` pipeline analysis has finished.

# Usage

__NOTE:__ Usage may change as development progresses

- Navigate to the directory containing your `sns` analysis output

```bash
cd /path/to/sns_output
```

- Clone this repository and navigate to its directory

```bash
git clone --recursive https://github.com/NYU-Molecular-Pathology/snsxt.git
cd snsxt
```

- Run the `run.py` script

```bash
snsxt/run.py ../ --analysis_id "<analysis_id>" --results_id "<results_id>" 
```

# Program Components

_Names and locations of these items may change with development_

Starting at the parent `snsxt` (this repo's parent dir):

- `snsxt`: main directory containing all code for the program

- `snsxt/config`: configuration module for the main program

- `snsxt/fixtures`: dummy analysis output files and directories for unit testing

- `snsxt/logs/`: default program log output directory

- [`snsxt/sns_classes`](https://github.com/NYU-Molecular-Pathology/sns_classes): submodule with Python classes for interacting with `sns` pipeline output

- `snsxt/sns_tasks`: submodule containing additional analysis tasks to be performed in the program

- [`snsxt/util`](https://github.com/NYU-Molecular-Pathology/util): submodule with utility functions and classes for usage in the program

- `snsxt/log.py`: custom logging package for the program

- `snsxt/logging.yml`: configurations for program logging

- `snsxt/test.py`: script to run all unit tests in the program and its submodules

- `snsxt/run.py`: main script used to run the program

# Adding Modules

You can add new analysis task modules to `snsxt` by following this workflow:

- enter the `sns_tasks` subdirectory and choose a pre-existing module to be the template:

```bash
cd snsxt/sns_tasks
```

- make a copy of the selected template Python module with the new name you wish to use for the new module (e.g. `Summary_Avg_Coverage.py`)

```bash
cp GATK_DepthOfCoverage_custom.py Summary_Avg_Coverage.py
```

- make a copy of the config file for the new module:

```
cp config/GATK_DepthOfCoverage_custom.yml config/Summary_Avg_Coverage.yml
```

- edit the new YAML config file with the corresponding info for the task

- load the new YAML file in the `config/__init__.py` file

```bash
open config/__init__.py
# add a line such as:
# with open(os.path.join(scriptdir, 'Summary_Avg_Coverage.yml'), "r") as f:
#     Summary_Avg_Coverage = yaml.load(f)
```
- edit the new Python module for the task, being sure to match the programming template provided in the source file

```bash
open Summary_Avg_Coverage.py
# edit the file with code for your task
```

- add the new module to the `run.py` file the same way other tasks are loaded & run, as appropriate

```bash
cd .. # pwd is now snsxt/snsxt
open run.py

# import your new module and add it to the `main` function to be run
```

# Tests

Unit tests for the various modules included in the program can be run with the `test.py` script. Individual modules can be tested with their corresponding `test_*.py` scripts.

# Software
Designed and tested in Python 2.7

Designed to run on Linux systems, tested under CentOS 6

Requires `pandoc` version 1.13+ for reporting

# Credits

[`sh.py`](https://github.com/amoffat/sh) is used as an included dependency.

[sns](https://github.com/NYU-Molecular-Pathology/sns) pipeline output is required to run this. 

`snsxt` uses the [util](https://github.com/NYU-Molecular-Pathology/util) and [sns_classes](https://github.com/NYU-Molecular-Pathology/sns_classes) libraries as dependecies
