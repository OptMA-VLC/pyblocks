# pyblocks-sim

Pyblocks is a simulator designed to integrate python code and scientific simulation software using a blocks diagram approach.

Blocks are python files that implement arbitrary code and that communicate with other blocks with input and output ports.

Simulations are specified through a project file that determine which blocks are to be used and their connections.

## Installation

For now, only running from code is supported by pyblocks-sim

Clone this repository and run ./src/pyblock_sim/main.py

## Documentation

Tutorials can be found at [/docs/tutorials](./docs/tutorials).

## Repository Organization

```
my_block
├─ docs  => Documentation 
|  └─ tutorials => Tutorials
├─ pyinstaller-build  => Proof-of-concept of packaging using pyinstaller
└─ src
   ├─ pyblock_sim  => Simulator source code
   ├─ pyblock  => Definition of BaseBlock and related classes
   ├─ block_library  => Block implementations
   ├─ tutorials  => Source code for the tutorials
   └─ experiments  => folder for experiments at OptMA Lab. should be removed from release
```

The simulator code (src/pyblock_sim) depends on pyblock which defines the interface of a block (that is, pyblock_sim imports from pyblock). pyblock is a separate module because it should be possible to depend only on this interface to write a third-party-block. The blocks in block_library depend on pyblock for this reason.

The simulator code (pyblock_sim) and the block implementations (block_library) do not and shall not depend on each other. The simulator discovers the block implementations at runtime by knowing the path to block_library.

## Troubleshooting

### No module named distutils.cmd

On linux + PyCharm package installation might fail with:
```
from distutils.cmd import Command as DistutilsCommand
ModuleNotFoundError: No module named 'distutils.cmd'
```

You need to install python3-distutils in your system:
```sudo apt install python3-distutils```
