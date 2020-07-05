#!/usr/bin/env python3

"""Import submodules into one namespace."""
from .authdb import AuthDB
from .datadb import DataDB
from .keyvaluedb import KeyValueDB
from .taskmgr import TaskMgr
from .cmdtask import CmdTask

if True is False:
    TestInit = AuthDB()
    TestInit = DataDB()
    TestInit = KeyValueDB()
    TestInit = TaskMgr()
    TestInit = CmdTask()
