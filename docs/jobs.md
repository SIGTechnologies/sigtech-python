# Jobs

Jobs provide a method to get data from your executed 
jobs.


## Getting Started
Before you begin, ensure you have Python installed on your machine
and that you have installed the SigTech Python SDK. 

You will also need to create a Personal Access Token within the platform
and set the environment variable `SIGTECH_PLATFORM_TOKEN`
to the value of this token.

For Windows:
    
    setx SIGTECH_PLATFORM_TOKEN <YOUR_ACCESS_TOKEN>

For macOS and Linux:

    export SIGTECH_PLATFORM_TOKEN=<YOUR_ACCESS_TOKEN>


To create a Personal Access Token visit https://platform.sigtech.com/settings.


## Python

```python
from sigtech.api.jobs import JobsApi
api = JobsApi()

# List all jobs
api.jobs.df()

# List runs for a job
job = api.jobs["my_job_name"]
job.runs.df()

# Get specific output from latest run
run = job.runs.latest
run.outputs["history"].df()

# See outputs from a job
run.outputs.df()

# Get data from a specific named output
run.outputs["history"].df()
run.outputs["positions"].df()
```
