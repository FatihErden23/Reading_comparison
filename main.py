import json
import pandas as pd

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
final_abb_inverter.to_excel('readings.xlsx', sheet_name='abb_inverter', index=False)
final_fluke.to_excel('readings2.xlsx', sheet_name='fluke',
                     columns=['Date', 'Time', 'Active Power AN Avg', 'Active Power BN Avg', 'Active Power CN Avg'],
                     index=False)

# AFTER LOOKING INTO EXCEL FILES, WE RETRIEVE THE RELEVANT DATA BACK SINCE
# FLUKE HAS TOO MANY IRRELEVANT DATA THAT I WANT TO GET RID OF
abb_inverter = pd.read_excel('readings.xlsx')
fluke = pd.read_excel('readings2.xlsx')

# AFTER THAT WE WANT A SINGLE TOTAL POWER VALUE FOR FLUKE READING
# OPEN A NEW COLUMN AND GET THE VALUES in kW
fluke['Total average power'] = (fluke['Active Power AN Avg'] + fluke['Active Power BN Avg'] + fluke[
    'Active Power CN Avg']) / 1000

abb_inverter['timestamp'] = pd.to_datetime(abb_inverter['timestamp'])

fluke['Date'] = fluke['Date'] + ' ' + fluke['Time']
print(fluke['Date'])

time_string = '4/8/2021 4:24:31 PM.492'

# BELOW FUNCTION DOES NOT DO ITS PURPOSE RIGHT NOW


def date_writer(time):
    date_string = str(time)
    date = date_string[0:8].replace('/', '-')
    time = date_string[-14:-10]
    return date + ' ' + time


dadada = date_writer(time_string)
print(dadada)
