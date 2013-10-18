from generic.forms import ActionForm
from rapidsms.models import Connection
from unregister.models import Blacklist
from django.utils.translation import ugettext as _
class BlacklistForm(ActionForm):
    """ abstract class for all the filter forms"""
    action_label = 'Blacklist/Opt-out Users'
    def perform(self, request, results):
        if request.user and request.user.has_perm('unregister.add_blacklist'):
            connections = Connection.objects.filter(contact__in=results)
            for c in connections:
                Blacklist.objects.get_or_create(connection=c)
            return (_("'You blacklisted %(connections)d numbers'" % {"connections":len(connections)}), 'success',)
        else:
            return (_("You don't have permissions to blacklist numbers"), 'error',)
