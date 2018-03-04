#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
from SystemOpera import SystemOpera
from UserOpera import UserOpera
from FileOpera import FileOpera


class Opera:

    @classmethod
    def help(cls, *args):
        if UserOpera.user:
            print("""
help                                显示本系统命令
shutdown                            关闭该系统
login                               更换用户
logout                              用户登出
passwd                              修改用户口令
dir                                 列出该用户下所有文件
chmod   [filename][mode]            改变文件权限
chown   [filename][new_owner]       改变文件拥有者
mv      [srcFile][desFile]          改变文件名
type    [filename]                  显示文件内容、读文件
copy    [srcFile][desFile]          文件拷贝
create  [filename][mode]            创建新文件
delete  [filename]                  删除文件
write   [filename][buffer][nbytes]  写文件 
                """)
        else:
            print("""
help                                显示本系统命令
shutdown                            关闭该系统
login                               用户登陆
registered                          用户注册
                            """)
        return True

    @classmethod
    def login(cls, *args):
        return UserOpera.login()

    @classmethod
    def registered(cls, *args):
        return UserOpera.registered()

    @classmethod
    def passwd(cls, *args):
        return UserOpera.passwd()

    @classmethod
    def logout(cls, *args):
        return UserOpera.logout()

    @classmethod
    def dir(cls, *args):
        fileopera = FileOpera()
        return fileopera.dir()

    @classmethod
    def chmod(cls, *args):
        if len(*args) != 2:
            print('错误:参数错误,请参考help命令')
            return False
        fileopera = FileOpera()
        return fileopera.chmod(*args[0])

    @classmethod
    def chown(cls, *args):
        if len(*args) != 2:
            print('错误:参数错误,请参考help命令')
        fileopera = FileOpera()
        fileopera.chown(*args[0])

    @classmethod
    def mv(cls, *args):
        if len(*args) != 2:
            print('错误:参数错误,请参考help命令')
            return False
        fileopera = FileOpera()
        return fileopera.mv(*args[0])

    @classmethod
    def type(cls, *args):
        if len(*args) != 1:
            print('错误:参数错误,请参考help命令')
            return False
        fileopera = FileOpera()
        return fileopera.type(*args[0])

    @classmethod
    def copy(cls, *args):
        if len(*args) != 2:
            print('错误:参数错误,请参考help命令')
            return False
        fileopera = FileOpera()
        return fileopera.copy(*args[0])

    @classmethod
    def create(cls, *args):
        if len(*args) != 2:
            print('错误:参数错误,请参考help命令')
            return False
        fileopera = FileOpera()
        return fileopera.create(*args[0])

    @classmethod
    def delete(cls, *args):
        if len(*args) != 1:
            print('错误:参数错误,请参考help命令')
            return False
        fileopera = FileOpera()
        return fileopera.delete(*args[0])

    @classmethod
    def write(cls, *args):
        if len(*args) != 3:
            print('错误:参数错误,请参考help命令')
            return False
        fileopera = FileOpera()
        return fileopera.write(*args[0])

    @classmethod
    def shutdown(cls, *args):
        SystemOpera.shutdown()
