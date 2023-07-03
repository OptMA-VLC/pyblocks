A simulation block is a python class that inherits from  BaseBlock.  It implements code that is called during the simulation in the `run(self)` method.  It communicates with other blocks through input and output ports and can receive user defined values through parameters.

### Block Library

The block library is the set of directories containing block implementations known to the simulator. To create a block, one must create a directory inside the block library containing a python file named `block.py`:

```
block_library_root
├─ block_1
│  ├─ block.py  # must define a class implementing BaseBlock  
│  └─ ...       # you can create other files and directories
├─ block_2
│  └─ ...
.
```

### Block Class

- Class structure

### Initializer

- do: declare block properties
- don't: run stuff

### Running

- run method
- error handling

### Special Signals

- time series
- multisignal




