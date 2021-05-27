import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


def interpolate_to_index(df, index):
    idx_after = np.searchsorted(df.index, index)
    after = df.loc[df.index[idx_after], :].to_numpy()
    before = df.loc[df.index[idx_after - 1], :].to_numpy()
    after_time = df.index[idx_after].to_numpy()
    before_time = df.index[idx_after - 1].to_numpy()
    span = after_time - before_time
    after_weight = (after_time - index.to_numpy()) / span
    before_weight = (index.to_numpy() - before_time) / span
    interpolated_data = (after.T * before_weight + before.T * after_weight).T
    rtn = pd.DataFrame(interpolated_data, index=index, columns=df.columns)
    return rtn


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
# Use ceil on start time and floor on end time since the interpolation method
# cannot extrapolate outside the provided data.
index = pd.date_range(
    start=start_time.ceil('5min'),
    end=end_time.floor('5min'),
    freq='5min',
)

rs = interpolate_to_index(fluke, index)
rs2 = interpolate_to_index(abb_inverter, index)

final_table = pd.merge(rs, rs2, left_index=True, right_index=True)
final_table['difference'] = final_table['fluke_reading'] - final_table['abb_inverter_reading']
# Hourly average values might be interesting, too
hourly = final_table.resample('1h').mean()

# Create filename from start and end dates
start_date = start_time.strftime("%Y%m%d")
end_date = end_time.strftime("%Y%m%d")
filename = start_date + '-' + end_date + '.pdf'

# PLOT THE FINAL TABLE.
plt.close('all')
with PdfPages(filename) as pdf:
    final_table.plot(ylabel='power reading in kW')
    pdf.savefig()
    hourly.plot()
    pdf.savefig()

