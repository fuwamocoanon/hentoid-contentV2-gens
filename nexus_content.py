import os
import json
import datetime

def get_image_files(book_folder):
    image_files = []
    supported_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
    
    try:
        for order, filename in enumerate(sorted(os.listdir(book_folder)), start=1):
            file_extension = filename.split('.')[-1].lower()
            if file_extension in supported_extensions:
                file_name_without_extension = os.path.splitext(filename)[0]
                mime_type = f"image/{file_extension}"
                # Dummy URL with page number appended at the end
                image_file = {
                    "chapterOrder": -1,  # Placeholder for chapter data
                    "favourite": False,
                    "isCover": (order == 1),  # First image is considered the cover
                    "isRead": False,
                    "isTransformed": False,  # Assuming not transformed
                    "mimeType": mime_type,
                    "name": file_name_without_extension,  # Removed file extension
                    "order": order,
                    "pHash": 0,  # Placeholder for perceptual hash
                    "pageUrl": "",
                    "status": "DOWNLOADED",
                    "url": f"https://dummyimage.com/{order}"  # Dummy URL with page number
                }
                image_files.append(image_file)
    except Exception as e:
        print(f"Error processing images in folder '{book_folder}': {e}")
    
    return image_files

def convert_info_to_contentV2(info_file, book_folder, output_file):
    # Debug to check which folder is being processed
    print(f"Processing folder: {book_folder}")

    try:
        # Read info.json with UTF-8 encoding
        with open(info_file, 'r', encoding='utf-8') as f:
            info_data = json.load(f)

        # Process image files from the book folder
        image_files = get_image_files(book_folder)

        # Debug to show how many image files are found
        print(f"Found {len(image_files)} image files in {book_folder}")

        # Construct attributes section based on available data
        attributes = {
        "ARTIST": [{"name": info_data.get("Artist", ""), "type": "ARTIST", "url": f"/artist/{info_data.get('Artist', '').replace(' ', '-').lower()}/"}] if "Artist" in info_data else [],
        "LANGUAGE": [{"name": "english", "type": "LANGUAGE", "url": "/language/english/"}],
        "CATEGORY": [{"name": "doujinshi", "type": "CATEGORY", "url": "/category/doujinshi/"}],
        "TAG": [{"name": tag, "type": "TAG", "url": f"/tag/{tag.replace(' ', '-').lower()}/"} for tag in info_data.get("Tags", [])],
        "SERIE": [{"name": info_data.get("Parody", ""), "type": "SERIE", "url": f"/parody/{info_data.get('Parody', '').replace(' ', '-').lower()}/"}] if "Parody" in info_data else [],
        "CHARACTER": []  # Assuming no characters available in info.json
        }

        # Construct contentV2 format
        contentV2_data = {
            "attributes": attributes,
            "bookPreferences": {},
            "chapters": [],  # Assuming no chapter data available in info.json
            "completed": False,
            "coverImageUrl": image_files[0]["url"] if image_files else "",  # First image as cover
            "downloadCompletionDate": int(datetime.datetime.now().timestamp() * 1000),
            "downloadDate": int(datetime.datetime.now().timestamp() * 1000),
            "downloadMode": 0,
            "errorRecords": [],
            "favourite": False,  # Placeholder, no favourites in info.json
            "groups": [{"name": group} for group in info_data.get("Groups", [])],
            "imageFiles": image_files,  # Processed image files
            "isFrozen": False,
            "lastReadDate": 0,
            "lastReadPageIndex": 0,
            "manuallyMerged": False,
            "qtyPages": info_data.get("Pages", len(image_files)),
            "rating": 0,  # Default to 0 regardless of input
            "reads": 0,  # Placeholder, no read count in info.json
            "site": "NEXUS",  # Updated site to NEXUS
            "status": "DOWNLOADED",
            "title": info_data.get("Title", ""),
            "uploadDate": int(datetime.datetime.now().timestamp() * 1000),
            "url": info_data.get("Source", "https://google.com")  # Correct URL field
        }

        # Write the converted data to contentV2.json format
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(contentV2_data, f, indent=4)

        print(f"Conversion successful for {book_folder}")

    except Exception as e:
        print(f"Error processing folder '{book_folder}': {e}")

def process_folders(root_folder):
    # Recursively search for info.json in all subfolders
    for dirpath, _, filenames in os.walk(root_folder):
        if 'info.json' in filenames:
            info_file_path = os.path.join(dirpath, 'info.json')
            output_file_path = os.path.join(dirpath, 'contentV2.json')  # Save output in the same folder
            print(f"Processing info.json in folder: {dirpath}")
            convert_info_to_contentV2(info_file_path, dirpath, output_file_path)

# Main execution
if __name__ == "__main__":
    root_folder = os.path.abspath('.')  # Use current directory if root folder is set to "./" or "."
    process_folders(root_folder)
