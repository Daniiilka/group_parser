# group_parser
To use the parser, you need to close all current Google Chrome windows.



## install selenium
```python
pip install selenium
```
## Args
As arguments to the program, you need to pass the path to the file with your browser session.

Example:

*C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data*

The program allows you to save data to a MongoDB database or to a JSON file.

## Install browser driver
Due to the fact that the parser is specialized for Chrome, download chromedriver.exe and place it at the root of the project.

[chromedriver.zip (version 102)](https://chromedriver.storage.googleapis.com/index.html?path=102.0.5005.61/)

## Vk group's link
```python
config['GROUP_LINK'] 
```

You can use config['GROUP_LINK'] to specify a reference to the group.

Or you can specify a link to the group in the file .env specifying GROUP_LINK.
