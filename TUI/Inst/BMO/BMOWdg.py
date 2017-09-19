#!/usr/bin/env python
# encoding: utf-8
#
# file.py
#
# Created by José Sánchez-Gallego on 18 Sep 2017.


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import Tkinter
import opscore.actor
import RO.Constants
import RO.Wdg
import TUI.Models
# import TUI.Base.Wdg


class BMOStatusWdg(Tkinter.Frame):

    def __init__(self, master):
        """Create the BMO status widget."""

        Tkinter.Frame.__init__(self, master)

        self.model = TUI.Models.getModel(master.actor)

        gridder = RO.Wdg.Gridder(master=self, sticky='w')
        self.gridder = gridder

        self.onCameraWdg = RO.Wdg.StrLabel(
            master=self,
            helpText='Status of the on-axis camera',
            helpURL='',
            anchor='w',
            width=30)
        gridder.gridWdg('On-axis camera', self.onCameraWdg)

        self.offCameraWdg = RO.Wdg.StrLabel(
            master=self,
            helpText='Status of the off-axis camera',
            helpURL='',
            anchor='w',
            width=30)
        gridder.gridWdg('Off-axis camera', self.offCameraWdg)

        self.vimbaWdg = RO.Wdg.StrLabel(
            master=self,
            helpText='Status of the Vimba controller',
            helpURL='',
            anchor='w',
            width=10)
        gridder.gridWdg('Vimba', self.vimbaWdg)

        self.columnconfigure(1, weight=1)

        gridder.allGridded()

        self.model.bmoVimbaState.addCallback(self._bmoVimbaStateCallback)

    def _bmoVimbaStateCallback(self, keyVar):
        """Callback to set Vimba state."""

        self.vimbaWdg.set(keyVar[0], isCurrent=keyVar.isCurrent)


class BMOExposureWdg(Tkinter.Frame):

    def __init__(self, master):
        """Create the BMO exposure widget."""

        Tkinter.Frame.__init__(self, master)

        self.gridder = RO.Wdg.Gridder(master=self, sticky='w')

        self.exposureFrame = Tkinter.Frame(self)

        self.exposureTimeEntry = RO.Wdg.StrEntry(
            master=self.exposureFrame,
            label='ExposeTime',
            helpText='Desired exposure time. Comma-separated for multiple cameras.')
        self.exposureTimeEntry.pack(side='left', padx=(10, 0))

        self.exposureTimeUnits = RO.Wdg.StrLabel(
            master=self.exposureFrame,
            text='sec ',
            helpText='Desired exposure time. Comma-separated for multiple cameras.')
        self.exposureTimeUnits.pack(side='left')

        self.exposureOnCheck = RO.Wdg.Checkbutton(
            master=self.exposureFrame,
            defValue=True,
            text='On',
            helpText='Expose the on-axis camera?')
        self.exposureOnCheck.pack(side='left')

        self.exposureOffCheck = RO.Wdg.Checkbutton(
            master=self.exposureFrame,
            defValue=True,
            text='Off',
            helpText='Expose the off-axis camera?')
        self.exposureOffCheck.pack(side='left')

        self.gridder.gridWdg('Exposure Time', self.exposureFrame)

        self.subtractBackCheck = RO.Wdg.Checkbutton(
            master=self,
            defValue=True,
            text='Subtract Background',
            helpText='Subtract background from image?')
        self.gridder.gridWdg('', self.subtractBackCheck)

        self.singleExposureCheck = RO.Wdg.Checkbutton(
            master=self,
            defValue=False,
            text='Single exposure',
            helpText='Expose only one frame.')
        self.gridder.gridWdg('', self.singleExposureCheck)

        self.gridder.allGridded()


class BMODS9Wdg(Tkinter.Frame):

    def __init__(self, master, statusBar):
        """Create the BMO DS9 widget."""

        Tkinter.Frame.__init__(self, master)

        self.gridder = RO.Wdg.Gridder(master=self, sticky='w')
        self.statusBar = statusBar

        self.actor = master.actor

        self.connectBtn = RO.Wdg.Button(
            master=self,
            text='Connect',
            command=self.connectDS9,
            helpText='Connect to DS9')

        self.resetBtn = RO.Wdg.Button(
            master=self,
            text='Reset',
            command=self.resetDS9,
            helpText='Reset to DS9')

        self.gridder.gridWdg('DS9', (self.connectBtn, self.resetBtn), sticky='w')

        self.showChartPlateEntry = RO.Wdg.IntEntry(
            master=self,
            label='ShowChartPlate',
            helpText='Plate to show charts for. Empty for current cart.')

        self.showChartBtn = RO.Wdg.Button(
            master=self,
            text='Show',
            command=self.showCharts,
            helpText='Show chart')

        self.gridder.gridWdg('Show charts', (self.showChartPlateEntry, self.showChartBtn),
                             sticky='w')

        self.gridder.allGridded()

    def connectDS9(self):
        pass

    def resetDS9(self):
        pass

    def showCharts(self):
        """Shows finding charts in DS9."""

        showChartsCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='ds9 show_chart {0}'.format(self.showChartPlateEntry.getString()))

        self.statusBar.doCmd(showChartsCmdVar)


class BMOWdg(Tkinter.Frame):

    def __init__(self, master):
        """Create the BMO status/control/exposure widget."""

        Tkinter.Frame.__init__(self, master)

        self.actor = 'bmo'
        self.model = TUI.Models.getModel(self.actor)
        self.tuiModel = TUI.Models.getModel('tui')
        self._stateTracker = RO.Wdg.StateTracker(logFunc=self.tuiModel.logFunc)

        self.statusBar = TUI.Base.Wdg.StatusBar(self)

        row = 0

        self.statusWdg = BMOStatusWdg(self)
        self.statusWdg.grid(row=row, column=0, sticky='w')

        row += 1

        self.exposureWdg = BMOExposureWdg(self)
        self.exposureWdg.grid(row=row, column=0, sticky='w')
        row += 1

        self.ds9Wdg = BMODS9Wdg(self, self.statusBar)
        self.ds9Wdg.grid(row=row, column=0, sticky='w')
        row += 1

        self.statusBar.grid(row=row, column=0, sticky='ew')
        row += 1

        buttonFrame = Tkinter.Frame(self)
        self.exposeBtn = RO.Wdg.Button(
            master=buttonFrame,
            text='Expose',
            command=self.startExposure,
            helpText='Start exposure(s)')
        self.exposeBtn.pack(side='left')

        self.stopBtn = RO.Wdg.Button(
            master=buttonFrame,
            text='Stop',
            command=self.stopExposure,
            helpText='Stop current exposure')
        self.stopBtn.pack(side='left')

        buttonFrame.grid(row=row, column=0, sticky='ew')
        row += 1

        # self.model.exposureState.addCallback(self.enableButtons)

        self.enableButtons()

    def getStateTracker(self):
        """Return the state tracker"""

        return self._stateTracker

    def enableButtons(self, *dumArgs):
        """Enable or disable widgets as appropriate."""

        # isExposing = self.model.exposureState[0] in self.RunningExposureStates
        # isRunning = self.scriptRunner.isExecuting

        isExposing = False
        isRunning = False
        self.exposeBtn.setEnable(not (isRunning or isExposing))
        self.stopBtn.setEnable(isExposing)

    def startExposure(self):
        """Start exposure."""

        startCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='expose start')
        self.statusBar.doCmd(startCmdVar)

    def stopExposure(self):
        """Stop exposure."""

        stopCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='expose stop')
        self.statusBar.doCmd(stopCmdVar)


if __name__ == '__main__':

    root = RO.Wdg.PythonTk()

    import TestData
    tuiModel = TestData.tuiModel

    testFrame = BMOWdg(tuiModel.tkRoot)
    testFrame.pack(side='top', expand=True)

    Tkinter.Button(text='Demo', command=TestData.start).pack(side='top')

    TestData.start()

    tuiModel.reactor.run()
