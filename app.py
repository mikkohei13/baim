import tkinter as tk
import time

def run_application():
    print(f"LOG: {analyze_directory.get()}, {threshold_value.get()}")

    if not analyze_directory.get():
        status_label.configure(text="Please give path to directory")
        return

    # Update the status label to show that the process has started
    status_label.configure(text="Process started...")

    # Perform some time-consuming task here...

    # Update the status label to show that the process has finished
    status_label.configure(text="Process finished!")
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


placeholder_threshold = 0.75


root = tk.Tk()
root.geometry("600x500")
root.title("BAIM")
root.configure(background="#E6E8E9")
root.option_add("*foreground", "#0A5061")
root.option_add("*background", "#E6E8E9")
#root.columnconfigure(0, minsize=140)

# Logo image
image = tk.PhotoImage(file="baim-icon.png")
image_label = tk.Label(root, image=image)
image_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

# Intro text
text_label = tk.Label(root, text="BAIM - Bird Audio Identification Manager\nVersion 0.1 / 2023-02-17\nUser manual at biomi.org/baim")
text_label.grid(row=0, column=1, padx=10, pady=40, sticky="N")

# Create input fields
analyze_directory_label = tk.Label(root, text="Directory for BirdNET files")
analyze_directory_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="W")
analyze_directory = tk.Entry(root, width=65, background="#F5F5F5")
analyze_directory.grid(row=2, column=0, columnspan=2, padx=10, pady="0", sticky="W")

threshold_value_label = tk.Label(root, text="Prediction threshold (between 0.01-0.99)")
threshold_value_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="W")
threshold_value = tk.Entry(root, validate="key", width=10, validatecommand=(root.register(validate_float), "%P"), background="#F5F5F5")
threshold_value.insert(0, placeholder_threshold)
threshold_value.grid(row=4, column=0, columnspan=2, padx=10, pady="0", sticky="W")

# Button to submit the fields
run_button = tk.Button(root, text="Analyze", command=run_application, background="#F5F5F5")
run_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="W")

# Display the status message
status_label = tk.Label(root, text="")
status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="W")


root.mainloop()
