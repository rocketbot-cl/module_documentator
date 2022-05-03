# Module documentator

Generates documentation for a Rocketbot module.

This script assume that the package module has description field in all attributes.

### Usage:

```
documentator.py [--module, -m] [--readme, -r] [--lang, -l] [--help, -h] <module>
```

### Options:

```
        -h --help     Show this screen.
        --version, -v     Show version.
        --manual, -m      Generate documentation for a module.
        --readme, -r      Generate readme for a module.
        --lang, -l        Language of the documentation.
```

### Examples:

`documentator.py -a -m -l en /home/user/Rocketbot/modules/advancedExcel `

`documentator.py`

This file can also be imported as a module and contains the following classes:

- **Documentator**: Generates documentation for a Rocketbot module.
- **Package**: Class that represent the package file of a module.
- **Module**: Class with funtion related with a module.
