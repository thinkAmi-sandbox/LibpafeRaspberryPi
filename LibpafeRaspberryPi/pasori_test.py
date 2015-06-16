# -*- coding: utf-8 -*-

# print時の改行を制御したいので、Python3.xのprint関数を使う
from __future__ import print_function
from ctypes import *


# PASORI_TYPE
# libpafe.hの17行目にenumとして定義
PASORI_TYPE_S310 = 0
PASORI_TYPE_S320 = 1
PASORI_TYPE_S330 = 2

TEST_DATA = "test data."


def test(libpafe, pasori):
    data = c_char_p(TEST_DATA)
    data_length = c_int(len(TEST_DATA) - 1)

    print("Echo test...", end="")
    # Pythonの場合、数字の0はfalseとして扱われるので、
    # 関数が成功した場合はfalseが返ってくることになる
    if (libpafe.pasori_test_echo(pasori, data, byref(data_length))):
        print("error!")
    else:
        print("success")


    print("EPROM test... ", end="");
    if (libpafe.pasori_test_eprom(pasori)):
        print("error!")
    else:
        print("success")


    print("RAM test... ", end="");
    if (libpafe.pasori_test_ram(pasori)):
        print("error!")
    else:
        print("success")


    print("CPU test... ", end="")
    if (libpafe.pasori_test_cpu(pasori)):
        print("error!")
    else:
        print("success")


    print("Polling test... ", end="");
    if (libpafe.pasori_test_polling(pasori)):
        print("error!")
    else:
        print("success")


def show_version(libpafe, pasori):

    v1 = c_int()
    v2 = c_int()
    if (libpafe.pasori_version(pasori, byref(v1), byref(v2)) != 0):
        print("cannot get version")
        return

    # RC-S320以外は所持していないので、未テスト
    pasori_type = libpafe.pasori_type(pasori)
    if pasori_type == PASORI_TYPE_S320:
        print("PaSoRi (RC-S320)\n firmware version %d.%02d" % (v1.value, v2.value))
    elif pasori_type == PASORI_TYPE_S310:
        print("PaSoRi (RC-S310)\n firmware version %d.%02d" % (v1.value, v2.value))
    elif pasori_type == PASORI_TYPE_S330:
        print("PaSoRi (RC-S330)\n firmware version %d.%02d" % (v1.value, v2.value))
    else:
        print("unknown hardware.")
        

if __name__ == '__main__':

    libpafe = cdll.LoadLibrary("/usr/local/lib/libpafe.so")

    libpafe.pasori_open.restype = c_void_p
    pasori = libpafe.pasori_open()
    
    libpafe.pasori_init(pasori)
    show_version(libpafe, pasori)

    type = libpafe.pasori_type(pasori)

    if (type in {PASORI_TYPE_S310, PASORI_TYPE_S320}):
        test(libpafe, pasori)

    libpafe.pasori_close(pasori)