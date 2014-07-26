
import os
import unittest
from pymlconf import ConfigDict, ConfigManager
from pymlconf.config_manager import ERROR, IGNORE
from pymlconf.errors import ConfigFileNotFoundError, ConfigFileEncryptedError


this_dir = os.path.abspath(os.path.dirname(__file__))
conf_dir = os.path.join(this_dir, 'conf')

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.builtin_config = {
            'version': 2.5,
            'general': {'name': 'albatross'},
            'domains': ConfigDict({'coldon_ir': ConfigDict(), 'fangtooth_ir': ConfigDict({'name': 'fangtooth'})}),
            'data': {'url': 'some uri'}  # without ConfigDict
        }

    def test_builtins(self):
        cm = ConfigManager(init_value=self.builtin_config)
        cm.version = 2.6
        self.assertEqual(cm.version, 2.6)
        self.assertEqual(cm.general.name, self.builtin_config['general']['name'])
        self.assertIsInstance(cm.domains['coldon_ir'], ConfigDict)
        self.assertEqual(cm.data.url, 'some uri')
 
    def test_files(self):
 
        # noinspection PyUnresolvedReferences
        files = [os.path.join(conf_dir, '../files', 'c111.conf'),
                 os.path.join(conf_dir, '../files', 'something-that-not-exists.conf')]
        cm = ConfigManager(init_value=self.builtin_config, dirs=[conf_dir], files=files)
        
        
 
        # root.conf
        self.assertEqual(cm.version, 2.5)
        self.assertEqual(cm.domains.coldon_ir.name, 'coldon')
        self.assertEqual(cm.general.tcp_port, 5671)
 
        # general.conf
        self.assertEqual(cm.general.name, 'Vahid')
        self.assertEqual(cm.domains['fangtooth_ir'].name, 'Fangtooth2')
 
        # domains_coldon.ir.conf
        self.assertEqual(cm.domains['coldon_ir'].path, '/home/local/coldon')
 
        # domains_dobisel.com.conf
        self.assertEqual(cm.domains['dobisel_com'].path, '/home/local/dobisel')
        self.assertEqual(cm.domains['dobisel_com'].name, 'dobisel')
        self.assertEqual(cm.domains['dobisel_com'].applications.app1.name, 'app1')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.fullname, 'Vahid Mardani')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.password, 'himopolxx')
        self.assertEqual(cm.baghali, 2)
        # builtins
        self.assertEqual(cm.data.url, 'some uri')
 
    def test_non_existence_file(self):
        # noinspection PyUnresolvedReferences
        files = [os.path.join(conf_dir, '../files', 'c111.conf'),
                 os.path.join(conf_dir, '../files', 'something-that-not-exists.conf')]
        
        import logging
        import sys
        from pymlconf.compat import StringIO
        logger = logging.getLogger('pymlconf')
        logger.level = logging.DEBUG
        saved_stdout = sys.stdout

        sys.stdout = StringIO()        
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        try:
            # Testing ignore behavior
            ConfigManager(init_value=self.builtin_config, dirs=[conf_dir], files=files,
                          missing_file_behavior=IGNORE)
            output = sys.stdout.getvalue().strip()
            self.assertNotRegexpMatches(output, "^File not found: ['\"]?(?:/[^/]+)*['\"]?$")

            # Testing default behavior which just prints a warning
            ConfigManager(init_value=self.builtin_config, dirs=[conf_dir], files=files)
            output = sys.stdout.getvalue().strip()
            self.assertRegexpMatches(output, "^File not found: ['\"]?(?:/[^/]+)*['\"]?$")

            # Testing strict behavior
            self.assertRaises(ConfigFileNotFoundError, ConfigManager,
                              init_value=self.builtin_config,
                              dirs=[conf_dir],
                              files=files,
                              missing_file_behavior=ERROR)

        finally:
            logger.removeHandler(stream_handler)
            sys.stdout = saved_stdout

    def test_dirs(self):
        dirs = [conf_dir]
        cm = ConfigManager(init_value=self.builtin_config, dirs=dirs)
 
        # root.conf
        self.assertEqual(cm.version, 2.5)
        self.assertEqual(cm.domains['coldon_ir'].name, 'coldon')
        self.assertEqual(cm.general.tcp_port, 5671)
 
        # general.conf
        self.assertEqual(cm.general.name, 'Vahid')
        self.assertEqual(cm.domains['fangtooth_ir'].name, 'Fangtooth2')
 
        # domains_coldon.ir.conf
        self.assertEqual(cm.domains['coldon_ir'].path, '/home/local/coldon')
 
        # domains_dobisel.com.conf
        self.assertEqual(cm.domains['dobisel_com'].path, '/home/local/dobisel')
        self.assertEqual(cm.domains['dobisel_com'].name, 'dobisel')
        self.assertEqual(cm.domains['dobisel_com'].applications.app1.name, 'app1')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.fullname, 'Vahid Mardani')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.password, 'himopolxx')
 
        # builtins
        self.assertEqual(cm.data.url, 'some uri')


    def test_new_extension(self):
        dirs = [conf_dir]
        cm = ConfigManager(init_value=self.builtin_config, dirs=dirs,extension=".yaml")
 
        # root.conf
        self.assertEqual(cm.run.baseurl, 'http://localhost:9090')
        self.assertEqual(cm.run.skipurlcheck, True)
        self.assertEqual(cm.type, 'selenium')
        self.assertEqual(cm.testpath, './')
         
        #self.assertEqual(cm.selenium.xvfb.options.server-args, '-screen 0 1024x768x24')


    def test_cryptography(self):
        dirs = [conf_dir]
        cm = ConfigManager(init_value=self.builtin_config, dirs=dirs,extension=".yaml",encryption_key='baghali')

        self.assertEqual(cm.run.baseurl, 'http://localhost:9090')
        self.assertEqual(cm.run.skipurlcheck, True)
        self.assertEqual(cm.type, 'selenium')
        self.assertEqual(cm.testpath, './')

        out_filename = os.path.join(this_dir, 'files', 'encrypted_file.pconf')
        out_filename_plain = os.path.join(this_dir, 'files', 'plain_file.yaml')
        cm.save(out_filename)
        cm.save(out_filename_plain, plain=True)

        self.assertRaises(ConfigFileEncryptedError, ConfigManager, files=out_filename)
        cm = ConfigManager(files=out_filename_plain)
        self.assertEqual(cm.run.baseurl, 'http://localhost:9090')
        self.assertEqual(cm.run.skipurlcheck, True)
        self.assertEqual(cm.type, 'selenium')
        self.assertEqual(cm.testpath, './')



if __name__ == '__main__':
    unittest.main()