

Personal notes on Google Docs.


Creating audio snipperts & spectrograms of species

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


# Setup with venv

    git clone https://github.com/mikkohei13/baim.git
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    deactivate

