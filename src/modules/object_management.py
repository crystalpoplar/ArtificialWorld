def makeListbeCommaSeparated(list):
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
