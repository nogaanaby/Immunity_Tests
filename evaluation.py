import librosa
import numpy as np
import mir_eval
import soundfile as sf
from pydub import AudioSegment
import os


def load_audio(file_path, sr=44100):
    """Loads an audio file in MP3 format into a NumPy array."""
    audio, _ = librosa.load(file_path, sr=sr, mono=True)  # Load as mono signal
    return audio

def convert_wav_to_mp3(file_path):
    """
    Converts a WAV file to MP3 and saves it in the same folder with the same name.

    :param file_path: Path to the WAV file.
    """
    # Ensure the file is a WAV file
    wav_file = f"{file_path}.wav"
    mp3_file = f"{file_path}.mp3"

    if os.path.exists(mp3_file):
        print(f"Skipping {mp3_file}: Already exists.")
        return

    if os.path.exists(wav_file):
        # Load the WAV file
        audio = AudioSegment.from_wav(wav_file)

        # Get the directory and filename without extension
        directory, filename = os.path.split(wav_file)
        name_without_ext = os.path.splitext(filename)[0]

        # Define the MP3 output path
        mp3_path = os.path.join(directory, f"{name_without_ext}.mp3")

        # Export as MP3
        audio.export(mp3_path, format="mp3", bitrate="192k")  # Adjust bitrate if needed
        print(f"Converted successfully: {mp3_path}")


def convert_sources_to_mp3(folder_path):
    sources = ["vocals", "drums", "bass", "other"]

    for name in sources:
        file = os.path.join(folder_path, f"{name}")
        convert_wav_to_mp3(file)


def get_seperated_files(folder_path, length):
    separated_files_path = {
        "vocals": f'{folder_path}/vocals.mp3',
        "drums": f'{folder_path}/drums.mp3',
        "bass": f'{folder_path}/bass.mp3',
        "other": f'{folder_path}/other.mp3'
    }
    sources_files={
        "vocals": [],
        "drums": [],
        "bass": [],
        "other": []
    }

    for name,path in separated_files_path.items():
        audio = load_audio(path)
        if(audio.shape[0] < length):
            audio = np.pad(audio, (0, length - audio.shape[0]), mode='constant')
        else:
            audio = audio[:length]
        sources_files[name] = audio
    return sources_files


def evaluate_by_metrics(song_name):
    """
    Computes SDR and SIR by comparing the original mix to separated sources.

    :param mixture_path: Path to the MIXTURE file.
    :param sources_paths: Dictionary with paths to separated source files
                          {"vocals": "path.mp3", "drums": "path.mp3", ...}.
    :return: Dictionary with SDR and SIR results for each source.
    """
    song_path=f'songs/{song_name}'
    original_sources_path=f'{song_path}/originals'
    estimated_sources_path=f'{song_path}/estimated'

    try:
        if not os.path.exists(original_sources_path) or not os.path.exists(estimated_sources_path):
            raise FileNotFoundError

        original_mixture_file_path = f'{original_sources_path}/mixture'
        convert_wav_to_mp3(original_mixture_file_path)
        convert_sources_to_mp3(original_sources_path)
        convert_sources_to_mp3(estimated_sources_path)

        mixture = load_audio(original_mixture_file_path+".mp3")

        estimated_sources_audio=get_seperated_files(estimated_sources_path,mixture.shape[0])
        original_sources_audio=get_seperated_files(original_sources_path,mixture.shape[0])

        # Convert sources into a matrix (rows = sources, columns = signal values)
        estimated_sources = np.array(list(estimated_sources_audio.values()))
        original_sources = np.array(list(original_sources_audio.values()))

        (sdr, sir, _, _) = mir_eval.separation.bss_eval_sources(original_sources, estimated_sources)

        results={}
        for i, name in enumerate(estimated_sources_audio.keys()):
            results[f"{name}_SDR"] = sdr[i]
            results[f"{name}_SIR"] = sir[i]

        return results
    except FileNotFoundError:
        print(f"I couldn't find the music files of the given song. please ensure you have the song directory with the correct name and ddata as the instructions")
