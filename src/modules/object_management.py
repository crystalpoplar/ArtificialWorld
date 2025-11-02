import traceback
import re
import logger
import file_management

mainLog = logger.mainLog

def make_list_comma_separated(list):
    """
    Converts a list to a comma-separated string.

    Parameters:
        list (list): The list to convert.

    Returns:
        str: The comma-separated string.
    """
    text = ''
    for entry in list:
        text = str(text) + str(entry) + ', '
    text = text.rstrip(', ') + '.'
    return text

def list2csv(list_check):
    """
    Converts a list to a CSV string.

    Parameters:
        list (list): The list to convert.

    Returns:
        str: The CSV string.
    """
    csv_list = ''
    if not isinstance(list_check, list):
        for value in list_check:
            csv_list = csv_list + ',' + value
        return csv_list[1:]
    else:
        return list_check

def makeTextJson(textStr):
    """
    Converts a text string to JSON format.

    Parameters:
        textStr (str): The text string to convert.

    Returns:
        str: The JSON string.
    """
    while textStr[0] != '{' and len(textStr) > 0:
        textStr = textStr[1:]
    while textStr[-1] != '}' and len(textStr) > 0:
        textStr = textStr[:-1]
    return textStr

def getValuesFromJson(keys, jsonFilePath):
    """
    Retrieves values from a JSON file based on the provided keys.

    Parameters:
        keys (list): A list of string keys to retrieve values for. Nested keys should be provided as lists.
        jsonFilePath (str): The path to the JSON file.

    Returns:
        tuple: A tuple of values corresponding to the keys. If a key does not exist, the value will be None.
    """
    def get_nested_value(data, key_list):
        """
        Helper function to retrieve nested values from a dictionary.
        """
        for key in key_list:
            if isinstance(data, dict):
                data = data.get(key, None)
            else:
                return None
        return data

    # Load the JSON file
    jsonData = file_management.getJsonDict(jsonFilePath)
    
    # Retrieve values for the keys, set to None if key does not exist
    values = tuple(get_nested_value(jsonData, key) if isinstance(key, list) else jsonData.get(key, None) for key in keys)
    
    return values

def stringFormatter(string: str) -> str:
    """
    Replace placeholders in the input string:
      - {functionName} -> call a zero-argument function with that name from globals() and substitute its return value
      - [LOOKUP]        -> lookup value from globals() or JSON files with special prefix DICT.<file>.<key1>.<key2>...
    
    Behavior and improvements:
      - Uses regular expressions with callback functions for efficient single-pass replacements.
      - Performs iterative passes (up to max_passes) to resolve placeholders introduced by replacements,
        preventing infinite loops by bounding iterations.
      - Robustly handles missing functions/values and logs warnings/errors to mainLog.
      - Supports nested dict lookups in JSON files and nested attribute/key access for globals variables.
      - Normalizes replacement values to strings and strips newlines/tabs.
    """

    max_passes = 5  # limit to avoid infinite recursion loops
    pass_num = 0

    if not isinstance(string, str):
        mainLog.debug("stringFormatter received non-str input; converting to str")
        string = str(string)

    func_pattern = re.compile(r'\{([^{}]+)\}')
    lookup_pattern = re.compile(r'\[([^\[\]]+)\]')

    def _format_value(val):
        """Normalize various types to a safe string representation."""
        if val is None:
            return ''
        if isinstance(val, bool):
            return str(val).lower()
        if isinstance(val, (int, float)):
            return str(val)
        if isinstance(val, list):
            return ', '.join(str(x) for x in val)
        if isinstance(val, dict):
            return ', '.join(f"{k}: {v}" for k, v in val.items())
        # other types -> string, sanitize whitespace/newlines/tabs
        s = str(val)
        return s.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    def _replace_function(match):
        name = match.group(1).strip()
        func_name = name.split('(')[0].strip()
        func = globals().get(func_name)
        if not callable(func):
            mainLog.warning(f"stringFormatter: function '{func_name}' not found or not callable")
            return ''
        try:
            result = func()
            formatted = _format_value(result)
            mainLog.debug(f"stringFormatter: replaced function {{{name}}} -> '{formatted}'")
            return formatted
        except Exception as e:
            mainLog.error(f"stringFormatter: error calling function '{func_name}': {e}")
            mainLog.error(traceback.format_exc())
            return ''

    def _resolve_dict_lookup(dict_name: str, keys):
        """Load a JSON file and traverse nested keys."""
        try:
            jsonData = file_management.getJsonDict(dict_name + '.json')
        except Exception as e:
            mainLog.error(f"stringFormatter: error loading JSON '{dict_name}.json': {e}")
            return None
        data = jsonData
        for k in keys:
            if isinstance(data, dict):
                data = data.get(k, None)
            else:
                return None
        return data

    def _resolve_global_lookup(parts):
        """Resolve nested lookups in globals (dict keys or attributes)."""
        obj = globals().get(parts[0])
        if obj is None:
            return None
        for p in parts[1:]:
            if isinstance(obj, dict):
                obj = obj.get(p, None)
            else:
                # try attribute access
                obj = getattr(obj, p, None)
            if obj is None:
                return None
        return obj

    def _replace_lookup(match):
        content = match.group(1).strip()
        try:
            if content.startswith('DICT.'):
                # DICT.filename.key1.key2...
                rest = content[len('DICT.'):].strip()
                parts = rest.split('.')
                dict_name = parts[0]
                keys = parts[1:] if len(parts) > 1 else []
                val = _resolve_dict_lookup(dict_name, keys)
            else:
                parts = content.split('.')
                val = _resolve_global_lookup(parts)
            formatted = _format_value(val)
            mainLog.debug(f"stringFormatter: replaced lookup [{content}] -> '{formatted}'")
            return formatted
        except Exception as e:
            mainLog.error(f"stringFormatter: error resolving lookup '[{content}]': {e}")
            mainLog.error(traceback.format_exc())
            return ''

    # Iteratively replace until stable or max_passes reached
    previous = None
    while pass_num < max_passes and string != previous:
        previous = string
        # Replace function placeholders
        try:
            string = func_pattern.sub(_replace_function, string)
        except Exception as e:
            mainLog.error(f"stringFormatter: error during function replacements: {e}")
            mainLog.error(traceback.format_exc())
            break
        # Replace lookup placeholders
        try:
            string = lookup_pattern.sub(_replace_lookup, string)
        except Exception as e:
            mainLog.error(f"stringFormatter: error during lookup replacements: {e}")
            mainLog.error(traceback.format_exc())
            break
        pass_num += 1

    if pass_num == max_passes:
        mainLog.warning("stringFormatter: maximum passes reached; result may still contain unresolved placeholders")

    return string

def executeFunctionInString(string):
    """
    This function replaces placeholders in the format {functionName} within the input string
    with the result of calling the corresponding function.

    Arguments:
    string (str): The input string containing placeholders.

    Returns:
    str: The string with placeholders replaced by function results.
    """
    while '{' in string and '}' in string:
        try:
            # Extract the function name from the placeholder
            function_name = string.split('{')[1].split('}')[0]
            # Get the function object from the global scope
            function_result = globals().get(function_name.split('(')[0])
            if function_result:
                # Call the function and get the result
                function_string = function_result()
                # Replace the placeholder with the function result
                string = string.replace(f'{{{function_name}}}', function_string)
            else:
                raise ValueError(f"Function '{function_name}' not found.")
        except Exception as e:
            # Handle any errors that occur during function execution
            print(f"Error executing function '{function_name}': {e}")
            break
    return string
