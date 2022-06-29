# group_parser
To use the parser, you need to close all current Google Chrome windows.

## Example of run

```python main.py --profile_path 'C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data' --storage json```


## Args
```--profile_path``` - you need to pass the path to the file with your browser session.

Example: ```'C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data'```

```--storage``` - the program allows you to save data to a MongoDB database or to a JSON file.

For specify saver use this args: *'mongo'* or *'json'*

## Install browser driver
Due to the fact that the parser is specialized for Chrome, download chromedriver.exe and place it at the root of the project.
Check the version of your browser before installing the driver (the version of the driver and the browser must match)

[chromedriver.zip](https://chromedriver.storage.googleapis.com/index.html)

## Vk group's link
```python
config['GROUP_LINK'] 
```

You can use ```config['GROUP_LINK']``` to specify a reference to the group.

You can specify a link to the group in the file ```.env``` specifying ```GROUP_LINK```.


Please rename ```.env_template``` to ```.env``` with your correct link to the group
