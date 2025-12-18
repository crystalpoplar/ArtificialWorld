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
    Prompt the user for multiple inputs (text, yes/no, checkboxes) in a single window and return a dictionary of responses.
    Uses OS-appropriate UI:
    - Windows: tkinter with scrollable frame
    - macOS: osascript with multiple dialogs (sequential)
    - Linux: terminal input (fallback to terminal on all platforms if GUI unavailable)
    
    Args:
        questions (list): List of question dictionaries with format:
            {"question": str, "type": "text"|"yesno"|"checkbox", "default": optional default value}
            If "type" is omitted, defaults to "text".
        prompt_message (str): Optional message to display at the top of the dialog. Default is "".
        title (str): The title of the dialog window (if applicable). Default is "Input Required".
    
    Returns:
        dict: Dictionary mapping each question to the user's response.
              Text inputs return strings, yes/no and checkboxes return booleans.
              Returns empty dict if cancelled.
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
                for q_text, widget in widgets.items():
                    if isinstance(widget, tk.Entry):
                        responses[q_text] = widget.get()
                    else:  # BooleanVar for yesno/checkbox
                        responses[q_text] = widget.get()
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
            
            # Add questions and input widgets
            widgets = {}  # Maps question text -> widget
            first_widget = None
            
            for i, q_data in enumerate(questions):
                # Normalize question format
                if isinstance(q_data, str):
                    q_data = {"question": q_data, "type": "text"}
                
                q_text = q_data["question"]
                q_type = q_data.get("type", "text")
                q_default = q_data.get("default", None)
                
                label = ttk.Label(scrollable_frame, text=q_text)
                label.grid(row=i*2, column=0, sticky=tk.W, pady=(5, 2))
                
                if q_type == "text":
                    entry = ttk.Entry(scrollable_frame, width=50)
                    if q_default:
                        entry.insert(0, str(q_default))
                    entry.grid(row=i*2+1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
                    widgets[q_text] = entry
                    if first_widget is None:
                        first_widget = entry
                        
                elif q_type == "yesno":
                    var = tk.BooleanVar(value=q_default if q_default is not None else False)
                    frame = ttk.Frame(scrollable_frame)
                    frame.grid(row=i*2+1, column=0, sticky=tk.W, pady=(0, 10))
                    
                    yes_radio = ttk.Radiobutton(frame, text="Yes", variable=var, value=True)
                    yes_radio.pack(side=tk.LEFT, padx=(0, 10))
                    
                    no_radio = ttk.Radiobutton(frame, text="No", variable=var, value=False)
                    no_radio.pack(side=tk.LEFT)
                    
                    widgets[q_text] = var
                    if first_widget is None:
                        first_widget = yes_radio
                        
                elif q_type == "checkbox":
                    var = tk.BooleanVar(value=q_default if q_default is not None else False)
                    checkbox = ttk.Checkbutton(scrollable_frame, variable=var)
                    checkbox.grid(row=i*2+1, column=0, sticky=tk.W, pady=(0, 10))
                    widgets[q_text] = var
                    if first_widget is None:
                        first_widget = checkbox
                
                scrollable_frame.columnconfigure(0, weight=1)
            
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
            
            # Focus first widget
            if first_widget:
                first_widget.focus()
            
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
            for q_data in questions:
                # Normalize question format
                if isinstance(q_data, str):
                    q_data = {"question": q_data, "type": "text"}
                
                q_text = q_data["question"]
                q_type = q_data.get("type", "text")
                q_default = q_data.get("default", None)
                
                safe_question = q_text.replace('"', '\\"')
                safe_title = title.replace('"', '\\"')
                
                if q_type == "text":
                    default_text = str(q_default) if q_default else ""
                    script = f'display dialog "{safe_question}" default answer "{default_text}" with title "{safe_title}"'
                    result = subprocess.run(
                        ['osascript', '-e', script],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        output = result.stdout.strip()
                        if "text returned:" in output:
                            answer = output.split("text returned:", 1)[1].strip()
                            responses[q_text] = answer
                    else:
                        return {}
                        
                elif q_type in ("yesno", "checkbox"):
                    script = f'display dialog "{safe_question}" buttons {{"No", "Yes"}} default button "Yes" with title "{safe_title}"'
                    result = subprocess.run(
                        ['osascript', '-e', script],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        responses[q_text] = "Yes" in result.stdout
                    else:
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
        
        for q_data in questions:
            # Normalize question format
            if isinstance(q_data, str):
                q_data = {"question": q_data, "type": "text"}
            
            q_text = q_data["question"]
            q_type = q_data.get("type", "text")
            q_default = q_data.get("default", None)
            
            if q_type == "text":
                default_str = f" [{q_default}]" if q_default else ""
                answer = input(f"{q_text}{default_str}: ").strip()
                if not answer and q_default:
                    answer = str(q_default)
                responses[q_text] = answer
                
            elif q_type in ("yesno", "checkbox"):
                while True:
                    default_str = " [Y/n]" if q_default else " [y/N]"
                    answer = input(f"{q_text}{default_str}: ").strip().lower()
                    
                    if not answer:
                        responses[q_text] = bool(q_default)
                        break
                    elif answer in ('yes', 'y'):
                        responses[q_text] = True
                        break
                    elif answer in ('no', 'n'):
                        responses[q_text] = False
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
        
        return responses
        
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        return {}

# ...existing code...

def prompt_choice(prompt: str, choices: list, title: str = "Select Option") -> str:
    """
    Prompt the user to select one option from a list of choices.
    Uses OS-appropriate UI:
    - Windows: tkinter with clickable buttons (one click selection)
    - macOS: osascript with button list (limited to ~3 choices due to dialog constraints)
    - Linux: terminal input with numbered menu
    
    Args:
        prompt (str): The prompt message to display to the user.
        choices (list): List of string choices for the user to select from.
        title (str): The title of the dialog window (if applicable). Default is "Select Option".
    
    Returns:
        str: The selected choice, or empty string if cancelled/error.
    """
    if not choices:
        return ""
    
    os_name = platform.system()
    
    if os_name == "Windows":
        try:
            import tkinter as tk
            from tkinter import ttk
            
            selected = None
            
            def on_choice(choice):
                nonlocal selected
                selected = choice
                root.quit()
            
            # Create main window
            root = tk.Tk()
            root.title(title)
            root.attributes('-topmost', True)
            
            # Set minimum size
            root.minsize(300, 150)
            root.geometry("400x300")
            
            # Create main frame
            main_frame = ttk.Frame(root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Configure grid weights
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(1, weight=1)
            
            # Add prompt message
            msg_label = ttk.Label(main_frame, text=prompt, wraplength=350)
            msg_label.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            # Create canvas and scrollbar for choices
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add clickable buttons for each choice
            for choice in choices:
                btn = ttk.Button(
                    scrollable_frame,
                    text=choice,
                    command=lambda c=choice: on_choice(c),
                    width=40
                )
                btn.pack(pady=5, padx=10, fill=tk.X)
            
            scrollable_frame.columnconfigure(0, weight=1)
            
            # Place canvas and scrollbar
            canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
            
            # Bind mousewheel for scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            # Handle window close (X button)
            root.protocol("WM_DELETE_WINDOW", lambda: on_choice(""))
            
            root.mainloop()
            
            # Clean up
            try:
                canvas.unbind_all("<MouseWheel>")
            except:
                pass
            root.destroy()
            
            return selected if selected is not None else ""
            
        except Exception:
            # Fall back to terminal if tkinter fails
            pass
    
    elif os_name == "Darwin":  # macOS
        try:
            import subprocess
            
            # macOS dialogs are limited in the number of buttons they can display
            # If there are too many choices, fall back to terminal
            if len(choices) > 3:
                pass  # Fall through to terminal implementation
            else:
                safe_prompt = prompt.replace('"', '\\"')
                safe_title = title.replace('"', '\\"')
                
                # Build button list
                buttons = '", "'.join(choice.replace('"', '\\"') for choice in choices)
                script = f'display dialog "{safe_prompt}" buttons {{"{buttons}"}} default button 1 with title "{safe_title}"'
                
                result = subprocess.run(
                    ['osascript', '-e', script],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    # Extract button clicked from output
                    output = result.stdout.strip()
                    if "button returned:" in output:
                        button_text = output.split("button returned:", 1)[1].strip()
                        return button_text
                return ""
                
        except Exception:
            # Fall back to terminal if osascript fails
            pass
    
    # Linux or fallback: terminal-based numbered menu
    try:
        print(f"\n{prompt}\n")
        
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        
        while True:
            try:
                answer = input(f"\nEnter choice (1-{len(choices)}): ").strip()
                
                if answer.isdigit():
                    idx = int(answer) - 1
                    if 0 <= idx < len(choices):
                        return choices[idx]
                
                print(f"Invalid choice. Please enter a number between 1 and {len(choices)}.")
                
            except (EOFError, KeyboardInterrupt):
                print("\nSelection cancelled.")
                return ""
                
    except Exception:
        return ""

def prompt_notification(message: str, title: str = "Notification") -> None:
    """
    Display a notification message to the user that can be easily dismissed.
    Uses OS-appropriate UI:
    - Windows: tkinter messagebox with single OK button
    - macOS: osascript notification or dialog
    - Linux: terminal output (fallback to terminal on all platforms if GUI unavailable)
    
    Args:
        message (str): The notification message to display.
        title (str): The title of the notification (if applicable). Default is "Notification".
    
    Returns:
        None
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
            
            # Show info message box with OK button
            messagebox.showinfo(title, message, parent=root)
            root.destroy()
            return
        except Exception:
            # Fall back to terminal if tkinter fails
            pass
    
    elif os_name == "Darwin":  # macOS
        try:
            import subprocess
            
            # Use osascript to show native notification
            # Try notification center first (non-blocking)
            safe_message = message.replace('"', '\\"')
            safe_title = title.replace('"', '\\"')
            
            try:
                # Display notification (non-blocking, auto-dismisses)
                script = f'display notification "{safe_message}" with title "{safe_title}"'
                subprocess.run(['osascript', '-e', script], capture_output=True, timeout=2)
                return
            except:
                # Fall back to dialog (requires click to dismiss)
                script = f'display dialog "{safe_message}" buttons {{"OK"}} default button "OK" with title "{safe_title}"'
                subprocess.run(['osascript', '-e', script], capture_output=True)
                return
                
        except Exception:
            # Fall back to terminal if osascript fails
            pass
    
    # Linux or fallback: terminal-based notification
    print(f"\n{'='*60}")
    print(f"{title.upper()}")
    print(f"{'='*60}")
    print(f"{message}")
    print(f"{'='*60}\n")

def prompt_list_manager(left_list: list, right_list: list, left_title: str = "Available", right_title: str = "Selected", window_title: str = "List Manager") -> tuple:
    """
    Display a dual-list manager where users can move items between two lists.
    Right list takes precedence - duplicates are automatically removed from the left list.
    Uses OS-appropriate UI:
    - Windows/macOS/Linux with GUI: tkinter with dual scrollable listboxes and move buttons
    - Fallback: terminal-based interface
    
    Args:
        left_list (list): Initial items for the left list.
        right_list (list): Initial items for the right list (takes precedence).
        left_title (str): Title/label for the left list. Default is "Available".
        right_title (str): Title/label for the right list. Default is "Selected".
        window_title (str): Title of the window. Default is "List Manager".
    
    Returns:
        tuple: (left_list, right_list) - The final state of both lists after user interaction.
               Returns ([], []) if cancelled.
    """
    # Remove duplicates - right list takes precedence
    left_items = [item for item in left_list if item not in right_list]
    right_items = list(right_list)
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        result_left = []
        result_right = []
        cancelled = False
        
        def move_to_right():
            """Move selected items from left to right."""
            selection = left_listbox.curselection()
            if not selection:
                return
            
            # Get selected items (in reverse to maintain indices)
            items_to_move = [left_listbox.get(i) for i in selection]
            
            # Remove from left (in reverse order to maintain indices)
            for i in reversed(selection):
                left_listbox.delete(i)
            
            # Add to right (avoid duplicates)
            for item in items_to_move:
                if item not in right_listbox.get(0, tk.END):
                    right_listbox.insert(tk.END, item)
        
        def move_to_left():
            """Move selected items from right to left."""
            selection = right_listbox.curselection()
            if not selection:
                return
            
            # Get selected items (in reverse to maintain indices)
            items_to_move = [right_listbox.get(i) for i in selection]
            
            # Remove from right (in reverse order to maintain indices)
            for i in reversed(selection):
                right_listbox.delete(i)
            
            # Add to left (avoid duplicates)
            for item in items_to_move:
                if item not in left_listbox.get(0, tk.END):
                    left_listbox.insert(tk.END, item)
        
        def on_ok():
            """Save changes and close."""
            nonlocal result_left, result_right
            result_left = list(left_listbox.get(0, tk.END))
            result_right = list(right_listbox.get(0, tk.END))
            root.quit()
        
        def on_cancel():
            """Cancel and close."""
            nonlocal cancelled
            cancelled = True
            root.quit()
        
        # Create main window
        root = tk.Tk()
        root.title(window_title)
        root.geometry("700x500")
        root.minsize(600, 400)
        
        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Main container frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left list frame
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        left_label = ttk.Label(left_frame, text=left_title, font=('TkDefaultFont', 10, 'bold'))
        left_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        left_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL)
        left_listbox = tk.Listbox(left_frame, yscrollcommand=left_scroll.set, selectmode=tk.EXTENDED)
        left_scroll.config(command=left_listbox.yview)
        left_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        left_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Populate left listbox
        for item in left_items:
            left_listbox.insert(tk.END, item)
        
        # Middle buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=1, padx=10)
        
        move_right_btn = ttk.Button(button_frame, text="→", command=move_to_right, width=5)
        move_right_btn.pack(pady=5)
        
        move_left_btn = ttk.Button(button_frame, text="←", command=move_to_left, width=5)
        move_left_btn.pack(pady=5)
        
        # Right list frame
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=2, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        right_label = ttk.Label(right_frame, text=right_title, font=('TkDefaultFont', 10, 'bold'))
        right_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        right_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL)
        right_listbox = tk.Listbox(right_frame, yscrollcommand=right_scroll.set, selectmode=tk.EXTENDED)
        right_scroll.config(command=right_listbox.yview)
        right_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_scroll.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Populate right listbox
        for item in right_items:
            right_listbox.insert(tk.END, item)
        
        # Bottom buttons frame
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ok_btn = ttk.Button(bottom_frame, text="OK", command=on_ok)
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(bottom_frame, text="Cancel", command=on_cancel)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Handle window close
        root.protocol("WM_DELETE_WINDOW", on_cancel)
        
        root.mainloop()
        root.destroy()
        
        if cancelled:
            return ([], [])
        return (result_left, result_right)
        
    except Exception as e:
        # Fallback to terminal-based interface
        print(f"\nGUI unavailable, using terminal interface. Error: {e}\n")
        
        left_items = [item for item in left_list if item not in right_list]
        right_items = list(right_list)
        
        while True:
            print(f"\n{'='*60}")
            print(f"{left_title} (Left) | {right_title} (Right)")
            print(f"{'='*60}")
            
            max_len = max(len(left_items), len(right_items))
            for i in range(max_len):
                left_item = left_items[i] if i < len(left_items) else ""
                right_item = right_items[i] if i < len(right_items) else ""
                print(f"{i+1:3}. {left_item:25} | {right_item}")
            
            print(f"\nCommands:")
            print(f"  r <index>  - Move item from left to right")
            print(f"  l <index>  - Move item from right to left")
            print(f"  ok         - Accept changes")
            print(f"  cancel     - Cancel changes")
            
            try:
                cmd = input(f"\nEnter command: ").strip().lower()
                
                if cmd == "ok":
                    return (left_items, right_items)
                elif cmd == "cancel":
                    return ([], [])
                elif cmd.startswith("r "):
                    try:
                        idx = int(cmd.split()[1]) - 1
                        if 0 <= idx < len(left_items):
                            item = left_items.pop(idx)
                            if item not in right_items:
                                right_items.append(item)
                    except (ValueError, IndexError):
                        print("Invalid index.")
                elif cmd.startswith("l "):
                    try:
                        idx = int(cmd.split()[1]) - 1
                        if 0 <= idx < len(right_items):
                            item = right_items.pop(idx)
                            if item not in left_items:
                                left_items.append(item)
                    except (ValueError, IndexError):
                        print("Invalid index.")
                else:
                    print("Invalid command.")
                    
            except (EOFError, KeyboardInterrupt):
                print("\nCancelled.")
                return ([], [])
