#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponseDialog.py $ $Id: ResponseDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from ResponseParameters import ResponseParameters
from ResponsePanel import ResponsePanel

class ResponseDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,600))

    self.theResponseId = -1
    self.panel = 0
    self.buildControls(parameters)

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ResponsePanel(self,parameters.responseType(),parameters.panel())
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.RESPONSE_BUTTONCOMMIT_ID,self.onCommit)


  def load(self,response):
    self.theResponseId = response.id()
    self.panel.loadControls(response)

  def onCommit(self,evt):
    if (self.panel.commit() != -1):
      self.EndModal(armid.RESPONSE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = self.panel.parameters()
    parameters.setId(self.theResponseId)
    return parameters
