#!/usr/bin/python

import copy
import wx
import gettext
import ConfigParser as cf
import os
import mdrrc2serial, mdrrcsettings
import mdrrc2_config, mdrrc2_loclist

# Language suppport
gettext.install('mdrrc-editor')

class MenuFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, _("MDRRC-II Config Menu"), size=(425, 175))

        # Read settings for config program
        config = cf.ConfigParser()
        config.read('settings.cfg')
        self.settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore')]

        # A statusbar
        self.CreateStatusBar()

	# A menubar
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuItem = filemenu.Append(wx.ID_ABOUT, _("&About"),_(" Information about this program"))
        self .Bind(wx.EVT_MENU, self.OnAbout, menuItem)
        filemenu.AppendSeparator()

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,_("&File")) # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Create a toolbar        
        tb = self.CreateToolBar()
        
        ID_CONFIGEDIT = wx.NewId()
        tb.AddLabelTool(id=ID_CONFIGEDIT, label=_('Config Editor'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/128x128/categories/preferences-other.png'), longHelp='Open configuration Editor')
        self.Bind(wx.EVT_TOOL, self.ConfigEditor, id=ID_CONFIGEDIT)
        
        ID_LOCLIST = wx.NewId()
        tb.AddLabelTool(id=ID_LOCLIST, label=_('Loclist Editor'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/128x128/actions/view-media-lyrics.png'), longHelp=_('Open Loclist editor'))
        self.Bind(wx.EVT_TOOL, self.LocListEditor, id=ID_LOCLIST)
        
        ID_SETTINGS = wx.NewId()
        tb.AddLabelTool(id=ID_SETTINGS, label=_('Change Settings'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/128x128/actions/configure.png'), longHelp=_('Change settings of program'))
        self.Bind(wx.EVT_TOOL, self.Settings, id=ID_SETTINGS)
        
        tb.Realize()
    
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, _("Editors for the MDRRC-II system"), _("About MDRRC-II Editor"), wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def LocListEditor(self, e):
        mdrrc2_loclist.startup()

    def ConfigEditor(self, e):
        mdrrc2_config.startup()
                
    def Settings(self, e):
        config = cf.ConfigParser()
        config.read('settings.cfg')
        self.settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore')]
        settings_dialog = mdrrcsettings.Settings(self.settings, self)
        res = settings_dialog.ShowModal()
        if res == wx.ID_OK:
            self.settings = settings_dialog.GetSettings()
        settings_dialog.Destroy()

def MenuWindow():
  MenuApp = wx.PySimpleApp()
  frame = MenuFrame(None)
  frame.Centre()
  frame.Show(True)
  MenuApp.MainLoop()

MenuWindow()

