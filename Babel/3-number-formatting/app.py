from babel.numbers import format_decimal, format_percent

number = 1234.5678

print('# Locale number format')
print('USA', format_decimal(number=number, locale='en_US'))
print('Denmark', format_decimal(number=number, locale='da_DK'))

print('# Customer number format')
print('change to 2 decimals', format_decimal(number=number, format='#,##0.##', locale='da'))
print('strip to clean int', format_decimal(number=number, format='#', locale='da'))
print('strip to clean float', format_decimal(number=number, format='#.##', locale='en'))