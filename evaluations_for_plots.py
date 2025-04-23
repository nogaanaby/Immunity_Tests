import librosa
import numpy as np
import mir_eval
import soundfile as sf
from pydub import AudioSegment
import os


def compute_sdr(original, estimated, eps=1e-10):
    """
    Compute Signal-to-Distortion Ratio (SDR) for one pair of signals.

    :param original: The ground-truth signal (numpy array)
    :param estimated: The estimated separated signal (numpy array)
    :param eps: A small value to avoid division by zero
    :return: SDR value in dB
    """
    original_energy = np.sum(original ** 2)
    error_energy = np.sum((original - estimated) ** 2)
    sdr = 10 * np.log10((original_energy + eps) / (error_energy + eps))
    return sdr



def compute_sir(estimated, all_estimated_sources, eps=1e-10):
    """
    Compute Signal-to-Interference Ratio (SIR) for one source, given all estimated sources.

    :param original: The ground-truth signal for this source
    :param estimated: The estimated signal for this source
    :param all_estimated_sources: A list of all estimated source arrays
    :param eps: A small value to avoid division by zero
    :return: SIR value in dB
    """
    interference = np.zeros_like(estimated)
    for other in all_estimated_sources:
        if not np.allclose(other, estimated):  # skip the target source
            interference += other
    interference_energy = np.sum(interference ** 2)
    target_energy = np.sum(estimated ** 2)
    sir = 10 * np.log10((target_energy + eps) / (interference_energy + eps))
    return sir

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


def evaluate_by_metrics(song_name, original_dir_name="originals", estimated_dir_name="estimated"):
    """
    Computes SDR and SIR by comparing the original mix to separated sources.

    :param mixture_path: Path to the MIXTURE file.
    :param sources_paths: Dictionary with paths to separated source files
                          {"vocals": "path.mp3", "drums": "path.mp3", ...}.
    :return: Dictionary with SDR and SIR results for each source.
    """
    song_path=f'songs/{song_name}'
    original_sources_path=f'{song_path}/{original_dir_name}'
    estimated_sources_path=f'{song_path}/{estimated_dir_name}'

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

        # Ensure both arrays have the same shape
        min_length = min(original_sources.shape[1], estimated_sources.shape[1])
        original_sources = original_sources[:, :min_length]
        estimated_sources = estimated_sources[:, :min_length]

        results={
            "SDR":[],
            "SIR":[]
        }


        for i, name in enumerate(["vocals", "drums", "bass", "other"]):
            sdr_val = compute_sdr(original_sources[i], estimated_sources[i])
            results["SDR"].append({name: sdr_val})

            sir_val = compute_sir(estimated_sources[i], estimated_sources)
            results["SIR"].append({name: sir_val})
            print(f"{name.upper()}: SDR = {sdr_val:.2f} dB, SIR = {sir_val:.2f} dB")


        return results
    except FileNotFoundError:
        print(f"I couldn't find the music files of the given song. please ensure you have the song directory with the correct name and data as the instructions")
