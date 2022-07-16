
import os
import pandas as pd
import datetime
import re

def get_datafile_list(directory, limit):
  datafile_list = []
  objects = os.listdir(directory)
  i = 0
  for filename in objects:
    if filename.lower().endswith(".results.csv"):
      datafile_list.append(filename)
      i = i + 1
    if i >= limit:
        break

  return datafile_list


# Todo: identify filename format: Audiomoth & SM4
def datetime_from_filename(filename):
    parts = filename.split(".")
    datepart = parts[0]

    # Note: order of these if-clauses are important.
    # Wildlife Acoustics SM4
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


dir = "/mnt/c/Users/mikko/Documents/Audiomoth_2022/20220311-25-Nissinmäki"
dir = "/mnt/c/Users/mikko/Documents/_linux"
dir = "./test"

limit = 2000

datafile_list = get_datafile_list(dir, limit)
datafile_list.sort()
print(datafile_list)

df_list = []

for filename in datafile_list:
    df = pd.read_csv(dir + "/" + filename)
    if df.empty:
        continue

    # ~Audio filename
    df['Filename'] = audio_filename_from_filename(filename)

    # Datetime
    df['Date (UTC)'] = datetime_from_filename(filename)

    # Start time in h:m:s
    df['Start (h:m:s)'] = df.apply(lambda row: str(datetime.timedelta(seconds= row['Start (s)'])), axis = 1)

    # Confidence comma-separated
    df['Confidence (cs)'] = df.apply(lambda row: str(row['Confidence']).replace(".", ","), axis = 1)

    df_list.append(df)
    print("Handled file " + filename)

full_df = pd.concat(df_list, ignore_index=True) # TODO: does not work properly: only stores the last list item data

full_df.to_csv(dir + "/birdnet-output.csv", index=True)
