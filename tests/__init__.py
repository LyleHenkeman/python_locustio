"""Unit test for bootstrap file."""
import os
from unittest import TestCase

import mock

import requests_mock

from src.start import bootstrap


class TestEnvironmentVariable(TestCase):
    """Unit test class to test method bootstrap."""

    @mock.patch('subprocess.Popen')
    def test_valid_master(self, mocked_popen):
        os.environ['ROLE'] = 'master'
        os.environ['TARGET_HOST'] = 'https://test.com'
        os.environ['LOCUST_FILE'] = 'test/test.py'

        self.assertFalse(mocked_popen.called)
        bootstrap()
        self.assertTrue(mocked_popen.called)

    @mock.patch('subprocess.Popen')
    def test_valid_slave(self, mocked_popen):
        os.environ['ROLE'] = 'slave'
        os.environ['TARGET_HOST'] = 'https://test.com'
        os.environ['LOCUST_FILE'] = 'test/test.py'
        os.environ['MASTER_HOST'] = '127.0.0.1'
        os.environ['SLAVE_MUL'] = '3'

        self.assertFalse(mocked_popen.called)
        bootstrap()
        self.assertTrue(mocked_popen.called)

    @mock.patch('time.sleep')
    def test_valid_controller_manual(self, mocked_timeout):
        os.environ['ROLE'] = 'controller'
        os.environ['AUTOMATIC'] = str(False)
        self.assertFalse(mocked_timeout.called)
        bootstrap()
        self.assertFalse(mocked_timeout.called)

    @mock.patch('time.sleep')
    @mock.patch('os.makedirs')
    @mock.patch('__builtin__.open')
    @requests_mock.Mocker()
    def test_valid_controller_automatic(self, mocked_timeout, mocked_dir, mocked_open, mocked_request):
        os.environ['ROLE'] = 'controller'
        os.environ['AUTOMATIC'] = str(True)
        os.environ['MASTER_HOST'] = '127.0.0.1'
        os.environ['SLAVE_MUL'] = '3'
        os.environ['USERS'] = '100'
        os.environ['HATCH_RATE'] = '5'
        os.environ['DURATION'] = '10'

        mocked_request.get(url='http://127.0.0.1:8089', text='ok')
        mocked_request.post(url='http://127.0.0.1:8089/swarm', text='ok')
        mocked_request.get(url='http://127.0.0.1:8089/stop', text='ok')
        mocked_request.get(url='http://127.0.0.1:8089/htmlreport', text='ok')
        self.assertFalse(mocked_timeout.called)
        self.assertFalse(mocked_request.called)
        self.assertFalse(mocked_dir.called)
        self.assertFalse(mocked_open.called)
        bootstrap()
        self.assertTrue(mocked_timeout.called)
        self.assertTrue(mocked_request.called)
        self.assertTrue(mocked_dir.called)
        self.assertTrue(mocked_open.called)

    def test_invalid_role(self):
        os.environ['ROLE'] = 'unknown'
        with self.assertRaises(RuntimeError):
            bootstrap()

    def test_missing_env_variables(self):
        roles = ['master', 'slave']

        for role in roles:
            os.environ['ROLE'] = role
            with self.assertRaises(RuntimeError):
                bootstrap()

    def test_invalid_env_variables(self):
        os.environ['ROLE'] = 'controller'
        os.environ['AUTOMATIC'] = str(True)
        os.environ['MASTER_HOST'] = '127.0.0.1'
        os.environ['USERS'] = 'test'

        bootstrap()
        self.assertRaises(ValueError)
