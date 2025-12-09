import os

def copyTextToClipboard(text):
    """
    Copies the provided text to the system clipboard.

    Args:
        text (str): The text string to be copied to the clipboard.

    Note:
        This function uses the Windows 'clip' command via os.system and may not work
        on non-Windows operating systems. The text is passed to the clipboard without
        any escaping, which may cause issues with special characters.

    Example:
        >>> copyTextToClipboard("Hello, World!")
        # "Hello, World!" is now in the clipboard
    """
    os.system(f'echo {text} | clip')
