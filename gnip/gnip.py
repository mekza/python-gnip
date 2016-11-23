import requests
import json
from .helpers import raise_errors_on_failure


class Gnip(object):
    stream_host = "gnip-stream.twitter.com"
    api_host = "gnip-api.twitter.com"
    use_ssl = True
    USER_AGENT = 'python-gnip'
    token = None
    login = None
    password = None

    def __init__(self, account_name, service="powertrack", **kwargs):
        if "token" in kwargs:
            self.token = kwargs.pop("token")

        elif "password" in kwargs and "login" in kwargs:
            self.login = kwargs.pop('login')
            self.password = kwargs.pop('password')
        else:
            raise Exception("Provide either a token or login/password")

        self.service = service
        self.account_name = account_name
        self.source = kwargs.pop("source")
        self.use_ssl = kwargs.pop('use_ssl', self.use_ssl)
        self.scheme = self.use_ssl and 'https://' or 'http://'
        self.stream_url = "{0}{1}/stream/{2}/accounts/{3}/publishers/{4}/prod.json".format(self.scheme,
                                                                                           self.stream_host,
                                                                                           self.service,
                                                                                           self.account_name,
                                                                                           self.source)
        self.api_url = "{0}{1}/".format(self.scheme, self.api_host)

    def make_request(self, endpoint, method, payload=None, params=None):
        if params is None:
            params = {}
        if payload:
            payload = json.dumps(payload)

        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if self.token:
            headers["Authorization"] = "Basic {t}".format(t=self.token)
            auth = None

        if self.login and self.password:
            auth = (self.login, self.password)

        if method is 'GET':
            r = requests.get(self.api_url + endpoint,
                             params=params,
                             headers=headers,
                             auth=auth)
            r = raise_errors_on_failure(r)

        if method is "POST":
            r = requests.post(self.api_url + endpoint,
                              params=params,
                              headers=headers,
                              auth=auth,
                              data=payload)
            r = raise_errors_on_failure(r)
        if method is "DELETE":
            r = requests.delete(self.api_url + endpoint,
                                params=params,
                                headers=headers,
                                auth=auth,
                                data=payload)
            r = raise_errors_on_failure(r)

        return r.json()

    def get_metrics(self):
        endpoint = "metrics/usage/accounts/{0}.json".format(self.account_name)
        return self.make_request(endpoint, "GET")

    def get_rules(self):
        endpoint = "rules/{0}/accounts/{1}/publishers/{2}/prod.json".format(self.service,
                                                                            self.account_name,
                                                                            self.source)
        return self.make_request(endpoint, "GET")

    def add_rules(self, rules):
        if not isinstance(rules, list):
            raise AttributeError("Rules have to be in a list")

        endpoint = "rules/{0}/accounts/{1}/publishers/{2}/prod.json".format(self.service,
                                                                            self.account_name,
                                                                            self.source)
        payload = {
            "rules": rules
        }

        return self.make_request(endpoint, "POST", payload=payload)

    def delete_rules(self, rules):
        if not isinstance(rules, list):
            raise AttributeError("Rules have to be in a list")

        endpoint = "rules/{0}/accounts/{1}/publishers/{2}/prod.json".format(self.service,
                                                                            self.account_name,
                                                                            self.source)
        payload = {
            "rules": rules
        }
        params = {
            "_method": "delete"
        }
        return self.make_request(endpoint,
                                 "POST",
                                 params=params,
                                 payload=payload)

    def connect_stream(self):
        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if self.token:
            headers["Authorization"] = "Basic {t}".format(t=self.token)
            auth = None
        elif self.login and self.password:
            auth = (self.login, self.password)

        # TODO: Refactor stream handling
        stream = requests.get(self.stream_url,
                              stream=True,
                              auth=auth,
                              headers=headers)
        return stream
