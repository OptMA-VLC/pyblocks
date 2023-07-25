# Commands

## Block Help

This command will make the simulator print a help text for the block

#### Example Usage:
```json
{
  "command": "block_help",
  "parameters": [
    {
      "param_id": "distribution_id",
      "value": "com.pyblocks.integrations.ltspice"
    }
  ]
},
```
- - - 

## Simulate

Runs a simulation on the block diagram described in the `blocks` and `connections` sections.
This command must be run before other commands that operate on signals (ex: `plot`, `save`) are called.

#### Example Usage:
```json
{
"command": "simulate"
}
```
- - - 

## Plot

TODO

- - -

## Save

TODO

