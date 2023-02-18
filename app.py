import tkinter as tk
import os
import handle_files
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def run_application():
    dir = analyze_directory.get()
    threshold = threshold_value.get()
    print(f"LOG: { dir }, { threshold }")

    # Validations
    if not analyze_directory.get():
        status_label.configure(text="Please give path to directory.")
        return

    # Debug helper
    if "t" == dir:
        dir = "/mnt/c/Users/mikko/Documents/Audiomoth_2022/baimtest"

    if not threshold:
        status_label.configure(text="Please threshold value.")
        return
    if not validate_float(threshold):
        status_label.configure(text="Threshold value must be a decimal number between 0.01-0.99.")
        return


    # Update the status label to show that the process has started
    status_label.configure(text="Processing files now...")
    root.update()

    # Perform some time-consuming task here...
    # If there's an error, birdnet_file_count is False, and segment_file_count contains error message
    # TODO: return tuple/dict instead, with specific error value
    birdnet_file_count, segment_file_count = handle_files.handle_files(dir, threshold)

    if False == birdnet_file_count:
        status_label.configure(text = segment_file_count)
    else:
        status_label.configure(text = f"Process finished, analyzed { birdnet_file_count } BirdNET files and created { segment_file_count } audio segments. \nThe results are in directory { dir }\n\nReady to process more files.")

    root.update()
    return


def validate_float(new_value):
    try:
        float_value = float(new_value)
        if 0 < float_value < 1:  # check if input is between 0 and 1
            return True
        else:
            return False
    except ValueError:
        return False


version = "0.1.2 / 2023-02-18"
placeholder_threshold = 0.75

window_width_px = 600
window_height_px = 500
logo_width_px = 140


root = tk.Tk()
root.geometry(f"{ window_width_px }x{ window_height_px }")
root.title("BAIM")
root.configure(background="#E6E8E9")
root.option_add("*foreground", "#0A5061")
root.option_add("*background", "#E6E8E9")
root.columnconfigure(1, minsize=logo_width_px)
root.columnconfigure(2, minsize=(window_width_px - logo_width_px))

# Logo image
image = tk.PhotoImage(file = resource_path("baim-icon.png"))
image_label = tk.Label(root, image=image)
image_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

# Intro text
text_label = tk.Label(root, justify="left", text=f"BAIM - BIRD AUDIO IDENTIFICATION MANAGER\nVersion { version }\nUser manual at biomi.org/baim")
text_label.grid(row=0, column=1, padx=10, pady=40, sticky="NW")

# Create input fields
analyze_directory_label = tk.Label(root, justify="left", text="Directory for BirdNET files (copy-paste here):")
analyze_directory_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="W")
analyze_directory = tk.Entry(root, width=70, background="#F5F5F5")
analyze_directory.grid(row=2, column=0, columnspan=2, padx=10, pady="0", sticky="W")

threshold_value_label = tk.Label(root, justify="left", text="Prediction threshold (between 0.01-0.99):")
threshold_value_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="W")
threshold_value = tk.Entry(root, validate="key", width=10, background="#F5F5F5")
threshold_value.insert(0, placeholder_threshold)
threshold_value.grid(row=4, column=0, columnspan=2, padx=10, pady="0", sticky="W")

# Button to submit the fields
run_button = tk.Button(root, text="Analyze", command=run_application, background="#F5F5F5")
run_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="W")

# Display the status message
status_label = tk.Label(root, justify="left", text="Ready to process files.", wraplength=(window_width_px - 50))
status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="W")


root.mainloop()
