#!/usr/bin/python

import wx
import wx.grid
import mdrrc2serial
import copy
import gettext
import mdrrcsettings
import ConfigParser as cf
import os

# Language suppport
gettext.install('mdrrc-editor')

class LoclistFrame(wx.Frame, list):
    def __init__(self, parent, list):
        wx.Frame.__init__(self, parent, -1, _("MDRRC-II Loc Editor"), size=(350, 1300))

        # Read settings for config program
        config = cf.ConfigParser()
        config.read('settings.cfg')
        self.settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore')]
        
        global selected_address
        
        # A statusbar
        global sb
        sb = self.CreateStatusBar()
        
	# A menubar
        filemenu= wx.Menu()

        # Create menu items
        menuItem = filemenu.Append(wx.ID_ABOUT, _("&About"),_(" Information about this program"))
        self.Bind(wx.EVT_MENU, self.OnAbout, menuItem)
        filemenu.AppendSeparator()
        
        menuItem = filemenu.Append(wx.ID_NEW, _("&New loco"),_(" Create new loco"))
        self.Bind(wx.EVT_MENU, self.NewLoco, menuItem)        
        filemenu.AppendSeparator()

        menuItem = filemenu.Append(wx.ID_DELETE, _("&Delete loco"),_(" Delete loco"))
        self.Bind(wx.EVT_MENU, self.DelLoc, menuItem)        
        filemenu.AppendSeparator()

        menuItem = filemenu.Append(wx.ID_SAVE, _("&Save and exit"),_(" Save and reboot"))
        self.Bind(wx.EVT_MENU, self.SaveAndReset, menuItem)

        menuItem = filemenu.Append(wx.ID_SAVEAS, _("Save &only"),_(" Save without reboot"))
        self.Bind(wx.EVT_MENU, self.SaveOnly, menuItem)
        
        filemenu.AppendSeparator()
        menuItem = filemenu.Append(wx.ID_EXIT,_("E&xit without reset"),_(" Terminate the program"))
        self.Bind(wx.EVT_MENU, self.SaveOnly, menuItem)

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,_("&File")) # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        
        # Create a toolbar
        ID_NEWLOCO = wx.NewId()
        ID_DELLOCO = wx.NewId()
        ID_SAVE = wx.NewId()
        ID_SAVERESET = wx.NewId()
        ID_REFRESH = wx.NewId()
        tb = self.CreateToolBar()
        tb.AddLabelTool(id=ID_NEWLOCO, label=_('New Loco'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/document-new.png'), longHelp=_('Add a new loco')) 
        tb.AddLabelTool(id=ID_DELLOCO, label=_('Delete Loco'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/edit-delete.png'), longHelp=_('Delete an existing loco'))
        tb.AddLabelTool(id=ID_SAVE, label=_('Store config'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/document-save.png'), longHelp=_('Store config on controller'))
        tb.AddLabelTool(id=ID_SAVERESET, label=_('Store config and reset'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/document-save-all.png'), longHelp=_('Store config and reset controller'))
        tb.AddLabelTool(id=ID_REFRESH, label=_('Refresh'), bitmap=wx.Bitmap('/usr/share/icons/oxygen/48x48/actions/view-refresh.png'), longHelp=_('Refresh listing'))
        tb.Realize()
        self.Bind(wx.EVT_TOOL, self.NewLoco, id=ID_NEWLOCO)
        self.Bind(wx.EVT_TOOL, self.SaveOnly, id=ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.SaveAndReset, id=ID_SAVERESET)
        self.Bind(wx.EVT_TOOL, self.DelLoc, id=ID_DELLOCO)
        self.Bind(wx.EVT_TOOL, self.Refresh, id=ID_REFRESH)
        
        #Create an editor for the protocol selection
        ProtocolEditor = wx.grid.GridCellChoiceEditor(['DCC','MM'], allowOthers=False)

        # Determine size of grid
        NumberOfLines = len(list)
        NumberOfRows = len(list[1])+1

        # Create grid
        self.locgrid = wx.grid.Grid(id=-1, name='locgrid',
              parent=self, pos=wx.Point(0, 0), style=0)
        self.locgrid.CreateGrid(NumberOfLines, NumberOfRows)

        # Set headers for columns
        self.locgrid.SetColLabelValue(0, _("Address"))
        self.locgrid.SetColLabelValue(1, _("Name"))
        self.locgrid.SetColLabelValue(2, _("Protocol"))

        # Fill grid with data from list
        BuildLocoGrid(list, self.locgrid)

        # Update the statusbar
        CountLocs(list, sb)

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

       # Selection
        self.locgrid.Bind(wx.grid.EVT_GRID_SELECT_CELL, 
              self._OnSelectedCell )

    def _OnSelectedCell( self, event ):
         """Internal update to the selection tracking list"""
         global selected_address
         cursor = [ event.GetRow() ]
         selected_address = self.locgrid.GetCellValue(int(cursor[0]),0)
         UpdateStatus('Selected loco = '+str(selected_address))
         event.Skip()

    #This method fires when a grid cell changes. We are simply showing
    #what has changed and any associated index and client data. Typically
    #this method is where you would put your real code for processing grid
    #cell changes.
    def OnGrid1GridCellChange(self, event):
        Row = event.GetRow()
        Col = event.GetCol()

        global listoflocs
        global sb
        
        #All cells have a value, regardless of the editor.
        print 'Changed cell: (%u, %u)' % (Row, Col)
        print 'value: %s' % self.locgrid.GetCellValue(Row, Col)
        
        print ''            #blank line to make it pretty.

        # Modify item in list as a result from editing in the grid
        key = self.locgrid.GetCellValue(Row, 0)
        print('Data was: '+listoflocs[int(key)][Col-1])
        print('Data is : '+self.locgrid.GetCellValue(Row, Col))
        listoflocs[int(key)][Col-1] = self.locgrid.GetCellValue(Row, Col).encode('ascii','ignore')
        if Col == 1:
           mdrrc2serial.ChangeLocName(int(key),self.locgrid.GetCellValue(Row, Col))
        elif Col == 2:
           mdrrc2serial.ChangeLocType(int(key))
           
        CountLocs(listoflocs,sb)
        event.Skip()
 
    
    #This method fires when the underlying GridCellChoiceEditor ComboBox
    #is done with a selection.
    def OnGrid1ComboBox(self, event):
        #Save the index and client data for later use.
        self.locgrid.index = self.comboBox.GetSelection()
        self.locgrid.data = self.comboBox.GetClientData(self.locgrid.index)
        
        print 'ComboBoxChanged: %s' % self.comboBox.GetValue()
        print 'ComboBox index: %u' % self.locgrid.index 
        print 'ComboBox data: %u\n' % self.locgrid.data
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
        
        print 'ComboBoxText: %s' % self.comboBox.GetValue()
        print 'ComboBox index: %u\n' % self.locgrid.index
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
            
            #Update the silly client data counter0
            self.locgrid.counter = self.locgrid.counter + 1
        
        print 'OnGrid1EditorHidden: (%u, %u)\n' % (Row, Col)

        event.Skip()

    #This method fires when a cell editor is created. It appears that this
    #happens only on the first edit using that editor.
    def OnGrid1GridEditorCreated(self, event):
        Row = event.GetRow()
        Col = event.GetCol()
        
        print 'OnGrid1EditorCreated: (%u, %u)\n' % (Row, Col)
        
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
            for (item, data) in self.locgrid.list:
                self.comboBox.Append(item, data)
        
        event.Skip()

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, _("A loc editor for the MDRRC-II system"), _("About Loc Editor"), wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def SaveAndReset(self, e):
        print('save and reset')
        mdrrc2serial.StopConfig()
        self.Destroy()

    def NewLoco(self, e):
        print(listoflocs)
        chgdep = NewLocoDialog(None, 
            title=_('New Loco Address'))
        chgdep.ShowModal()
        chgdep.Destroy()  

    def DelLoc(self, e):
        print('delete loc')
        BuildLocoGrid(listoflocs,self.locgrid)

    def SaveOnly(self, e):
        print('save only')
        mdrrc2serial.StoreConfig()
        self.Destroy()
        
    def SaveOnly(self, e):
        print('refresh')
        wx.Yield()
        BuildLocoGrid(list, self.locgrid)
        
  
class NewLocoDialog(wx.Dialog):
    
    def __init__(self, *args, **kw):
        super(NewLocoDialog, self).__init__(*args, **kw) 
            
        self.InitUI()
        self.SetSize((250, 110))
        self.SetTitle(_("New Loco Address"))
        
    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label=_('Loco'))
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)        
        global text
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
        hbox1.Add(wx.RadioButton(pnl, label=_('Adress')))
        text = wx.TextCtrl(pnl)
        hbox1.Add(text, flag=wx.LEFT, border=5)
        
        sbs.Add(hbox1)
        
        pnl.SetSizer(sbs)
       
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label=_('Save'))
        closeButton = wx.Button(self, label=_('Cancel'))
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnCancel)
           
    def OnClose(self, e):
        print('Adding loco '+text.GetValue())
        UpdateStatus(mdrrc2serial.AddLoco(text.GetValue()))
        self.Destroy()
        
    def OnCancel(self, e):
        self.Destroy()        

def BuildLocoGrid(list,locgrid):
  ProtocolEditor = wx.grid.GridCellChoiceEditor(['DCC','MM'], allowOthers=False)
  print(list)
  for l, (index) in enumerate(zip(list)):
    locgrid.SetCellValue(l, 0, str(index[0]))
    locgrid.SetReadOnly(l, 0, True)
    locgrid.SetCellValue(l, 1, list[index[0]][0])
    locgrid.SetCellValue(l, 2, list[index[0]][1])
    locgrid.SetCellEditor(l, 2, ProtocolEditor)

def UpdateStatus(text):
  sb.SetStatusText(text)

def PrintLocList(loclist):
  print("Address".ljust(10)+"Name".ljust(10)+"Protocol")
  for l in loclist:
    print(str(l).ljust(10)+loclist[l][0].ljust(10)+loclist[l][1])

def CountLocs(list, sb):
  NumberOfDCCLocs = 0
  NumberOfMMLocs = 0
  for l in enumerate(list):
    if (list[l[1]][1] == 'DCC'):
      NumberOfDCCLocs += 1
    else:
      NumberOfMMLocs += 1
  sb.SetStatusText(_('Current loc addresses: ')+str(NumberOfDCCLocs)+' DCC / '+str(NumberOfMMLocs)+' MM') 

def Foutmelding(parent, message, caption = _('MDRRC-II loc editor: Error!')):
  dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
  dlg.ShowModal()
  dlg.Destroy()

def startup():
  # Read settings for config program
  config = cf.ConfigParser()
  config.read('settings.cfg')
  settings = [config.get('Connection', 'port').encode('ascii','ignore'), config.get('Connection', 'speed').encode('ascii','ignore')]
  
# Bug: Uncommenting this leads to not being able to close menu...
#  app = wx.PySimpleApp()
  
  if mdrrc2serial.TestConnection():
    loclist = mdrrc2serial.ParseLocList()
    if len(loclist) > 0:
      frame = LoclistFrame(None, loclist)
      frame.Centre()
      frame.Show(True)
      app.MainLoop()
    else:
      Foutmelding(None, _('Centrale not in config mode or not connected!\nMake sure MDRRC-II controller is connected and set to config mode (SET->CON)...'))
  else:
    Foutmelding(None, _('Connection parameters not correct or controller not connected!'))
  
if __name__ == '__main__':
  startup()
