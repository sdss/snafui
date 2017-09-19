#!/usr/bin/env python
# encoding: utf-8
#
# BMOWindow.py
#
# Created by José Sánchez-Gallego on 18 Sep 2017.


from __future__ import division
from __future__ import print_function

import BMOWdg


WindowName = 'Inst.BMO'


def addWindow(tlSet, visible=False):
    """Create the window."""

    tlSet.createToplevel(name=WindowName,
                         defGeom='+346+398',
                         visible=visible,
                         resizable=False,
                         wdgFunc=BMOWdg.BMOWdg,
                         doSaveState=True)


if __name__ == '__main__':

    import TUI.Base.TestDispatcher

    testDispatcher = TUI.Base.TestDispatcher.TestDispatcher('tcc')
    tuiModel = testDispatcher.tuiModel
    root = tuiModel.tkRoot

    addWindow(tuiModel.tlSet, visible=True)

    tuiModel.reactor.run()
