import os
import sys
import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Access to the script’s directory
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def get_kanye_quote():
    url = "https://api.kanye.rest/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        quote = data['quote']
        # Remove leading and trailing double quotes if they exist
        return quote.strip('"')
    else:
        return "Failed to retrieve quote"


def fetch_quote():
    quote = get_kanye_quote()
    update_text(quote)


def convert_to_unicode(text):
    # Extended Unicode mapping for a wider range of characters
    unicode_map = {
        'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': '𝑒', 'f': '𝒻', 'g': '𝑔', 'h': '𝒽', 'i': '𝒾',
        'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃', 'o': '𝑜', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇',
        's': '𝓈', 't': '𝓉', 'u': '𝓊', 'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏',
        'A': '𝒜', 'B': '𝐵', 'C': '𝐶', 'D': '𝐷', 'E': '𝐸', 'F': '𝐹', 'G': '𝐺', 'H': '𝐻', 'I': '𝐼',
        'J': '𝒥', 'K': '𝐾', 'L': '𝐿', 'M': '𝑀', 'N': '𝑁', 'O': '𝑂', 'P': '𝑃', 'Q': '𝑄', 'R': '𝑅',
        'S': '𝑆', 'T': '𝑇', 'U': '𝑈', 'V': '𝑉', 'W': '𝑊', 'X': '𝑋', 'Y': '𝑌', 'Z': '𝑍',
        ' ': ' ',
        '"': '“', "'": '’', '-': '–', ',': '，', '.': '.',
        '!': '！', '?': '？', ':': '：', ';': '；',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    }
    return ''.join(unicode_map.get(c, c) for c in text)


def update_text(text):
    canvas.delete("quote")  # Clear previous text

    # Convert the text to Unicode fancy characters
    fancy_text = convert_to_unicode(text)
    fancy_name = convert_to_unicode("-ye")

    # Create text shadow (stroke effect) by drawing multiple layers
    shadow_offset = 3  # Adjusted for larger text
    for x_offset in (-shadow_offset, 0, shadow_offset):
        for y_offset in (-shadow_offset, 0, shadow_offset):
            if x_offset != 0 or y_offset != 0:
                canvas.create_text(
                    canvas.winfo_width() // 2 + x_offset,
                    canvas.winfo_height() // 2 + y_offset,
                    text=f'“{fancy_text}”',
                    fill="white",
                    font=("Helvetica", 18, "bold"),  # Increased font size
                    tags="quote",
                    width=canvas.winfo_width() - 40
                )

    # Main text with quotation marks
    text_id = canvas.create_text(
        canvas.winfo_width() // 2,
        canvas.winfo_height() // 2,
        text=f'“{fancy_text}”',
        fill="black",
        font=("Helvetica", 18, "bold"),  # Increased font size
        tags="quote",
        width=canvas.winfo_width() - 40
    )

    # Get the bounding box of the main quote text
    bbox = canvas.bbox(text_id)
    quote_height = bbox[3] - bbox[1]  # Calculate the height of the text

    # Add "-ye" below the quote with the same stroke effect
    for x_offset in (-shadow_offset, 0, shadow_offset):
        for y_offset in (-shadow_offset, 0, shadow_offset):
            if x_offset != 0 or y_offset != 0:
                canvas.create_text(
                    canvas.winfo_width() // 2 + x_offset,
                    canvas.winfo_height() // 2 + quote_height + y_offset + 40,  # Adjusted position
                    text=fancy_name,
                    fill="white",
                    font=("Helvetica", 18, "italic"),  # Slightly increased font size
                    tags="quote"
                )

    # Main "-ye" text
    canvas.create_text(
        canvas.winfo_width() // 2,
        canvas.winfo_height() // 2 + quote_height + 40,  # Adjusted position
        text=fancy_name,
        fill="black",
        font=("Helvetica", 18, "italic"),  # Slightly increased font size
        tags="quote"
    )


# Function to resize the image while maintaining aspect ratio
def resize_image(image, max_width, max_height):
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    new_ratio = min(width_ratio, height_ratio)

    new_size = (int(image.width * new_ratio), int(image.height * new_ratio))
    return image.resize(new_size, Image.LANCZOS)


# Function to draw a button with rounded corners
def draw_rounded_button(canvas, x, y, width, height, text, command):
    radius = 15
    # Create rounded rectangle
    canvas.create_oval(x, y, x + 2 * radius, y + 2 * radius, fill='black', outline='black')
    canvas.create_oval(x + width - 2 * radius, y, x + width, y + 2 * radius, fill='black', outline='black')
    canvas.create_oval(x, y + height - 2 * radius, x + 2 * radius, y + height, fill='black', outline='black')
    canvas.create_oval(x + width - 2 * radius, y + height - 2 * radius, x + width, y + height, fill='black', outline='black')
    canvas.create_rectangle(x + radius, y, x + width - radius, y + height, fill='black', outline='black')
    canvas.create_rectangle(x, y + radius, x + width, y + height - radius, fill='black', outline='black')

    # Add text on the button
    button_text_id = canvas.create_text(x + width / 2, y + height / 2, text=text, fill='white', font=('Helvetica', 12, 'bold'))

    # Bind button click event
    canvas.tag_bind(button_text_id, '<Button-1>', lambda e: command())


# Create the main window
root = tk.Tk()
root.title("Kanye Quotes")

# Load the background image
bg_image_path = resource_path("YE.jpg")  # Use resource path to handle bundling
bg_image = Image.open(bg_image_path)

# Resize the image to fit the window
max_width, max_height = 800, 600  # Set your desired max dimensions
bg_image = resize_image(bg_image, max_width, max_height)

# Convert the image to a Tkinter-compatible photo image
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Canvas for the background image and text
canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Draw the background image on the Canvas
canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

# Draw the custom rounded button on the canvas
draw_rounded_button(canvas, bg_image.width // 2 - 75, bg_image.height - 50, 150, 30, "Get Kanye Quote", fetch_quote)

# Run the main loop
root.geometry(f"{bg_image.width}x{bg_image.height}")  # Set the window size to the image size
root.mainloop()
