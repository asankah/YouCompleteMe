"""TODO(asanka): DO NOT SUBMIT without one-line documentation for ycm.

TODO(asanka): DO NOT SUBMIT without a detailed description of ycm.
"""

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import neovim
import os
import sys
import traceback

DIR_OF_CURRENT_SCRIPT = os.path.dirname( os.path.abspath( __file__ ) )
DIR_OF_YCM = os.path.normpath( os.path.join( DIR_OF_CURRENT_SCRIPT, '..', '..', 'python'))

sys.path.insert(0, DIR_OF_YCM)
from ycm.setup import SetUpSystemPaths, SetUpYCM

@neovim.plugin
class YouCompleteMePlugin:

  def __init__(self, nvim):
    self.nvim_ = nvim
    self.ycm_state_ = None
    self.base_ = None

  @neovim.function('YcmEnable', sync=True)
  def Enable(self):
    assert(isinstance(self, YouCompleteMePlugin))
    SetUpSystemPaths()

    try:
      from ycm import vimsupport
      vimsupport.SetUpVimSupport(self.nvim_)

      self.ycm_state_ = SetUpYCM()

      from ycm import base
      self.base_ = base

    except Exception as error:
      # We don't use PostVimMessage or EchoText from the vimsupport module because
      # importing this module may fail.
      self.nvim_.command( 'redraw | echohl WarningMsg' )
      for line in traceback.format_exc().splitlines():
        self.nvim_.command( "echom '{0}'".format( line.replace( "'", "''" ) ) )

      self.nvim_.command( "echo 'YouCompleteMe unavailable: {0}'"
                   .format( str( error ).replace( "'", "''" ) ) )
      self.nvim_.command( 'echohl None' )
      self.nvim_.command( 'return 0' )

  @neovim.function('YcmGetErrorCount', sync=True)
  def GetErrorCount(self):
    return self.ycm_state_.GetErrorCount()

  @neovim.function('YcmGetWarningCount', sync=True)
  def GetWarningCount(self):
    return self.ycm_state_.GetWarningCount()

  @neovim.function('YcmOnVimLeave', sync=False)
  def OnVimLeave(self):
    self.ycm_state_.OnVimLeave()

  @neovim.function('YcmOnCompleteDone', sync=False)
  def OnCompleteDone(self):
    self.ycm_state_.OnCompleteDone()

  @neovim.function('YcmOnBufferVisit', sync=False)
  def OnBufferVisit(self):
    self.ycm_state_.OnBufferVisit()

  @neovim.function('YcmOnBufferUnload', sync=False)
  def OnBufferUnload(self, buffer_file):
    self.ycm_state_.OnBufferUnload(buffer_file)

  @neovim.function('YcmHandleFileParseRequest', sync=True)
  def HandleFileParseRequest(self, block=False):
    self.ycm_state_.HandleFileParseRequest(block=bool(block))

  @neovim.function('YcmOnFileReadyToParse', sync=False)
  def OnFileReadyToParse(self):
    self.ycm_state_.OnFileReadyToParse()

  @neovim.function('YcmNativeFiletypeCompletionUsable', sync=True)
  def NativeFiletypeCompletionUsable(self):
    return self.ycm_state_.NativeFiletypeCompletionUsable()

  @neovim.function('YcmOnCursorMoved', sync=False)
  def OnCursorMoved(self):
    self.ycm_state_.OnCursorMoved()

  @neovim.function('YcmLastEnteredCharIsIdentifierChar', sync=True)
  def LastEnteredCharIsIdentifierChar(self):
    return self.base_.LastEnteredCharIsIdentifierChar()

  @neovim.function('YcmOnInsertLeave', sync=False)
  def OnInsertLeave(self):
    self.ycm_state_.OnInsertLeave()

  @neovim.function('YcmCurrentIdentifierFinished', sync=True)
  def CurrentIdentifierFinished(self):
    return self.base_.CurrentIdentifierFinished()

  @neovim.function('YcmOnCurrentIdentifierFinished', sync=False)
  def OnCurrentIdentifierFinished(self):
    self.ycm_state_.OnCurrentIdentifierFinished()

  @neovim.function('YcmCreateCompletionRequest', sync=True)
  def CreateCompletionRequest(self, force_semantic=False):
    self.ycm_state_.CreateCompletionRequest(force_semantic=bool(force_semantic))

  @neovim.function('YcmCompletionStartColumn', sync=True)
  def CompletionStartColumn(self):
    return self.base_.CompletionStartColumn()

  @neovim.function('YcmShowDetailedDiagnostic', sync=True)
  def ShowDetailedDiagnostic(self):
    return self.ycm_state_.ShowDetailedDiagnostic()

  @neovim.function('YcmDebugInfo', sync=True)
  def DebugInfo(self):
    return self.ycm_state_.DebugInfo()

  @neovim.function('YcmToggleLogs', sync=False)
  def ToggleLogs(self, args):
    self.ycm_state_.ToggleLogs(args)

  @neovim.function('YcmSendCommandRequest', sync=False)
  def SendCommandRequest(self, args, completer):
    self.ycm_state_.SendCommandRequest(args, completer)

  @neovim.function('YcmGetLogFiles', sync=True)
  def GetLogfiles(self):
    return self.ycm_state_.GetLogfiles()

  @neovim.function('YcmGetDefinedSubcommands', sync=True)
  def GetDefinedSubcommands(self):
    return self.ycm_state_.GetDefinedSubcommands()

  @neovim.function('YcmGetCompletions', sync=True)
  def GetCompletions(self):
    return self.ycm_state_.GetCompletions()

  @neovim.function('YcmPopulateLocationListWithLatestDiagnostics', sync=False)
  def PopulateLocationListWithLatestDiagnostics(self):
    self.ycm_state_.PopulateLocationListWithLatestDiagnostics()

