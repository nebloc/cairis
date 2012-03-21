#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SingleGoalDialog.py $ $Id: SingleGoalDialog.py 368 2010-12-15 17:04:13Z shaf $
import wx
import armid
import WidgetFactory
from SingleObstaclePanel import SingleObstaclePanel
from ObstacleParameters import ObstacleParameters
from ObstacleEnvironmentProperties import ObstacleEnvironmentProperties

class SingleObstacleDialog(wx.Dialog):
  def __init__(self,parent,envName):
    wx.Dialog.__init__(self,parent,armid.OBSTACLE_ID,'New Obstacle',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,400))
    self.theCommitVerb = 'Create'
    self.theEnvironmentName = envName
    self.theObstacleName = ''
    self.theObstacleDefinition = ''
    self.theObstacleCategory = ''
    self.theContributionType = 'and'
    self.theAssociations = []
    self.theSubAssociations = []
    self.theConcerns = []
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = SingleObstaclePanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.OBSTACLE_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.OBSTACLE_TEXTNAME_ID)
    definitionCtrl = self.FindWindowById(armid.OBSTACLE_TEXTDEFINITION_ID)
    categoryCtrl = self.FindWindowById(armid.OBSTACLE_COMBOCATEGORY_ID)
    goalAssociationCtrl = self.FindWindowById(armid.OBSTACLE_LISTGOALS_ID)
    subGoalAssociationCtrl = self.FindWindowById(armid.OBSTACLE_LISTSUBGOALS_ID)
    cCtrl = self.FindWindowById(armid.OBSTACLE_LISTCONCERNS_ID)

    self.theObstacleName = nameCtrl.GetValue()
    self.theObstacleDefinition = definitionCtrl.GetValue()
    self.theObstacleCategory = categoryCtrl.GetValue()
    self.theAssociations = goalAssociationCtrl.dimensions()
    self.theSubAssociations = subGoalAssociationCtrl.dimensions()
    self.theConcerns = cCtrl.dimensions()

    commitLabel = self.theCommitVerb + ' obstacle'

    if len(self.theObstacleName) == 0:
      dlg = wx.MessageDialog(self,'Environment name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theObstacleDefinition) == 0:
      errorTxt = 'No definition'
      dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theObstacleCategory) == 0:
      errorTxt = 'No category'
      dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    self.EndModal(armid.OBSTACLE_BUTTONCOMMIT_ID)

  def parameters(self):
    properties = ObstacleEnvironmentProperties(self.theEnvironmentName,'',self.theObstacleDefinition,self.theObstacleCategory,self.theAssociations,self.theSubAssociations,self.theConcerns)
    parameters = ObstacleParameters(self.theObstacleName,[properties])
    return parameters
