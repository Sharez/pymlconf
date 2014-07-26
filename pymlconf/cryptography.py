# -*- coding: utf-8 -*-
import simplecrypt
__author__ = 'vahid'



def encrypt(key, inp):
    return simplecrypt.encrypt(key, inp)


def decrypt(key, inp):
    return simplecrypt.decrypt(key, inp)