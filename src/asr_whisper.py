import os
from pydub import AudioSegment
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, WhisperTimeStampLogitsProcessor, GenerationConfig
import torch

def list_all_files_in_directory(directory_path):
    files = []
    for root, dirs, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return files


def convert_mp3_to_wav(mp3_file_path, wav_file_path, sample_rate=16000):
    """
    Converts an MP3 file to a WAV file with a specified sample rate.
    
    Args:
    mp3_file_path (str): Path to the input MP3 file.
    wav_file_path (str): Path to the output WAV file.
    sample_rate (int): Sample rate for the output WAV file (default is 16000).
    """
    if os.path.exists(wav_file_path):
        print(f"File {wav_file_path} already exists. Skipping conversion.")
        return wav_file_path
    try:
        # Load the MP3 file
        audio = AudioSegment.from_mp3(mp3_file_path)
        
        # Set the sample rate
        audio = audio.set_frame_rate(sample_rate)
        
        # Export as WAV
        audio.export(wav_file_path, format="wav")
        
        print(f"Successfully converted {mp3_file_path} to {wav_file_path} with sample rate {sample_rate} Hz")
    except Exception as e:
        print(f"An error occurred: {e}")

def setup_whisper_model(model_id = "openai/whisper-large-v3"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = model_id

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=False, use_safetensors=True
        )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe


# # Transcribe a local MP3 file in chunks
# file_path = file_paths[0]
# result = process_large_audio(file_path)

# # Print the transcription result
# print(result)
