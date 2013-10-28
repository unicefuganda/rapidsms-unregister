from rapidsms.apps.base import AppBase
from .models import Blacklist
from django.conf import settings
import re
from rapidsms_httprouter.models import Message
from django.utils.translation import ugettext as _


class App(AppBase):
    def handle(self, message):
        msg_txt = ' '.join(re.findall(r'\w+', message.text.lower(), re.UNICODE))

        msg_txt = msg_txt.encode('utf-8')
        if msg_txt in getattr(settings, 'OPT_IN_WORDS', []) and Blacklist.objects.filter(
                connection=message.connection).count():
            for b in Blacklist.objects.filter(connection=message.connection):
                b.delete()
            Message.objects.create(text=_(getattr(settings, 'OPT_IN_CONFIRMATION', '')), direction='O',
                                   connection=message.connection, status='Q')
            return True
        elif Blacklist.objects.filter(connection=message.connection).count():
            return True
        elif msg_txt in getattr(settings, 'OPT_OUT_WORDS', []):
            Blacklist.objects.create(connection=message.connection)
            Message.objects.create(text=_(getattr(settings, 'OPT_OUT_CONFIRMATION', '')), direction='O',
                                   connection=message.connection, status='Q')
            return True
        return False

    def outgoing(self, msg):
        if Blacklist.objects.filter(connection=msg.connection).count():
            return False
        return True