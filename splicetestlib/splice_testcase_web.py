import nose
import os
import report
import pageobjects
from pageobjects import namespace
from pageobjects.login import login_ctx
from pageobjects.users import user_experimental_ui_ctx
from pageobjects.sampageobject import organisation_ctx
from pageobjects.filters import filter_date_range_ctx, filter_hours_ctx
from selenium_wrapper import SE, current_url

from contextlib import contextmanager


class Splice_has_WebUI(object):
    @classmethod
    def check(self, ss):
        if not 'selenium_display' in ss.config:
            raise nose.exc.SkipTest("can't test without selenium_display")

    @classmethod
    def prepare(self, ss):
        # prepare DISPLAY
        self._old_os_environ_display = None
        if 'DISPLAY' in os.environ:
            self._old_os_environ_display = os.environ['DISPLAY']
        os.environ['DISPLAY'] = ss.config['selenium_display']

        # prepare config
        self.KATELLO = namespace.load_ns({
            'user': ss.config['katello_user'],
            'password': ss.config['katello_password'],
            'url': "https://" + ss.Instances['KATELLO'][0].parameters['public_dns_name']
        })

    @staticmethod
    @contextmanager
    def _env_ctx(url, username, password, organization):
         with current_url(url):
            with login_ctx(username, password):
                with user_experimental_ui_ctx(username):
                    with organisation_ctx(organization):
                        yield


    @classmethod
    def splice_check_report(typeinstance, days_start=None, days_end=None, past_hours=None, state=[u'Active', u'Inactive', u'Deleted'], current=0, invalid=0, insufficient=0, organizations=[u'Testing Org']):
        report_page = None
        KATELLO = typeinstance.KATELLO
        SE.reset(url=KATELLO.url)
        if days_start is not None and days_end is not None:
            # date-range mode
            start_date, end_date = report.date_ago(days_start), report.date_ago(days_end)
            filter_name = report.dates_filter_name(start_date, end_date, state)
            with typeinstance._env_ctx(KATELLO.url, KATELLO.user, KATELLO.password, organizations[0]):
                with filter_date_range_ctx(
                        name=filter_name,
                        start_date=start_date,
                        end_date=end_date,
                        organizations=organizations,
                        lifecycle_states=state
                    ) as (filters_page, report_filter):
                    report_page = report_filter.run_report()
                    # assert the values
                    nose.tools.assert_equal(report_page.current_subscriptions.count.text, unicode(current))
                    nose.tools.assert_equal(report_page.insufficient_subscriptions.count.text, unicode(insufficient))
                    nose.tools.assert_equal(report_page.invalid_subscriptions.count.text, unicode(invalid))
                                
        elif past_hours is not None:
            # hours-based operation
            filter_name = report.hours_filter_name(past_hours, state)
            with typeinstance._env_ctx(KATELLO.url, KATELLO.user, KATELLO.password, organizations[0]):
                with filter_hours_ctx(
                        name=filter_name,
                        hours=past_hours,
                        organizations=organizations,
                        lifecycle_states=state
                    ) as (filters_page, report_filter):
                    report_page = report_filter.run_report()
                    # assert the values
                    nose.tools.assert_equal(report_page.current_subscriptions.count.text, unicode(current))
                    nose.tools.assert_equal(report_page.insufficient_subscriptions.count.text, unicode(insufficient))
                    nose.tools.assert_equal(report_page.invalid_subscriptions.count.text, unicode(invalid))
        else:
            # Wrong usage
            assert False, "Wrong usage"
            return # not reached


    @classmethod
    def cleanup(self, ss):
        if self._old_os_environ_display is not None:
            os.environ['DISPLAY'] = self._old_os_environ_display
        else:
            del(os.environ['DISPLAY'])

