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
        self.master = master

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

        self.versionWdg = RO.Wdg.StrLabel(
            master=self,
            helpText='Version of the BMO actor',
            helpURL='',
            anchor='w',
            width=10)
        gridder.gridWdg('Actor version', self.versionWdg)

        self.vimbaWdg = RO.Wdg.StrLabel(
            master=self,
            helpText='Status of the Vimba controller',
            helpURL='',
            anchor='w',
            width=10)
        gridder.gridWdg('Vimba', self.vimbaWdg)

        self.columnconfigure(1, weight=1)

        gridder.allGridded()

        self.model.bmoCamera.addCallback(self._bmoCameraCallback)
        self.model.bmoVimbaVersion.addCallback(self._bmoVimbaVersionCallback)
        self.model.version.addCallback(self._setVersion)

    def _setVersion(self, keyVar):
        """Sets actor version."""

        self.versionWdg.set(keyVar[0])

    def _bmoCameraCallback(self, keyVar):
        """Callback to set camera state."""

        cameraOn, cameraOff, deviceOn, deviceOff = keyVar

        strOn = '{}{}'.format('Connected' if cameraOn is True else 'Disconnected',
                              ' ({})'.format(deviceOn) if cameraOn is True else '')
        self.onCameraWdg.set(strOn, isCurrent=keyVar.isCurrent)
        self.onCameraWdg.config(fg='black' if cameraOn else 'red')

        strOff = '{}{}'.format('Connected' if cameraOff is True else 'Disconnected',
                               ' ({})'.format(deviceOff) if cameraOff is True else '')
        self.offCameraWdg.set(strOff, isCurrent=keyVar.isCurrent)
        self.offCameraWdg.config(fg='black' if cameraOff else 'red')

    def _bmoVimbaVersionCallback(self, keyVar):
        """Callback to set Vimba version."""

        vimbaVersion = keyVar[0]
        fg = 'black' if vimbaVersion != 'Fake' else 'red'

        self.vimbaWdg.set(vimbaVersion, isCurrent=keyVar.isCurrent)
        self.vimbaWdg.config(fg=fg)


class BMOExposureWdg(Tkinter.Frame):

    def __init__(self, master):
        """Create the BMO exposure widget."""

        Tkinter.Frame.__init__(self, master)

        self.gridder = RO.Wdg.Gridder(master=self, sticky='w')

        self.master = master
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

        self.exposureTimeSetBtn = RO.Wdg.Button(
            master=self.exposureFrame,
            text='Set',
            command=self.setExposureTime,
            helpText='Set exposure time')
        self.exposureTimeSetBtn.pack(side='left')

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

        self.master.model.bmoCamera.addCallback(self._bmoCameraCallback)

    def _bmoCameraCallback(self, keyVar):
        """Callback to set camera state."""

        cameraOn, cameraOff, __, __ = keyVar

        # Sets exposure on-axis camera checkbox
        self.exposureOnCheck.setBool(cameraOn)
        self.exposureOnCheck.setEnable(cameraOn)

        # Sets exposure off-axis camera checkbox
        self.exposureOffCheck.setBool(cameraOff)
        self.exposureOffCheck.setEnable(cameraOff)

    def setExposureTime(self):
        """Sets exposure time."""

        exptime_string = self.exposureTimeEntry.getString().strip()
        if exptime_string == '':
            raise ValueError('invalid exposure time(s).')

        exptimes = list(map(lambda xx: float(xx.strip()), exptime_string.split(',')))

        if len(exptimes) > 2:
            raise ValueError('too many exposure times.')

        doExpose = [self.exposureOnCheck.getBool(), self.exposureOffCheck.getBool()]

        for ii, value in enumerate(['on', 'off']):
            if not doExpose[ii]:
                pass

            exptime = exptimes[ii if len(exptimes) > 1 else 0]

            exptimeCmdVar = opscore.actor.CmdVar(
                actor=self.master.actor,
                cmdStr='camera exptime --camera_type={} {:.1f}'.format(value, exptime))

            self.master.statusBar.doCmd(exptimeCmdVar)


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
        """Connects DS9."""

        connectCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='ds9 connect')

        self.statusBar.doCmd(connectCmdVar)

    def resetDS9(self):
        """Resets DS9."""

        resetCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='ds9 reset')

        self.statusBar.doCmd(resetCmdVar)

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

        self.centreUpFrame = Tkinter.Frame(self)
        self.centreUpGridder = RO.Wdg.Gridder(master=self.centreUpFrame, sticky='w')

        self.rotateCheck = RO.Wdg.Checkbutton(
            master=self.centreUpFrame,
            defValue=True,
            text='Rotate',
            helpText='Rotates the field')
        self.rotateCheck.pack(side='left')

        self.centreUpGridder.gridWdg('Centre up', self.rotateCheck)

        self.centreUpFrame.grid(row=row, column=0, sticky='ew')
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

        self.centreBtn = RO.Wdg.Button(
            master=buttonFrame,
            text='Centre Up',
            command=self.centreUp,
            helpText='Centres the field')
        self.centreBtn.pack(side='right')

        buttonFrame.grid(row=row, column=0, sticky='ew')
        row += 1

        self.model.bmoExposeState.addCallback(self.enableButtons)

        self.enableButtons()

    def centreUp(self):
        """Centres the field."""

        rotate = self.rotateCheck.getBool()

        centreCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='centre_up {}'.format('--translate' if rotate is False else ''))

        self.statusBar.doCmd(centreCmdVar)

    def getStateTracker(self):
        """Return the state tracker"""

        return self._stateTracker

    def enableButtons(self, *dumArgs):
        """Enable or disable widgets as appropriate."""

        cameraOn_state, cameraOff_state = self.model.bmoExposeState

        exposing = cameraOn_state != 'idle' or cameraOff_state != 'idle'

        self.exposeBtn.setEnable(not exposing)
        self.stopBtn.setEnable(exposing)

    def startExposure(self):
        """Start exposure."""

        onCheck = self.exposureWdg.exposureOnCheck.getBool()
        offCheck = self.exposureWdg.exposureOffCheck.getBool()

        if onCheck and offCheck:
            camera_type = 'all'
        elif onCheck and not offCheck:
            camera_type = 'on'
        else:
            camera_type = 'off'

        one = self.exposureWdg.singleExposureCheck.getBool()
        background = self.exposureWdg.subtractBackCheck.getBool()

        startCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='camera expose --camera_type={}{} {}'.format(
                camera_type, ' --one' if one else '',
                '--background' if background else '--no-background'))

        self.statusBar.doCmd(startCmdVar)

    def stopExposure(self):
        """Stop exposure."""

        stopCmdVar = opscore.actor.CmdVar(
            actor=self.actor,
            cmdStr='camera stop')
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
