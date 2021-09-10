
# Module Documentator
  
Module documentator is a script to create module documentation. Create the README.md in the root and Manual_module.md in the docs folder

## How to install
  
Clone this repository run the file documentator.py

## How to use this module

Run the code and select the module folder
  
To use this script, you need to have the following parameters in the package.json
- type: can be 'module', 'addon', etc.
- Each input must have the description field
- If you have add a banner in the manual, it's necessary to have a img folder in the docs folder. The name of banner must be "Banner_modulename.jpg"

In the manual file, it's necessary to change the 'How to use' description. Automatically add a lorem ipsum

### OS

- windows
- mac
- linux
- docker

### Dependencies
- [**mdutils**](https://pypi.org/project/mdutils/)