
from cryptography import decrypt, encrypt
from pymlconf import errors
from yaml import load, dump, SafeDumper
try:
    from yaml import CLoader as Loader  #, CSafeDumper as Dumper
except ImportError:
    from yaml import Loader

def _normalize(content):
    return content.replace('\t', ' ')

def load_yaml(filepath, encryption_key=None):
    stream = open(filepath)
    try:
        line = stream.readline()
        if line and line.startswith('pymlconf-'):
            if not encryption_key:
                raise errors.ConfigFileEncryptedError(filepath)
            data = decrypt(encryption_key, stream.read())
        else:
            stream.seek(0)
            data = stream.read()
        return load(_normalize(data), Loader)
    finally:
        stream.close()

def load_string(str_data, encryption_key=None):
    if str_data.startswith('pymlconf-'):
        if not encryption_key:
            raise errors.ConfigFileEncryptedError('')
        str_data = decrypt(encryption_key, str_data)

    return load(_normalize(str_data), Loader)

def save_yaml(filepath, content, encryption_key=None):
    with open(filepath, 'w') as f:
        yaml_data = dump(content, SafeDumper)
        if encryption_key:
            import pymlconf
            f.write('pymlconf-%s\n' % pymlconf.__version__)
            yaml_data = encrypt(encryption_key, yaml_data)
        f.write(yaml_data)
