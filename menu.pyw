#!/usr/bin/python

import copy
import wx
import gettext
import ConfigParser as cf
import os,sys
import mdrrc2serial, mdrrcsettings
import mdrrc2_config, mdrrc2_loclist

# Language suppport
if sys.platform.startswith('win'):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang
gettext.install('mdrrc-editor')

class MenuFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1)
        
        self.SetTitle(_("MDRRC-II Config Menu"))

        # Read settings for config program
        self.settings = mdrrcsettings.ReadConfig(None)

        # A statusbar
        self.CreateStatusBar()

        # A menubar
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuItem = filemenu.Append(wx.ID_ABOUT, _("&About\tCtrl+A"),_(" Information about this program"))
        self.Bind(wx.EVT_MENU, self.OnAbout, menuItem)
        
        ID_MENUCONFIG = wx.NewId()
        menuItem = filemenu.Append(ID_MENUCONFIG, _("Config &Editor\tCtrl+E"),_(" Configuration Editor"))
        self.Bind(wx.EVT_MENU, self.ConfigEditor, menuItem)
        
        ID_LOCLISTMENU = wx.NewId()
        menuItem = filemenu.Append(ID_LOCLISTMENU, _("&Loclist Editor\tCtrl+L"),_(" Loclist Editor"))
        self.Bind(wx.EVT_MENU, self.LocListEditor, menuItem)  

        ID_SETTINGSMENU = wx.NewId()
        menuItem = filemenu.Append(ID_SETTINGSMENU, _("&Settings\tCtrl+S"),_(" Program Settings"))
        self.Bind(wx.EVT_MENU, self.Settings, menuItem)         
        
        filemenu.AppendSeparator()

        menuItem = filemenu.Append(wx.ID_EXIT,_("&Quit menu\tCtrl+Q"),_(" Terminate the program"))
        self.Bind(wx.EVT_MENU, self.Quit, menuItem)

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,_("&File")) # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Create a toolbar        
        tb = self.CreateToolBar()
        
        ID_CONFIGEDIT = wx.NewId()
        tb.AddLabelTool(id=ID_CONFIGEDIT, label=_('Config Editor'), bitmap=wx.Bitmap('icons/config.png'), longHelp=_('Open configuration Editor'))
        self.Bind(wx.EVT_TOOL, self.ConfigEditor, id=ID_CONFIGEDIT)
        
        ID_LOCLIST = wx.NewId()
        tb.AddLabelTool(id=ID_LOCLIST, label=_('Loclist Editor'), bitmap=wx.Bitmap('icons/loclist.png'), longHelp=_('Open Loclist editor'))
        self.Bind(wx.EVT_TOOL, self.LocListEditor, id=ID_LOCLIST)
        
        ID_SETTINGS = wx.NewId()
        tb.AddLabelTool(id=ID_SETTINGS, label=_('Change Settings'), bitmap=wx.Bitmap('icons/settings.png'), longHelp=_('Change settings of program'))
        self.Bind(wx.EVT_TOOL, self.Settings, id=ID_SETTINGS)
        
        tb.Realize()
        self.SetSize((425,215))
    
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, _("Editors for the MDRRC-II system"), _("About MDRRC-II Editor"), wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def LocListEditor(self, e):
        mdrrc2_loclist.startup()

    def ConfigEditor(self, e):
        mdrrc2_config.startup()
      
    def Quit(self, e):
        self.Destroy()      
                
    def Settings(self, e):
        self.settings = mdrrcsettings.ReadConfig(None)
        settings_dialog = mdrrcsettings.Settings(self.settings, self)
        res = settings_dialog.ShowModal()
        if res == wx.ID_OK:
            self.settings = settings_dialog.GetSettings()
        settings_dialog.Destroy()

def MenuWindow():
  MenuApp = wx.App(False)
  frame = MenuFrame(None)
  frame.Centre()
  frame.Show(True)
  MenuApp.MainLoop()

MenuWindow()

