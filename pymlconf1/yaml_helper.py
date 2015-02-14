# -*- coding: utf-8 -*-
from yaml import load, dump
from pymlconf1 import errors
from pymlconf1.compat import Loader, Dumper
from pymlconf1.cryptography import CryptoDumperFactory, CryptoLoaderFactory
__author__ = 'vahid'


def load_yaml_file(filepath, encryption_key=None):
  stream = open(filepath)
  try:
    line = stream.readline()
    if line and line.startswith('pymlconf-'):
      if not encryption_key:
        raise errors.EncryptionKeyMissingError(filepath)
      loader_class = CryptoLoaderFactory(encryption_key)
    else:
      stream.seek(0)
      loader_class = Loader
    return load(stream, Loader=loader_class)
  finally:
    stream.close()


def load_yaml_string(yaml_str, encryption_key=None):
  if yaml_str and yaml_str.startswith('pymlconf-'):
    if not encryption_key:
      raise errors.EncryptionKeyMissingError()
    loader_class = CryptoLoaderFactory(encryption_key)
  else:
    loader_class = Loader
  return load(yaml_str, Loader=loader_class)


def save_yaml(filepath, content, encryption_key=None):
  stream = open(filepath)
  try:
    if encryption_key:
      dumper_class = CryptoDumperFactory(encryption_key)
    else:
      dumper_class = Dumper
    dump(content, stream=stream, Dumper=dumper_class)
  finally:
    stream.close()
