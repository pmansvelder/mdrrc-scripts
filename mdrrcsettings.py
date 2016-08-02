import wx
import ConfigParser as cf
import os
#
class Settings(wx.Dialog):
    def __init__(self, settings, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetTitle(_('Program Settings'))
        self.settings = settings
        self.panel = wx.Panel(self)
        self.quote = wx.StaticText(self.panel, label = _("Port settings:"))
        self.exportlabel = wx.StaticText(self.panel, label = _("Export settings:"))
        self.formatlabel = wx.StaticText(self.panel, label = _("Version-dependent settings:"))
        self.result = wx.StaticText(self.panel, label = "")
        self.result.SetForegroundColour(wx.RED)
        self.button = wx.Button(self.panel, label=_("Save"))
        self.button.Bind(wx.EVT_BUTTON, self.onSave)

        self.portlabel = wx.StaticText(self.panel, label=_("Port name:"))
        self.portedit = wx.TextCtrl(self.panel, size=(140, -1))
        self.portedit.SetValue(self.settings[0])
        
        self.baudlabel = wx.StaticText(self.panel, label=_("Baud rate:"))
        self.baudedit = wx.TextCtrl(self.panel, size=(140, -1))
        self.baudedit.SetValue(self.settings[1])
        
        self.filelabel =  wx.StaticText(self.panel, label=_("Export filename:"))
        self.fileedit = wx.TextCtrl(self.panel, size=(140, -1))
        self.fileedit.SetValue(self.settings[2])

        self.configfilelabel =  wx.StaticText(self.panel, label=_("Config filename:"))
        self.configfileedit = wx.TextCtrl(self.panel, size=(140, -1))
        self.configfileedit.SetValue(self.settings[3])

        self.spacinglabel =  wx.StaticText(self.panel, label=_("Loclist spacing (18 for version <= 3.6.2, else 21):"))
        self.spacingedit = wx.TextCtrl(self.panel, size=(140, -1))
        self.spacingedit.SetValue(self.settings[4])

        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)  

        self.sizer = wx.GridBagSizer(5,5)
        self.sizer.Add(self.quote, (0,0))       
        self.sizer.Add(self.result, (0,1))
        self.sizer.Add(self.portlabel, (1, 0))
        self.sizer.Add(self.portedit, (1, 1))
        self.sizer.Add(self.baudlabel, (2, 0))
        self.sizer.Add(self.baudedit, (2, 1))
        self.sizer.Add(self.exportlabel, (4,0))
        self.sizer.Add(self.filelabel, (5,0))
        self.sizer.Add(self.fileedit, (5,1))
        self.sizer.Add(self.configfilelabel, (6,0))
        self.sizer.Add(self.configfileedit, (6,1)) 
        self.sizer.Add(self.formatlabel, (7,0))
        self.sizer.Add(self.spacinglabel, (8,0))
        self.sizer.Add(self.spacingedit, (8,1))     
        self.sizer.Add(self.button, (9, 0), (1, 2), flag=wx.EXPAND)
        
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onSave(self, e):
        self.settings[0] = self.portedit.GetValue().encode('ascii','ignore')
        self.settings[1] = self.baudedit.GetValue().encode('ascii','ignore')
        self.settings[2] = self.fileedit.GetValue().encode('ascii','ignore')
        self.settings[3] = self.configfileedit.GetValue().encode('ascii','ignore')
        self.settings[4] = int(self.spacingedit.GetValue().encode('ascii','ignore'))
        config = cf.ConfigParser()
        config.read('settings.cfg')
        config.set('Connection','port', self.settings[0])
        config.set('Connection','speed', self.settings[1])
        config.set('Export','filename', self.settings[2])
        config.set('Export','configfilename', self.settings[3])
        try:
          config.set('Format','spacing', self.settings[4])
        except:
          config.add_section('Format')
          config.set('Format','spacing', self.settings[4])
        with open('settings.cfg', 'wb') as configfile:
          config.write(configfile)
        self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings
        self.sizer.Add(self.filelabel, (5,0))
        self.sizer.Add(self.fileedit, (5,1))    
        
def ReadConfig(self):
        config = cf.ConfigParser()
        config.read('settings.cfg')
        try: 
          settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore'), config.get('Export','filename').encode('ascii','ignore'), config.get('Export','configfilename').encode('ascii','ignore'), config.get('Format','spacing').encode('ascii','ignore')]
        except:
          settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore'), config.get('Export','filename').encode('ascii','ignore'), config.get('Export','configfilename').encode('ascii','ignore'), str(18)]
        return settings
