
import librosa
import soundfile as sf
import os
import time


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Created dir " + dir_path)
        return True
    
    print("Dir already exists " + dir_path)
    return True


def make_audio_segment(props):

    # Setup
    print(props["audio_filepath"])
    print(props["file_extension"])
    unixtime_start = int(time.time())

    # Calculate segment start and end times
    # Add 2 seconds to beginning & end
    # TODO: speed this up slightly by caching file durations to a global variable
    duration = librosa.get_duration(filename=props["audio_filepath"])
    start_time = props["start_sec"] - 2
    if start_time < 0:
        start_time = 0
    end_time = props["end_sec"] + 2
    if end_time > duration:
        end_time = duration

    segment_filename = props["audio_filename"].replace(".wav", "") + "_" + str(start_time) + "-" + str(end_time) + "_" + props["scientific_name"].replace(" ", "_") + "_" + str(props["confidence"]) + "." + props["file_extension"]

    # Load only the segment into memory
    y, sr = librosa.load(props["audio_filepath"], offset=start_time, duration=(end_time-start_time))

    # Save the segment as a new audio file
    segment_path = props["segment_dir"] + "/" + segment_filename
    sf.write(segment_path, y, sr)
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


