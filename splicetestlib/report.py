'''API--WebUI common report tools'''
import datetime, re

unsafe_pattern = re.compile(r'([\[\],/\\\'\s])')

def safe_name(s):
    return re.sub(unsafe_pattern, '_', s)

def date_ago(ago):
    '''return the report-formated date some time ago(timedelta); format: "%m/%d/%Y"'''
    return (datetime.datetime.now() - datetime.timedelta(ago)).strftime('%m/%d/%Y')



def dates_filter_name(start_date, end_date, status):
    return safe_name("testing_dates_filter_%s_%s_%s" % (start_date, end_date, status))

def hours_filter_name(hours, status):
    return safe_name("testing_hours_filter_%s_%s" % (hours, status))


