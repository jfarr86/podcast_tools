import os
import requests
from bs4 import BeautifulSoup

def download_file(url, folder_path):
    local_filename = url.split("/")[-1]
    local_filepath = os.path.join(folder_path, local_filename)
    
    # Check if the file already exists
    if os.path.exists(local_filepath):
        print(f"File {local_filename} already exists. Skipping download.")
        return local_filepath
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    print(f"Downloaded {url}")
    return local_filepath

def download_podcast_episodes(rss_feed_url, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    print(f"Fetching episodes feed: {rss_feed_url}")
    response = requests.get(rss_feed_url)
    response.raise_for_status()
    print("Fetched episodes feed successfully.")
    
    soup = BeautifulSoup(response.content, "xml")
    
    # Find all <enclosure> tags with type="audio/mpeg"
    enclosure_tags = soup.find_all("enclosure", type="audio/mpeg")
    
    for enclosure in enclosure_tags:
        href = enclosure['url']
        if href.endswith(".mp3"):
            print(f"Processing {href}...")
            download_file(href, folder_path)

if __name__ == "__main__":
    RSS_FEED_URL = "https://www.buzzsprout.com/1228499.rss"
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    FOLDER_PATH = os.path.abspath(os.path.join(current_script_dir, os.pardir, 'podcast_episodes'))
    
    print(f"Script is running from: {current_script_dir}")
    print(f"Saving episodes to: {FOLDER_PATH}")
    
    download_podcast_episodes(RSS_FEED_URL, FOLDER_PATH)
