import os
import code_interpret

APPENDED_NAME = ' - commented'
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

# print(os.getcwd()) # C:\Users\tsung\Desktop\Projects\OpenAIProjects\AICodeCommentDocument
# print(os.path.dirname(os.getcwd())) # C:\Users\tsung\Desktop\Projects\OpenAIProjects
# print(os.path.split(os.getcwd())) # ('C:\\Users\\tsung\\Desktop\\Projects\\OpenAIProjects', 'AICodeCommentDocument')

# TODO: Put source and output directories as requirement
# this would remove unneccessary conditions in is_valid_content function

def main():
    path = os.getcwd()
    parent_directory, new_directory_name = os.path.split(path)
    new_directory_name += APPENDED_NAME
    new_directory_path = path + "\\" + new_directory_name

    # if copy directory already made, return
    if os.path.exists(new_directory_path):
        return

    os.makedirs(new_directory_path)

    # copy content into copy directory
    copy_content(path, new_directory_path)

    # TODO: Create sphinx documentation for the commented files

def get_files_and_subdirectories(current_directory, new_directory_name):
    return [item_name for item_name in os.listdir(current_directory) if is_valid_content(item_name, current_directory, new_directory_name)]

def is_valid_content(content, current_directory, new_directory_name):
    if content[-3:] == '.py' and content != 'main.py' and content != 'code_interpret.py' and content != 'create_docs.py':
        return True
    if os.path.isdir(os.path.join(current_directory, content)) and content != new_directory_name and content != '.git' and content[-16:] != APPENDED_NAME  and content != '__pycache__':
        return True
    return False

def copy_content(path, destination):
    # print("current path: ", path)
    # print('current dest: ', destination)
    file_directory_names = get_files_and_subdirectories(path, destination)
    # print("contents: ", file_directory_names)

    # check for __init__.py, create if not exist
    if not '__init__.py' in file_directory_names:
        init = open(os.path.join(path, '__init__.py'), 'w')
        init.close()

    for content in file_directory_names:
        content_path = os.path.join(path, content)
        if os.path.isfile(content_path):
            # create new copied file, write to it with added comments

            commented_file_text = get_copy(content_path)
            
            # create copied file in directory
            with open(os.path.join(destination, content), "w") as new_file:
                new_file.write(commented_file_text)
            
        elif os.path.isdir(content_path):
            new_destination = os.path.join(destination, content)
            # create new copied subdirectory, call itself
            os.mkdir(new_destination)

            copy_content(content_path, new_destination)

def get_copy(content_path):
    lines = []
    with open(content_path, "r") as content_file:
        while True:
            line = content_file.readline()
            
            if not line:
                break

            # check if it is a method
            if line.strip()[0:3] == "def":
                # handle indent to find the end of the method, and then add the indent back to the line
                # initial indent is the indent of the function header
                initial_indent = 0
                while line[initial_indent] == ' ':
                    initial_indent += 1
                
                # body indent is the indent inside the function
                body_indent = 0
                body_line = content_file.readline()

                if not body_line:
                    raise Exception("The function does not have a body")
                
                while body_line[initial_indent + body_indent] == ' ':
                    body_indent += 1

                if not body_indent:
                    raise Exception("The function does not have a body")
                
                body = []
                while body_line[:initial_indent + body_indent] == ' ' * (initial_indent + body_indent):
                    body.append(body_line[initial_indent:]) # only append the body with relative indent to function header
                    body_line = content_file.readline()

                function_text = line.strip() + "\n" + ''.join(body)
                # print(function_text)
                docstrings = code_interpret.get_function_docstrings(function_text)
                
                # print("docstrings -\n" + docstrings)
                # print("body -\n" + ''.join(body))

                lines.append(line)
                lines.append(' ' * (initial_indent + body_indent) + ('\n' + ' ' * (initial_indent + body_indent)).join(docstrings.split("\n")) + "\n")
                lines.append(' ' * (initial_indent) + ''.join(body) + "\n")
            else:
                # print("line -\n" + line)
                lines.append(line)
    commented_file_text = ''.join(lines)
    # print("FINAL PRODUCT: ")

    return commented_file_text

if __name__ == "__main__":
    main()
