
import librosa
import soundfile as sf
import os
import time

latest_audio_y = None
latest_audio_sr = None
latest_audio_filepath = ""


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Created dir " + dir_path)
        return True
    
    print("Dir already exists " + dir_path)
    return True


def make_audio_segment(props):

    global latest_audio_y
    global latest_audio_sr
    global latest_audio_filepath

    # Setup
    print(props["audio_filepath"])
    print(props["file_extension"])
    unixtime_start = int(time.time())

    # load the audio file
    # To save some time, the latest audio file information is saved into global variables and used from there, thus avoiding need to load it again. But since segments are handled in the order of species, this often does not help.
    # Another option would be to keep all audio files in memory, but does that take too much memory?
    # TODO: Major refactoring: Handle files one at a time, and store species data in an array, and generate report only after handling all segments and sorting the result in order by species. 
    if latest_audio_filepath == props["audio_filepath"]:
        y = latest_audio_y
        sr = latest_audio_sr
        print("Previous audio file used in " + str(int(time.time()) - unixtime_start))
    else:
        y, sr = librosa.load(props["audio_filepath"], mono=False, sr=None)
        latest_audio_y = y
        latest_audio_sr = sr
        latest_audio_filepath = props["audio_filepath"]
        print("New audio file loaded in " + str(int(time.time()) - unixtime_start))

    # Calculate segment start and end times
    # Add 2 seconds to beginning & end
    duration = librosa.get_duration(y=y, sr=sr)
    start_time = props["start_sec"] - 2
    if start_time < 0:
        start_time = 0
    end_time = props["end_sec"] + 2
    if end_time > duration:
        end_time = duration

    segment_filename = props["audio_filename"].replace(".wav", "") + "_" + str(start_time) + "-" + str(end_time) + "_" + props["scientific_name"].replace(" ", "_") + "_" + str(props["confidence"]) + "." + props["file_extension"]

    # convert the start and end positions from seconds to samples
    start_sample = int(start_time * sr)
    end_sample = int(end_time * sr)
    print("Positions converted in " + str(int(time.time()) - unixtime_start))

    # extract the segment from the audio
    segment = y[start_sample:end_sample]
    print("Segment extracted in " + str(int(time.time()) - unixtime_start))

    # save the segment as a new audio file
#    librosa.output.write_wav(segment_filename, segment, sr)
    segment_path = props["segment_dir"] + "/" + segment_filename
    sf.write(segment_path, segment, sr)
    print("Segment saved to " + segment_filename + " in " + str(int(time.time()) - unixtime_start))

    return segment_filename

'''
def make_audio_segment_OLD(props):
    print(props["audio_filepath"])
    print(props["file_extension"])


    # Load audiofile
    audio_full = pydub.AudioSegment.from_file(props["audio_filepath"], format = props["file_extension"])

    len_sec = audio_full.duration_seconds

    # Add 2 seconds to beginning & end
    start_sec = props["start_sec"] - 2
    if start_sec < 0:
        start_sec = 0
    end_sec = props["end_sec"] + 2
    if end_sec > len_sec:
        end_sec = len_sec

    segment_filename = props["audio_filename"].replace(".wav", "") + "_" + str(start_sec) + "-" + str(end_sec) + "_" + props["scientific_name"].replace(" ", "_") + "_" + str(props["confidence"]) + ".wav"

    segment_path = props["segment_dir"] + "/" + segment_filename

    audio_segment = audio_full[(start_sec * 1000):(end_sec * 1000)]
    audio_segment.export(segment_path, format="wav") # TODO: flac or mp3? requires ffmpeg

    print("exported segment " + segment_filename)

    return segment_filename
'''


