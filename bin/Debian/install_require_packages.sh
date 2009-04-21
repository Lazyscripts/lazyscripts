#!/bin/bash
# -*- coding: utf-8 -*-
# Copyright (C) 2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 1 Apr 2009
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for debian and ubuntu
# with all architecture.
# Please run as root.

set -x

TOPDIR=`pwd`
TMPDIR="/tmp"

cd $TMPDIR

echo "正在下載並安裝Lazyscripts執行所需的套件...."

echo "Check for required packsges..."
if dpkg -l python-nose python-setuptools git-core &> /dev/null ; then
    echo "Require packages installed."
else
    echo "Require packages not installed."
    apt-get update
    apt-get -y --force-yes install git-core python-setuptools python-nose make
fi

if python -c "import imp;imp.find_module('git')" &> /dev/null ; then
    echo "Require module found."
else
    echo "Require module not found."
    echo "easy_install GitPython" >> $ENV_EXPORT_SCRIPT
fi

cd $TOPDIR

echo "執行完畢！即將啟動Lazyscripts..."

#END
