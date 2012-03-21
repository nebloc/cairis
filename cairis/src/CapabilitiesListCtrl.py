#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CapabilitiesListCtrl.py $ $Id: CapabilitiesListCtrl.py 330 2010-10-31 15:01:28Z shaf $
import wx
import armid
import ARM
from CapabilityDialog import CapabilityDialog

class CapabilitiesListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dp,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dbProxy = dp
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Capability')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Value')
    self.SetColumnWidth(1,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.CAPABILITIESLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.CAPABILITIESLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.setCapabilities = {}
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theDimMenu,armid.CAPABILITIESLISTCTRL_MENUADD_ID,self.onAddCapability)
    wx.EVT_MENU(self.theDimMenu,armid.CAPABILITIESLISTCTRL_MENUDELETE_ID,self.onDeleteCapability)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName
    if ((self.theCurrentEnvironment in self.setCapabilities) == False):
      self.setCapabilities[self.theCurrentEnvironment] = set([])

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddCapability(self,evt):
    dlg = CapabilityDialog(self,self.setCapabilities[self.theCurrentEnvironment],self.dbProxy)
    if (dlg.ShowModal() == armid.CAPABILITY_BUTTONADD_ID):
      capName = dlg.capability()
      capValue = dlg.value()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,capName)
      self.SetStringItem(idx,1,capValue)
      self.theSelectedValue = capName
      (self.setCapabilities[self.theCurrentEnvironment]).add(capName)

  def onDeleteCapability(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No capability selected'
      errorLabel = 'Delete Capability'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      (self.setCapabilities[self.theCurrentEnvironment]).remove(selectedValue)

  def load(self,capabilities):
    for name,value in capabilities:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,name)
      self.SetStringItem(idx,1,value)
      (self.setCapabilities[self.theCurrentEnvironment]).add(name)

  def capabilities(self):
    capabilities = []
    for x in range(self.GetItemCount()):
      capName = self.GetItemText(x)
      capValue = self.GetItem(x,1)
      capabilities.append((capName,capValue.GetText()))
    return capabilities
