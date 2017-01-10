# Copyright (C) 2013  Google Inc.
#
# This file is part of YouCompleteMe.
#
# YouCompleteMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YouCompleteMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # noqa

import contextlib
import logging
import requests
import urllib.parse
import json
from future.utils import native
from base64 import b64decode, b64encode
from retries import retries
from requests_futures.sessions import FuturesSession
from ycm.unsafe_thread_pool_executor import UnsafeThreadPoolExecutor
from ycm import vimsupport
from ycmd.utils import ToBytes
from ycmd.hmac_utils import CreateRequestHmac, CreateHmac, SecureBytesEqual
from ycmd.responses import ServerError, UnknownExtraConf

_HEADERS = {'content-type': 'application/json'}
_EXECUTOR = UnsafeThreadPoolExecutor(max_workers=30)
# Setting this to None seems to screw up the Requests/urllib3 libs.
_DEFAULT_TIMEOUT_SEC = 30
_HMAC_HEADER = 'x-ycm-hmac'
_logger = logging.getLogger(__name__)


class BaseRequest(object):

  def __init__(self, ycmd_proxy):
    self._ycmd = ycmd_proxy

  def Start(self):
    pass

  def Done(self):
    return True

  def Response(self):
    return {}


def BuildRequestData(filepath=None):
  """Build request for the current buffer or the buffer corresponding to
  |filepath| if specified."""
  current_filepath = vimsupport.GetCurrentBufferFilepath()

  if filepath and current_filepath != filepath:
    # Cursor position is irrelevant when filepath is not the current buffer.
    return {
        'filepath': filepath,
        'line_num': 1,
        'column_num': 1,
        'file_data': vimsupport.GetUnsavedAndSpecifiedBufferData(filepath)
    }

  line, column = vimsupport.CurrentLineAndColumn()

  return {
      'filepath': current_filepath,
      'line_num': line + 1,
      'column_num': column + 1,
      'file_data': vimsupport.GetUnsavedAndSpecifiedBufferData(current_filepath)
  }


@contextlib.contextmanager
def HandleServerException(ycmd_proxy, display=True, truncate=False):
  """Catch any exception raised through server communication. If it is raised
  because of a unknown .ycm_extra_conf.py file, load the file or ignore it after
  asking the user. Otherwise, log the exception and display its message to the
  user on the Vim status line. Unset the |display| parameter to hide the message
  from the user. Set the |truncate| parameter to avoid hit-enter prompts from
  this message.

  The GetDataFromHandler, PostDataToHandler, and JsonFromFuture functions should
  always be wrapped by this function to avoid Python exceptions bubbling up to
  the user.

  Example usage:

   with HandleServerException():
     response = BaseRequest.PostDataToHandler( ... )
  """
  try:
    yield
  except UnknownExtraConf as e:
    if vimsupport.Confirm(str(e)):
      ycmd_proxy.LoadExtraConfFile({'filepath': e.extra_conf_file})
    else:
      ycmd_proxy.IgnoreExtraConfFile({'filepath': e.extra_conf_file})
  except Exception as e:
    _logger.exception('Error while handling server response')
    if display:
      DisplayServerException(e, truncate)


def DisplayServerException(exception, truncate=False):
  serialized_exception = str(exception)

  # We ignore the exception about the file already being parsed since it comes
  # up often and isn't something that's actionable by the user.
  if 'already being parsed' in serialized_exception:
    return
  vimsupport.PostVimMessage(serialized_exception, truncate=truncate)


def _ToUtf8Json(data):
  return ToBytes(json.dumps(data) if data else None)


def MakeServerException(data):
  if data['exception']['TYPE'] == UnknownExtraConf.__name__:
    return UnknownExtraConf(data['exception']['extra_conf_file'])

  return ServerError('{0}: {1}'.format(data['exception']['TYPE'], data[
      'message']))
