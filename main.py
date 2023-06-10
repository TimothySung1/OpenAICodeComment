import openai
import os

"""
App to select a folder in which to code comment all python files in its subdirectories and to create documentation for it.
"""

# Create a copied directory of the current directory
# Loop through all files and directories in the current directory
# if it is a file, create a copy of it in the copied directory
# turn the file into a string and ask chatgpt to create code comments
#       Method 1: give chat gpt the whole file and just ask (slow, long, but could be better)
#       Method 2: calculate where functions/classes begin/end and give chatgpt those functions in chunks (faster)
# if it is a directory, copy it inside of the copied directory and repeat steps above.

# print(os.getcwd())
# print(os.path.dirname(os.getcwd()))
# print(os.path.split(os.getcwd()))

def main():
    path = os.getcwd()
    parent_directory, new_directory_name = os.path.split(path)
    new_directory_name += ' - CodeCommented'
    new_directory_path = path + "\\" + new_directory_name
    print(new_directory_path)

    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
    else:
        print("Delete folder", new_directory_name, "in order to complete the application")
        # return
        

    files_and_subdirectories = [item_name for item_name in os.listdir(path) if item_name != new_directory_name]
    print(files_and_subdirectories)

def get_comments(file_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": ""}
        ]
    )




if __name__ == "__main__":
    main()