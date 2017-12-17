# -*- coding: utf-8 -*-

"""Evaluate simple python expressions.
Use it with care every keystroke triggers an evaluation."""

from albertv0 import *
from math import *
import json
import re
from builtins import pow
import clipboard

try:
    import numpy as np
except ImportError:
    pass
import os

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Python Eval"
__version__ = "1.0"
__trigger__ = "sed "
__author__ = "Angelo Gazzola"
__dependencies__ = ["clipboard"]

iconPath = os.path.dirname(__file__)+"/icons/python.svg"
cl = ''

def handleQuery(query):
    def sed(pattern='', replace=''):
        return re.sub(re.compile(pattern, re.MULTILINE), replace, cl)

    if query.isTriggered:
        cl = clipboard.paste()
        item = Item(id=__prettyname__, completion=query.rawString)
        stripped = query.string.strip()

        if stripped == '':
            item.text = "Enter pattern - substitute"
            item.subtext = "Replace stuff with regex <3"
            return [item]
        else:
            try:
                result = stripped.split(' - ')

                if len(result) == 2:
                    result = sed(result[0], result[1])
                else:
                    result = sed(result[0])
                #result = eval(stripped)
            except Exception as ex:
                result = ex
            item.text = str(result)
            item.subtext = type(result).__name__
            item.addAction(ClipAction("Copy result to clipboard", str(result)))
            item.addAction(FuncAction("Execute", lambda: exec(str(result))))
        return [item]
