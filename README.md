# Automatic Code Commenting with OpenAI

This simple python program can automatically create python docstrings for any python file.
This goes through an entire directory (including subdirectories) and creates AI generated docstrings for all functions and methods.
To handle rate limits of 3 requests per minute, the program is somewhat slow (but it still works, so please be patient)

With the docstrings, you can use it to generate formal documentation using Sphinx.

Some future features:
- Automatically create Sphinx documentation
- Create comments for Java (javadocs) and other languages

## Note:
### The current generate docstrings python file does not work. To test the program out, copy the python files into the directory you want to comment.
### After changing the API key in the openai handler, run the main python file. The program will create a separate directory inside.
