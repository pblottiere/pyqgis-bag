# -*- coding: utf-8 -*-

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"
__license__ = "GPLv3"

from .timefilter import TimeFilter


class WMST(object):

    def __init__(self, serverIface):
        serverIface.registerFilter( TimeFilter(serverIface), 100 )
