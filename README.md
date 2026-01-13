# Random Roll Flow Launcher Plugin

A simple Flow Launcher plugin that generates random numbers, yes/no answers, or picks from custom labels.

## Installation
Installation instructions will be provided soon.

## Usage

Trigger the plugin by typing `roll` in Flow Launcher, followed by optional arguments:

### No Arguments (Default Behavior)
```
roll
```
Behavior depends on the **Default Roll Type** setting:
- **Yes/No**: Returns either "Yes" or "No" (customizable)
- **Number**: Returns a random number from configured range (default: 1-6)
- **CustomLabel**: Returns a random pick from your custom labels

### Random Number (1 to N)
```
roll 6
```
Returns a random number from 1 to 6 (inclusive).

### Random Number (A to B)
```
roll 10 20
```
Returns a random number from 10 to 20 (inclusive). Order doesn't matter - `roll 20 10` works the same.

### Custom Labels
```
roll Joe Kane John Katie
```
Returns a random pick from the provided labels (when arguments are not numbers).

## Settings

The plugin includes configurable settings that can be edited through Flow Launcher's settings interface:

- **Default Roll Type**: Choose behavior when no arguments are provided (Yes/No, Number, or CustomLabel)
- **Default From**: Default starting number for number ranges (default: 1)
- **Default To**: Default ending number for number ranges (default: 6)
- **Yes Label**: Text for positive yes/no answers (default: "Yes")
- **No Label**: Text for negative yes/no answers (default: "No")
- **Custom Labels**: Space-separated labels for random picking (default: "Joe Kane John Katie")

## Examples

```
roll               → "Yes" or "No" (or number/custom label based on settings)
roll 6             → Random number: 1, 2, 3, 4, 5, or 6
roll 1 10          → Random number between 1 and 10
roll 100 200       → Random number between 100 and 200
roll A B C D       → Random pick from: A, B, C, or D
```

## Edge Cases

- **Invalid number input**: Shows usage instructions
- **Large ranges**: Ranges larger than 10,000,000 are rejected for performance
- **Single number**: `roll N` is treated as `roll 1 N`
- **Order independence**: `roll 5 1` works the same as `roll 1 5`
- **Empty custom labels**: Shows error if custom labels are not configured

## Requirements

- Python 3.6+
- Flow Launcher

## License

This plugin is provided as-is for personal use.