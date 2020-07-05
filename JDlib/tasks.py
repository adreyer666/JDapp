#!/usr/bin/env python3

import os
import stat
import subprocess
import re
import json
from uuid import uuid4
from time import sleep
from JDlib import KeyValueDB

# -------------- task queue -------------------------------------------------


class Tasker(object):
    """Task object class for async start/monitor of external jobs."""
    verbose = 0
    joblist = KeyValueDB(table='tasks')
    queue = None
    taskdir = None

    def __init__(self, verbose=None):
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

    def _uuid(self):
        return str(uuid4())

    def _job_update(self, job):
        """Store/update job in DB."""
        if self.verbose:
            print("Update: ", job)
        self.joblist.set(job['uuid'], json.dumps(job))

    def _job_query(self, uuid=None):
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

    def add(self, params):
        job = {
            "uuid": self._uuid(),
            "params": params,
            "status": 'created'
        }
        job["location"] = os.sep.join([self.taskdir, job['uuid']])
        self._job_update(job)
        task = CmdTask(job)
        pid = task.run()
        if pid is None:
            return None
        if pid:
            job['status'] = 'running'
            self._job_update(job)
        return job['uuid']

    def fixer(self):
        for uuid in self._job_query():
            job = self._job_query(uuid)
            task = CmdTask(job)
            taskstate = task.status()
            job['status'] = taskstate['status']
            self._job_update(job)

    def status(self, uuid=None, verbose=False):
        if uuid is None:
            return self._job_query()
        else:
            job = self._job_query(uuid)
            task = CmdTask(job)
            taskstate = task.status(verbose=verbose)
            job['status'] = taskstate['status']
            self._job_update(job)
            if verbose:
                taskstate['job'] = job
            return taskstate

# --------- task object ------------------------------------------------------


class CmdTask(object):
    """Execute a task command."""
    verbose = 0
    badchars = {
        'command': r"[^\d\w\t /.,]",
        'options': r"[^\d\w\t /.,'\"]",
    }
    taskdir = None
    task = None

    def __init__(self, task, verbose=None):
        if task is None:
            return
        if verbose:
            self.verbose = verbose
        self.task = task
        if "location" not in self.task:
            self.task["location"] = '.'
        self.task['in'] = '.'.join([self.task["location"], 'stdin'])
        self.task['out'] = '.'.join([self.task["location"], 'stdout'])
        self.task['err'] = '.'.join([self.task["location"], 'stderr'])
        self.task['res'] = '.'.join([self.task["location"], 'result'])
        self.task['cmdfile'] = '.'.join([self.task["location"], 'cmd'])

    def readfile(self, file):
        if file:
            with open(file, 'r', encoding='utf8') as x:
                f = x.read()
            return f

    def writefile(self, file, data=None):
        if file:
            if data is None:
                data = ''
            with open(file, 'x', encoding='utf8') as x:
                x.write(data)

    def run(self):
        if 'command' not in self.task['params']:
            return None
        if ('options' not in self.task['params']) or \
           (self.task['params']['options'] is None):
            self.task['params']['options'] = ''
        # primitive sanity ccheck for command and options
        m = re.search(self.badchars['command'], self.task['params']['command'])
        if m is not None:
            print("Error: <command> pos: {}, ".format(m.start()) +
                  "invalid char '{}'".format(m.group(0)))
            return None
        m = re.search(self.badchars['options'], self.task['params']['options'])
        if m is not None:
            print("Error: <options> pos: {}, ".format(m.start()) +
                  "invalid char '{}'".format(m.group(0)))
            return None
        # set some fallback values
        if 'input' not in self.task['params']:
            self.task['params']['input'] = ''
        self.writefile(self.task['in'], self.task['params']['input'])
        if 'timeout' not in self.task['params']:
            self.task['params']['timeout'] = 3600
        if 'kill' not in self.task['params']:
            ktmout = float(self.task['params']['timeout']) * 1.1
            self.task['params']['kill'] = ktmout
        if 'signal' not in self.task['params']:
            self.task['params']['signal'] = 'TERM'
        tmout = '-s {} -k {}s {}s'.format(self.task['params']['signal'],
                                          self.task['params']['kill'],
                                          self.task['params']['timeout'])
        if 'path' in self.task['params']:
            path = ":{}".format(self.task['params']['path'])
        else:
            path = ""
        cmdscript = [
            '#!/bin/sh -f',
            '',
            'exec 1>{}'.format(self.task['out']),
            'exec 2>{}'.format(self.task['err']),
            'trap "touch {}" 0 1 2 3 15'.format(self.task['res']),
            'PATH=/usr/bin{}:/bin:$PATH; export PATH'.format(path),
            'timeout {} \\'.format(tmout),
            '  "{}" {} <{}'.format(self.task['params']['command'],
                                   self.task['params']['options'],
                                   self.task['in']),
            'echo $? > {}'.format(self.task['res'])
        ]
        self.writefile(self.task['cmdfile'], "\n".join(cmdscript))
        RWX = stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR
        os.chmod(self.task['cmdfile'], RWX)
        if self.verbose:
            print("Job", self.task)
        pid = subprocess.Popen([self.task['cmdfile'], ]).pid
        if self.verbose:
            print("Pid: {}".format(pid))
        sleep(0.5)
        return pid

    def status(self, verbose=False):
        if self.task is None:
            if self.verbose:
                print("invalid status")
            return
        status = dict()
        status['status'] = self.task['status']
        if verbose:
            try:
                if os.stat(self.task['out']):
                    status['output'] = self.readfile(self.task['out'])
            except FileNotFoundError as err:
                if self.verbose > 1:
                    print(err)
                pass
            try:
                if os.stat(self.task['err']):
                    status['errors'] = self.readfile(self.task['err'])
            except FileNotFoundError as err:
                if self.verbose > 1:
                    print(err)
                pass
        try:
            if os.stat(self.task['res']):
                status['RC'] = self.readfile(self.task['res']).rstrip()
                if status['RC'] == 124:
                    status['status'] = 'timed out'
                else:
                    status['status'] = 'finished'
        except FileNotFoundError as err:
            if self.verbose > 1:
                print(err)
            pass
        return status


# --------- main -------------------------------------------------------------

if __name__ == '__main__':
    x = Tasker()
    task = {
        "command": "echo",            # safe command only! sanity checks first!
        "options": "hello world"      # sofe options/parameters only!
    }
    id = x.add(task)
    # always check return value!
    if id is None:
        print("Task aborted")
    print("Tasks running: {}".format(len(x.status())))
    if id is not None:
        print("Task status:   {}".format(x.status(id)))
        print("Tasks running: {}".format(len(x.status())))
        print("Task verbose status:\n{}".format(x.status(id, verbose=True)))
