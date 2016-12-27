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

from ycm.client.base_request import (BaseRequest, BuildRequestData,
                                     HandleServerException)


class CompleterAvailableRequest(BaseRequest):

  def __init__(self, filetypes, ycmd_proxy):
    super(CompleterAvailableRequest, self).__init__(ycmd_proxy)
    self.filetypes = filetypes
    self._response = None

  def Start(self):
    request_data = BuildRequestData()
    request_data.update({'filetypes': self.filetypes})
    with HandleServerException(self._ycmd):
      self._response = self._ycmd.FiletypeCompletionAvailable(
          request_data).result()

  def Response(self):
    return self._response


def SendCompleterAvailableRequest(filetypes, ycmd_proxy):
  request = CompleterAvailableRequest(filetypes, ycmd_proxy)
  # This is a blocking call.
  request.Start()
  return request.Response()
