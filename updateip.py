#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# #      Created Date: Tue May 29 2018
# #      Author: Ryan
# #      mail: ryaninf@outlook.com
# #      Last Modified: 
# #      Modified By: 
# #------------------------------------------
# #      Copyright (c) 2018  
# #------------------------------------------
# #
###

from getProxyIP import *


def main():
    getIPFrom66()
    getIPFromKD()
    getIPFromXD()
    print('已更新待测试IP列表，共：', len(unchkiplist))
    saveuncheckip()


if __name__ == '__main__':
    main()
