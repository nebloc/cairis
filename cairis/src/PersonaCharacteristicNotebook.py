#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristicNotebook.py $ $Id: PersonaCharacteristicNotebook.py 465 2011-05-01 16:00:00Z shaf $

from ReferenceListCtrl import ReferenceListCtrl
from WarrantListCtrl import WarrantListCtrl
from PersonaCharacteristic import PersonaCharacteristic
from Borg import Borg
import armid
import wx

class GeneralPage(wx.Panel):
  def __init__(self,parent,isTask,taskComboShown):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    if (isTask and taskComboShown):
      b = Borg()
      self.dbProxy = b.dbProxy
      tasks = self.dbProxy.getDimensionNames('task')
      tBox = wx.StaticBox(self,-1,'Task')
      tBoxSizer = wx.StaticBoxSizer(tBox,wx.VERTICAL)
      topSizer.Add(tBoxSizer,0,wx.EXPAND)
      self.taskCtrl = wx.ComboBox(self,armid.TASKCHARACTERISTIC_COMBOTASK_ID,'',choices=tasks,size=wx.DefaultSize,style=wx.CB_READONLY)
      tBoxSizer.Add(self.taskCtrl,0,wx.EXPAND)

    qBox = wx.StaticBox(self,-1,'Modal Qualifier')
    qBoxSizer = wx.StaticBoxSizer(qBox,wx.VERTICAL)
    topSizer.Add(qBoxSizer,0,wx.EXPAND)
    self.qualifierCtrl = wx.TextCtrl(self,armid.PERSONACHARACTERISTIC_TEXTQUALIFIER_ID,'')
    qBoxSizer.Add(self.qualifierCtrl,0,wx.EXPAND)

    defBox = wx.StaticBox(self,-1,'Definition')
    defBoxSizer = wx.StaticBoxSizer(defBox,wx.VERTICAL)
    topSizer.Add(defBoxSizer,1,wx.EXPAND)
    self.definitionCtrl = wx.TextCtrl(self,armid.PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID,'',style=wx.TE_MULTILINE)
    defBoxSizer.Add(self.definitionCtrl,1,wx.EXPAND)

    self.SetSizer(topSizer)

class ReferencePage(wx.Panel):
  def __init__(self,parent,winId,crTypeName,pName):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    pBox = wx.StaticBox(self,-1)
    pBoxSizer = wx.StaticBoxSizer(pBox,wx.HORIZONTAL)
    topSizer.Add(pBoxSizer,1,wx.EXPAND)
    refList = ReferenceListCtrl(self,winId,crTypeName,pName)
    pBoxSizer.Add(refList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class BackingPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    pBox = wx.StaticBox(self,-1)
    pBoxSizer = wx.StaticBoxSizer(pBox,wx.HORIZONTAL)
    topSizer.Add(pBoxSizer,1,wx.EXPAND)
    self.backingList = wx.ListCtrl(self,armid.PERSONACHARACTERISTIC_LISTBACKING_ID,size=wx.DefaultSize,style=wx.LC_REPORT)
    self.backingList.InsertColumn(0,'Backing')
    self.backingList.SetColumnWidth(0,150)
    self.backingList.InsertColumn(1,'Warrant')
    self.backingList.SetColumnWidth(1,300)
    pBoxSizer.Add(self.backingList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class WarrantPage(wx.Panel):
  def __init__(self,parent,backingPage,isTask,pName):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    pBox = wx.StaticBox(self,-1)
    pBoxSizer = wx.StaticBoxSizer(pBox,wx.HORIZONTAL)
    topSizer.Add(pBoxSizer,1,wx.EXPAND)
    backingList = backingPage.FindWindowById(armid.PERSONACHARACTERISTIC_LISTBACKING_ID)
    refList = WarrantListCtrl(self,backingList,isTask,pName)
    pBoxSizer.Add(refList,1,wx.EXPAND)
    self.SetSizer(topSizer)

class PersonaCharacteristicNotebook(wx.Notebook):
  def __init__(self,parent,pName = '',isTask = False,taskComboShown = True):
    wx.Notebook.__init__(self,parent,armid.ASSET_NOTEBOOKENVIRONMENT_ID)
    self.thePersona = pName
    genPage = GeneralPage(self,isTask,taskComboShown)
    groundsPage = ReferencePage(self,armid.PERSONACHARACTERISTIC_LISTGROUNDS_ID,'grounds',self.thePersona)

    backingPage = BackingPage(self)
    warrantPage = WarrantPage(self,backingPage,isTask,self.thePersona)

    rebPage = ReferencePage(self,armid.PERSONACHARACTERISTIC_LISTREBUTTAL_ID,'rebuttal',self.thePersona)
    self.AddPage(genPage,'General')
    self.AddPage(groundsPage,'Grounds')
    self.AddPage(warrantPage,'Warrant')
    self.AddPage(backingPage,'Backing')
    self.AddPage(rebPage,'Rebuttal')


  def loadControls(self,objt):
    qualCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_TEXTQUALIFIER_ID)
    charCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    groundsCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTGROUNDS_ID)
    warrantCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTWARRANT_ID)
    rebuttalCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTREBUTTAL_ID)

    qualCtrl.SetValue(objt.qualifier())
    charCtrl.SetValue(objt.characteristic())     
    groundsCtrl.load(objt.grounds())
    warrantCtrl.load(objt.id(),objt.warrant())
    rebuttalCtrl.load(objt.rebuttal())
