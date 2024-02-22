import os
import requests


def download_video(avatar_url):
    # save the video locally
    local_filename = download_file(avatar_url, os.getcwd())
    print(f'{local_filename} downloaded.')
    return local_filename

# Helper functions

def download_file(url, local_path):
    """
    Download a file from a given URL to a local path. This function streams the file from the URL and writes it in chunks to the local
    file system. This allows it to handle large files that might not fit in memory.

    Parameters:
    url (str): The URL of the file to download.
    local_path (str): The local path where the file should be saved.

    Returns:
    str: The local path to the downloaded file.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        print("URL: ", url)

        # Extract filename from URL
        filename = url.split("/")[-1].split("?")[0]

        print("Filename: ", filename)

        local_filename = os.path.join(local_path, filename)
        
        print("Local filename: ", local_filename)

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)

    return local_filename