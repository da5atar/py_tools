'''
text_translator.py

This script creates a simple clipboard manager that detects the language of the copied text and translates it to English if it is not already in English.
The script uses the 'pyperclip' library to access the clipboard contents and the 'deep_translator' library to detect and translate the text.
The translated text is displayed in a GUI window using Tkinter.

To run the script, simply execute it. The clipboard manager will start monitoring the clipboard for changes.
When text is copied, the script will detect the language and translate it to English if needed.

Note: You need to install the 'pyperclip', 'deep_translator', 'langdetect', and 'tkinter' libraries to run this script.
'''
import tkinter as tk
from tkinter import ttk
import pyperclip   # PIP Install
from deep_translator import GoogleTranslator
from langdetect import detect

def detect_and_translate(text):
    """Detect the language of the text and translate it to English if needed.
    If the text is already in English, return the original text.

    Args:
        text (str): The text to detect and translate.
    Returns:
        str: The translated text in English.
    Raises:
        Exception: If an error occurs during translation.
    """
    try:
        # Detect the language
        detected_language = detect(text)
        print(f"Detected language: {detected_language}")
        if detected_language != 'en':
            translated_text = GoogleTranslator(source=detected_language, target='en').translate(text)
            print(f"Translated text: {translated_text}")
            return translated_text
        else:
            print("The text is already in English.")
            return text
    except Exception as e:
        print(f"Error: {e}")
        return text

## Update and Append GUI with Newly Coped Text
def update_listbox():
    """Update the listbox with newly copied text."""
    new_item = pyperclip.paste()
    new_item = detect_and_translate(new_item)
    if new_item not in X:
        X.append(new_item)
        listbox.insert(tk.END, new_item)
        listbox.insert(tk.END, "----------------------")
    listbox.yview(tk.END)
    root.after(1000, update_listbox)

## Checks for Copied Contet
def copy_to_clipboard(event):
    """Copy the selected item to the clipboard when double-clicked."""
    selected_item = listbox.get(listbox.curselection())
    if selected_item:
        pyperclip.copy(selected_item)

X = []
root = tk.Tk()
root.title("Clipboard Manager")
root.geometry("500x500")
root.configure(bg="#f0f0f0")
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=10, pady=10)
label = tk.Label(frame, text="Clipboard Contents:", bg="#f0f0f0")
label.grid(row=0, column=0)
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(root, width=150, height=150, yscrollcommand=scrollbar.set)
listbox.pack(pady=10)
scrollbar.config(command=listbox.yview)
update_listbox()
listbox.bind("<Double-Button-1>", copy_to_clipboard)
root.mainloop()
