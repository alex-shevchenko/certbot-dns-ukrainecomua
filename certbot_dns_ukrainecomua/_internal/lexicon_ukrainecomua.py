"""Module provider for Ukraine.com.ua"""
from __future__ import absolute_import
import json
import logging
import time

import requests
from lexicon.providers.base import Provider as BaseProvider

LOGGER = logging.getLogger(__name__)


class Provider(BaseProvider):
    """Provider class for Ukraine.com.ua"""
    def __init__(self, config):
        super(Provider, self).__init__(config)
        self.domain_id = None
        self.api_endpoint = self._get_provider_option(
            'api_endpoint') or 'https://adm.tools/action'

    def _authenticate(self):
        dompayload = self._post(
                '/dns/list/')

        if dompayload and dompayload['list'][self.domain]['domain_id']:
            self.domain_id = dompayload['list'][self.domain]['domain_id']


        if not self.domain_id:
            raise Exception('No domain found like {}'.format(self.domain))

    # Create record. If record already exists with the same content, do nothing

    def _create_record(self, rtype, name, content):
        # check if record already exists
        existing_records = self._list_records(rtype, name, content)
        if len(existing_records) == 1:
            return True

        record = {
            'domain_id': self.domain_id,
            'type': rtype,
            'record': self._relative_name(name),
            'data': content
        }
        if self._get_lexicon_option('priority'):
            record['priority'] = self._get_lexicon_option('priority')

        payload = self._post(
            '/dns/record_add', record)

        LOGGER.debug('create_record')

    # List all records. Return an empty list if no records found
    # type, name and content are used to filter records.
    # If possible filter during the query, otherwise filter after response is received.
    def _list_records(self, rtype=None, name=None, content=None):
        payload = self._post(
            '/dns/records_list/', { 'domain_id': self.domain_id }
        )

        LOGGER.debug('list_records: %s', payload['list'])
        LOGGER.debug('list_records: %s', rtype)
        LOGGER.debug('list_records: %s', name)
        LOGGER.debug('list_records: %s', content)

        records = []
        for record in payload['list']:
            if record['type'] == rtype and record['record'] == self._relative_name(name) and record['data'] == content:
                records.append(record)

        LOGGER.debug('list_records: %s', records)
        return records

    def _update_record(self, identifier, rtype=None, name=None, content=None):
        if identifier:
            try:
                self._delete_record(identifier)
            except NonExistError:
                pass

        return self._create_record(rtype=rtype, name=name, content=content)

    # Delete an existing record.
    # If record does not exist, do nothing.
    def _delete_record(self, identifier=None, rtype=None, name=None, content=None):
        delete_record_id = []
        if not identifier:
            records = self._list_records(rtype, name, content)
            delete_record_id = [record['id'] for record in records]
        else:
            delete_record_id.append(identifier)

        for record_id in delete_record_id:
            records = {
                'subdomain_id': record_id
            }
            LOGGER.debug('delete_record: %s', records)
            self._post('/dns/record_delete/', records)

        # is always True at this point; if a non 2xx response is returned, an error is raised.
        LOGGER.debug('delete_record: True')
        return True

    # Helpers

    def _request(self, action='GET', url='/', data=None, query_params=None):
        time.sleep(1) #not more than 2 requests per second allowed
        if data is None:
            data = {}
        if query_params is None:
            query_params = {}
        default_headers = {
            'User-Agent': 'certbot'
        }
        default_auth = None

        if self._get_provider_option('auth_token'):
            default_headers['Authorization'] = "Bearer {0}".format(
                self._get_provider_option('auth_token'))

        else:
            raise Exception('No valid authentication mechanism found')

        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

        response = requests.request(action, self.api_endpoint + url, params=query_params,
                                    data=data,
                                    headers=default_headers,
                                    auth=default_auth)
        # if the request fails for any reason, throw an error.
        response.raise_for_status()
        if response.text and not response.json()['result']:
            raise Exception('Response unsuccessful')

        return response.json()['response'] if response.text else None

    def _patch(self, url='/', data=None, query_params=None):
        return self._request('PATCH', url, data=data, query_params=query_params)
