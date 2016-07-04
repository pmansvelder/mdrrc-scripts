#!/usr/bin/python

import wx

class Settings(wx.Dialog):
    def __init__(self, settings, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.settings = settings

        self.panel = wx.Panel(self)
        self.button_ok = wx.Button(self.panel, label="OK")
        self.button_cancel = wx.Button(self.panel, label="Cancel")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)

        self.checkboxes = []
        for i in range(3):
            checkbox = wx.CheckBox(self.panel, label=str(i))
            checkbox.SetValue(self.settings[i])
            self.checkboxes.append(checkbox)

        self.sizer = wx.BoxSizer()
        for checkbox in self.checkboxes:
            self.sizer.Add(checkbox)
        self.sizer.Add(self.button_ok)
        self.sizer.Add(self.button_cancel)

        self.panel.SetSizerAndFit(self.sizer)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        for i in range(3):
            self.settings[i] = self.checkboxes[i].GetValue()
        self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self)
        self.button = wx.Button(self.panel, label="Show settings")
        self.button.Bind(wx.EVT_BUTTON, self.onSettings)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.button)

        self.panel.SetSizerAndFit(self.sizer)  
        self.Show()

        self.settings = [False, False, False]

    def onSettings(self, e):
        settings_dialog = Settings(self.settings, self)
        res = settings_dialog.ShowModal()
        if res == wx.ID_OK:
            self.settings = settings_dialog.GetSettings()
        settings_dialog.Destroy()

app = wx.App(False)
win = MainWindow(None)
app.MainLoop()
