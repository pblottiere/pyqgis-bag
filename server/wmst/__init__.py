# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"
__license__ = "GPLv3"


def serverClassFactory(serverIface):
    from .kronos import Kronos
    return Kronos(serverIface)
