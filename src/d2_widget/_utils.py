import json
import re
import ast
from typing import Dict, Any


def parse_magic_arguments(args_string: str) -> Dict[str, Any]:
    """
    Parse IPython magic arguments into a dictionary.

    Args:
        args_string: Raw arguments string from IPython magic

    Returns:
        Dictionary of parsed arguments

    This function first tries to parse the string as JSON.
    If that fails, it parses it as key=value pairs, with special handling for:
    - Values containing equals signs
    - Quoted values
    - Numbers
    - Booleans
    """
    if not args_string.strip():
        return {}

    # First try parsing as JSON
    try:
        return json.loads(args_string)
    except json.JSONDecodeError:
        pass

    # Parse as key=value pairs with regex
    options = {}

    # Match key=value pairs
    # Handles: key="value with spaces", key=123, key=value, key='quoted value'
    pattern = r'(\w+)=(?:([^"\'\s]+)|(\'[^\']*\')|(\"[^\"]*\"))'
    matches = re.findall(pattern, args_string)

    for match in matches:
        key, simple_val, single_quoted, double_quoted = match

        # Determine which value format was matched
        if simple_val:
            value = simple_val
        elif single_quoted:
            value = single_quoted[1:-1]  # Remove quotes
        elif double_quoted:
            value = double_quoted[1:-1]  # Remove quotes
        else:
            continue

        # Try to convert value to appropriate type
        try:
            # Try to evaluate as a Python literal (handles ints, floats, bools)
            parsed_value = ast.literal_eval(value)
            options[key] = parsed_value
        except (SyntaxError, ValueError):
            # If it's not a Python literal, keep it as a string
            options[key] = value

    return options
