import requests


class Katello(object):
    """ Katello API calls """
    def __init__(self, hostname='localhost', path='/headpin', username='admin', password='admin', verify=False):
        self.hostname = hostname
        self.path = path
        self.username = username
        self.password = password
        self.verify = verify

    @staticmethod
    def _request_return(req):
        if req.status_code == 200:
            return req.json()
        else:
            return None

    def list_organizations(self):
        """ List oraganizations """
        return self._request_return(requests.get('https://%s%s/api/organizations' % (self.hostname, self.path), auth=(self.username, self.password), verify=self.verify))

    def list_systems(self, organization_label):
        """ List systems """
        return self._request_return(requests.get('https://%s%s/api/organizations/%s/systems' % (self.hostname, self.path, organization_label), auth=(self.username, self.password), verify=self.verify))

    def list_attached_subscriptions(self, system_id):
        """ List attached subscriptions """
        return self._request_return(requests.get('https://%s%s/api/systems/%s/subscriptions' % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify))

    def list_pools(self, system_id):
        """ List available pools """
        return self._request_return(requests.get("https://%s%s/api/systems/%s/pools" % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify))

    def show_system(self, system_id):
        """ List systems """
        return self._request_return(requests.get('https://%s%s/api/systems/%s' % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify))

    def delete_subscription(self, system_id, subscription_id):
        """ Detach subscription """
        return self._request_return(requests.delete("https://%s%s/api/systems/%s/subscriptions/%s" % (self.hostname, self.path, system_id, subscription_id), auth=(self.username, self.password), verify=self.verify))

    def attach_subscription(self, system_id, pool_id, quantity=1):
        """ Attach subscription from pool """
        data = data = {"quantity": quantity, 'pool': pool_id}
        return self._request_return(requests.post("https://%s%s/api/systems/%s/subscriptions" % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify, params=data))
