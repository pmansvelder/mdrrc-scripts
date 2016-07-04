import wx
import ConfigParser as cf
import os
#
class Settings(wx.Dialog):
    def __init__(self, settings, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetTitle(_('Connection Settings'))
        self.settings = settings
        self.panel = wx.Panel(self)
        self.quote = wx.StaticText(self.panel, label = "Port settings:")
        self.result = wx.StaticText(self.panel, label = "")
        self.result.SetForegroundColour(wx.RED)
        self.button = wx.Button(self.panel, label="Save")
        self.button.Bind(wx.EVT_BUTTON, self.onSave)

        self.portlabel = wx.StaticText(self.panel, label="Port name:")
        self.portedit = wx.TextCtrl(self.panel, size=(140, -1))
        self.portedit.SetValue(self.settings[0])
        self.baudlabel = wx.StaticText(self.panel, label="Baud rate:")
        self.baudedit = wx.TextCtrl(self.panel, size=(140, -1))
        self.baudedit.SetValue(self.settings[1])

        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)  

        self.sizer = wx.GridBagSizer(5,5)
        self.sizer.Add(self.quote, (0,0))
        self.sizer.Add(self.result, (0,1))
        self.sizer.Add(self.portlabel, (1, 0))
        self.sizer.Add(self.portedit, (1, 1))
        self.sizer.Add(self.baudlabel, (2, 0))
        self.sizer.Add(self.baudedit, (2, 1))
        self.sizer.Add(self.button, (3, 0), (1, 2), flag=wx.EXPAND)
        
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onSave(self, e):
        self.settings[0] = self.portedit.GetValue().encode('ascii','ignore')
        self.settings[1] = self.baudedit.GetValue().encode('ascii','ignore')
        config = cf.ConfigParser()
        config.read('settings.cfg')
        config.set('Connection','port', self.settings[0])
        config.set('Connection','speed', self.settings[1])
        with open('settings.cfg', 'wb') as configfile:
          config.write(configfile)
        self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

#
