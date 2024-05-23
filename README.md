# Podcast Tools
## The goal of this project is to create a tool that does 4 functions:
1. Scrapes a website containing hundreds of podcast files (mp3) and downloads them to our directory for future use. It should scan the website but only download new files or files it doesn't have in its directory
2. Passes the audio through an ASR to create a transcription file for each episode
3. Use an LLM to read in each individual transcript and produce a brief summary of the podcast episode
4. Create a RAG LLM chatbot to be able to take questions and draw on the transcriptions to answer questions as well as direct users to listen to individual episodes
