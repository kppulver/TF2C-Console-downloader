import os
import re
import requests
import bz2
from glob import glob

# Base TF2C mod folder
mod_dir = r'C:\Program Files (x86)\Steam\steamapps\sourcemods\tf2classic'

# Find the latest condump###.txt file
def get_latest_condump():
    pattern = os.path.join(mod_dir, 'condump*.txt')
    condump_files = glob(pattern)
    if not condump_files:
        raise FileNotFoundError("No condump files found.")

    # Sort by modification time, descending
    condump_files.sort(key=os.path.getmtime, reverse=True)
    return condump_files[0]

# Base tf2classic download folder
base_dir = os.path.join(mod_dir, 'download')

# Valid first-level folders
valid_subdirs = {'maps', 'materials', 'models', 'particles', 'sound'}

# Regex to extract only .bz2 URLs
url_pattern = re.compile(r'http[s]?://[^\s"]+\.bz2')

# Track already-seen URLs
seen_urls = set()

# Get the latest condump file
input_file = get_latest_condump()
print(f"📄 Using input file: {input_file}")

with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
    for line in f:
        match = url_pattern.search(line)
        if not match:
            continue

        url = match.group(0)
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Extract subpath after 'tf2classic/'
        path_split = re.split(r'tf2classic[\\/]', url, maxsplit=1)
        if len(path_split) < 2:
            print(f"⚠️ Skipping URL (missing 'tf2classic/'): {url}")
            continue

        relative_path = path_split[1].replace('/', os.sep).replace('\\', os.sep)
        parts = relative_path.split(os.sep)

        if parts[0] not in valid_subdirs:
            print(f"⚠️ Skipping (invalid subfolder): {url}")
            continue

        target_folder = os.path.join(base_dir, *parts[:-1])
        filename_bz2 = parts[-1]
        filename_extracted = filename_bz2[:-4]  # remove .bz2

        target_bz2 = os.path.join(target_folder, filename_bz2)
        target_extracted = os.path.join(target_folder, filename_extracted)

        if os.path.exists(target_extracted):
            print(f"✅ Already exists: {target_extracted}")
            continue

        os.makedirs(target_folder, exist_ok=True)

        print(f"⬇️ Downloading: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(target_bz2, 'wb') as f_out:
                f_out.write(response.content)

            with bz2.open(target_bz2, 'rb') as f_in, open(target_extracted, 'wb') as f_out:
                f_out.write(f_in.read())

            os.remove(target_bz2)
            print(f"✅ Extracted to: {target_extracted}")

        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
