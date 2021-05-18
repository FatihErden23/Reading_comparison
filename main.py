import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# READ .JSON FILES FROM ABB_INVERTER.
result = {}
for i in glob.iglob('*.json'):
    with open(i) as f:
        data = json.load(f)
        result[i] = pd.json_normalize(data, ["feeds", "ser4:106052-3M22-4717", "datasets", "m103_1_W", "data"])

final_abb_inverter = pd.concat(result)
final_abb_inverter.drop_duplicates(inplace=True)

# READ TEXT FILES FROM FLUKE.
another = {}
for i in glob.iglob('*.txt'):
    another[i] = pd.read_csv(i, sep='\t', encoding='UTF-16LE')

final_fluke = pd.concat(another)
final_fluke['timestamp'] = pd.to_datetime(final_fluke['Date']+final_fluke['Time'], format="%m/%d/%Y%I:%M:%S %p.%f")

abb_inverter = final_abb_inverter
fluke = final_fluke[['timestamp', 'Active Power Total Avg']]

pd.set_option('mode.chained_assignment', None)
fluke['fluke_reading'] = fluke['Active Power Total Avg']/1000
pd.set_option('mode.chained_assignment', 'warn')
fluke = fluke.drop(columns=['Active Power Total Avg'])

abb_inverter['timestamp'] = pd.to_datetime(abb_inverter['timestamp'])

# SET INDEXES OF DATAFRAMES TO TIMESTAMPS
abb_inverter = abb_inverter.set_index('timestamp').sort_index()
abb_inverter = abb_inverter.tz_convert(None)    # STRIP AWAY THE TIMEZONE.

fluke = fluke.set_index('timestamp').sort_index()

# RENAME THE VALUE COLUMN
abb_inverter = abb_inverter.rename(columns={'value': 'abb_inverter_reading'})

fluke['fluke_reading'] *= -1    # CONVERT NEGATIVE POWER READINGS


# SELECT THE START AND END TIMES OF OVERLAPPING DATA.
start_time = max(fluke.index[0], abb_inverter.index[0])
end_time = min(fluke.index[-1], abb_inverter.index[-1])

# SET THE DESIRED TIME_RANGE INDEX.
index = pd.date_range(
    start=start_time,
    end=end_time,
    freq='5min',
)

# TODO : LINEAR INTERPOLATION
rs = pd.DataFrame(index=index)      # rs FOR FLUKE READINGS

idx_after = np.searchsorted(fluke.index.values, rs.index.values)
rs['after'] = fluke.loc[fluke.index[idx_after], 'fluke_reading'].values
rs['before'] = fluke.loc[fluke.index[idx_after-1], 'fluke_reading'].values
rs['after_time'] = fluke.index[idx_after]
rs['before_time'] = fluke.index[idx_after-1]

rs['span'] = rs['after_time'] - rs['before_time']
rs['after_weight'] = (rs['after_time']-rs.index)/rs['span']
rs['before_weight'] = (rs.index - rs['before_time']) / rs['span']

rs['values'] = rs.eval('after * before_weight + before * after_weight')

# -----------------------------------------------------
rs2 = pd.DataFrame(index=index)     # rs2 FOR ABB READINGS

idx_after_2 = np.searchsorted(abb_inverter.index.values, rs2.index.values)
rs2['after'] = abb_inverter.loc[abb_inverter.index[idx_after_2], 'abb_inverter_reading'].values
rs2['before'] = abb_inverter.loc[abb_inverter.index[idx_after_2-1], 'abb_inverter_reading'].values
rs2['after_time'] = abb_inverter.index[idx_after_2]
rs2['before_time'] = abb_inverter.index[idx_after_2-1]

rs2['span'] = rs2['after_time'] - rs2['before_time']
rs2['after_weight'] = (rs2['after_time']-rs2.index) / rs2['span']
rs2['before_weight'] = (rs2.index - rs2['before_time']) / rs2['span']

rs2['values'] = rs2.eval('after * before_weight + before * after_weight')

# GENERATE AN EMPTY DATAFRAME WITH SPECIFIED COLUMNS
final_table = pd.DataFrame(index=index, columns=['fluke_reading', 'abb_reading', 'difference'])

final_table['fluke_reading'] = rs['values']
final_table['abb_reading'] = rs2['values']


final_table['difference'] = final_table['fluke_reading'] - final_table['abb_reading']


# TODO Filename work
start_date = start_time.strftime("%Y%m%d")
end_date = end_time.strftime("%Y%m%d")
filename = start_date + '-' + end_date + '.pdf'

# PLOT THE FINAL TABLE.
plt.close('all')
final_table.plot(ylabel='power reading in kW')
plt.savefig(filename)
