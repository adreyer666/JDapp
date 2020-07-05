#!/usr/bin/env python3

"""
Task list class and a task running class.

Tasker is managing tasks in a job list, this is the public interface.
CmdTask is executing tasks and fetching results.
"""

import os
import json
from uuid import uuid4
# from jd_lib import KeyValueDB, CmdTask
from .keyvaluedb import KeyValueDB
from .cmdtask import CmdTask

# -------------- task queue -------------------------------------------------


class TaskMgr():
    """Task object class for async start/monitor of external jobs."""

    verbose = 0
    joblist = KeyValueDB(table='tasks')
    queue = None
    taskdir = None

    def __init__(self, verbose=None):
        """Update internal class default values if needed."""
        if verbose:
            self.verbose = verbose
        # cwd = os.path.abspath(os.getcwd())
        # cwd = os.getcwd()
        cwd = '.'
        self.taskdir = os.sep.join([cwd, "tasks"])
        try:
            os.stat(self.taskdir)
        except FileNotFoundError as err:
            if self.verbose:
                print('Taskdir does not exist, creating it.')
            if self.verbose > 2:
                print(err)
            os.mkdir(self.taskdir)

    def _uuid(self) -> str:
        """Create new UUID as string."""
        uuid = str(uuid4())
        if self.verbose > 1:
            print("New UUID: ", uuid)
        return uuid

    def _job_update(self, job=None) -> bool:
        """Store/update job in DB."""
        if job is None:
            return False
        if self.verbose:
            print("Update: ", job)
        self.joblist.set(job['uuid'], json.dumps(job))
        return True

    def _job_query(self, uuid=None) -> dict:
        """Query DB for job['uuid']."""
        if uuid is None:
            uuids = list()
            for k in self.joblist.get():
                # print("K: ",k)
                result = self.joblist.get(k)
                # print("R: ",result)
                if result is None:
                    return None
                value = json.loads(result['value'])
                # print("V: ", value)
                if value['status'] == 'running':
                    uuids.append(k)
            return uuids
        if self.verbose:
            print("Query: ", uuid)
        res = self.joblist.get(uuid)
        if res is None:
            return None
        return json.loads(res['value'])

    def add(self, params=None, task_type='cmd') -> str:
        """Add new task to job list."""
        if params is None:
            return None
        job = {
            "uuid": self._uuid(),
            "type": task_type,
            "params": params,
            "status": 'created'
        }
        job["location"] = os.sep.join([self.taskdir, job['uuid']])
        self._job_update(job)
        if job['type'] == 'cmd':
            cmd_task = CmdTask(job)
            pid = cmd_task.run()
        else:
            pid = None
        if pid is None:
            return None
        if pid:
            job['status'] = 'running'
            self._job_update(job)
        return job['uuid']

    def fixer(self) -> bool:
        """Go through running tasks in job list and update status."""
        for uuid in self._job_query():
            job = self._job_query(uuid)
            if job['type'] == 'cmd':
                cmd_task = CmdTask(job)
                taskstate = cmd_task.status()
            else:
                taskstate = {'status': 'invalid'}
            job['status'] = taskstate['status']
            self._job_update(job)
        return True

    def status(self, uuid=None, verbose=False) -> dict:
        """Fetch status of a given task from job list."""
        if uuid is None:
            return self._job_query()
        job = self._job_query(uuid)
        if job['type'] == 'cmd':
            cmd_task = CmdTask(job)
            taskstate = cmd_task.status(verbose=verbose)
        else:
            taskstate = {'status': 'invalid'}
        job['status'] = taskstate['status']
        self._job_update(job)
        if verbose:
            taskstate['job'] = job
        return taskstate


# --------- main -------------------------------------------------------------

if __name__ == '__main__':
    x = TaskMgr()
    task = {
        "command": "echo",            # safe command only! sanity checks first!
        "options": "hello world"      # sofe options/parameters only!
    }
    tid = x.add(task)
    # always check return value!
    if tid is None:
        print("Task aborted")
    print("Tasks running: {}".format(len(x.status())))
    if tid is not None:
        print("Task status:   {}".format(x.status(tid)))
        print("Tasks running: {}".format(len(x.status())))
        print("Task verbose status:\n{}".format(x.status(tid, verbose=True)))
