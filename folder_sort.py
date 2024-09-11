import os
import shutil

def sort_folders(root_folder, json_folder, yaml_folder, none_folder):
    # List of folders to skip (the destination folders)
    skip_folders = {json_folder, yaml_folder, none_folder}

    # Loop through the immediate subdirectories of root_folder
    for item in os.listdir(root_folder):
        dirpath = os.path.join(root_folder, item)
        folder_name = os.path.basename(dirpath)
        
        # Only process directories and skip the destination folders
        if not os.path.isdir(dirpath) or dirpath in skip_folders:
            continue
        
        # Delete any existing contentV2.json files
        content_v2_file = os.path.join(dirpath, 'contentV2.json')
        if os.path.exists(content_v2_file):
            print(f"Deleting '{content_v2_file}' from '{folder_name}'")
            os.remove(content_v2_file)

        # Check if the folder contains info.json or info.yaml
        filenames = os.listdir(dirpath)
        if 'info.json' in filenames:
            print(f"Moving folder '{folder_name}' to '{json_folder}' (contains info.json)")
            shutil.move(dirpath, os.path.join(json_folder, folder_name))
        elif 'info.yaml' in filenames:
            print(f"Moving folder '{folder_name}' to '{yaml_folder}' (contains info.yaml)")
            shutil.move(dirpath, os.path.join(yaml_folder, folder_name))
        else:
            print(f"Moving folder '{folder_name}' to '{none_folder}' (contains neither)")
            shutil.move(dirpath, os.path.join(none_folder, folder_name))

# Main execution
if __name__ == "__main__":
    # Set the root folder to the current directory where the script is located
    root_folder = os.path.abspath('.')  
    json_folder = os.path.join(root_folder, 'json_directory')  # Destination for folders with info.json
    yaml_folder = os.path.join(root_folder, 'yaml_directory')  # Destination for folders with info.yaml
    none_folder = os.path.join(root_folder, 'none_directory')  # Destination for folders with neither
    
    # Create destination folders if they don't exist
    os.makedirs(json_folder, exist_ok=True)
    os.makedirs(yaml_folder, exist_ok=True)
    os.makedirs(none_folder, exist_ok=True)
    
    # Start sorting
    sort_folders(root_folder, json_folder, yaml_folder, none_folder)
