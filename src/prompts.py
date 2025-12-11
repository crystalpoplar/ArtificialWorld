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

def prompt_multiple_inputs(questions: list, prompt_message: str = "", title: str = "Input Required") -> dict:
    """
    Prompt the user for multiple text inputs in a single window and return a dictionary of responses.
    Uses OS-appropriate UI:
    - Windows: tkinter with scrollable frame
    - macOS: osascript with multiple text input dialogs (sequential)
    - Linux: terminal input (fallback to terminal on all platforms if GUI unavailable)
    
    Args:
        questions (list): List of question strings to prompt the user for.
        prompt_message (str): Optional message to display at the top of the dialog. Default is "".
        title (str): The title of the dialog window (if applicable). Default is "Input Required".
    
    Returns:
        dict: Dictionary mapping each question to the user's response. Returns empty dict if cancelled.
    """
    os_name = platform.system()
    
    if os_name == "Windows":
        try:
            import tkinter as tk
            from tkinter import ttk
            
            responses = {}
            cancelled = False
            
            def on_submit():
                nonlocal responses, cancelled
                for q, entry in entries.items():
                    responses[q] = entry.get()
                root.quit()
            
            def on_cancel():
                nonlocal cancelled
                cancelled = True
                root.quit()
            
            # Create main window
            root = tk.Tk()
            root.title(title)
            root.attributes('-topmost', True)
            
            # Set minimum size and make resizable
            root.minsize(400, 300)
            root.geometry("500x400")
            
            # Create main frame
            main_frame = ttk.Frame(root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Configure grid weights for resizing
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(1, weight=1)
            
            # Add prompt message at top if provided
            if prompt_message:
                msg_label = ttk.Label(main_frame, text=prompt_message, wraplength=450)
                msg_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            # Create canvas and scrollbar for scrolling
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add questions and entry fields
            entries = {}
            for i, question in enumerate(questions):
                label = ttk.Label(scrollable_frame, text=question)
                label.grid(row=i*2, column=0, sticky=tk.W, pady=(5, 2))
                
                entry = ttk.Entry(scrollable_frame, width=50)
                entry.grid(row=i*2+1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
                
                scrollable_frame.columnconfigure(0, weight=1)
                entries[question] = entry
            
            # Place canvas and scrollbar
            canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
            
            # Button frame
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
            
            submit_btn = ttk.Button(button_frame, text="Submit", command=on_submit)
            submit_btn.pack(side=tk.LEFT, padx=5)
            
            cancel_btn = ttk.Button(button_frame, text="Cancel", command=on_cancel)
            cancel_btn.pack(side=tk.LEFT, padx=5)
            
            # Focus first entry
            if entries:
                first_entry = list(entries.values())[0]
                first_entry.focus()
            
            # Bind mousewheel for scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            root.mainloop()
            
            # Clean up
            canvas.unbind_all("<MouseWheel>")
            root.destroy()
            
            return {} if cancelled else responses
            
        except Exception:
            # Fall back to terminal if tkinter fails
            pass
    
    elif os_name == "Darwin":  # macOS
        try:
            import subprocess
            
            responses = {}
            
            # Show prompt message first if provided
            if prompt_message:
                safe_message = prompt_message.replace('"', '\\"')
                safe_title = title.replace('"', '\\"')
                script = f'display dialog "{safe_message}" buttons {{"OK"}} with title "{safe_title}"'
                subprocess.run(['osascript', '-e', script], capture_output=True)
            
            # Show sequential dialogs for each question
            for question in questions:
                safe_question = question.replace('"', '\\"')
                safe_title = title.replace('"', '\\"')
                script = f'display dialog "{safe_question}" default answer "" with title "{safe_title}"'
                result = subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    if "text returned:" in output:
                        answer = output.split("text returned:", 1)[1].strip()
                        responses[question] = answer
                else:
                    # User cancelled
                    return {}
            
            return responses
            
        except Exception:
            # Fall back to terminal if osascript fails
            pass
    
    # Linux or fallback: terminal-based prompt
    try:
        responses = {}
        
        if prompt_message:
            print(f"\n{prompt_message}\n")
        
        for question in questions:
            answer = input(f"{question}: ").strip()
            responses[question] = answer
        
        return responses
        
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return {}
