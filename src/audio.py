import pyttsx3
import re

def remove_unicode_escapes(text: str) -> str:
    """
    Removes special Unicode escape sequences and surrogate characters from a text string.
    """
    # Remove literal escape sequences like \ud83c\udf1e
    text = re.sub(r'(\\u[0-9a-fA-F]{4})+', '', text)
    # Remove actual surrogate characters (U+D800 to U+DFFF)
    return re.sub(r'[\ud800-\udfff]', '', text)

def speak_text(text: str,
               rate: int = 210,
               volume: float = 1.0,
               voice_index: int = 1) -> None:
    """
    Speaks the provided text out loud using the system's TTS engine.

    Args:
        text (str): The text to be spoken.
        rate (int): The speech rate (default is 210).
        volume (float): The volume level (default is 1.0, max is 1.0).
        voice_index (int): The index of the voice to use (default is 1).

    Example:
        speak_text("This is a test of the emergency broadcast system.")
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', rate)    # Speed percent (can go over 100)
    engine.setProperty('volume', volume)  # Volume 0-1
    engine.setProperty('voice', voices[voice_index].id)  # Voice type
    engine.say(remove_unicode_escapes(text))
    engine.runAndWait()
