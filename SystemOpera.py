#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'


class SystemOpera:
    """
    startsystem 开启该系统
    shutdown    关闭该系统
    """
    __filename = 'disk.txt'
    MFD = []  # 用户信息
    UFD = []  # 文件信息
    UOF = []
    file_block = []  # 文件内容
    is_using = False  # True时候已经开启系统

    @classmethod
    def startsystem(cls):
        """
        初始化读入文件内容，开启文件系统
        :return:
        """
        try:
            file = open(cls.__filename, 'r')
            cls.MFD = []
            cls.UFD = []
            cls.file_block = []
            for _ in file:
                if _ == '\n':
                    # 遇到换行符表示该模块结束
                    break
                cls.MFD.append(_)
            for _ in file:
                if _ == '\n':
                    break
                cls.UFD.append(_)
            for _ in file:
                if _ == '\n':
                    break
                cls.UOF.append(_)
            for _ in file:
                if _ == '\n':
                    break
                cls.file_block.append(_)

            cls.MFD = [userInfo.rsplit() for userInfo in cls.MFD]  # 将字符串转成列表，并去除最后的\n
            cls.UFD = [userInfo.rsplit() for userInfo in cls.UFD]
            cls.UOF = [userInfo.rsplit() for userInfo in cls.UOF]

            cls.is_using = True  # 成功启动系统
            print('开机成功,欢迎使用该系统\nmade by 马晟\n有问题联系heianhu@live.com')

        except FileNotFoundError:
            print('从磁盘中读入时失败！')
            cls.is_using = False  # 系统被关闭
        finally:
            file.close()

    @classmethod
    def shutdown(cls):
        """
        关闭文件系统
        :return:
        """
        cls.write_system()
        print('Bye~')
        cls.is_using = False  # 系统被关闭

    @classmethod
    def write_system(cls):
        """
        将数据写入磁盘
        :return:
        """
        # with open('disk.txt') as file:
        content = ''
        for _ in cls.MFD:
            content += ' '.join(_) + '\n'
        content += '\n'
        for _ in cls.UFD:
            content += ' '.join(_) + '\n'
        content += '\n'
        for _ in cls.UOF:
            content += ' '.join(_) + '\n'
        content += '\n'
        for _ in cls.file_block:
            content += _
        with open('disk.txt', 'w') as file:
            file.write(content)
