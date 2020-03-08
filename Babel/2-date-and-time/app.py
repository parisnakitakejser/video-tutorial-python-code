from datetime import datetime, timedelta
from time import time
from babel.dates import format_date, format_time, format_timedelta, format_datetime, get_timezone

print('# Date format')
d = datetime.utcnow()
print('English:', format_date(d, locale='en'))
print('Danish (default)', format_date(d, locale='da_DK'))
print('Danish (short)', format_date(d, format='short', locale='da_DK'))
print('Danish (medium)', format_date(d, format='medium', locale='da_DK'))
print('Danish (long)', format_date(d, format='long', locale='da_DK'))
print('Danish (full)', format_date(d, format='full', locale='da_DK'))

print('# Time format')
t = time()
print('Danish', format_time(t, locale='da'))
print('Danish (am/pm)', format_time(t, 'h:mm a', locale='da'))
print('Danish (secound)', format_time(t, 'H:mm:ss', locale='da'))

print('# Time Delta')
delta = timedelta(days=6)
print('USA:', format_timedelta(delta, locale='en_US'))
print('Denmark:', format_timedelta(delta, locale='da_DK'))
print('USA (min. month):', format_timedelta(delta, granularity='month', locale='en_US'))

print('# Time-zone')
d = datetime.utcnow()
print('English:', format_datetime(d, 'H:mm Z', locale='en_US'))
print('USA/Eastern:', format_datetime(d, 'H:mm Z', tzinfo=get_timezone('US/Eastern'), locale='en_US'))
print('Europe/Copenhagen:', format_datetime(d, 'H:mm Z', tzinfo=get_timezone('Europe/Copenhagen'), locale='en_US'))