import TUI
import TUI.Models.TUIModel
import TUI.TUIMenu.AboutWindow
import TUI.TUIMenu.ConnectWindow
import TUI.TUIMenu.DownloadsWindow
import TUI.TUIMenu.LogWindow
import TUI.TUIMenu.PreferencesWindow
import TUI.TUIMenu.PythonWindow
import TUI.TUIMenu.UsersWindow
import TUI.Inst.APOGEE.APOGEEWindow
import TUI.Inst.APOGEEQL.APOGEEQLWindow
import TUI.Inst.Guide.FocusPlotWindow
import TUI.Inst.Guide.GuideWindow
import TUI.Inst.GuideMonitor.AxisMonitorWindow
import TUI.Inst.GuideMonitor.FluxMonitorWindow
import TUI.Inst.GuideMonitor.FocusMonitorWindow
import TUI.Inst.GuideMonitor.GuideMonitorWindow
import TUI.Inst.GuideMonitor.ScaleMonitorWindow
import TUI.Inst.GuideMonitor.SeeingMonitorWindow
import TUI.Inst.GuideMonitor.GuideRMSMonitorWindow
import TUI.Inst.SOP.SOPWindow
import TUI.Inst.BMO.BMOWindow
import TUI.Misc.MessageWindow
import TUI.TCC.FocalPlaneWindow
import TUI.TCC.FocusWindow
import TUI.TCC.NudgerWindow
import TUI.TCC.OffsetWdg.OffsetWindow
import TUI.TCC.SkyWindow
import TUI.TCC.SlewWdg.SlewWindow
import TUI.TCC.StatusWdg.StatusWindow
import TUI.TCC.MirrorStatusWindow
import TUI.TCC.ScaleRingStatusWindow

def loadAll():
    tuiModel = TUI.Models.TUIModel.Model()
    tlSet = tuiModel.tlSet
    TUI.TUIMenu.AboutWindow.addWindow(tlSet)
    TUI.TUIMenu.ConnectWindow.addWindow(tlSet)
    TUI.TUIMenu.DownloadsWindow.addWindow(tlSet)
    TUI.TUIMenu.LogWindow.addWindow(tlSet)
    TUI.TUIMenu.PreferencesWindow.addWindow(tlSet)
    TUI.TUIMenu.PythonWindow.addWindow(tlSet)
    TUI.TUIMenu.UsersWindow.addWindow(tlSet)
    TUI.Inst.APOGEE.APOGEEWindow.addWindow(tlSet)
    TUI.Inst.APOGEEQL.APOGEEQLWindow.addWindow(tlSet)
    TUI.Inst.Guide.FocusPlotWindow.addWindow(tlSet)
    TUI.Inst.Guide.GuideWindow.addWindow(tlSet)
    TUI.Inst.GuideMonitor.AxisMonitorWindow.addWindow(tlSet)
    TUI.Inst.GuideMonitor.FluxMonitorWindow.addWindow(tlSet)
    TUI.Inst.GuideMonitor.FocusMonitorWindow.addWindow(tlSet)
    TUI.Inst.GuideMonitor.GuideMonitorWindow.addWindow(tlSet)
    TUI.Inst.GuideMonitor.ScaleMonitorWindow.addWindow(tlSet)
    TUI.Inst.GuideMonitor.SeeingMonitorWindow.addWindow(tlSet)
    TUI.Inst.GuideMonitor.GuideRMSMonitorWindow.addWindow(tlSet)
    TUI.Inst.SOP.SOPWindow.addWindow(tlSet)
    TUI.Inst.BMO.BMOWindow.addWindow(tlSet)
    TUI.Misc.MessageWindow.addWindow(tlSet)
    TUI.TCC.FocalPlaneWindow.addWindow(tlSet)
    TUI.TCC.FocusWindow.addWindow(tlSet)
    TUI.TCC.MirrorStatusWindow.addWindow(tlSet)
    TUI.TCC.NudgerWindow.addWindow(tlSet)
    TUI.TCC.OffsetWdg.OffsetWindow.addWindow(tlSet)
    TUI.TCC.SkyWindow.addWindow(tlSet)
    TUI.TCC.SlewWdg.SlewWindow.addWindow(tlSet)
    TUI.TCC.StatusWdg.StatusWindow.addWindow(tlSet)
    TUI.TCC.ScaleRingStatusWindow.addWindow(tlSet)
