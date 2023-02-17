import tkinter as tk


def run_application():
    print(f"LOG: {analyze_directory.get()}, {threshold_value.get()}")

    # Update the status label to show that the process has started
    status_label.configure(text="Process started...")

    # Perform some time-consuming task here...

    # Update the status label to show that the process has finished
    status_label.configure(text="Process finished!")


def validate_float(new_value):
    try:
        float_value = float(new_value)
        if 0 <= float_value <= 1:  # check if input is between 0 and 1
            return True
        else:
            return False
    except ValueError:
        return False


root = tk.Tk()
root.geometry("600x400")
root.title("BAIM")
#root.configure(background="#E6E8E9")  # set the background color to light gray

# Create input fields
analyze_directory_label = tk.Label(root, text="Directory for BirdNET files", foreground="#0A5061")
analyze_directory_label.pack(pady=10)
analyze_directory = tk.Entry(root, width=65)
analyze_directory.pack()

placeholder_threshold = 0.75
threshold_value_label = tk.Label(root, text="Prediction threshold (between 0.01-0.99)")
threshold_value_label.pack(pady=10)
threshold_value = tk.Entry(root, validate="key", width=10, validatecommand=(root.register(validate_float), "%P"))
threshold_value.insert(0, placeholder_threshold)
threshold_value.pack()

run_button = tk.Button(root, text="Analyze", command=run_application)
run_button.pack(pady=20)

# Create a Label widget to display the status message
status_label = tk.Label(root, text="")
status_label.pack()


root.mainloop()
