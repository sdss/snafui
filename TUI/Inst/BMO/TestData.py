#!/usr/bin/env python
# encoding: utf-8
#
# TestData.py
#
# Created by José Sánchez-Gallego on 18 Sep 2017.


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import TUI.Base.TestDispatcher


testDispatcher = TUI.Base.TestDispatcher.TestDispatcher('bmo', delay=5)
tuiModel = testDispatcher.tuiModel

MainDataList = ()


def start():
    testDispatcher.dispatch(MainDataList)
