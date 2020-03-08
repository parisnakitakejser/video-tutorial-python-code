from babel import Locale

print('# Output in english:')
locale = Locale('en', 'US')
print(locale.territories['US'])

print('# Output in danish:')
locale = Locale('da', 'DK')
print(locale.territories['US'])

print('# output lang and country:')
locale = locale.parse('de_DE')
print(locale.get_display_name('en_US'))

locale = locale.parse('da_DK')
print(locale.get_display_name('en_US'))

print('# Output calender days')
locale = Locale('en')
month_names = locale.months['format']['wide'].items()
print(list(month_names))

locale = Locale('da')
month_names = locale.months['format']['wide'].items()
print(list(month_names))