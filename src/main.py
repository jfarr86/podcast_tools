import os
from datasets import load_dataset
from asr_whisper import convert_mp3_to_wav, list_all_files_in_directory, setup_whisper_model

mp3_directory_path = '/home/jfarr/workspace/podcast_tools/podcast_episodes/mp3'
wav_directory_path = '/home/jfarr/workspace/podcast_tools/podcast_episodes/wav'
text_directory_path = '/home/jfarr/workspace/podcast_tools/podcast_episodes/text'
mp3_file_paths = list_all_files_in_directory(mp3_directory_path)


# for mp3_file in mp3_file_paths:
#     wav_file_name = os.path.splitext(os.path.basename(mp3_file))[0] + '.wav'
#     wav_file_path = os.path.join(wav_directory_path, wav_file_name)

#     convert_mp3_to_wav(mp3_file, wav_file_path)

wav_file_paths = list_all_files_in_directory(wav_directory_path)
pipe = setup_whisper_model()

# dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
# sample = dataset[0]["audio"]
# result = pipe(sample)
# print(result["text"])

for wav_file in wav_file_paths:
    transcription_name = os.path.splitext(os.path.basename(wav_file))[0] +'.txt'
    transcription_path = os.path.join(text_directory_path, transcription_name)
    
    result = pipe(wav_file, generate_kwargs={"language" : "english"})
    with open (transcription_path, "w") as f:
        f.write(result["text"])


    