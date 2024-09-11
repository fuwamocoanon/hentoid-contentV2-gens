import os
import re

# Regex pattern to match emojis
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

def remove_emojis_from_folder_names(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder, topdown=False):
        # Process directory names
        for dirname in dirnames:
            # Remove emojis from the folder name
            clean_dirname = re.sub(emoji_pattern, '', dirname)
            old_folder_path = os.path.join(dirpath, dirname)
            new_folder_path = os.path.join(dirpath, clean_dirname)

            # Rename the folder if the name has changed
            if clean_dirname != dirname:
                print(f"Renaming folder: {old_folder_path} -> {new_folder_path}")
                os.rename(old_folder_path, new_folder_path)

if __name__ == "__main__":
    root_folder = os.path.abspath('.')  # Start from the current directory
    remove_emojis_from_folder_names(root_folder)
