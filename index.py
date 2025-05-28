import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont

df = pd.read_csv('alzheimers_disease_data.csv')
X = df.drop(['Diagnosis', 'PatientID', 'DoctorInCharge'], axis=1) #features
y = df['Diagnosis'] #target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = GaussianNB()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)  # Compute test accuracy

BG_COLOR = "#fff0f5"
HEADER_COLOR = "#db7093"
ENTRY_COLOR = "#ffffff"
ERROR_COLOR = "#ff1493"
TEXT_COLOR = "#800080"

root = tk.Tk()
root.title("Alzheimer's Risk Assessment")
root.geometry("450x550")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use('default')
style.configure("Vertical.TScrollbar", background=ENTRY_COLOR, troughcolor=ENTRY_COLOR, arrowcolor=HEADER_COLOR)
style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
style.configure("TButton", background=HEADER_COLOR, foreground="white")
style.configure("TRadiobutton", background=BG_COLOR, foreground=TEXT_COLOR)

title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
text_font = tkFont.Font(family="Arial", size=11)

main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

content_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

title_label = tk.Label(content_frame, text="Alzheimer's Risk Assessment", font=title_font, bg=BG_COLOR, fg=HEADER_COLOR)
subtitle_label = tk.Label(content_frame, text="Complete all fields to assess your Alzheimer's risk", font=("Arial", 10), bg=BG_COLOR, fg=TEXT_COLOR)
title_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
subtitle_label.grid(row=1, column=0, pady=(0, 15), sticky="w")

def create_field(parent, label_text, row, field_type, options=None, min_val=None, max_val=None):
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=0, sticky="w", pady=3)

    tk.Label(frame, text=label_text + " *", bg=BG_COLOR, font=text_font, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w")

    if field_type == "radiobutton":
        var = tk.StringVar()
        radio_frame = ttk.Frame(frame)
        radio_frame.grid(row=1, column=0, sticky="w")
        for i, option in enumerate(options):
            ttk.Radiobutton(radio_frame, text=option, value=option, variable=var).grid(row=0, column=i, sticky="w", padx=(0, 10))
        error_label = tk.Label(frame, text="", font=("Arial", 8), bg=BG_COLOR, fg=ERROR_COLOR)
        error_label.grid(row=2, column=0, sticky="w")
        var.trace_add("write", lambda *args: error_label.config(text=""))
        return var, error_label
    else:
        entry = tk.Entry(frame, font=text_font, width=22, bg=ENTRY_COLOR, highlightthickness=1, highlightbackground="#ddd")
        entry.grid(row=1, column=0, sticky="w")
        tk.Label(frame, text=f"({min_val}-{max_val})", font=("Arial", 8), bg=BG_COLOR, fg="#777").grid(row=1, column=1, sticky="w", padx=5)
        error_label = tk.Label(frame, text="", font=("Arial", 8), bg=BG_COLOR, fg=ERROR_COLOR)
        error_label.grid(row=2, column=0, columnspan=2, sticky="w")
        entry.bind("<KeyRelease>", lambda e: validate_field(entry, (min_val, max_val), error_label))
        return entry, error_label

def validate_field(widget, validation_range, error_label):
    value = widget.get()
    error_label.config(text="")
    try:
        num = float(value)
        if validation_range and (num < validation_range[0] or num > validation_range[1]):
            error_label.config(text=f"Must be between {validation_range[0]}-{validation_range[1]}")
            return False
        return True
    except ValueError:
        if value:
            error_label.config(text="Numbers only")
        return False

fields = []
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
        widget, error = create_field(content_frame, field_def[0], i * 2 + 2, "radiobutton", options=field_def[2])
    else:
        widget, error = create_field(content_frame, field_def[0], i * 2 + 2, "entry", min_val=field_def[2], max_val=field_def[3])
    fields.append({"widget": widget, "error": error, "type": field_def[1]})

def predict():
    all_valid = True
    input_data = []

    for idx, field in enumerate(fields):
        widget, error_label, field_type = field["widget"], field["error"], field["type"]
        error_label.config(text="")

        if field_type == "radiobutton":
            val = widget.get()
            if not val:
                error_label.config(text="This selection is required")
                all_valid = False
            else:
                input_data.append(1 if val in ["Yes", "Female"] else 0)
        else:
            val = widget.get()
            if not val:
                error_label.config(text="This field is required")
                all_valid = False
                continue
            try:
                num = float(val)
                min_val, max_val = field_definitions[idx][2], field_definitions[idx][3]
                if not (min_val <= num <= max_val):
                    error_label.config(text=f"Must be between {min_val}-{max_val}")
                    all_valid = False
                else:
                    input_data.append(num)
            except ValueError:
                error_label.config(text="Numbers only")
                all_valid = False

    if not all_valid:
        messagebox.showerror("Validation Error", "Please correct all highlighted fields")
        return

    try:
        input_df = pd.DataFrame([input_data], columns=X_train.columns)
        prediction = model.predict(input_df)
        result = "High Risk" if prediction[0] == 1 else "Low Risk"
        result_window = tk.Toplevel(root)
        result_window.title("Assessment Result")
        result_window.geometry("350x220")  # Increased height for extra label
        result_window.configure(bg=BG_COLOR)
        result_color = "#ff1493" if result == "High Risk" else "#4b0082"
        icon = "⚠" if result == "High Risk" else "✅"

        tk.Label(result_window, text=f"{icon} {result} of Alzheimer's", font=title_font, bg=BG_COLOR, fg=result_color).pack(pady=20)
        tk.Label(result_window, text=f"Model Test Accuracy: {accuracy*100:.2f}%", font=("Arial", 10), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
        tk.Label(result_window, text="This is a preliminary assessment.\nPlease consult a healthcare professional.", font=("Arial", 10), bg=BG_COLOR).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Prediction Error", f"An error occurred during prediction:\n{str(e)}")

ttk.Button(content_frame, text="Assess My Risk", command=predict).grid(row=len(field_definitions)*2 + 2, column=0, pady=20)

tk.Label(content_frame, text="* Required fields", font=("Arial", 8), bg=BG_COLOR, fg="#777").grid(row=len(field_definitions)*2 + 3, column=0, pady=(0, 20))

root.mainloop()