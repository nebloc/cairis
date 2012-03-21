#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetPanel.py $ $Id: AssetPanel.py 527 2011-11-07 11:46:40Z shaf $
import wx
import armid
from BasePanel import BasePanel
import Asset
from Borg import Borg
from AssetSummaryNotebook import AssetSummaryNotebook
from AssetEnvironmentPanel import AssetEnvironmentPanel

class AssetPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.ASSET_ID)
    self.theAssetId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.ASSET_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Short Code',(87,30),armid.ASSET_TEXTSHORTCODE_ID),0,wx.EXPAND)
    typeList = self.dbProxy.getDimensionNames('asset_type')
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.ASSET_COMBOTYPE_ID,typeList),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(AssetSummaryNotebook(self),1,wx.EXPAND)

    mainSizer.Add(AssetEnvironmentPanel(self,self.dbProxy),1,wx.EXPAND)
    if (isUpdateable):
      mainSizer.Add(self.buildCommitButtonSizer(armid.ASSET_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)
    environmentCtrl = self.FindWindowById(armid.ASSET_PANELENVIRONMENT_ID)

  def loadControls(self,asset,isReadOnly=False):
    self.theAssetId = asset.id()
    nameCtrl = self.FindWindowById(armid.ASSET_TEXTNAME_ID)
    nameCtrl.SetValue(asset.name())
    shortCodeCtrl = self.FindWindowById(armid.ASSET_TEXTSHORTCODE_ID)
    shortCodeCtrl.SetValue(asset.shortCode())
    typeCtrl = self.FindWindowById(armid.ASSET_COMBOTYPE_ID)
    typeCtrl.SetValue(asset.type())
    descriptionCtrl = self.FindWindowById(armid.ASSET_TEXTDESCRIPTION_ID)
    descriptionCtrl.SetValue(asset.description())
    sigCtrl = self.FindWindowById(armid.ASSET_TEXTSIGNIFICANCE_ID)
    sigCtrl.SetValue(asset.significance())
    criticalCtrl = self.FindWindowById(armid.ASSET_CHECKCRITICAL_ID)
    criticalCtrl.SetValue(asset.critical())
    if (asset.critical() == True):
      criticalRationaleCtrl = self.FindWindowById(armid.ASSET_TEXTCRITICALRATIONALE_ID)
      criticalRationaleCtrl.Enable()
      criticalRationaleCtrl.SetValue(asset.criticalRationale())

    environmentCtrl = self.FindWindowById(armid.ASSET_PANELENVIRONMENT_ID)
    environmentCtrl.loadControls(asset)
