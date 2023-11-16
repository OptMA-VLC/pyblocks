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

### Implementing a Block

See the example in [Tutorial 2](./tutorials/2_calculator/tutorial_2_calculator.md).

### Q & A

**Q: What should be in the initializer?**

**A**: Only declare the inputs, outputs and parameters. You may declare / initialize variables used by your code but the initializer should run quickly, because the simulator needs to run it before the simulation to discover the inputs, outputs and parameters this block declares. For example, if you need to open a file, it's best to do it at the beginning of `run` rather than at `__init__`.


**Q: How to handle errors?**

**A**: If your block throws an exception in the `run` method, the simulator will catch it and append to the simulation logs. So just throw an exception. Be helpful to your user and create the exception with a message that points to the cause of the error or to the probable solution.


**Q: Are the inputs, outputs and parameters type checked?**

**A**: Sadly, no. It would be ideal but the Python type system is a mess. So you will have to double-check the types and raise InputError yourself at the beginning of your `run` function.


**Q: What are the supported parameter types?**

**A**: The parameters are parsed from a json file, so you can expect the mapping between JSON and Python types from the builtin JSON parser. This means that it is possible to receive "objects" as a parameter in the sense that the JSON object described by the user as a parameter value will be parsed as a Dict and relayed to the block.



