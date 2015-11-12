# Toss File
Sublime Text plugin for copying the current file to new location(s)

The general idea is if you invoke the toss file command against the current working file and the file path STARTS WITH with any of the path keys listed in the settings file, the path key is replaced with the corresponding destination value and the file is copied to that location. See below for more in depth information

# Install
Using [Package Control](http://wbond.net/sublime_packages/package_control):

1. In Sublime Text press `Ctrl+Shift+P` or `Cmd+Shift+P`
2. Type `install`, select `Package Control: Install Package`
3. Find `Toss File` and install

Manual install

1. Download the [latest release](https://github.com/jbaranski/TossFile/releases) using the link above
2. Extract the zip into a folder
3. Copy the folder to `<SUBLIME_TEXT_HOME>/Data/Packages/`

After install add some paths to your settings (see below) and now you're ready to go.

# Settings
NOTE: It's better to ALWAYS use a trailing slash to end the path source / destination you list

*nix
```
"paths": [
    {
        "/home/source1/": "/home/destination1/"
    },
    {
        "/home/source2/": "/home/destination2/"
    }
]
```
Windows
```
"paths": [
    {
        "C:\\home\\source1\\": "C:\\home\\destination1\\"
    },
    {
        "C:\\home\\source2\\": "C:\\home\\destination2\\"
    }
]

# Usage
The plugin can be invoked via a right click context menu in the current file
The plugin can be invoked pressing `Ctrl+Shift+P` and running the `Toss File` command

# Example Scenarios
Example 1 (assume you are using the settings listed above):

1. Run the toss file command against a file, for example `/home/source1/my/special/file/file.txt`
2. The file is copied to `/home/destination1/my/special/file/file.txt`
3. If the directory at step 2 doesn't already exist, it will be created

Example 2 (assume you are using the settings listed above):

1. Run the toss file command against a file, for example `/home/source77/my/special/file/file.txt`
2. No matches found, nothing happens