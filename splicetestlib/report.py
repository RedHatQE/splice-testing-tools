'''API--WebUI common report tools'''
import datetime

def date_ago(ago):
    '''return the report-formated date some time ago(timedelta); format: "%m/%d/%Y"'''
    return (datetime.datetime.now() - datetime.timedelta(ago)).strftime('%m/%d/%Y')

def dates_filter_name(start_date, end_date, status):
    return "testing_dates_filter_%s_%s_%s" % (start_date, end_date, status) 

def hours_filter_name(hours, status):
    return "testing_hours_filter_%s_%s" % (hours, status)


