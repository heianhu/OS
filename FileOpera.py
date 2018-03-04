#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'

from UserOpera import UserOpera, check_has_login
from SystemOpera import SystemOpera


class FileOpera:
    """
    dir         列出该用户下所有文件
    chmod   [filename][mode]            改变文件权限
    chown   [filename][new_owner]       改变文件拥有者
    mv      [srcFile][desFile]          改变文件名
    type    [filename]                  显示文件内容
    copy    [srcFile][desFile]          文件拷贝
    create  [filename][mode]            建立文件
    delete  [filename]                  删除文件
    write   [filename][buffer][nbytes]  写文件
    """

    @classmethod
    def __name__(cls):
        return 'FileOpera'

    @check_has_login
    def dir(self):
        """
        列出该用户下所有文件
        :return:
        """
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            print(SystemOpera.UFD[i][0])

    @check_has_login
    def chmod(self, filename, mode):
        """
        更改文件权限
        :param filename: 文件名
        :param mode: 文件权限
        :return: 是否修改成功
        """
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == filename:
                SystemOpera.UFD[i][1] = str(mode)
                print('{}权限修改成功!'.format(filename))
                UserOpera.refulh_next_user_block()
                return True
        else:
            print('错误:{}不存在或者该文件不属于{}'.format(filename, UserOpera.user[0]))
            return False

    @check_has_login
    def chown(self, filename, new_owner):
        """
        更改文件所有权
        将UFD区移动，更改MFD区的文件指针
        :param filename: 文件名
        :param new_owner: 新的文件归属用户
        :return: 是否更改成功
        """
        if new_owner == UserOpera.user[0]:
            print('不能将文件所有者设为自己!')
            return False
        up_or_down = True  # False为新拥有者在旧拥有者下方，True为上方
        for i in range(len(SystemOpera.MFD)):
            if UserOpera.user[0] == SystemOpera.MFD[i][0]:
                up_or_down = False
            # 找到new_owner
            # 在用户信息列表中找到包含用户名的用户信息组
            if new_owner == SystemOpera.MFD[i][0]:
                new_owner_add = int(SystemOpera.MFD[i][2])
                new_owner_MFD_add = i
                break
        else:
            print('错误:用户{}不存在!'.format(new_owner))
            return False

        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == filename:
                temp = SystemOpera.UFD[i]
                del SystemOpera.UFD[i]
                if up_or_down:
                    # 新拥有者在旧拥有者上方
                    SystemOpera.UFD.insert(new_owner_add, temp)  # 在新拥有者中插入数据
                    for _ in range(new_owner_MFD_add + 1, UserOpera.user_MFD_add + 1):
                        SystemOpera.MFD[_][2] = str(int(SystemOpera.MFD[_][2]) + 1)
                else:
                    # 新拥有者在旧拥有者下方
                    SystemOpera.UFD.insert(new_owner_add - 1, temp)
                    for _ in range(UserOpera.user_MFD_add + 1, new_owner_MFD_add + 1):
                        SystemOpera.MFD[_][2] = str(int(SystemOpera.MFD[_][2]) - 1)
                print('{}拥有者已变为{}!'.format(filename, new_owner))
                UserOpera.refulh_next_user_block()
                return True
        else:
            print('错误:文件{}不存在或者不属于{}!'.format(filename, UserOpera.user[0]))
            return False

    @check_has_login
    def mv(self, srcFile, desFile):
        """
        改变文件名
        :param srcFile: 旧名称
        :param desFile: 新名称
        :return: 是否更改成功
        """
        # print(srcFile,desFile)
        if not desFile.rsplit() or (len(desFile.rsplit()) > 1):
            print('错误:新文件名不符合标准!')
            return False
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == srcFile:
                SystemOpera.UFD[i][0] = desFile
                print('{} 更名为 {}!'.format(srcFile, desFile))
                UserOpera.refulh_next_user_block()
                return True
        else:
            print('错误:{} 不存在或者该文件不属于 {}'.format(srcFile, UserOpera.user[0]))
            return False

    @check_has_login
    def type(self, filename):
        """
        显示文件内容
        :param filename: 文件名
        :return: 是否成功显示
        """
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == filename:
                if SystemOpera.UFD[i][1] in '02':
                    print(SystemOpera.file_block[int(SystemOpera.UFD[i][-1])])
                    return True
                else:
                    print('错误:{} 没有读取权限'.format(filename))
                    return False
        else:
            print('错误:{} 不存在或者该文件不属于 {}'.format(filename, UserOpera.user[0]))
            return False

    @check_has_login
    def copy(self, srcFile, desFile):
        """
        文件拷贝
        :param srcFile: 原文件名
        :param desFile: 新文件名
        :return: 是否拷贝成功
        """
        if desFile == srcFile:
            print('错误:两个文件名称不能相同!')
            return False
        if not desFile.rsplit() or (len(desFile.rsplit()) > 1):
            print('错误:新文件名不符合标准!')
            return False
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == srcFile:
                temp_UFD = SystemOpera.UFD[i].copy()  # 复制一份原版文件指针
                temp_UFD[0], temp_UFD[-1] = desFile, str(len(SystemOpera.file_block))  # 修图文件名和文件指向的地址
                # print(SystemOpera.UFD[i])
                temp_file_block = SystemOpera.file_block[int(SystemOpera.UFD[i][-1])]  # 复制一份原版文件内容
                SystemOpera.UFD.insert(int(UserOpera.user[2]), temp_UFD)  # 插入一个文件指针UFD
                for j in range(UserOpera.user_MFD_add + 1, len(SystemOpera.MFD)):
                    # 调整后面用户的目录地址
                    SystemOpera.MFD[j][2] = str(int(SystemOpera.MFD[j][2]) + 1)
                SystemOpera.file_block.append(temp_file_block)
                # print(SystemOpera.file_block[int(SystemOpera.UFD[i][-1])])
                UserOpera.refulh_next_user_block()
                print('拷贝成功!')
                # print(UserOpera.next_user_block)
                return True
        else:
            print('错误:{} 不存在或者该文件不属于 {}'.format(srcFile, UserOpera.user[0]))
            return False

    @check_has_login
    def create(self, filename, mode):
        """
        建立文件
        :param filename: 文件名
        :param mode: 权限
        :return: 是否创建成功
        """
        if not filename.rsplit() or (len(filename.rsplit()) > 1):
            print('错误:文件名不符合标准!')
            return False
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == filename:
                print('错误:该文件已存在!')
                return False
        new_UFD = [filename, str(mode), '0', str(len(SystemOpera.file_block))]
        SystemOpera.UFD.insert(int(UserOpera.user[2]), new_UFD)
        for j in range(UserOpera.user_MFD_add + 1, len(SystemOpera.MFD)):
            # 调整后面用户的目录地址
            SystemOpera.MFD[j][2] = str(int(SystemOpera.MFD[j][2]) + 1)
        SystemOpera.file_block.append('\n\\n')
        print('{} 创建成功'.format(filename))
        UserOpera.refulh_next_user_block()
        return True

    @check_has_login
    def delete(self, filename):
        """
        删除文件
        :param filename: 文件名
        :return: 是否删除成功
        """
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == filename:
                for j in range(len(SystemOpera.UFD)):
                    # 在该用户后面的用户UFD的文件指针-1
                    if int(SystemOpera.UFD[j][-1]) > int(SystemOpera.UFD[i][-1]):
                        SystemOpera.UFD[j][-1] = str(int(SystemOpera.UFD[j][-1]) - 1)
                file_block_num = int(SystemOpera.UFD[i][-1])
                del SystemOpera.UFD[i]  # 删除所属UFD
                for j in range(UserOpera.user_MFD_add + 1, len(SystemOpera.MFD)):
                    # 调整后面用户的目录地址
                    SystemOpera.MFD[j][2] = str(int(SystemOpera.MFD[j][2]) - 1)
                del SystemOpera.file_block[file_block_num]  # 删除所属file_block
                print('{} 删除成功!'.format(filename))
                UserOpera.refulh_next_user_block()
                return True
        else:
            print('错误:{} 不存在或者该文件不属于 {}'.format(filename, UserOpera.user[0]))
            return False

    @check_has_login
    def write(self, filename, buffer, nbytes):
        """
        写文件
        :param filename: 文件名
        :param buffer: 内容
        :param nbytes: 长度
        :return: 是否写入成功
        """
        for i in range(int(UserOpera.user[2]), UserOpera.next_user_block):
            if SystemOpera.UFD[i][0] == filename:
                if SystemOpera.UFD[i][1] in '12':
                    SystemOpera.file_block[int(SystemOpera.UFD[i][-1])] = str(buffer)
                    SystemOpera.UFD[i][2] = str(nbytes)
                    print('{} 写入成功!'.format(filename))
                    UserOpera.refulh_next_user_block()
                    return True
                else:
                    print('错误:{} 没有写入权限'.format(filename))
                    return False
        else:
            print('错误:{} 不存在或者该文件不属于 {}'.format(filename, UserOpera.user[0]))
            return False
