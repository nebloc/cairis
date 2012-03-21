#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCaseDialog.py $ $Id: MisuseCaseDialog.py 413 2011-01-20 14:49:30Z shaf $
import wx
import armid
from TaskParameters import TaskParameters
import WidgetFactory
from MisuseCasePanel import MisuseCasePanel
from MisuseCaseParameters import MisuseCaseParameters
import ObjectFactory
from Borg import Borg

class MisuseCaseDialog(wx.Dialog):
  def __init__(self,parent,isCreate = False):
    wx.Dialog.__init__(self,parent,armid.MISUSECASE_ID,'Create Misuse Case',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(700,800))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theMisuseCaseId = -1
    self.theName = ''
    self.theRisk = ''
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(isCreate)
    self.theCommitVerb = 'Create'

  def buildControls(self,isCreate):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = MisuseCasePanel(self,self.dbProxy)
    self.panel.buildControls(isCreate)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.MISUSECASE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,mc):
    mc.theThreatName,mc.theVulnerabilityName  = self.dbProxy.misuseCaseRiskComponents(mc.name())
    self.loadMisuseCase(mc)

  def loadMisuseCase(self,mc):
    self.theMisuseCaseId = mc.id()
    self.panel.loadMisuseCase(mc)
    self.theCommitVerb = 'Edit'
    self.SetTitle('Edit Misuse Case')

  def loadRiskComponents(self,riskName,threatName,vulnerabilityName):
    self.panel.loadRiskComponents(riskName,threatName,vulnerabilityName)

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.MISUSECASE_TEXTNAME_ID)
    riskCtrl = self.FindWindowById(armid.MISUSECASE_TEXTRISK_ID)
    environmentCtrl = self.FindWindowById(armid.MISUSECASE_PANELENVIRONMENT_ID)

    self.theName = nameCtrl.GetValue()
    self.theRisk = riskCtrl.GetValue()
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()
    commitLabel = self.theCommitVerb +  ' Misuse Case'

    for environmentProperties in self.theEnvironmentProperties:
      if len(environmentProperties.narrative()) == 0:
        errorTxt = 'No narrative defined in environment ' + environmentProperties.name()
        dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
        dlg.ShowModal()
        dlg.Destroy()
        return
    self.EndModal(armid.MISUSECASE_BUTTONCOMMIT_ID)

  def parameters(self): 
    parameters = MisuseCaseParameters(self.theName,self.theEnvironmentProperties,self.theRisk)
    parameters.setId(self.theMisuseCaseId)
    return parameters
