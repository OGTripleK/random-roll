#!/usr/bin/env python3
"""
Random Roll Flow Launcher Plugin

A plugin that generates random numbers or yes/no answers.
Usage:
- rolls: Random yes/no answer
- rolls N: Random number from 1 to N
- rolls A B: Random number from A to B (inclusive)
"""

import json
import sys
import random
from pathlib import Path

class RandomRollPlugin:
    def __init__(self, settings=None):
        self.plugin_dir = Path(__file__).parent
        # Settings will be passed from Flow Launcher
        self.settings = settings if settings is not None else {}
    
    def update_settings(self, settings):
        """Update settings with values from Flow Launcher"""
        if settings:
            self.settings = settings

    def handle_query(self, query):
        """Handle a query from Flow Launcher"""
        parts = query.strip().split()

        if not parts:
            # No arguments: use default roll type
            roll_type = self.settings.get("Default Roll Type", "Number")
            if roll_type == "Yes/No":
                return self.roll_yes_no()
            elif roll_type == "CustomLabel":
                return self.roll_custom_label()
            else:
                # Default to Number roll with configured from/to values
                try:
                    from_val = int(self.settings.get("default_from", 1))
                    to_val = int(self.settings.get("default_to", 6))
                except (ValueError, TypeError):
                    from_val = 1
                    to_val = 6
                return self.roll_range(from_val, to_val)

        if len(parts) == 1:
            # One argument: try to roll from 1 to N
            try:
                to_val = int(parts[0])
                return self.roll_range(1, to_val)
            except ValueError:
                # Not a number, treat as single custom label (not very useful, but handle it)
                return self.roll_custom_label_from_args(parts)

        if len(parts) == 2:
            # Two arguments: try to roll from A to B
            try:
                a_val = int(parts[0])
                b_val = int(parts[1])
                return self.roll_range(a_val, b_val)
            except ValueError:
                # Not valid numbers, treat as custom labels
                return self.roll_custom_label_from_args(parts)

        # Multiple arguments: treat as custom labels
        return self.roll_custom_label_from_args(parts)

    def roll_yes_no(self):
        """Generate a random yes/no result"""
        result = random.choice([True, False])
        yes_label = self.settings.get("yes_label", "Yes")
        no_label = self.settings.get("no_label", "No")
        title = yes_label if result else no_label
        subtitle = f"Random {yes_label}/{no_label} answer"

        return [{
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": "icon.png"
        }]

    def roll_custom_label(self):
        """Generate a random result from custom labels"""
        custom_labels_str = self.settings.get("custom_labels", "")
        if not custom_labels_str or not custom_labels_str.strip():
            return self.show_usage("No custom labels configured. Please set custom labels in settings.")
        
        # Split by whitespace to get individual labels
        labels = custom_labels_str.strip().split()
        
        if not labels:
            return self.show_usage("No custom labels configured. Please set custom labels in settings.")
        
        result = random.choice(labels)
        title = result
        subtitle = f"Random choice from: {', '.join(labels)}"

        return [{
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": "icon.png"
        }]

    def roll_custom_label_from_args(self, labels):
        """Generate a random result from provided custom labels"""
        if not labels:
            return self.show_usage("No labels provided.")
        
        result = random.choice(labels)
        title = result
        subtitle = f"Random choice from: {', '.join(labels)}"

        return [{
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": "icon.png"
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
                "IcoPath": "icon.png"
            }]
        except (ValueError, OverflowError):
            return self.show_usage("Invalid range values.")

    def show_usage(self, error_msg=None):
        """Show usage instructions"""
        title = "Random Roll Usage"
        subtitle_parts = [
            "* roll: Random based on default type (yes/no, number, or custom label)",
            "* roll N: Random number 1 to N",
            "* roll A B: Random number A to B",
            "* roll X Y Z...: Random choice from custom labels"
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
            settings = request.get("settings", {})
            
            # Update plugin settings with values from Flow Launcher
            plugin.update_settings(settings)

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