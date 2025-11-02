import file_management

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
