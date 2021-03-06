#!/usr/bin/python
#
# Copyright 2015 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires Python 2.4+

import os
import re
import platform

from UbuntuPatching import UbuntuPatching
from debianPatching import debianPatching
from redhatPatching import redhatPatching
from centosPatching import centosPatching
from SuSEPatching import SuSEPatching
from oraclePatching import oraclePatching

# Define the function in case waagent(<2.0.4) doesn't have DistInfo()
def DistInfo():
    if 'FreeBSD' in platform.system():
        release = re.sub('\-.*\Z', '', str(platform.release()))
        distinfo = ['FreeBSD', release]
        return distinfo
    if 'linux_distribution' in dir(platform):
        distinfo = list(platform.linux_distribution(full_distribution_name=0))
        # remove trailing whitespace in distro name
        distinfo[0] = distinfo[0].strip()
        return distinfo
    else:
        return platform.dist()

def GetDistroPatcher(logger):
    """
    Return DistroPatcher object.
    NOTE: Logging is not initialized at this point.
    """
    dist_info = DistInfo()
    if 'Linux' in platform.system():
        Distro = dist_info[0]
    else: # I know this is not Linux!
        if 'FreeBSD' in platform.system():
            Distro = platform.system()
    Distro = Distro.strip('"')
    Distro = Distro.strip(' ')
    patching_class_name = Distro + 'Patching'

    if not globals().has_key(patching_class_name):
        logger.log('{0} is not a supported distribution.'.format(Distro))
        return None
    patchingInstance = globals()[patching_class_name](logger,dist_info)
    return patchingInstance