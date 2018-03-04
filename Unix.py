#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'

from SystemOpera import SystemOpera
from UserOpera import UserOpera
from Opera import Opera


class Unix:
    def __init__(self):
        SystemOpera.startsystem()

    def UI(self):
        while SystemOpera.is_using:
            try:
                if UserOpera.user:
                    args = input('{}: '.format(UserOpera.user[0])).rsplit()
                    eval('Opera.{}({})'.format(args[0], args[1:]))
                else:
                    args = input('{}: '.format('guest')).rsplit()
                    eval('Opera.{}({})'.format(args[0], args[1:]))
            except AttributeError:
                print('命令错误,请参考help命令!')


if __name__ == '__main__':
    system = Unix()
    system.UI()
