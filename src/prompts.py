import platform
import sys

def prompt_yes_no(question: str) -> bool:
    """
    Prompt the user with a yes/no question and return a boolean.
    Uses OS-appropriate UI:
    - Windows: tkinter messagebox
    - macOS: osascript (AppleScript) dialog
    - Linux: terminal input (fallback to terminal on all platforms if GUI unavailable)
    
    Args:
        question (str): The question to ask the user.
    
    Returns:
        bool: True if user answers yes, False if user answers no.
    """
    os_name = platform.system()
    
    if os_name == "Windows":
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            # Create a hidden root window
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            # Show yes/no dialog
            result = messagebox.askyesno("Confirmation", question, parent=root)
            root.destroy()
            return result
        except Exception:
            # Fall back to terminal if tkinter fails
            pass
    
    elif os_name == "Darwin":  # macOS
        try:
            import subprocess
            
            # Use osascript to show native dialog
            script = f'display dialog "{question}" buttons {{"No", "Yes"}} default button "Yes"'
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            # osascript returns exit code 0 if "Yes" clicked, non-zero if "No" or cancelled
            return result.returncode == 0 and "Yes" in result.stdout
        except Exception:
            # Fall back to terminal if osascript fails
            pass
    
    # Linux or fallback: terminal-based prompt
    while True:
        try:
            response = input(f"{question} (yes/no): ").strip().lower()
            if response in ('yes', 'y'):
                return True
            elif response in ('no', 'n'):
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        except (EOFError, KeyboardInterrupt):
            print("\nPrompt cancelled.")
            return False
