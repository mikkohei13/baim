
from pydub import AudioSegment
import os

def create_dir(dir_path):
  if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    print("Created dir " + dir_path)
  return True


def make_audio_segment(props):

    # Load audiofile
    # TODO: From flac
    audio_full = AudioSegment.from_wav(props["audio_filepath"])
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

    audio_segment = audio_full[(props["start_sec"] * 1000):(props["end_sec"] * 1000)]
    audio_segment.export(segment_path, format="wav") # TODO: flac or mp3? requires ffmpeg

    print("exported segment " + segment_filename)

