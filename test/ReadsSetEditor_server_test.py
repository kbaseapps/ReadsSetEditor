# -*- coding: utf-8 -*-
import unittest
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from ReadsSetEditor.ReadsSetEditorImpl import ReadsSetEditor
from ReadsSetEditor.ReadsSetEditorServer import MethodContext


class ReadsSetEditorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'ReadsSetEditor',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('ReadsSetEditor'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = ReadsSetEditor(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_ReadsSetEditor_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'.
    def test_save_read_set_ok(self):
        savereadssetparams = {}
        savereadssetparams['workspace_name'] = 'marcin:1475008857456'
        savereadssetparams['output_readset_name'] = "testReadsSet"
        savereadssetparams['input_reads_list'] = ['test_SRR400615_1000', 'test_SRR400616_1000']
        savereadssetparams['desc'] = "first read set"
        
        #setAPI_Client = SetAPI (url=self.serviceWizardURL, token=ctx['token']) 
        #results = setAPI_Client.save_read_set(self.getContext(),savereadssetparams)
        result = self.getImpl().save_read_set(self.getContext(),savereadssetparams)
        print('RESULT:')
        pprint(result)
