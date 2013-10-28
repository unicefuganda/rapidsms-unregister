# coding=utf-8
import unittest
from django.test import TestCase
from unregister.models import Blacklist
from rapidsms.models import Backend, Connection

from rapidsms.tests.scripted import TestScript
from rapidsms_httprouter.router import get_router
from django.conf import settings
from unregister.app import App as UnregisterApp


class TestUnregisterApp(TestScript):
    apps = (UnregisterApp,)

    testJoin = """
        256712123456 > quit
        256712123456 < You have just quit.
    """


class TestUnRegister(TestCase):
    def setUp(self):
        self.opt_out_word_backup = settings.OPT_OUT_WORDS

    def tearDown(self):
        settings.OPT_OUT_WORDS = self.opt_out_word_backup

    def fake_incoming_message(self, message, connection):
        self.router = get_router()
        self.router.handle_incoming(connection.backend.name, connection.identity, message)

    def test_sending_opt_out_word_adds_connection_to_blacklist(self):
        backend = Backend.objects.create(name='test')
        connection = Connection.objects.create(identity='0783010831', backend=backend)
        settings.OPT_OUT_WORDS = ["quit"]

        self.fake_incoming_message('quit', connection)

        self.assertTrue(Blacklist.objects.filter(connection=connection).exists())

    def test_sending_opt_out_word_in_a_character_set_different_from_english_adds_connection_to_blacklist(self):
        backend = Backend.objects.create(name='test')
        connection = Connection.objects.create(identity='0783010831', backend=backend)
        settings.OPT_OUT_WORDS = ["استقال"]

        self.fake_incoming_message(u'استقال', connection)

        self.assertTrue(Blacklist.objects.filter(connection=connection).exists(), "Connection is not blacklisted")


if __name__ == "__main__":
    unittest.main()
