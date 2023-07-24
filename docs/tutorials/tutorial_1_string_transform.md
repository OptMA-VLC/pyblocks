# Tutorial 1: String Transform

In this tutorial you will learn:
- How to configure a simulation with a project file
- Using existing blocks
- Extracting text input to a file

A simulation is described as a block diagram, where outputs of some blocks are connected to the input of others and 
data flows between them. In this tutorial, we will assemble a simulation consisting of two blocks: one will produce 
a string and the other will apply a transformation to it. The figure below represents this scenario. Connections 
between inputs and outputs are indicated by solid arrows, the solid arrow coming out of `string_transform` represents
the output value that is produced even if this output is not connected to other block. The dashed arrow represents
a user parameter being provided to the `string_transform` block.

![Block diagram for example 1](tutorial_1_string_transform.png?raw=true)

To describe a simulation scenario, we must write a file that tells the simulator what blocks will be used and
how they are connected. This file is in the JSON format and is called the project file.

### About Block Identifiers

We will assume that both our blocks (string_source and string_transform) are already implemented. To tell the simulator
which blocks are to be used, a unique "name" for that block must exist. This name is the **Distribution ID** of the
block. This is declared by the block implementation. In a simulation we may use more than one instance of the same 
block and both will have the same distribution id, we need another identifier to uniquely name the blocks used in the
simulation. This is the **Instance ID** of each instance of the block and is chosen by the user when writing the 
project file. In this example we will use the following blocks:

```
String Source
  - distribution id: "com.pyblocks.tutorials.string_source"
  - instance id: "string_source"

String Transform
   - distribution_id: "com.pyblocks.tutorials.string_transform"
   - instance_id: "string_transform"
```

The distribution IDs use the reverse-domain-name notation to avoid independent developers accidentally creating blocks
with the same ID.

### Using Blocks

Project files are JSON files composed of three sections: blocks, connections and commands. We will start by
writing the first section, which specifies the blocks to be used in this simulation and the connections section:

```JSON
// project.json
{
  "blocks": [
    {
      "distribution_id": "com.pyblocks.tutorials.string_source",
      "instance_id": "string_source"
    },
    {
      "distribution_id": "com.pyblocks.tutorials.string_transform",
      "instance_id": "string_transform"
    }
  ],
  "connections": [
    {
      "from": "string_source::output",
      "to": "string_transform::input"
    }
  ],
  "commands": [...]
}
```

Each block has the two mandatory fields `distribution_id` and `instance_id`, that correspond 
to the IDs discussed preivously.

Each connection has the `from` and `to` fields. These specify the output port of the origin
block and the input port of the destination block. The values of these fields use the 
*port selector* syntax, in the form:

`block_instance_id::port_id`

The ID of input and output ports are determined by the block implementation. Specifying 
a port that the block has not declared will result in an error when the simulator tries 
to build the simulation.

#### A Note About Cyclical Connections

```
TLDR: Connecting blocks in a cycle will raise an error when simulating.
```

Cyclical connections happen when following the connections in a diagram leads back to the same starting point.
The following diagram has a cyclical connection:

```
      ┌─────┐
      ↓     |
A ──> B ──> C
```

The simulator resolves the dependencies between block inputs and outputs. Example: A must run before B because B uses 
an output of A. When there are cyclical connections in the block diagram, there is no solution to these dependencies 
(C needs B that needs C that needs B that...). It is possible to describe a diagram with cycles in the project file
but an error will be raised when running the simulation.

### Running and Extracting Outputs

To simulate, we need to write the corresponding command to the project file:

```JSON
// project.json
{
  "commands": [
    {
      "command": "simulate"
    }
  ],
  "blocks": [...],
  "connections": [...]
}

When a block runs, its output ports are populated with results. As a user, you can view or save them 
with additional entries in the commands section of the project file. In this example we will use the 
`save` command to write the produced string to a file:

```JSON
// project.json
{
  "blocks": [...],
  "connections": [...],
  "commands": [
    {
      "command": "simulate"
    },
    {
      "command": "save",
      "parameters": [
        {
          "param_id": "signals",
          "value": ["string_transform::output"]
        },
        {
          "param_id": "save_path",
          "value": "./output.txt"
        }
      ]
    }
  ]
}
```

Each command object has the `command` field and can have the `parameters` field which
has a list of parameter objects, each having a `param_id` and a `value`. In the save
command, `signals` is a list of port selectors to select what output should be saved
and `save_path` is the directory where the data should be saved, relative to the 
path of the `project.json` file.

Running the project file at this point should produce the string `hello world!` in a 
file called `output.txt`.

### Parameters

Blocks can receive user data in the form of parameters. The available parameters are declared in the block
implementation and are provided by the user in the `blocks` section of the project file.

The string_transform block has a parameter `transform` that specifies the transformation to be applied to the
string. Its default value is `to_lower`. The following code shows the entire project.json file altered to pass
the value `to_upper` to this parameter. Running it should produce the string `HELLO WORLD!` in `output.txt`

```JSON
{
  "blocks": [
    {
      "distribution_id": "com.pyblocks.tutorials.string_source",
      "instance_id": "string_source",
    },
    {
      "distribution_id": "com.pyblocks.tutorials.string_transform",
      "instance_id": "string_transform",
      "parameters": [
        {
          "param_id": "transform",
          "value": "to_upper"
        }
      ]
    }
  ],
  "connections": [
    {
      "from": "string_source::output",
      "to": "string_transform::input"
    }
  ],
  "commands": [
    {
      "command": "simulate"
    },
    {
      "command": "save",
      "args": {
        "signals": ["string_transform::output"],
        "save_path": "./output.txt"
      }
    }
  ]
}
```
