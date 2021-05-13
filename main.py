import json
import glob
import pandas as pd
import matplotlib.pyplot as plt

# HERE WE EXTRACT THE DESIRED DATES AND VOLTAGE VALUES FROM .JSON FILES
# FROM ABB  INVERTER
result = {}  # Could also use a list instead of a dict.
# Iterate over all the json files in the directory so you don't have to hard-code the filenames.
for i in glob.iglob('*.json'):
    # Use a context manager when you open a file. This will automatically close the file when you're done,
    # even if an exception occurs to interrupt program flow.
    with open(i) as f:
        data = json.load(f)
        result[i] = pd.json_normalize(data, ["feeds", "ser4:106052-3M22-4717", "datasets", "m103_1_W", "data"])
        # If you used a list, you could add to it like this:
        # result.append( ... )

final_abb_inverter = pd.concat(result)
# Because of how the data is downloaded, some time samples appear in multiple json files.
final_abb_inverter.drop_duplicates(inplace=True)

# HERE WE READ THE TEXT FILES FROM FLUKE AND THEN CONCATENATE THEM
# ON A SINGLE DATA FRAME
another = {}
# Iterate over txt files in the directory
for i in glob.iglob('*.txt'):
    another[i] = pd.read_csv(i, sep='\t', encoding='UTF-16LE')

final_fluke = pd.concat(another)
# Fix Fluke datetimes. For some reason it looks like the milliseconds are after the AM/PM.
final_fluke['timestamp'] = pd.to_datetime(final_fluke['Date']+final_fluke['Time'], format="%m/%d/%Y%I:%M:%S %p.%f")

# THEN WE WANT TO OBSERVE TABLE IN AN EXCEL FILE
# AFTER LOOKING INTO EXCEL FILES, WE WILL RETRIEVE THE RELEVANT DATA BACK SINCE
# Saving to Excel could be useful if you want to use Excel to look through the data. But generally you probably
# wouldn't want to do this.
#final_abb_inverter.to_excel('readings.xlsx', sheet_name='abb_inverter', index=False)
#final_fluke.to_excel('readings2.xlsx', sheet_name='fluke',
#                     columns=['Date', 'Time', 'Active Power Total Avg'],
#                     index=False)

# RETRIEVE THE DATA BACK
# No need to read from Excel data we have already in memory
# I make new variables and select the desired column from fluke
abb_inverter = final_abb_inverter #pd.read_excel('readings.xlsx')
fluke = final_fluke[['timestamp', 'Active Power Total Avg']]

# HERE WE GET THE KW VALUE OF ACTIVE POWER READING
pd.set_option('mode.chained_assignment', None) # Ignore this warning in this case
fluke['fluke_reading'] = fluke['Active Power Total Avg']/1000
pd.set_option('mode.chained_assignment', 'warn')
fluke = fluke.drop(columns=['Active Power Total Avg'])

abb_inverter['timestamp'] = pd.to_datetime(abb_inverter['timestamp'])

# Make the timestamp to be the DataFrame index
abb_inverter = abb_inverter.set_index('timestamp').sort_index()
# ABB inverter timestamp is set as UTC timezone, but it actually appears to be localized.
# We can either correct the timezone or strip the timezone and do everything in local time
# It's easiest to just strip away the timezone since the Fluke data is not timezone aware
abb_inverter = abb_inverter.tz_convert(None)
fluke = fluke.set_index('timestamp').sort_index()
# Fluke timestamp is in local time only -- not timezone aware

# ----------------------------------------------

# I think your time_format_arranger and related functions are more complicated than needed.
# Just use pandas datetime parsing and work with datetime columns.


# WE CHANGE THE NAME OF COLUMNS FOR UNDERSTANDING.
abb_inverter = abb_inverter.rename(columns={'value': 'abb_inverter_reading'})

# SINCE FLUKE HAS NEGATIVE POWER READINGS(INDICATING SUPPLYING), MULTIPLY VALUES WITH -1
fluke['fluke_reading'] *= -1


# THEN MERGE DATAFRAMES.
# final_table = pd.concat([abb_inverter, fluke], axis=1)

# HERE WE SELECT THE START AND END TIME WHERE DATASETS OVERLAP.
# Hint: You can get the last item in a Python list using the index -1.
start_time = max(fluke.index[0], abb_inverter.index[0])
end_time = min(fluke.index[-1], abb_inverter.index[-1])

# TODO: Normalize the sampling times to the same times with linear interpolation
# See https://stackoverflow.com/a/51920191

# THEN WE GET RID OF NON-OVERLAPPING DATA.
# Hint: Use pandas datetime indexing to do this in a vectorized manner
# Rarely do you want to loop over the items of a DataFrame
fluke = fluke.loc[start_time:end_time]
abb_inverter = abb_inverter.loc[start_time:end_time]

# FINALLY MERGE BOTH READINGS THEN TAKE DIFFERENCE OF THEM.
final_table = pd.merge(fluke, abb_inverter, left_index=True, right_index=True)
final_table['difference'] = final_table['fluke_reading'] - final_table['abb_inverter_reading']

# HERE PLOTTING IS ACHIEVED. THEN SAVED INTO A PDF FILE NAMED WITH OVERLAP START AND END TIMES.
plt.close('all')
final_table.plot(ylabel='power reading in kW')
# TODO: Times aren't strings any more, so need to use another way to make the filename
# For example, see Python's strftime function.
file_name = start_time[0:-6] + '--' + end_time[0:-6] + '.pdf'
plt.savefig(file_name)
