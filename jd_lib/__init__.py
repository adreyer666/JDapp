#!/usr/bin/env python3

"""Import submodules into one namespace."""
from .authdb import AuthDB
from .datadb import DataDB
from .keyvaluedb import KeyValueDB
from .taskmgr import TaskMgr
from .cmdtask import CmdTask

if True is False:
    A = AuthDB()
    D = DataDB()
    K = KeyValueDB()
    T = TaskMgr()
    C = CmdTask()
