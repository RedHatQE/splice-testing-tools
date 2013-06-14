import requests


class Katello(object):
    """ Katello API calls """
    def __init__(self, hostname='localhost', path='/headpin', username='admin', password='admin', verify=False):
        self.hostname = hostname
        self.path = path
        self.username = username
        self.password = password
        self.verify = verify

    def list_attached_subscriptions(self, system_id):
        """ List attached subscriptions """
        req = requests.get('https://%s%s/api/systems/%s/subscriptions' % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify)
        if req.status_code == 200:
            return req.json()
        else:
            return None

    def list_pools(self, system_id):
        """ List available pools """
        req = requests.get("https://%s%s/api/systems/%s/pools" % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify)
        if req.status_code == 200:
            return req.json()
        else:
            return None

    def delete_subscription(self, system_id, subscription_id):
        """ Detach subscription """
        req = requests.delete("https://%s%s/api/systems/%s/subscriptions/%s" % (self.hostname, self.path, system_id, subscription_id), auth=(self.username, self.password), verify=self.verify)
        if req.status_code == 200:
            return req.json()
        else:
            return None

    def attach_subscription(self, system_id, pool_id, quantity=1):
        """ Attach subscription from pool """
        data = data = {"quantity": quantity, 'pool': pool_id}
        req = requests.post("https://%s%s/api/systems/%s/subscriptions" % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify, params=data)
        if req.status_code == 200:
            return req.json()
        else:
            return None

    
