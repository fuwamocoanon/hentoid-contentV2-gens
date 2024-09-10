import os
import yaml
import json
import datetime
import logging

# Set up logging to a file
log_file = os.path.join(os.path.abspath('.'), 'conversion_debug.log')

try:
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging initialized successfully.")
except Exception as e:
    print(f"Failed to initialize logging: {e}")

def get_image_files(book_folder):
    image_files = []
    supported_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']

    try:
        for order, filename in enumerate(sorted(os.listdir(book_folder)), start=1):
            file_extension = filename.split('.')[-1].lower()
            if file_extension in supported_extensions:
                file_name_without_extension = os.path.splitext(filename)[0]
                mime_type = f"image/{file_extension}"
                # Use dummy URL with page number appended at the end
                image_file = {
                    "chapterOrder": -1,
                    "favourite": False,
                    "isCover": (order == 1),
                    "isRead": False,
                    "isTransformed": False,
                    "mimeType": mime_type,
                    "name": file_name_without_extension,
                    "order": order,
                    "pHash": 0,
                    "pageUrl": "",
                    "status": "DOWNLOADED",
                    "url": f"https://dummyimage.com/{order}"  # Dummy URL with page number
                }
                image_files.append(image_file)
    except Exception as e:
        logging.error(f"Error processing images in folder '{book_folder}': {e}")

    return image_files

def convert_info_to_contentV2(info_file, book_folder, output_file):
    logging.info(f"Processing folder: {book_folder}")

    try:
        # Read info.yaml with UTF-8 encoding
        with open(info_file, 'r', encoding='utf-8') as f:
            info_data = yaml.safe_load(f)

        # Process image files from the book folder
        image_files = get_image_files(book_folder)

        logging.info(f"Found {len(image_files)} image files in {book_folder}")

        # Extract fields from YAML
        title = info_data.get("Title", "")
        artist_list = info_data.get("Artist", [])
        artist = ", ".join(artist_list)  # Join multiple artists if present
        tags = info_data.get("Tags", [])
        parody_list = info_data.get("Parody", [])
        parody = ", ".join(parody_list)

        # Construct attributes section
        attributes = {
            "ARTIST": [{"name": artist, "type": "ARTIST", "url": f"/artist/{artist.replace(' ', '-').lower()}/"}] if artist else [],
            "LANGUAGE": [{"name": "english", "type": "LANGUAGE", "url": "/language/english"}],
            "CATEGORY": [{"name": "doujinshi", "type": "CATEGORY", "url": "/category/doujinshi"}],
            "TAG": [{"name": tag, "type": "TAG", "url": f"/tag/{tag.replace(' ', '-').lower()}/"} for tag in tags],
            "SERIE": [{"name": parody, "type": "SERIE", "url": f"/parody/{parody.replace(' ', '-').lower()}/"}] if parody else [],
            "CHARACTER": []
        }

        # Construct contentV2 format
        contentV2_data = {
            "attributes": attributes,
            "bookPreferences": {},
            "chapters": [],
            "completed": False,
            "coverImageUrl": image_files[0]["url"] if image_files else "https://google.com",
            "downloadCompletionDate": int(datetime.datetime.now().timestamp() * 1000),
            "downloadDate": int(datetime.datetime.now().timestamp() * 1000),
            "downloadMode": 0,
            "errorRecords": [],
            "favourite": False,
            "groups": [],  # No group data assumed
            "imageFiles": image_files,
            "isFrozen": False,
            "lastReadDate": 0,
            "lastReadPageIndex": 0,
            "manuallyMerged": False,
            "qtyPages": info_data.get("Pages", len(image_files)),
            "rating": 0,  # Default to 0
            "reads": 0,
            "site": "ANCHIRA",  # Changed site to ANCHIRA
            "status": "DOWNLOADED",
            "title": title,
            "uploadDate": int(datetime.datetime.now().timestamp() * 1000),
            "url": info_data.get("Source", "https://google.com")  # Use default URL if not present
        }

        # Write the converted data to contentV2.json format
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(contentV2_data, f, indent=4)

        logging.info(f"Conversion successful for {book_folder}")

    except Exception as e:
        logging.error(f"Error processing folder '{book_folder}': {e}")

def process_folders(root_folder):
    # Recursively search for info.yaml in all subfolders
    for dirpath, _, filenames in os.walk(root_folder):
        if 'info.yaml' in filenames:
            info_file_path = os.path.join(dirpath, 'info.yaml')
            output_file_path = os.path.join(dirpath, 'contentV2.json')
            logging.info(f"Processing info.yaml in folder: {dirpath}")
            convert_info_to_contentV2(info_file_path, dirpath, output_file_path)

if __name__ == "__main__":
    root_folder = os.path.abspath('.')  # Use current directory if root folder is set to "./" or "."
    process_folders(root_folder)
