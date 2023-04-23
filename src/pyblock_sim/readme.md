# Pyblocks-sim

Pyblocks is a simulator designed to integrate python code and scientific simulation software using a blocks diagram approach.

Python code can be written as blocks by using the BaseBlock class. The simulation user can writhe a project file (in JSON format) that describes which blocks are used in a simulation and how signals flow between those blocks.


# Writing a project file

In this tutorial, we will assemble the following simulation:

>> TODO: add image

Project files are JSON files that are composed of three sections: blocks, connections and commands.

```JSON
{
  "blocks": [ ... ],
  "connections": [ ... ],
  "commands": [ ... ]
}
```

### Blocks

The blocks section specifies which blocks take part in a simulation. Each block has the following fields:

```JSON
{
  "instance_of": "com.pyblocks.example.string_source",
  "instance_id": "string_source",
  "parameters": [
    {
      "param_id": "value", "value": "Hello World!"
    }
  ]
}
```

- `instance_of` contains the **distribution id** of the block. This is a unique identifier 
  for a block in your block library and tells the simulator which block you want to use.
- `instance_id` is an id that names that specific instance of the block in your simulation.
- `parametes` is a list that lets you configure the block

A simulation can have multiple instances of the same block type. If we 
had two string source blocks in our simulations, both would have the 
**distribution id** `com.pyblocks.example.string_source` but their **instance_id**'s
might be `string_source_1` and `string_source_2`. Writing a simulation 
file that has two blocks with the same instance_id is an error.

The parameter list depends on the block implementation. The string generator block in our
example takes one parameter (`value`) that will be copied to the output.

### Connections

This section specifies how the blocks are connected. It is only possible to
connect an output to an input. Cyclical connections are not supported if we have a diagram
with three blocks connected as such:

```
A -> B -> C
```

Connecting block C to block A would be an error because the simulator would not know where
to start the simulation.

Connections have two fields: `to` and `from`. They specify the origin and destination ports
for that connection in the format `block_instance_id::port_id` the block instance ids are
those defined in the blocks section. The port ids are defined by the block implementation.
The following snippet shows the connection from the string source to the string transform block:

```JSON
{
  "from": "string_source::output",
  "to": "string_transform::input"
}
```

### Commands

Commands allow plotting and saving signals. Currently, the only signal types that support saving
are numpy arrays (np.ndarray), the TimeSignal type defined by the simulator (which uses numpy 
arrays internally) and strings. The syntax for these commands is:

```JSON
[
  {
    "command": "plot",
    "args": {
      "signals": [
        "block_1::signal_1",
        "block_2::output"
      ],
      "save_path": "./plot_image.png"   // optional
    }
  },
  {
    "command": "save",
    "args": {
      "signals": [
        "block_1::signal_1",
        "block_2::output"
      ],
      "save_path": "./save_path.csv"
    }
  }
]
```

### Putting It All Together

The project file for our example then becomes:

```JSON
{
  "blocks": [
    {
      "instance_of": "com.pyblocks.example.string_source",
      "instance_id": "string_source",
      "parameters": [
        {
          "param_id": "value",
          "value": "Hello World!"
        }
      ]
    },
    {
      "instance_of": "com.pyblocks.example.string_transform",
      "instance_id": "string_transform",
      "parameters": [
        {
          "param_id": "transform_type",
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
      "command": "save",
      "args": {
        "signals": ["string_transform::output"],
        "save_path": "./output.txt"
      }
    }
  ]
}
```

Running the example should produce the file `output.txt` (in the same directory as your `project.json`):

```text
HELLO WORLD!
```

# Writing a Block