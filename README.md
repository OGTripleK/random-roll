# Random Roll Flow Launcher Plugin

A simple Flow Launcher plugin that generates random numbers or yes/no answers.

## Installation

1. Download or clone this repository
2. Copy the plugin files to your Flow Launcher plugins directory:
   - On Windows: `%APPDATA%\FlowLauncher\Plugins\`
   - Create a new folder for the plugin (e.g., `RandomRoll`)
3. Place all files (`plugin.json`, `randomroll.py`, `settings.json`, `icon.png`) in the plugin folder
4. Restart Flow Launcher or reload plugins

## Usage

Trigger the plugin by typing `roll` in Flow Launcher, followed by optional arguments:

### Random Yes/No
```
roll
```
Returns either "Yes" or "No" (labels can be customized in settings).

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

## Settings

The plugin includes configurable settings that can be edited through Flow Launcher's settings interface:

- **Default From**: Default starting number for ranges (default: 1)
- **Default To**: Default ending number for ranges (default: 6)
- **Yes Label**: Text for positive yes/no answers (default: "Yes")
- **No Label**: Text for negative yes/no answers (default: "No")

## Examples

```
roll          → "Yes" or "No"
roll 6        → Random number: 1, 2, 3, 4, 5, or 6
roll 1 10     → Random number between 1 and 10
roll 100 200  → Random number between 100 and 200
```

## Edge Cases

- **Invalid input**: Non-numeric arguments show usage instructions
- **Large ranges**: Ranges larger than 10,000,000 are rejected for performance
- **Single argument**: `roll N` is treated as `roll 1 N`
- **Order independence**: `roll 5 1` works the same as `roll 1 5`

## Requirements

- Python 3.6+
- Flow Launcher

## License

This plugin is provided as-is for personal use.