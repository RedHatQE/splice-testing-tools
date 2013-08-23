import requests
import time
import re
import tempfile
import zipfile
import os
import json
import iso8601
import datetime


class Katello(object):
    """ Katello API calls """
    def __init__(self, hostname='localhost', deployment='sam', username='admin', password='admin', verify=False):
        self.hostname = hostname
        self.deployment = deployment
        self.path = '/' + deployment
        self.username = username
        self.password = password
        self.verify = verify
        self.signo = True

    @staticmethod
    def _request_return(req):
        if req.status_code == 200:
            try:
                return req.json()
            except ValueError:
                return {}
        else:
            return None

    def _wait_for_task(self, task_id, maxtries=30):
        """ Wait for task """
        cnt = maxtries
        while cnt > 0:
            task_status = self._request_return(requests.get('https://%s%s/api/tasks/%s' % (self.hostname, self.path, task_id), auth=(self.username, self.password), verify=self.verify))
            if task_status is None or task_status['pending?'] is False:
                break
            time.sleep(2)
            cnt -= 1
        assert cnt > 0, "maxtries %s while waiting for task %s" % (maxtries, task_id)
        return task_status

    def list_roles(self):
        """ List roles """
        return self._request_return(requests.get('https://%s%s/api/roles' % (self.hostname, self.path), auth=(self.username, self.password), verify=self.verify))

    def list_users(self):
        """ List users """
        return self._request_return(requests.get('https://%s%s/api/users' % (self.hostname, self.path), auth=(self.username, self.password), verify=self.verify))

    def list_organizations(self):
        """ List oraganizations """
        return self._request_return(requests.get('https://%s%s/api/organizations' % (self.hostname, self.path), auth=(self.username, self.password), verify=self.verify))

    def list_systems(self, organization_label):
        """ List systems """
        return self._request_return(requests.get('https://%s%s/api/organizations/%s/systems' % (self.hostname, self.path, organization_label), auth=(self.username, self.password), verify=self.verify))

    def list_systems_by_custom_info(self, organization_label, key, value):
        """ List systems by custom info"""
        data = {'search': "custom_info.%s:%s" % (key, value)}
        return self._request_return(requests.get('https://%s%s/api/organizations/%s/systems' % (self.hostname, self.path, organization_label),
                                                 auth=(self.username, self.password),
                                                 verify=self.verify,
                                                 params=data))

    def list_providers(self, organization_label):
        """ List providers """
        return self._request_return(requests.get('https://%s%s/api/organizations/%s/providers' % (self.hostname, self.path, organization_label), auth=(self.username, self.password), verify=self.verify))

    def list_attached_subscriptions(self, system_id):
        """ List attached subscriptions """
        return self._request_return(requests.get('https://%s%s/api/systems/%s/subscriptions' % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify))

    def list_pools(self, system_id):
        """ List available pools """
        return self._request_return(requests.get('https://%s%s/api/systems/%s/pools' % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify))

    def show_system(self, system_id):
        """ Show system """
        return self._request_return(requests.get('https://%s%s/api/systems/%s' % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify))

    def show_user(self, user_id):
        """ Show user """
        return self._request_return(requests.get('https://%s%s/api/users/%s' % (self.hostname, self.path, user_id), auth=(self.username, self.password), verify=self.verify))

    def delete_organization(self, organization_label):
        """ Delete org """
        ret = self._request_return(requests.delete('https://%s%s/api/organizations/%s' % (self.hostname, self.path, organization_label), auth=(self.username, self.password), verify=self.verify))
        return self._wait_for_task(ret['uuid'])

    def delete_role(self, role_id):
        """ Detach role """
        return self._request_return(requests.delete('https://%s%s/api/roles/%s' % (self.hostname, self.path, role_id), auth=(self.username, self.password), verify=self.verify))

    def delete_subscription(self, system_id, subscription_id):
        """ Detach subscription """
        return self._request_return(requests.delete('https://%s%s/api/systems/%s/subscriptions/%s' % (self.hostname, self.path, system_id, subscription_id), auth=(self.username, self.password), verify=self.verify))

    def attach_subscription(self, system_id, pool_id, quantity=1):
        """ Attach subscription from pool """
        data = {'quantity': quantity, 'pool': pool_id}
        return self._request_return(requests.post('https://%s%s/api/systems/%s/subscriptions' % (self.hostname, self.path, system_id), auth=(self.username, self.password), verify=self.verify, params=data))

    def upload_manifest(self, org_label, manifest_file, provider_name='Red Hat'):
        """ Upload manifest """
        provider_id = None
        for provider in self.list_providers(org_label):
            if provider['name'] == provider_name:
                provider_id = provider['id']
                break
        if provider_id is None:
            # no such provider
            return None
        files = {'import': ('manifest.zip', open(manifest_file, 'rb'))}
        ret = self._request_return(requests.post('https://%s%s/api/providers/%s/import_manifest' % (self.hostname, self.path, provider_id), auth=(self.username, self.password), verify=self.verify, files=files))
        return self._wait_for_task(ret['uuid'])

    def delete_manifest(self, provider_id):
        """ Delete manifest """
        return self._request_return(requests.post('https://%s%s/api/providers/%s/delete_manifest' % (self.hostname, self.path, provider_id), auth=(self.username, self.password), verify=self.verify))

    def _get_csrf(self):
        """ Get CSRF token """
        data = {'username': self.username, 'password': self.password, 'commit': 'Login'}
        session = requests.session()
        req_type = session.get('https://%s%s' % (self.hostname, self.path), data=data, verify=self.verify)
        if req_type.content.find("/signo/") != -1:
            # signo
            self.signo = True
            req_login = session.post('https://%s/signo/login' % self.hostname, data=data, verify=self.verify)
        else:
            # Let's try without signo
            self.signo = False
            req_login = session.post('https://%s%s/user_session' % (self.hostname, self.path), data=data, verify=self.verify)
        assert req_login.status_code == 200, "Failed to login to %s%s" % (self.hostname, self.path)
        req_dashboard = session.get('https://%s%s/dashboard' % (self.hostname, self.path), verify=self.verify)
        assert req_dashboard.status_code == 200
        csrf = re.search('.*<meta content="(.*=)" name="csrf-token" />', req_dashboard.content, re.DOTALL)
        assert csrf is not None
        return session, csrf.group(1)

    def _select_org(self, session, csrf, org_id=1):
        """ Select Org in interactive session """
        req_setgroup = session.post('https://%s%s/user_session/set_org?org_id=%s' % (self.hostname, self.path, org_id), verify=self.verify, allow_redirects=False, data={"authenticity_token": csrf})
        assert req_setgroup.status_code == 302
        assert req_setgroup.content.find('/dashboard') != -1

    def run_report(self, report_id, set_org=1):
        """ Run report """
        session, csrf = self._get_csrf()
        self._select_org(session, csrf, set_org)
        req_report = session.get('https://%s%s/splice_reports/filters/%s/reports/items.zip?encrypt=0&skip_expand=0' % (self.hostname, self.path, report_id), verify=self.verify)
        assert req_report.status_code == 200
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.file.write(req_report.content)
        tf.close()
        zf = zipfile.ZipFile(tf.name)
        expcsv, metadata, expjson = '','',''
        for archfile in zf.filelist:
            if archfile.filename.endswith("/export.csv"):
                expcsv = zf.open(archfile.filename).read()
            elif archfile.filename.endswith("/metadata"):
                metadata = zf.open(archfile.filename).read()
            elif archfile.filename.endswith("expanded_export.json"):
                expjson = json.loads(zf.open(archfile.filename).read())
        zf.close()
        os.unlink(tf.name)
        return expcsv, metadata, expjson

    def create_report(self, name, organizations=None, time='choose_daterange', hours='', start_date='', end_date='', status=['Current', 'Invalid', 'Insufficient'], satellite_name='', description='', state=['Active', 'Inactive', 'Deleted'], set_org=1):
        """ Create report """
        assert (time == 'choose_hour' and hours != '' and start_date == '' and end_date == '') or \
            (time == 'choose_daterange' and start_date != '' and end_date != '' and hours == '')
        if organizations is None:
            # no orgs specified, adding all of them
            organizations = sorted([str(org['id']) for org in self.list_organizations()])
        session, csrf = self._get_csrf()
        self._select_org(session, csrf, set_org)
        report_form = {'authenticity_token': csrf,
                       'splice_reports_filter[name]': name,
                       'splice_reports_filter[description]': description,
                       'splice_reports_filter[status][]': [''] + status,
                       'splice_reports_filter[state][]': [''] + state,
                       'splice_reports_filter[satellite_name]': satellite_name,
                       'splice_reports_filter[organizations][]': [''] + organizations,
                       'time': time,
                       'splice_reports_filter[hours]': hours,
                       'splice_reports_filter[start_date]': start_date,
                       'splice_reports_filter[end_date]': end_date
                       }
        headers = {'X-CSRF-Token': csrf}

        req_report = session.post('https://%s%s/splice_reports/filters/' % (self.hostname, self.path), data=report_form, headers=headers, verify=self.verify)
        assert req_report.status_code == 200
        report_id = re.search('.*\'filter_([0-9]*)\'', req_report.content, re.DOTALL)
        assert report_id is not None
        return report_id.group(1)

    def delete_report(self, report_id, set_org=1):
        """ Delete report """
        session, csrf = self._get_csrf()
        self._select_org(session, csrf, set_org)
        headers = {'X-CSRF-Token': csrf}

        req_delete = session.delete('https://%s%s/splice_reports/filters/%s' % (self.hostname, self.path, report_id), headers=headers, verify=self.verify)
        assert req_delete.status_code == 200
        return req_delete.content

    def find_last_checkin(self):
        """ Find first and last checkins among all systems"""
        initdate = iso8601.parse_date("1900-01-01T00:00:00Z")
        for org in self.list_organizations():
            for system in self.list_systems(org['label']):
                last_checkin_s = self.show_system(system['uuid'])['checkin_time']
                last_checkin = iso8601.parse_date(last_checkin_s)
                if last_checkin > initdate:
                    initdate = last_checkin
        return initdate
