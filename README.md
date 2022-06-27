# group_parser
To use the parser, you need to close all current Google Chrome windows.



## install selenium
```python
pip install selenium
```
## Args
*--profile_path* - you need to pass the path to the file with your browser session.

Example: *'C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data'*

*--storage* - the program allows you to save data to a MongoDB database or to a JSON file.

For specify saver use this args: *'mongoDB'* or *'JSON'*

## Install browser driver
Due to the fact that the parser is specialized for Chrome, download chromedriver.exe and place it at the root of the project.

[chromedriver.zip (version 102)](https://chromedriver.storage.googleapis.com/index.html?path=102.0.5005.61/)

## Vk group's link
```python
config['GROUP_LINK'] 
```

You can use config['GROUP_LINK'] to specify a reference to the group.

Or you can specify a link to the group in the file .env specifying GROUP_LINK.

Example for *.env* file: *GROUP_LINK='https://vk.com/cyberleninka'*
