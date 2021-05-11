import json
import pandas as pd
import matplotlib.pyplot as plt

# HERE WE EXTRACT THE DESIRED DATES AND VOLTAGE VALUES FROM .JSON FILES
# FROM ABB  INVERTER
abb_inverter_readings = ['20210315_1623.json', '20210325_1401.json', '20210408_1618.json']
f = {}
data = {}
result = {}
for i in abb_inverter_readings:
    f[i] = open(i)
    data[i] = json.load(f[i])
    result[i] = pd.json_normalize(data[i], ["feeds", "ser4:106052-3M22-4717", "datasets", "m103_1_W", "data"])

final_abb_inverter = pd.concat(result)

# HERE WE READ THE TEXT FILES FROM FLUKE AND THEN CONCATENATE THEM
# ON A SINGLE DATA FRAME

fluke_readings = ['meas16.txt', 'meas18.txt', 'meas19.txt']
another = {}
for i in range(len(fluke_readings)):
    another[i] = pd.read_csv(fluke_readings[i], sep='\t', encoding='UTF-16LE')

final_fluke = pd.concat(another)

# THEN WE WANT TO OBSERVE TABLE IN AN EXCEL FILE
# AFTER LOOKING INTO EXCEL FILES, WE WILL RETRIEVE THE RELEVANT DATA BACK SINCE
final_abb_inverter.to_excel('readings.xlsx', sheet_name='abb_inverter', index=False)
final_fluke.to_excel('readings2.xlsx', sheet_name='fluke',
                     columns=['Date', 'Time', 'Active Power Total Avg'],
                     index=False)


# RETRIEVE THE DATA BACK
abb_inverter = pd.read_excel('readings.xlsx')
fluke = pd.read_excel('readings2.xlsx')

# HERE WE GET THE KW VALUE OF ACTIVE POWER READING
fluke['Active Power Total Avg'] = fluke['Active Power Total Avg']/1000

abb_inverter['timestamp'] = pd.to_datetime(abb_inverter['timestamp'])

# ----------------------------------------------


def time_format_arranger(date_string, time_string):
    month, date, year = date_string.split('/')
    hour, minute, second = time_string.split(':')
    new_month, new_date, new_minute, new_hour = ['', '', '', '']
    if len(month) == 1:
        new_month = '0' + month
    else:
        new_month = month
    if len(date) == 1:
        new_date = '0' + date
    else:
        new_date = date
    if len(minute) == 1:
        new_minute = '0' + minute
    else:
        new_minute = minute
    if 'PM' in second:
        new_hour = str(12 + int(hour))
    elif hour == '11' or hour == '09':
        new_hour = hour
    else:
        new_hour = '0' + hour
    return '{}-{}-{} {}:{}'.format(year, new_month, new_date, new_hour, new_minute)


def time_format_clipper(timestamp):
    long_time = str(timestamp)
    return long_time[0:-9]


fluke['hour_minute'] = ''
abb_inverter['hour_minute'] = ''
for i in range(len(fluke)):
    fluke['hour_minute'][i] = time_format_arranger(fluke['Date'][i], fluke['Time'][i])
for i in range(len(abb_inverter)):
    abb_inverter['hour_minute'][i] = time_format_clipper(abb_inverter['timestamp'][i])

# BELOW WE REMOVE THE COLUMNS THAT WE ARE NOT GONNA USE. THEN ARRANGE THE ORDER OF COLUMNS.
fluke = fluke.drop(columns=['Date', 'Time'])
cols = ['hour_minute', 'Active Power Total Avg']
fluke = fluke[cols]

abb_inverter = abb_inverter.drop(columns=['timestamp'])
cols2 = ['hour_minute', 'value']
abb_inverter = abb_inverter[cols2]

# WE CHANGE THE NAME OF COLUMNS FOR UNDERSTANDING.
fluke = fluke.rename(columns={'Active Power Total Avg': 'fluke_reading'})
abb_inverter = abb_inverter.rename(columns={'value': 'abb_inverter_reading'})

# THEN SORT THE ROWS BY THE DATE COLUMN WHICH IS CALLED: 'hour_minute'
fluke = fluke.sort_values('hour_minute', ignore_index=True)
abb_inverter = abb_inverter.sort_values('hour_minute', ignore_index=True)

# SINCE FLUKE HAS NEGATIVE POWER READINGS(INDICATING SUPPLYING), MULTIPLY VALUES WITH -1
fluke['fluke_reading'] = -1 * fluke['fluke_reading']


# THEN MERGE DATAFRAMES.
# final_table = pd.concat([abb_inverter, fluke], axis=1)

# HERE WE SELECT THE START AND END TIME WHERE DATASETS OVERLAP.
start_time = ''
end_time = ''
fluke_last_index = len(fluke) - 1
abb_last_index = len(abb_inverter) - 1

if abb_inverter['hour_minute'][0] < fluke['hour_minute'][0]:
    start_time = fluke['hour_minute'][0]
else:
    start_time = abb_inverter['hour_minute'][0]

if abb_inverter['hour_minute'][abb_last_index] < fluke['hour_minute'][fluke_last_index]:
    end_time = abb_inverter['hour_minute'][abb_last_index]
else:
    end_time = fluke['hour_minute'][fluke_last_index]

# THEN WE GET RID OF NON-OVERLAPPING DATA.
for i in range(len(fluke)):
    if fluke['hour_minute'][i] < start_time or fluke['hour_minute'][i] > end_time:
        fluke = fluke.drop(index=i)
for i in range(len(abb_inverter)):
    if abb_inverter['hour_minute'][i] < start_time or abb_inverter['hour_minute'][i] > end_time:
        abb_inverter = abb_inverter.drop(index=i)

# FINALLY MERGE BOTH READINGS THEN TAKE DIFFERENCE OF THEM.
final_table = pd.merge(fluke, abb_inverter, how='inner', on='hour_minute')
final_table['difference'] = final_table['fluke_reading'] - final_table['abb_inverter_reading']

# HERE PLOTTING IS ACHIEVED. THEN SAVED INTO A PDF FILE NAMED WITH OVERLAP START AND END TIMES.
plt.close('all')
final_table.plot(xlabel='time_ordered_index', ylabel='power reading in kW')
file_name = start_time[0:-6] + '--' + end_time[0:-6] + '.pdf'
plt.savefig(file_name)
