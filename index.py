import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont

df = pd.read_csv('alzheimers_disease_data.csv')

X = df.drop(['Diagnosis', 'PatientID','DoctorInCharge'], axis=1)
y = df['Diagnosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = GaussianNB()
model.fit(X_train, y_train)

# UI colors and fonts
BG_COLOR = "#fff0f5"
HEADER_COLOR = "#db7093"
ENTRY_COLOR = "#ffffff"
ERROR_COLOR = "#ff1493"
TEXT_COLOR = "#800080"
BUTTON_COLOR = "#ff69b4"
HIGHLIGHT_COLOR = "#ffe4e1"

root = tk.Tk()
root.title("Alzheimer's Risk Assessment")
root.geometry("450x550")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use('default')
style.configure("Vertical.TScrollbar", background=ENTRY_COLOR, troughcolor=ENTRY_COLOR, arrowcolor=HEADER_COLOR)
style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
style.configure("TButton", background=BUTTON_COLOR, foreground="white")
style.configure("TRadiobutton", background=BG_COLOR, foreground=TEXT_COLOR)

title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
label_font = tkFont.Font(family="Arial", size=11)
entry_font = tkFont.Font(family="Arial", size=11)
button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

main_frame = ttk.Frame(root, style="TFrame")
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
content_frame = ttk.Frame(canvas, style="TFrame")

content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=content_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

title_frame = ttk.Frame(content_frame, style="TFrame")
title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

tk.Label(title_frame, text="Alzheimer's Risk Assessment", font=title_font, bg=BG_COLOR, fg=HEADER_COLOR).pack()
tk.Label(title_frame, text="Complete all fields to assess your Alzheimer's risk", font=("Arial", 10), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)

def create_field(parent, label_text, row, field_type, options=None, min_val=None, max_val=None):
    frame = ttk.Frame(parent, style="TFrame")
    frame.grid(row=row, column=0, sticky="ew", pady=3)

    tk.Label(frame, text=label_text + " *", bg=BG_COLOR, font=label_font, fg=TEXT_COLOR, anchor="w").grid(row=0, column=0, sticky="w", columnspan=2 if field_type == "radiobutton" else 1)

    if field_type == "radiobutton":
        var = tk.StringVar()
        radio_frame = ttk.Frame(frame, style="TFrame")
        radio_frame.grid(row=1, column=0, sticky="w", pady=(0, 3))
        
        for i, option in enumerate(options):
            ttk.Radiobutton(radio_frame, text=option, value=option, variable=var, style="TRadiobutton").grid(row=0, column=i, sticky="w", padx=(0, 10))

        error_label = tk.Label(frame, text="", font=("Arial", 8), bg=BG_COLOR, fg=ERROR_COLOR)
        error_label.grid(row=2, column=0, columnspan=2, sticky="w")

        def clear_error(*args):
            error_label.config(text="")
            
        var.trace_add("write", clear_error)
        return var, error_label

    else:
        field = tk.Entry(frame, font=entry_font, width=22, bg=ENTRY_COLOR, highlightthickness=1, highlightbackground="#ddd")
        error_label = tk.Label(frame, text="", font=("Arial", 8), bg=BG_COLOR, fg=ERROR_COLOR)
        field.bind("<KeyRelease>", lambda e: validate_field(field, (min_val, max_val), error_label))
        field.grid(row=1, column=0, sticky="w", pady=(0, 3))
        tk.Label(frame, text=f"({min_val}-{max_val})", font=("Arial", 8), bg=BG_COLOR, fg="#777777").grid(row=1, column=1, sticky="w", padx=5)
        error_label.grid(row=2, column=0, columnspan=2, sticky="w")
        return field, error_label

def validate_field(widget, validation_range, error_label):
    value = widget.get()
    error_label.config(text="")
    if not value:
        return False
    try:
        num = float(value)
        if validation_range and (num < validation_range[0] or num > validation_range[1]):
            error_label.config(text=f"Must be between {validation_range[0]}-{validation_range[1]}")
            return False
        return True
    except ValueError:
        error_label.config(text="Numbers only")
        return False

fields = []
current_row = 1

field_definitions = [
    ("Age (years)", "entry", 18, 100),
    ("Gender", "radiobutton", ["Male", "Female"]),
    ("BMI", "entry", 10, 50),
    ("Alcohol Consumption (units/week)", "entry", 0, 30),
    ("Diet Quality", "entry", 1, 10),
    ("Family History of Alzheimer's", "radiobutton", ["Yes", "No"]),
    ("Head Injury", "radiobutton", ["Yes", "No"]),
    ("Cholesterol Total (mg/dL)", "entry", 100, 300),
    ("MMSE Score", "entry", 10, 30),
    ("Memory Complaints", "radiobutton", ["Yes", "No"]),
    ("Behavioral Problems", "radiobutton", ["Yes", "No"]),
    ("Activities of Daily Living", "entry", 0, 10),
    ("Confusion", "radiobutton", ["Yes", "No"]),
    ("Forgetfulness", "radiobutton", ["Yes", "No"])
]

for i, field_def in enumerate(field_definitions):
    if field_def[1] == "radiobutton":
        field, error = create_field(content_frame, field_def[0], current_row + i*2, "radiobutton", options=field_def[2])
    else:
        field, error = create_field(content_frame, field_def[0], current_row + i*2, "entry", min_val=field_def[2], max_val=field_def[3])
    fields.append({"widget": field, "error": error, "type": field_def[1], "required": True})

def predict():
    all_valid = True
    input_data = []

    for field in fields:
        error_label = field["error"]
        error_label.config(text="")
        
        if field["type"] == "radiobutton":
            value = field["widget"].get()
            if not value:
                error_label.config(text="This selection is required")
                all_valid = False
                continue
            input_data.append(1 if value == "Yes" else 0 if value == "No" else 0 if value == "Male" else 1)
        else:
            value = field["widget"].get()
            if not value:
                error_label.config(text="This field is required")
                all_valid = False
                continue
            try:
                num = float(value)
                field_def = field_definitions[fields.index(field)]
                min_val, max_val = field_def[2], field_def[3]
                if num < min_val or num > max_val:
                    error_label.config(text=f"Must be between {min_val}-{max_val}")
                    all_valid = False
                    continue
                input_data.append(num)
            except ValueError:
                error_label.config(text="Numbers only")
                all_valid = False
                continue

    if not all_valid:
        messagebox.showerror("Validation Error", "Please correct all highlighted fields")
        return

    if len(input_data) != 14:
        messagebox.showerror("Error", f"Expected 14 features but got {len(input_data)}")
        return

    try:
        prediction = model.predict([input_data])
        result = "High Risk" if prediction[0] == 1 else "Low Risk"
        result_window = tk.Toplevel(root)
        result_window.title("Assessment Result")
        result_window.geometry("350x180")
        result_window.configure(bg=BG_COLOR)
        result_color = "#ff1493" if prediction[0] == 1 else "#4b0082"
        icon = "⚠" if prediction[0] == 1 else "✅"

        tk.Label(result_window, text=f"{icon} {result} of Alzheimer's", font=title_font, bg=BG_COLOR, fg=result_color).pack(pady=20)
        tk.Label(result_window, text="This is a preliminary assessment.\nPlease consult with a healthcare professional.", font=("Arial", 10), bg=BG_COLOR).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Prediction Error", f"An error occurred during prediction:\n{str(e)}")

button_frame = ttk.Frame(content_frame, style="TFrame")
button_frame.grid(row=current_row + len(field_definitions)*2 + 2, column=0, pady=20)
ttk.Button(button_frame, text="Assess My Risk", command=predict).pack(ipadx=20, ipady=5)

footer = ttk.Frame(content_frame, style="TFrame")
footer.grid(row=current_row + len(field_definitions)*2 + 3, column=0, pady=(0, 20))
tk.Label(footer, text="* Required fields", font=("Arial", 8), bg=BG_COLOR, fg="#777777").pack()

root.mainloop()