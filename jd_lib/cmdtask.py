#!/usr/bin/env python3

"""
Task for running command strings (Lunux CLI).

CmdTask is executing tasks and fetching results.
"""

import os
import stat
import subprocess
import re
from time import sleep

# --------- task object ------------------------------------------------------


class CmdTask():
    """Execute a task command."""

    badchars = {
        'command': r"[^\d\w\t /.,]",
        'options': r"[^\d\w\t /.,'\"]",
    }

    def __init__(self, newtask=None, verbose=None):
        """Update internal class default values if needed."""
        if newtask is None:
            return
        if verbose:
            self.verbose = verbose
        self.task = newtask
        if "location" not in self.task:
            self.task["location"] = '.'
        self.task['in'] = '.'.join([self.task["location"], 'stdin'])
        self.task['out'] = '.'.join([self.task["location"], 'stdout'])
        self.task['err'] = '.'.join([self.task["location"], 'stderr'])
        self.task['res'] = '.'.join([self.task["location"], 'result'])
        self.task['cmdfile'] = '.'.join([self.task["location"], 'cmd'])

    def readfile(self, file) -> str:
        """Read from file return contents or empty string."""
        if file:
            try:
                if os.stat(file):
                    with open(file, 'r', encoding='utf8') as file_handle:
                        file_content = file_handle.read()
                    return file_content
            except FileNotFoundError as err:
                if self.verbose > 1:
                    print(err)
        return ''

    def writefile(self, file, data=None) -> bool:
        """Write data to file, use empty string if no data provided."""
        if file:
            if data is None:
                data = ''
            try:
                with open(file, 'x', encoding='utf8') as file_handle:
                    file_handle.write(data)
            except OSError as err:
                if self.verbose > 1:
                    print(err)
                return False
        return True

    def run(self) -> int:
        """Run a task."""
        if 'command' not in self.task['params']:
            return None
        if ('options' not in self.task['params']) or \
           (self.task['params']['options'] is None):
            self.task['params']['options'] = ''
        # primitive sanity ccheck for command and options
        match = re.search(self.badchars['command'],
                          self.task['params']['command'])
        if match is not None:
            print("Error: <command> pos: {}, ".format(match.start())
                  + "invalid char '{}'".format(match.group(0)))
            return None
        match = re.search(self.badchars['options'],
                          self.task['params']['options'])
        if match is not None:
            print("Error: <options> pos: {}, ".format(match.start())
                  + "invalid char '{}'".format(match.group(0)))
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
        file_mode = stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR
        os.chmod(self.task['cmdfile'], file_mode)
        if self.verbose:
            print("Job", self.task)
        cmd_pid = subprocess.Popen([self.task['cmdfile'], ]).pid
        if self.verbose:
            print("Pid: {}".format(cmd_pid))
        sleep(0.5)
        return cmd_pid

    def status(self, verbose=False) -> dict:
        """Determine status of a task."""
        status = dict()
        if self.task is None:
            if self.verbose:
                print("invalid status")
            return status
        status['status'] = self.task['status']
        if verbose:
            status['output'] = self.readfile(self.task['out'])
            status['errors'] = self.readfile(self.task['err'])
        status['RC'] = self.readfile(self.task['res']).rstrip()
        if status['RC'] == 124:
            status['status'] = 'timed out'
        else:
            status['status'] = 'finished'
        return status


# --------- main -------------------------------------------------------------

if __name__ == '__main__':
    task = {
        "command": "echo",            # safe command only! sanity checks first!
        "options": "hello world"      # sofe options/parameters only!
    }
    x = CmdTask(task)
    pid = x.run()
    # always check return value!
    if pid is None:
        print("Task aborted")
    if pid is not None:
        print("Task status:   {}".format(x.status()))
        print("Task verbose status:\n{}".format(x.status(verbose=True)))
