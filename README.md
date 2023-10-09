# Automatic Code Commenting with OpenAI

This simple python program can automatically create python docstrings for any python file.
This goes through an entire directory (including subdirectories) and creates AI generated docstrings for all functions and methods.
To handle rate limits of 3 requests per minute (for free trials), the program is somewhat slow (but it still works, so please be patient)

It then creates documentation using Sphinx autodoc and build.

Some future features:
- Create comments for Java (javadocs) and other languages

## Note:
### Required packages/dependencies: openai, python-decouple, sphinx
### The program requires the absolute path of the directory that you want to comment
