#!/usr/bin/python

import copy
import wx
import wx.grid
import gettext
import ConfigParser as cf
import os
import csv

# Internal modules for mdrrc
import mdrrc2serial,mdrrcsettings

# Language suppport
gettext.install('mdrrc-editor')

class ConfiglistFrame(wx.Frame, list):
    def __init__(self, parent, list):
        wx.Frame.__init__(self, parent, -1, _("MDRRC-II Config List"), size=(310, 465))

        # Read settings for config program
        config = cf.ConfigParser()
        config.read('settings.cfg')
        self.settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore'), config.get('Export','filename').encode('ascii','ignore'), config.get('Export','configfilename').encode('ascii','ignore')]

        # A statusbar
        self.CreateStatusBar()

	# A menubar
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuItem = filemenu.Append(wx.ID_ABOUT, _("&About"),_(" Information about this program"))
        self .Bind(wx.EVT_MENU, self.OnAbout, menuItem)
        menuItem = filemenu.Append(wx.ID_SAVE, _("&Save and exit"),_(" Save and reboot"))
        self.Bind(wx.EVT_MENU, self.SaveAndReset, menuItem)
        menuItem2 = filemenu.Append(wx.ID_SAVEAS, _("Save &only"),_(" Save without reboot"))
        self.Bind(wx.EVT_MENU, self.SaveOnly, menuItem2)
        
        filemenu.AppendSeparator()
        
        menuItem3 = filemenu.Append(wx.ID_EXIT,_("E&xit without reset"),_(" Terminate the program"))
        self.Bind(wx.EVT_MENU, self.SaveOnly, menuItem3)

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,_("&File")) # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Create a toolbar
        tb = self.CreateToolBar()
        
        ID_SAVE = wx.NewId()
        tb.AddLabelTool(id=ID_SAVE, label=_('Store config'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/document-save.png'), longHelp=_('Store config on controller'))
        self.Bind(wx.EVT_TOOL, self.SaveOnly, id=ID_SAVE)
        
        ID_SAVERESET = wx.NewId()        
        tb.AddLabelTool(id=ID_SAVERESET, label=_('Store config and reset'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/document-save-all.png'), longHelp=_('Store config and reset controller'))
        self.Bind(wx.EVT_TOOL, self.SaveAndReset, id=ID_SAVERESET)

        
        ID_EXPORT = wx.NewId()
        tb.AddLabelTool(id=ID_EXPORT, label=_('Export'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/view-refresh.png'), longHelp=_('Export config'))
        self.Bind(wx.EVT_TOOL, self.Export, id=ID_EXPORT)
     
        tb.Realize()

        #Create an editor for the protocol selection
        Editor_OnOff = wx.grid.GridCellChoiceEditor(['On.','Off.'], allowOthers=False)
        Editor_YesNo = wx.grid.GridCellChoiceEditor(['Yes.','No.'], allowOthers=False)
        Editor_EnabledDisabled = wx.grid.GridCellChoiceEditor(['Enabled.','Disabled.'], allowOthers=False)
        Editor_HighLow = wx.grid.GridCellChoiceEditor(['High.','Low.'], allowOthers=False)

        # Determine size of grid
        NumberOfLines = len(list)
        NumberOfRows = 2

        # Create grid
        self.locgrid = wx.grid.Grid(id=-1, name='locgrid', parent=self, pos=wx.Point(0, 0), style=0)
        self.locgrid.CreateGrid(NumberOfLines, NumberOfRows)

        # Set headers for columns
        self.locgrid.SetColLabelValue(0, _("Key"))
        self.locgrid.SetColLabelValue(1, _("Value"))

        # Fill grid with data from list
        i = 0
        for l in list:
          self.locgrid.SetCellValue(i, 0, str(l))
          self.locgrid.SetReadOnly(i, 0, True)
          self.locgrid.SetCellValue(i, 1, list[l])
          if (l == 'Turnout DCC Only') or (l == 'XPressNet') or (l == 'Turnout auto off'):
            self.locgrid.SetCellEditor(i, 1, Editor_OnOff)
          elif (l == 'Touch calibrated') or (l == 'MM locs only'):
            self.locgrid.SetCellEditor(i, 1, Editor_YesNo)
          elif (l == 'Booster S/C enable') or (l == 'Acknowlegde enable') or (l == 'I2C manual control'):
            self.locgrid.SetCellEditor(i, 1, Editor_EnabledDisabled)
          elif (l == 'Booster S/C change'):
            self.locgrid.SetCellEditor(i, 1, Editor_HighLow)
          i += 1

        self.locgrid.AutoSizeColumn(0)
        self.locgrid.AutoSizeColumn(1)
        global listoflocs
        listoflocs = list

	# Experimental part: handling selection
        self.locgrid.data = None
        self.locgrid.index = None

        self.locgrid.Bind(wx.grid.EVT_GRID_CELL_CHANGE,
              self.OnGrid1GridCellChange)

        self.locgrid.Bind(wx.grid.EVT_GRID_EDITOR_CREATED,
              self.OnGrid1GridEditorCreated)

        self.locgrid.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN,
              self.OnGrid1GridEditorHidden)
              
        self.Centre()
        self.Show(True)

    #This method fires when a grid cell changes. We are simply showing
    #what has changed and any associated index and client data. Typically
    #this method is where you would put your real code for processing grid
    #cell changes.
    def OnGrid1GridCellChange(self, event):
        Row = event.GetRow()
        Col = event.GetCol()

        global configList
        
        #All cells have a value, regardless of the editor.

        # Modify item in list as a result from editing in the grid
        key = self.locgrid.GetCellValue(Row, 0)
        OldValue = configList[key]
        NewValue = self.locgrid.GetCellValue(Row, Col).encode('ascii','ignore')
        configList[key] = NewValue
        mdrrc2serial.ChangeConfig(key, NewValue, configList)
        event.Skip()
 
    #This method fires when the underlying GridCellChoiceEditor ComboBox
    #is done with a selection.
    def OnGrid1ComboBox(self, event):
        #Save the index and client data for later use.
        self.locgrid.index = self.comboBox.GetSelection()
        self.locgrid.data = self.comboBox.GetClientData(self.locgrid.index)
        event.Skip()


    #This method fires when any text editing is done inside the text portion
    #of the ComboBox. This method will fire once for each new character, so
    #the print statements will show the character by character changes.
    def OnGrid1ComboBoxText(self, event):
        #The index for text changes is always -1. This is how we can tell
        #that new text has been entered, as opposed to a simple selection
        #from the drop list. Note that the index will be set for each character,
        #but it will be -1 every time, so the final result of text changes is
        #always an index of -1. The value is whatever text that has been 
        #entered. At this point there is no client data. We will have to add
        #that later, once all of the text has been entered.
        self.locgrid.index = self.comboBox.GetSelection()
        event.Skip()

    #This method fires after editing is finished for any cell. At this point
    #we know that any added text is complete, if there is any.
    def OnGrid1GridEditorHidden(self, event):
        Row = event.GetRow()
        Col = event.GetCol()
        
        #If the following conditions are true, it means that new text has 
        #been entered in a GridCellChoiceEditor cell, in which case we want
        #to append the new item to our selection list.
        if Row == 0 and self.locgrid.index == -1:
            #Get the new text from the grid cell
            item = self.comboBox.GetValue()
            
            #The new item will be appended to the list, so its new index will
            #be the same as the current length of the list (origin zero).
            self.locgrid.index = self.comboBox.GetCount()
            
            #Generate some unique client data. Remember this counter example
            #is silly, but it makes for a reasonable demonstration. Client
            #data is optional. If you can use it, this is where you attach
            #your real client data.
            self.locgrid.data = self.locgrid.counter
            
            #Append the new item to the selection list. Remember that this list
            #is used by all cells with the same editor, so updating the list
            #here updates it for every cell using this editor.
            self.comboBox.Append(item, self.locgrid.data)
            
            #Update the silly client data counter
            self.locgrid.counter = self.locgrid.counter + 1
        
        event.Skip()

    #This method fires when a cell editor is created. It appears that this
    #happens only on the first edit using that editor.
    def OnGrid1GridEditorCreated(self, event):
        Row = event.GetRow()
        Col = event.GetCol()
        
        #In this example, all cells in row 0 are GridCellChoiceEditors,
        #so we need to setup the selection list and bindings. We can't
        #do this in advance, because the ComboBox control is created with
        #the editor.
        if Row == 0:
            #Get a reference to the underlying ComboBox control.
            self.comboBox = event.GetControl()
            
            #Bind the ComboBox events.
            self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnGrid1ComboBox)
            self.comboBox.Bind(wx.EVT_TEXT, self.OnGrid1ComboBoxText)
            
            #Load the initial choice list.
        
        event.Skip()

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, _("A config editor for the MDRRC-II system"), _("About Config Editor"), wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def SaveAndReset(self, e):
        mdrrc2serial.StopConfig()
        self.Destroy()

    def SaveOnly(self, e):
        mdrrc2serial.StoreConfig()
        self.Destroy()

    def Export(self, e):
        csvfile = self.settings[3]
        with open(csvfile, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                writer.writerow([_('Parameter'), _('Value')])
                for c in configList:
                        writer.writerow([c]+[configList[c]])
        self.Destroy()

def Foutmelding(parent, message, caption = _('MDRRC-II config editor: Error!')):
  dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
  dlg.ShowModal()
  dlg.Destroy()

def startup():
  # Read settings for config program
  config = cf.ConfigParser()
  config.read('settings.cfg')
  settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore'), config.get('Export','filename').encode('ascii','ignore'), config.get('Export','configfilename').encode('ascii','ignore')]
  if mdrrc2serial.TestConnection():
    global configList
    configList = mdrrc2serial.ReadConfig()

    if len(configList) > 0:
      frame = ConfiglistFrame(None, configList)
    else:
      Foutmelding(None, _('Centrale not in config mode!\nMake sure MDRRC-II controller is connected and set to config mode (SET->CON)...'))
  else:
    Foutmelding(None, _('Connection parameters not correct or controller not connected!'))

if __name__ == '__main__':
  startup()
