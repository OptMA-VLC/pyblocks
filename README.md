# The Modular Electro-Optical Workbench

## Installation

The recommended IDE to develop this project is PyCharm.

Dependency management is done with a requirements.txt file.

---

## Usage

Run ```src/meow_sim/main.py```

---

## Testing

Make sure to have pytest installed. Installing the dependencies in requirements.txt will install it.

Unit tests are in ```./src/test```

---

## Troubleshooting

### No module named distutils.cmd

On linux + PyCharm package installation might fail with:
```
from distutils.cmd import Command as DistutilsCommand
ModuleNotFoundError: No module named 'distutils.cmd'
```

You need to install python3-distutils in your system:
```sudo apt install python3-distutils```
