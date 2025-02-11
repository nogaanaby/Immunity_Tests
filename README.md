# Music Source Separation Evaluation

This project allows you to evaluate music source separation by comparing estimated separated tracks with the original song. It calculates evaluation metrics (SDR, SIR) and lets you manually review the separation quality.

## 🎵 Add a Song

1. **Create a directory structure**  
   - Inside the project root, create a new folder named **`songs`** (if it doesn’t exist).  
   - Inside **`songs`**, create a folder with the **song name**.  
   - Inside the song's folder, create two subfolders:  
     - **`Estimated`** (for the AI-separated sources)  
     - **`Originals`** (for the original sources)  

2. **Place the audio files**  
   - Each directory must contain the following files (either `.wav` or `.mp3`), mixture.wav is the original song:  
    - originals
      - mixture.wav
      - drums.wav
      - bass.wav
      - vocals.wav
      - other.wav
    - estimated
      - mixture.wav
      - drums.wav
      - bass.wav
      - vocals.wav
      - other.wav
      
3. **Run the main.py file**
    Run the program and type in your review. it will add it to evaluation.csv file which will create in the root folder of this project