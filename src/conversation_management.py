from datetime import datetime

def convo_timestamp():
    """
    Returns the current timestamp in YYYY-MM-DD HH:MM:SS format.

    Returns:
        str: The current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
