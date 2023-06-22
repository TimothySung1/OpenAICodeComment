import os
import code_interpret


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

def main():
    path = os.getcwd()
    parent_directory, new_directory_name = os.path.split(path)
    new_directory_name += ' - CodeCommented'
    new_directory_path = path + "\\" + new_directory_name

    # if copy directory already made, return
    if os.path.exists(new_directory_path):
        return

    os.makedirs(new_directory_path)
    
    # get content in current folder
    files_and_subdirectories = get_files_and_subdirectories(new_directory_name)

    # copy content into copy directory
    copy_content(files_and_subdirectories, new_directory_path)



def get_files_and_subdirectories(new_directory_name):
    return [item_name for item_name in os.listdir(os.getcwd()) if is_valid_content(item_name, new_directory_name)]

def is_valid_content(content, new_directory_name):
    if content[-3:] == '.py':
        return True
    if os.path.isdir(os.path.join(os.getcwd(), content)) and content != new_directory_name and content != '.git':
        return True
    return False

def copy_content(file_directory_names, destination):
    for content in file_directory_names:
        if os.path.isfile(content):
            # create new copied file, write to it with added comments

            commented_file_text = get_copy(content)
            
            # create copied file in directory
            with open(destination + "\\" + content, "w") as new_file:
                new_file.write(commented_file_text)
            
        elif os.path.isdir(content):
            # create new copied subdirectory, call itself
            new_subdirectory = content + ' - CodeCommentedSub'
            os.mkdir(new_subdirectory)

            files_and_subdirectories = get_files_and_subdirectories(new_subdirectory)
            copy_content(files_and_subdirectories, os.getcwd() + "\\" + new_subdirectory)

def get_copy(content_name):
    lines = []
    with open(content_name, "r") as content_file:
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
                docstrings = code_interpret.get_function_docstrings(function_text)
                # print("docstrings -\n" + docstrings)
                # print("body -\n" + ''.join(body))

                lines.append(line)
                lines.append(' ' * initial_indent + docstrings + "\n")
                lines.append(' ' * initial_indent + ''.join(body))
            else:
                # print("line -\n" + line)
                lines.append(line)
    commented_file_text = ''.join(lines)
    # print("FINAL PRODUCT: ")

    return commented_file_text

if __name__ == "__main__":
    main()
