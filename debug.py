# Copyright 2019 Sree Chandan.R . All rights reserved.
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

from typing import List, Any

#import nodeLib
#from . import structure


class Debug_Tools:
    force_on = False  # if true overrides local_debug preference
    forcu_off = False  # main off switch

    @staticmethod
    def debug_msg(msg, local_debug=True):
        """ 
        If DEBUG_GLOBAL or local_debug is true print the msg

        Arguments:
            msg {[type]} -- [description]

        Keyword Arguments:
            local_debug {bool} -- [description] (default: {False})
        """
        """
        The purpose of debug_msg() custom function is to have a easy way to toggle all debug to on and off
        """
        if not Debug_Tools.forcu_off:
            if Debug_Tools.force_on or local_debug:
                print(msg)

    @classmethod
    def set_force_on(cls, bool_):
        cls.force_on = bool_

    @classmethod
    def set_force_off(cls, bool_):
        cls.forcu_off = bool_


class Debug_Tools_obj:
    def __init__(self, **kwargs):

        self.force_on = False  # if true overrides local_debug preference
        self.forcu_off = False  # main off switch

    def debug_msg(msg, local_bool=True):
        """ 
        If DEBUG_GLOBAL or local_debug is true print the msg

        Arguments:
            msg {[type]} -- [description]

        Keyword Arguments:
            local_debug {bool} -- [description] (default: {False})
        """
        """
        The purpose of debug_msg() custom function is to have a easy way to toggle all debug to on and off
        """
        if not self.forcu_off:
            if self.force_on or local_bool:
                print(msg)

    def set_force_on(bool_):
        self.force_on = bool_

    def set_force_off(bool_):
        self.forcu_off = bool_
