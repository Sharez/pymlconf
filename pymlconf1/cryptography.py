# -*- coding: utf-8 -*-
import simplecrypt
from pymlconf1.compat import Dumper, Loader
__author__ = 'vahid'


def encrypt(key, inp):
    return simplecrypt.encrypt(key, inp)


def decrypt(key, inp):
    return simplecrypt.decrypt(key, inp)


class CryptoDumper(Dumper):
  pass


class CryptoLoader(Loader):
  pass


class CryptoBaseFactory(object):
  def __init__(self, encryption_key):
    self._encryption_key = encryption_key


class CryptoDumperFactory(CryptoBaseFactory):
  def __init__(self, encryption_key, dumper_class=CryptoDumper):
    self.dumper_class = dumper_class
    super(CryptoDumperFactory, self).__init__(encryption_key)


class CryptoLoaderFactory(CryptoBaseFactory):
  def __init__(self, encryption_key, loader_class=CryptoLoader):
    self.loader_class = loader_class
    super(CryptoLoaderFactory, self).__init__(encryption_key)
