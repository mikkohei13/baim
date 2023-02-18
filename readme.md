

Spplication to convert bird sound analysis made with BirdNET into a more usable format:
* Excel file with sheets for
   * Predictions with filename, and position in h:mm:ss format, to make finding the sound eaier
   * Number of predictions per species above given threshold, to allow seeing what are the common vs. less common species
* HTML report page with five audio clips of each species. This makes it easy to check if predictions for each species is reliable or not.


# Setup

### Initial setup

    git clone https://github.com/mikkohei13/baim.git
    apt install python3.10-venv
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    (install Tkinter)

### Start virtual environment

    source .venv/bin/activate
    deactivate

### Using from command line

- Analyze audio files with BirdNET
- Have birdNET result files in a root directory and audio files in Data directory 
- Set path to directory to handle_files.py
- Run ´python3 handle_files.py´

### Compiling the app on Windows

- Setup Python on Windows
- Set Python to Powershell profile
- Copy files to Windows (no subdirectories): ´cp ./baim/* /mnt/c/Users/mikko/Documents/compile/´
- With Powershell:
   - Install requirements: ´pip install -r requirements.txt´
   - Compile the app:

    pyinstaller --windowed --onefile app.py --add-data "C:/Users/mikko/AppData/Local/Programs/Python/Python310/Lib/site-packages/librosa/util/example_data/registry.txt;librosa/util/example_data" --add-data "C:/Users/mikko/AppData/Local/Programs/Python/Python310/Lib/site-packages/librosa/util/example_data/index.json;librosa/util/example_data" --add-data "baim-icon.png;." --distpath "C:/Users/mikko/Desktop/"  --hidden-import "sklearn.metrics._pairwise_distances_reduction._datasets_pair" --hidden-import "sklearn.metrics._pairwise_distances_reduction._middle_term_computer"

# How it works

Creating audio snippets & spectrograms of species

- Have list of non-finnish species
- Have a prediction dataframe
- Filter confidence >= 0.9
- Set empty dict for predictions-to-check
- Set empty dict with scientific name as key, count as value
- Loop rows
    - If species has < 5 occurrences in names dict
        - If species is not non-finnish
            - Add to preditions dict
            - Add tp names dict
- Filter confidence <= 0.7
    - Do same loop as above
- Now we have dict of max 5 snippets per species
- Sort by scientific name asc, confidence asc (or time asc?)
- Loop the dict
    - Get start time & end time
    - Set cut_start == start - 5, cut_end == end + 5.
    - If cut_start < 0, set cut_start == 0
    - If cut_end > audio file len, set cut_end == len
    - Cut audio snippet from cut_start to cut_end
    - Make spectrogram, with width based on length in seconds
    - Save audio and spectro in report file
    - Generate html for the snippet, using
        - audio
        - spectro
        - species, confidence
        - filename
        - times (also in ISO format that Vihko uses)
- Save html report

### Expectations

- BirdNET files are in the csv format provided by birdnet
- All audio files have same file extension. This can be wav, mp3 or flac
- Audio filenames are in format created by Audiomoth (3 versions) or Wildlife Acoustics SM4


# Todo

DONE: Randomixe dataframe order before picking segments? To avoid having 5+ segments of the same local bird.

To get most probable identifications, sort by confidence desc.
To get a sample of all identifications above the threshold, shuffle, to get good idea of the variety.

Exceliin sarakkeiksi myös:
Laji - Määritys	Määrä - Havainto	Pesimävarmuusindeksi - Havainto	Lisätiedot - Havainto	Kokoelma/Avainsanat - Havainto

### Ideas

Filter low-frequency noise, unless predicted species has low frequency (botste, owls...)

