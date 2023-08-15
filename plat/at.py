"""
at.py - a Python interface to the unix "at" command
"""

import platform
import re
import subprocess
from subprocess import PIPE, STDOUT

from dateutil.parser import parse as parse_datetime

from utils import has_timezone, apply_local_timezone, now_local_timezone, strip_seconds


AT_DATETIME_FORMAT = '%H:%M %m%d%Y'


def job_full_command(job_id):
    """Return a string containing the full set of commands run as part
    of a scheduled job.
    """
    return subprocess.check_output(['at', '-c', job_id], text=True, encoding='latin-1')


def job_records():
    """Return a list of pending at jobs, sorted by time scheduled to run
    and then time created.
    """
    os_name = platform.system()

    # Build a list of job records.
    jobs = []
    for row in subprocess.check_output('atq', text=True, encoding='latin-1').split('\n'):
        if row:
            job_id, attribs = row.split('\t')
            if os_name == 'Linux':
                timestamp_str, status_code, username = attribs.rsplit(' ', 2)
            elif os_name == 'Darwin':
                timestamp_str = attribs
            else:
                raise OSError("Unsupported platform '{}'".format(os_name))
            full_command = job_full_command(job_id)  # includes any env settings
            jobs.append({
                'id': job_id,
                'timestamp': parse_datetime(timestamp_str),
                'full_command': full_command,
                'command': full_command.split('\n')[-3]  # "last" line only
            })

    return sorted(jobs, key=lambda job: (job['timestamp'], int(job['id'])))


def print_jobs():
    """Print a list of all queued jobs.

    Include job ID, scheduled run timestamp, and command to run. The
    command printed is only the last line of the command stored by `at`,
    which is the part that's useful to a human operator 99% of the time.
    (The full set of commands, accessible via `at -c [jobid]`, sets
    environment variables and `cd`s to the working directory at the time
    `at` was run.)
    """
    for job in job_records():
        command = job['command']
        timestamp = job['timestamp'].isoformat().replace('T', ' ')[:-3]
        print('\t'.join((job['id'], timestamp, command)))


def print_recreate_jobs_script():
    """Print a list of shell commands that would recreate the current
    `at` queue (not preserving job ID or environment, or CWD).

    NOTE: Just to reiterate that important last bit, this output does
    not preserve the environment or current working directory settings
    captured by the `at` job, which may be a critical omission.
    """
    for job in job_records():
        cmd = job['command']
        when = job['timestamp'].strftime(AT_DATETIME_FORMAT)
        print('echo "{}" | at {}'.format(cmd, when))


def schedule_job(command, run_at):
    """Queue a job to run at a specific time via the unix "at" command.
    `run_at` may be a string or datetime. If `run_at` is timezone-naive,
    use the local server timezone.
    """
    # Parse run_at to datetime if it's a string.
    if isinstance(run_at, str):
        run_at = parse_datetime(run_at)

    # Set to local server tz if run_at is tz-naive.
    if not has_timezone(run_at):
        run_at = apply_local_timezone(run_at)

    # Ensure run_at is set to the future.
    if strip_seconds(run_at) < strip_seconds(now_local_timezone()):
        raise ValueError('run_at must be a datetime in the future')

    # Pipe the text of the command to be run into the at command.
    proc = subprocess.Popen(('at', run_at.strftime(AT_DATETIME_FORMAT)),
                            stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = str(proc.communicate(command + '\n')[0])

    # Extract job_id from output
    mo = re.match(r'^job (\d+)', output)
    return mo.group(1) if mo else output


def remove_job(job_id):
    """Delete a queued job and return the job."""
    subprocess.check_call(['atrm', str(job_id)])
    return job_id


def clear_jobs():
    """Delete all queued jobs and return a list of their job IDs."""
    job_ids = [rec['id'] for rec in job_records()]
    for job_id in job_ids:
        remove_job(job_id)
    return job_ids
