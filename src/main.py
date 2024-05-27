import os
import re
from datasets import load_dataset
from asr_whisper import convert_mp3_to_wav, list_all_files_in_directory, setup_whisper_model

mp3_directory_path = '/home/jfarr/workspace/podcast_tools/podcast_tools/podcast_episodes/mp3'
wav_directory_path = '/home/jfarr/workspace/podcast_tools/podcast_tools/podcast_episodes/wav'
text_directory_path = '/home/jfarr/workspace/podcast_tools/podcast_tools/podcast_episodes/text'
mp3_file_paths = list_all_files_in_directory(mp3_directory_path)

# pattern = re.compile(r'^episode-(\d{3})-\d+-(.+)\.mp3$')

# # Loop through all files in the directory
# for filename in os.listdir(mp3_directory_path):
#     # Match the pattern
#     match = pattern.match(filename)
#     if match:
#         # Extract the padded episode number and the rest of the filename
#         episode_number = match.group(1)
#         rest_of_filename = match.group(2)
#         # Construct the new filename
#         new_filename = f'episode-{episode_number}-{rest_of_filename}.mp3'
#         # Get the full paths
#         old_file = os.path.join(mp3_directory_path, filename)
#         new_file = os.path.join(mp3_directory_path, new_filename)
#         # Rename the file
#         os.rename(old_file, new_file)
#         print(f'Renamed: {old_file} to {new_file}')

# for mp3_file in os.listdir(mp3_directory_path):
#     wav_file_name = os.path.splitext(os.path.basename(mp3_file))[0] + '.wav'
#     wav_file_path = os.path.join(wav_directory_path, wav_file_name)

#     convert_mp3_to_wav(mp3_file, wav_file_path)


wav_file_paths = list_all_files_in_directory(wav_directory_path)
pipe = setup_whisper_model()
print(f"returned pipe: {pipe}")

# dataset = load_dataset("distil-whisper/librispeech_long", "default", split="validation")
# sample = dataset[0]["audio"]
# result = pipe(sample)
# print(result["text"])

for wav_file in wav_file_paths:
    transcription_name = os.path.splitext(os.path.basename(wav_file))[0] +'.txt'
    transcription_path = os.path.join(text_directory_path, transcription_name)
    
    result = pipe(wav_file, generate_kwargs={"language" : "english"})
    with open (transcription_path, "w") as f:
        print(f"writing to {transcription_path}")
        f.write(result["text"])


    