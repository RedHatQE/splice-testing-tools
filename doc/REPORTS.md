Reports definition
==================

LifeCycle State
---------------
Time range is a period between start_date and end_date or (if being run by past hours) between start_date = 'current server time - N hours' and end_date = 'current server time'

'State' can be ['Active', 'Inactive', 'Deleted']
System is reported as 'Active' on a given time range if it has checkins during [start_date, end_date].
System is reported as 'Inactive' on a given time range if it has no checkins during [start_date, end_date] and it has checkins before start_date.
System is reported as 'Deleted' on a given time range if special 'Delete' event happened during [start_date, end_date]. This event can happen only once.

Status
------
'Status' can be ['Current', 'Invalid', 'Insufficient']
If system is 'Active' then its status is status of last checkin during [start_date, end_date]
If system is 'Inactive' then its status is status of last checkin before end_date (equals before start_date)
If system is 'Deleted' then its status is status of last checkin before end_date (equals last checkin ever)

Filters
-------
Applying filter criteria means throwing out systems which do not meet it.
