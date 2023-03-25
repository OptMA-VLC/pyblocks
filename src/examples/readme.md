# Writing Project Files

## General Structure

```json
{
  "blocks": [
    { /* block 1 */ },
    { /* block 2 */ },
    /* ... */
  ],
  "connections": [
    { /* connection 1 */ },
    /* ... */
  ]
}
```

## Blocks

To describe a block, we must be familiar with these concepts:

* Distribution ID &rarr; This is a string that identifies a specific block type. It has the format 'com.organization.block_name' and must match the distribution ID of a block in your library.
* Instance ID &rarr; This is a string that identifies a block in your simulation. For example, a simulation may use two signal generators, both with distribution ID 'com.pyblocks.signal_generator' but the first _instance_ has an instance id 'my_signal_gen_1' and the second 'my_signal_gen_2'
* Name &rarr; This is the user-friendly name of that block instance. In the previous example, the names could be 'Signal Generator 1' and 'Signal Generator 2'

### Block Parameters

## Connections