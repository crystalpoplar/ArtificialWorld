import platform

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


def prompt_text_input(prompt: str, title: str = "Input Required") -> str:
    """
    Prompt the user for text input and return the entered string.
    Uses OS-appropriate UI:
    - Windows: tkinter simpledialog
    - macOS: osascript (AppleScript) text input dialog
    - Linux: terminal input (fallback to terminal on all platforms if GUI unavailable)
    
    Args:
        prompt (str): The prompt message to display to the user.
        title (str): The title of the dialog window (if applicable). Default is "Input Required".
    
    Returns:
        str: The text entered by the user, or empty string if cancelled/error.
    """
    os_name = platform.system()
    
    if os_name == "Windows":
        try:
            import tkinter as tk
            from tkinter import simpledialog
            
            # Create a hidden root window
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            # Show text input dialog
            result = simpledialog.askstring(title, prompt, parent=root)
            root.destroy()
            return result if result is not None else ""
        except Exception:
            # Fall back to terminal if tkinter fails
            pass
    
    elif os_name == "Darwin":  # macOS
        try:
            import subprocess
            
            # Use osascript to show native text input dialog
            # Escape double quotes in prompt and title
            safe_prompt = prompt.replace('"', '\\"')
            safe_title = title.replace('"', '\\"')
            script = f'display dialog "{safe_prompt}" default answer "" with title "{safe_title}"'
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Extract text from "text returned:USER_INPUT" in stdout
                output = result.stdout.strip()
                if "text returned:" in output:
                    return output.split("text returned:", 1)[1].strip()
            return ""
        except Exception:
            # Fall back to terminal if osascript fails
            pass
    
    # Linux or fallback: terminal-based prompt
    try:
        response = input(f"{prompt}: ").strip()
        return response
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return ""
