import json
import os
import datetime

def get_image_files(book_folder):
    image_files = []
    supported_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']  # Supported image extensions

    for order, filename in enumerate(sorted(os.listdir(book_folder)), start=1):
        file_extension = filename.split('.')[-1].lower()
        if file_extension in supported_extensions:
            file_name_without_extension = os.path.splitext(filename)[0]
            mime_type = f"image/{file_extension}"
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
                "url": f"https://dummyimage.com/{file_name_without_extension}.{file_extension}"  # Dummy URL
            }
            image_files.append(image_file)
    
    return image_files

def convert_info_to_contentV2(info_file, book_folder, output_file):
    # Read info.json
    with open(info_file, 'r') as f:
        info_data = json.load(f)
    
    # Process image files from the book folder
    image_files = get_image_files(book_folder)
    
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
        "coverImageUrl": image_files[0]["url"] if image_files else "https://google.com",  # Dummy URL if no image is present
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
        "site": "NEXUS",  # Changed site to NEXUS
        "status": "DOWNLOADED",
        "title": info_data.get("Title", ""),
        "uploadDate": int(datetime.datetime.now().timestamp() * 1000),
        "url": info_data.get("Source", "https://google.com")  # Use https://google.com if no URL is provided
    }
    
    # Write the converted data to contentV2.json format
    with open(output_file, 'w') as f:
        json.dump(contentV2_data, f, indent=4)

    print(f"Conversion complete! Data saved to {output_file}")

def process_folders(root_folder):
    # Recursively search for info.json in all subfolders
    for dirpath, _, filenames in os.walk(root_folder):
        if 'info.json' in filenames:
            info_file_path = os.path.join(dirpath, 'info.json')
            output_file_path = os.path.join(dirpath, 'converted_contentV2.json')  # Save output in the same folder
            print(f"Processing {info_file_path}")
            convert_info_to_contentV2(info_file_path, dirpath, output_file_path)

# Main execution
if __name__ == "__main__":
    root_folder = os.path.abspath('.')  # Use current directory if root folder is set to "./" or "."
    process_folders(root_folder)
