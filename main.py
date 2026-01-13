#!/usr/bin/env python3
"""
Random Roll Flow Launcher Plugin

A plugin that generates random numbers or yes/no answers.
Usage:
- roll: Random yes/no answer
- roll N: Random number from 1 to N
- roll A B: Random number from A to B (inclusive)
"""

import json
import sys
import os
import random
from pathlib import Path

class RandomRollPlugin:
    def __init__(self):
        self.plugin_dir = Path(__file__).parent
        self.settings_file = self.plugin_dir / "settings.json"
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from settings.json"""
        default_settings = {
            "Default Roll Type": "Number",
            "default_from": 1,
            "default_to": 6,
            "yes_label": "Yes",
            "no_label": "No"
        }

        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

        return default_settings

    def save_settings(self):
        """Save settings to settings.json"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def handle_query(self, query):
        """Handle a query from Flow Launcher"""
        parts = query.strip().split()

        if not parts:
            # No arguments: use default roll type
            roll_type = self.settings.get("Default Roll Type", "Number")
            if roll_type == "Yes/No":
                return self.roll_yes_no()
            else:
                # Default to Number roll with configured from/to values
                from_val = int(self.settings.get("default_from", 1))
                to_val = int(self.settings.get("default_to", 6))
                return self.roll_range(from_val, to_val)

        if len(parts) == 1:
            # One argument: roll from 1 to N
            try:
                to_val = int(parts[0])
                return self.roll_range(1, to_val)
            except ValueError:
                return self.show_usage("Invalid number. Expected integer.")

        if len(parts) == 2:
            # Two arguments: roll from A to B
            try:
                a_val = int(parts[0])
                b_val = int(parts[1])
                return self.roll_range(a_val, b_val)
            except ValueError:
                return self.show_usage("Invalid numbers. Expected two integers.")

        # Too many arguments
        return self.show_usage("Too many arguments. Use 'roll', 'roll N', or 'roll A B'.")

    def roll_yes_no(self):
        """Generate a random yes/no result"""
        result = random.choice([True, False])
        title = self.settings["yes_label"] if result else self.settings["no_label"]
        subtitle = "Random yes/no answer"

        return [{
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": "icon.png",
            "JsonRPCAction": {
                "method": "copy_to_clipboard",
                "parameters": [title]
            }
        }]

    def roll_range(self, from_val, to_val):
        """Generate a random number in the given range"""
        # Ensure from <= to
        start = min(from_val, to_val)
        end = max(from_val, to_val)

        # Safety check: prevent extremely large ranges
        if abs(end - start) > 10_000_000:
            return self.show_usage("Range too large. Maximum range size is 10,000,000.")

        try:
            result = random.randint(start, end)
            title = str(result)
            subtitle = f"Random number between {start} and {end}"

            return [{
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath": "icon.png",
                "JsonRPCAction": {
                    "method": "copy_to_clipboard",
                    "parameters": [title]
                }
            }]
        except (ValueError, OverflowError):
            return self.show_usage("Invalid range values.")

    def show_usage(self, error_msg=None):
        """Show usage instructions"""
        title = "Random Roll Usage"
        subtitle_parts = [
            "* roll: Random yes/no",
            "* roll N: Random number 1 to N",
            "* roll A B: Random number A to B"
        ]

        if error_msg:
            subtitle = f"{error_msg}\n\n" + "\n".join(subtitle_parts)
        else:
            subtitle = "\n".join(subtitle_parts)

        return [{
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": "icon.png"
        }]

def main():
    """Main entry point for the plugin"""
    plugin = RandomRollPlugin()

    # Flow Launcher passes the JSON-RPC request via sys.argv[1]
    # not through stdin like traditional JSON-RPC
    if len(sys.argv) > 1:
        try:
            request = json.loads(sys.argv[1])
            method = request.get("method", "")
            parameters = request.get("parameters", [])

            if method == "query":
                query = parameters[0] if parameters else ""
                results = plugin.handle_query(query)
                response = {"result": results}
            else:
                response = {"error": f"Unknown method: {method}"}

            # Send response to stdout
            print(json.dumps(response, ensure_ascii=False))

        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"Invalid JSON request: {str(e)}"}))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
    else:
        # No arguments provided
        print(json.dumps({"error": "No JSON-RPC request provided"}))


if __name__ == "__main__":
    main()