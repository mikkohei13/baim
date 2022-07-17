
import os
import pandas as pd
import datetime
import re

import species

pd.io.formats.excel.ExcelFormatter.header_style = None


def get_datafile_list(directory, file_number_limit):
  datafile_list = []
  objects = os.listdir(directory)
  i = 0
  for filename in objects:
    if filename.lower().endswith(".results.csv"):
      datafile_list.append(filename)
      i = i + 1
    if i >= file_number_limit:
        break

  return datafile_list


# Todo: identify filename format: Audiomoth & SM4
def datetime_from_filename(filename):
    parts = filename.split(".")
    datepart = parts[0]

    # Note: order of these if-clauses are important.
    # Wildlife Acoustics SM4
    # TODO: Not UTC?
    pattern = re.compile("[A-Z0-9]{5}\_\d{8}\_\d{6}")
    if pattern.match(datepart):
        datepart = datepart[6:]
        return datetime.datetime.strptime(datepart, "%Y%m%d_%H%M%S")

    # Audiomoth new firmware
    pattern = re.compile("\d{8}\_\d{6}")
    if pattern.match(datepart):
        return datetime.datetime.strptime(datepart, "%Y%m%d_%H%M%S")

    # Audiomoth old firmware, 32-bit hexadecimal UNIX timestamp
    pattern = re.compile("[A-F0-9]{8}")
    if pattern.match(datepart):
        unix_seconds = int(datepart, 16)
        return datetime.datetime.fromtimestamp(unix_seconds)

    return datepart


def audio_filename_from_filename(filename):
    # Problem: cannot get original file extension, since it's not available on the Birdnet analysis files
    # Presume ".wav"
    parts = filename.split(".")
    return parts[0] + ".wav"


dir = "/mnt/c/Users/mikko/Documents/Audiomoth_2022/20210922-1008-Ks-SM4"
dir = "./test"
dir = "/mnt/c/Users/mikko/Documents/_linux/baim"

subdir_name = dir[(dir.rindex("/") + 1):]
export_file_path = dir + "/" + subdir_name + "-predictions.xlsx"

file_number_limit = 3 # Debug
filter_limit = 0.5

filtered_species_sheet_name = "Species conf " + str(filter_limit)


datafile_list = get_datafile_list(dir, file_number_limit)
datafile_list.sort()
print(datafile_list)

dataframe_list = []

# Do batch operations for each file
for filename in datafile_list:
    df = pd.read_csv(dir + "/" + filename)

    # Skip empty files
    if df.empty:
        continue

    # ~Audio filename
    df['Filename'] = audio_filename_from_filename(filename)

    # Datetime
    df['File start'] = datetime_from_filename(filename)

    # Start time in h:m:s
    df['Start (h:m:s)'] = df.apply(lambda row: str(datetime.timedelta(seconds= row['Start (s)'])), axis = 1)

    dataframe_list.append(df)

    print("Handled file " + filename)

# Combine per-file dataframes
full_dataframe = pd.concat(dataframe_list, ignore_index=True)

# Reorder columns
new_index = ["Start (s)", "End (s)", "File start", "Common name", "Scientific name", "Filename", "Confidence", "Start (h:m:s)"]
full_dataframe = full_dataframe[new_index]


'''
# Add indicator about changing filename. BUT: This is useless when data is filtered.
full_dataframe["New file"] = ""
prev_filename = ""
for ind in full_dataframe.index:
#    print("Prev " + prev_filename)
#    print("Current " + full_dataframe['Filename'][ind])

    if full_dataframe['Filename'][ind] != prev_filename:
        full_dataframe["New file"][ind] = "TRUE"


    prev_filename = full_dataframe['Filename'][ind]
#    print(df['Name'][ind], df['Stream'][ind])
'''


# Filter
filtered_dataframe = full_dataframe[full_dataframe['Confidence'] >= filter_limit]

# Count species occurrences
species_list = filtered_dataframe.groupby(['Scientific name']).size()
# This makes a dataframe with 0 as the column name
species_dataframe = pd.DataFrame(species_list)
# Rename column
species_dataframe.columns = ['Count']
# Sot descending
species_dataframe.sort_values("Count", ascending=False, inplace=True)

#print(species_dataframe)
#exit()

writer = pd.ExcelWriter(export_file_path)

full_dataframe.to_excel(writer, index=True, index_label="Row", sheet_name="Predictions", freeze_panes=(1, 1))
species_dataframe.to_excel(writer, index=True, index_label="Row", sheet_name=filtered_species_sheet_name, freeze_panes=(1, 1))

#workbook  = writer.book
#worksheet_prediction = writer.sheets[Predictions]
#worksheet_prediction.set_column(0,  max_col - 1, 12)

writer.save()

print(species.non_finnish_species)
