#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'

from SystemOpera import SystemOpera


def check_start_system(func):
    """
    装饰器
    验证系统是否启动
    启动则执行程序，未启动则报错
    """

    def wrapper(*args, **keargs):
        if SystemOpera.is_using:
            func(*args, **keargs)
        else:
            print('错误:还未开启系统，无法执行操作')

    return wrapper


def check_has_login(func):
    """
    装饰器
    验证系统是否已登录
    已登录则执行程序，未登录则报错
    """

    def wrapper(*args, **keargs):
        if UserOpera.user:
            # print(args[0].__class__.__name__)
            # func(args[0].__class__.__name__)
            # print('war', *args)
            func(*args, **keargs)

        else:
            print('错误:尚未登录，无法执行操作')

    return wrapper


class UserOpera:
    """
    login       用户登陆
    logout      用户登出
    passwd      修改用户口令
    """
    user = None  # 用户信息
    next_user_block = None  # 用户UFD块终结处
    user_MFD_add = None  # 用户所在MFD的index

    @classmethod
    def refulh_next_user_block(cls):
        """
        刷新用户的UFD块、其他用户MFD信息、保存文件
        :return:
        """
        username = cls.user[0]
        # print(username)
        is_found = False
        for i in range(len(SystemOpera.MFD)):
            if is_found:
                UserOpera.next_user_block = int(SystemOpera.MFD[i][2])
                break
            # 在用户信息列表中找到包含用户名的用户信息组
            if username == SystemOpera.MFD[i][0]:
                is_found = True
                if i == len(SystemOpera.MFD) - 1:
                    UserOpera.next_user_block = len(SystemOpera.UFD)
                    break
        SystemOpera.UOF.clear()
        for i in SystemOpera.UFD:
            temp_UOF = i.copy()
            temp_UOF.append('0')
            write_state = '0'
            read_state = '0'
            if i[1] in '02':
                read_state = '1'
            if i[1] in '12':
                write_state = '1'
            temp_UOF.append(read_state)
            temp_UOF.append(write_state)
            SystemOpera.UOF.append(temp_UOF)
        SystemOpera.write_system()
        # print(SystemOpera.UOF)

    @classmethod
    @check_start_system
    def login(cls):
        """
        登录
        """
        username = input('请输入用户名:')
        is_found = False
        for i in range(len(SystemOpera.MFD)):
            if is_found:
                UserOpera.next_user_block = int(SystemOpera.MFD[i][2])
                break
            # 在用户信息列表中找到包含用户名的用户信息组
            if username == SystemOpera.MFD[i][0]:
                userInfo = SystemOpera.MFD[i]
                cls.user_MFD_add = i
                is_found = True
                if i == len(SystemOpera.MFD) - 1:
                    UserOpera.next_user_block = len(SystemOpera.UFD)
                    break
        else:
            print('错误:用户名不存在!')
            return False
        for _ in range(3):
            # 有三次输入密码的机会
            password = input('请输入正确的密码:')
            if password == userInfo[1]:
                UserOpera.user = userInfo
                print('登录成功,欢迎您,{}'.format(UserOpera.user[0]))
                return True
        else:
            print('错误:密码错误!')
            return False

    @classmethod
    @check_has_login
    def logout(cls):
        """
        登出
        """
        print('登出成功,再见,{}'.format(UserOpera.user[0]))
        UserOpera.user = None
        UserOpera.next_user_block = 0
        return True

    @classmethod
    @check_has_login
    def passwd(cls):
        """
        注册用户
        """
        new_password = input('正在为 {} 修改密码\n请输入新密码:'.format(UserOpera.user[0]))
        if ' ' in new_password:
            print('错误:密码中不能包含空格,请重新尝试')
            return False
        if len(new_password) < 6:
            print('错误:密码长度不得低于6位!')
            return False
        if new_password == input('请再次输入密码:'):
            UserOpera.user[1] = new_password
            SystemOpera.write_system()
            print('密码修改成功!')
            return True
        else:
            print('错误:两次密码不匹配!')
            return False

    @classmethod
    @check_start_system
    def registered(cls):
        username = input('请输入新的用户名:')
        if len(username) < 1 and len(username.rsplit()) == 0:
            print('用户名不合法!')
            return False

        for i in SystemOpera.MFD:
            # 在用户信息列表中找到包含用户名的用户信息组
            if username == i[0]:
                print('错误:用户名已存在!')
                return False
        first_password = input('请输入密码:')
        second_password = input('请再次输入密码:')
        if first_password == second_password and len(first_password) > 5 and len(first_password.rsplit()) > 0:
            SystemOpera.MFD.append([username, first_password, str(len(SystemOpera.UFD))])
            print('用户创建成功，请牢记账号密码!')
            return True
        elif first_password != second_password:
            print('两次密码不一致!')
            return False
        else:
            print('密码不合法，请重新尝试!')
            return False
