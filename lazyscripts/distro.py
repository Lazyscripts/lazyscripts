#!/usr/bin/env python
# -*- encoding=utf-8 -*-
#
# Copyright © 2010 Hsin Yi Chen
#
# Lazyscripts is a free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This software is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this software; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
import commands
import os
import platform

from lazyscripts import pkgmgr
from lazyscripts.constant import *

class DistrobutionNotFound(Exception):
    "The distrobution can not be detected."

class Distribution(object):

    """
    Hyper Layer Distribution Informateions
    """

    #{{{def __str__(self):
    def __str__(self):
        return "%s %s (%s)" % (self.name,self.version,self.codename)
    #}}}

    #{{{def __repr__(self):
    def __repr__(self):
        return self.__str__()
    #}}}

    #{{{def __init__(self):
    def __init__(self):
        # linux_distribution is insted of dist
        # Ref: http://docs.python.org/library/platform.html
        if platform.python_version() < PYTHON_VERSION:
            (self.name, self.version, self.codename) = platform.dist()
        else:
            (self.name, self.version, self.codename) = platform.linux_distribution()

        # Because built-in funciton may not recognize all distrobution.
        self._reduce_name()
        self._reduce_version()
        self._reduce_architecture()
    #}}}

    #{{{def pkgsrc_name(self):
    @property
    def pkgsrc_name(self):
        """The source list file name of Package Manager

        @return str
        """
        if self.name in DIST_DEB_BASE:
            extend = 'list'
        elif self.name in DIST_RPM_BASE:
            extend = 'sh'
        return "lzs_%s_%s_%s.%s" % (platform.machine(),
                                          self.name,
                                          self.version,
                                          extend)
    #}}}

    #{{{def pkgmgr(self):
    @property
    def pkgmgr(self):
        "lazy initialize for package manager."
        return self.__dict__.setdefault('_pkgmgr', pkgmgr.get_pkgmgr(self.name))
    #}}}

    #{{{def _reduce_name(self):
    def _reduce_name(self):
        self.name = self.name.lower().strip()
        if not self.name:
            if os.path.exists('/etc/arch-release'):
                self.name = 'arch'
            elif os.path.exists('/usr/bin/pkg') and \
                commands.getoutput('cat /etc/release | grep "OpenSolaris"'):
                self.name = DIST_OPENSOLARIS
            else:
                raise DistrobutionNotFound()
        elif self.name == DIST_UBUNTU:
            if os.path.exists('/etc/ezgo-release'):
                self.name = DIST_EZGO
        elif self.name == DIST_SUSE:
            if commands.getoutput('cat /etc/SuSE-release | grep "openSUSE"'):
                self.name = DIST_OPENSUSE
        elif self.name == DIST_REDHAT:
            if commands.getoutput('cat /etc/redhat-release | grep "Red Hat"'):
                self.name = DIST_REDHAT
            if commands.getoutput('cat /etc/redhat-release | grep "CentOS"'):
                self.name = DIST_CENTOS
        elif self.name in ('mandrake', 'mandriva linux'):
            if os.path.exists('/etc/mandriva-release') and \
               commands.getoutput('cat /etc/mandriva-release | grep "Mandriva"'):
             self.name = DIST_MANDRIVA
    #}}}

    #{{{def _reduce_version(self):
    def _reduce_version(self):
        if self.name == DIST_OPENSOLARIS and not self.version:
            self.version = commands.getoutput('cat /etc/release | grep "OpenSolaris" | cut -d " " -f 27')
        elif self.name == DIST_DEBIAN:
            self.version = self.version.split('.')[0]
        elif self.name == DIST_EZGO:
            self.version = commands.getoutput('cat /etc/ezgo-release | grep "Version" | cut -d ":" -f 2')
    #}}}

    def _reduce_architecture(self):
        arch = platform.architecture()[0]
        if arch == '32bit':
            self.architecture = ARCH_I386
        elif arch == '64bit':
            self.architecture = ARCH_AMD64
        else:
            self.architecture = None

pass
