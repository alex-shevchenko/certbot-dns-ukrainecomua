"""DNS Authenticator for Ukraine.com.ua DNS."""
import logging

from . import lexicon_ukrainecomua as ukrainecomua
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://adm.tools/user/api/'


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Ukraine.com.ua

    This Authenticator uses the Ukraine.com.ua API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are using Ukraine.com.ua for DNS).'
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=180)
        add('credentials', help='Ukraine.com.ua credentials INI file.')

    def more_info(self):  # pylint: disable=missing-function-docstring
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Ukraine.com.ua API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Ukraine.com.ua credentials INI file',
            {
                'token': 'User access token for Ukraine.com.ua API. (See {0}.)'.format(ACCOUNT_URL)
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_ukrainecomua_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_ukrainecomua_client().del_txt_record(domain, validation_name, validation)

    def _get_ukrainecomua_client(self):
        return _UkrainecomuaLexiconClient(self.credentials.conf('token'), self.ttl)


class _UkrainecomuaLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the Ukraine.com.ua via Lexicon.
    """

    def __init__(self, token, ttl):
        super(_UkrainecomuaLexiconClient, self).__init__()

        config = dns_common_lexicon.build_lexicon_config('ukrainecomua', {
            'ttl': ttl,
        }, {
            'auth_token': token,
        })

        self.provider = ukrainecomua.Provider(config)

    def _handle_http_error(self, e, domain_name):
        hint = None
        if str(e).startswith('401 Client Error: Unauthorized for url:'):
            hint = 'Is your API token value correct?'

        return errors.PluginError('Error determining zone identifier for {0}: {1}.{2}'
                                  .format(domain_name, e, ' ({0})'.format(hint) if hint else ''))
