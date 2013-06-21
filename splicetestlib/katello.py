import requests
import time

class Katello(object):
    """ Katello API calls """
    def __init__(self, hostname='localhost', path='/sam', username='admin', password='admin', verify=False):
        self.hostname = hostname
        self.path = path
        self.username = username
        self.password = password
        self.verify = verify

    @staticmethod
    def _request_return(req):
        if req.status_code == 200:
            try:
                return req.json()
            except ValueError:
                return {}
        else:
            return None

    def list_roles(self):
        """ List roles """
        return self._request_return(requests.get('https://%s%s/api/roles' % (self.hostname, self.path), auth=(self.username, self.password), verify=self.verify))

    def list_organizations(self):
        """ List oraganizations """
        return self._request_return(requests.get('https://%s%s/api/organizations' % (self.hostname, self.path), auth=(self.username, self.password), verify=self.verify))

    def list_systems(self, organization_label):
        """ List systems """
        return self._request_return(requests.get('https://%s%s/api/organizations/%s/systems' % (self.hostname, self.path, organization_label), auth=(self.username, self.password), verify=self.verify))

    def list_providers(self, organization_label):
        """ List providers """
        return self._request_return(requests.get('https://%s%s/api/organizations/%s/providers' % (self.hostname, self.path, organization_label), auth=(self.username, self.password), verify=self.verify))

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
        data = {"quantity": quantity, 'pool': pool_id}
        return self._request_return(requests.post("https://%s%s/api/systems/%s/subscriptions" % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify, params=data))

    def upload_manifest(self, provider_id, manifest_file):
        """ Upload manifest """
        files = {'import': ('manifest.zip', open(manifest_file, 'rb'))}
        ret = self._request_return(requests.post("https://%s%s/api/providers/%s/import_manifest" % (self.hostname, self.path, provider_id), auth=(self.username, self.password), verify=self.verify, files=files))
        task_id = ret["uuid"]
        cnt = 30
        while cnt > 0:
            task_status = self._request_return(requests.get("https://%s%s/api/tasks/%s" % (self.hostname, self.path, task_id), auth=(self.username, self.password), verify=self.verify))
            if task_status is None:
                break
            if task_status['pending?'] == False:
                return task_status
            time.sleep(2)

    def delete_manifest(self, provider_id):
        """ Delete manifest """
        return self._request_return(requests.post("https://%s%s/api/providers/%s/delete_manifest" % (self.hostname, self.path, provider_id), auth=(self.username, self.password), verify=self.verify))
