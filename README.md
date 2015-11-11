# Toss File
Sublime Text plugin for copying the current file to a new location

```
"paths": [
    {
        "/home/source1": "/home/destination1"
    },
    {
        "/home/source2": "/home/destination2"
    }
]
```

# Use Cases
Example 1 (assume you are using the settings listed above):

1. Run the toss file command against a file, for example `/home/source1/my/special/file/file.txt`
2. The file is copied to `/home/destination1/my/special/file/file.txt`
3. If the directory at step 2 doesn't already exist, it will be created

Example 2 (assume you are using the settings listed above):

1. Run the toss file command against a file, for example `/home/source77/my/special/file/file.txt`
2. No matches found, nothing happens