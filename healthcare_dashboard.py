import tkinter as tk
from tkinter import messagebox
import csv
import math
from datetime import datetime


# ============================================================
# COLORS
# ============================================================

BG = "#F4F7FB"
NAVY = "#172554"
BLUE = "#2563EB"
CYAN = "#06B6D4"
PURPLE = "#7C3AED"
GREEN = "#10B981"
ORANGE = "#F59E0B"
RED = "#EF4444"
WHITE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#64748B"
LIGHT_BLUE = "#EFF6FF"
LIGHT_GREEN = "#ECFDF5"
LIGHT_PURPLE = "#F5F3FF"
LIGHT_ORANGE = "#FFFBEB"
BORDER = "#E2E8F0"


# ============================================================
# KNOWLEDGE BASE
# ============================================================

file_path = "../dataset/knowledge_rules.csv"

knowledge_base = {}

try:
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            disease = row["disease"]
            symptom = row["symptom"].strip().lower()

            if disease not in knowledge_base:
                knowledge_base[disease] = set()

            knowledge_base[disease].add(symptom)

except Exception as e:
    print("Knowledge Base Error:", e)


# ============================================================
# BAYESIAN REASONING
# ============================================================

def bayesian_reasoning(patient_symptoms):

    diseases = list(knowledge_base.keys())

    if not diseases:
        return {}

    scores = {}

    prior = 1 / len(diseases)

    for disease, symptoms in knowledge_base.items():

        probability = prior

        for symptom in patient_symptoms:

            if symptom in symptoms:
                probability *= 0.8
            else:
                probability *= 0.2

        scores[disease] = probability

    total = sum(scores.values())

    if total == 0:
        return {}

    probabilities = {}

    for disease, score in scores.items():
        probabilities[disease] = (score / total) * 100

    return dict(
        sorted(
            probabilities.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )


# ============================================================
# A* SEARCH
# ============================================================

graph = {

    "Start": [
        ("Fever Check", 1)
    ],

    "Fever Check": [
        ("Respiratory Check", 2),
        ("Pain Check", 2),
        ("Digestive Check", 3)
    ],

    "Respiratory Check": [
        ("Flu Assessment", 2),
        ("Pneumonia Assessment", 2)
    ],

    "Pain Check": [
        ("Malaria Assessment", 2),
        ("Migraine Assessment", 3)
    ],

    "Digestive Check": [
        ("Typhoid Assessment", 2),
        ("Gastritis Assessment", 2)
    ]
}


heuristic = {

    "Start": 5,
    "Fever Check": 4,
    "Respiratory Check": 2,
    "Pain Check": 2,
    "Digestive Check": 2,

    "Flu Assessment": 0,
    "Pneumonia Assessment": 0,
    "Malaria Assessment": 0,
    "Migraine Assessment": 0,
    "Typhoid Assessment": 0,
    "Gastritis Assessment": 0
}


def a_star_search():

    open_list = [(heuristic["Start"], 0, "Start", ["Start"])]
    visited = set()

    while open_list:

        open_list.sort(key=lambda x: x[0])

        f, cost, current, path = open_list.pop(0)

        if current in visited:
            continue

        visited.add(current)

        if current.endswith("Assessment"):

            return path, cost

        for next_node, edge_cost in graph.get(current, []):

            new_cost = cost + edge_cost

            new_f = new_cost + heuristic.get(next_node, 0)

            open_list.append(
                (
                    new_f,
                    new_cost,
                    next_node,
                    path + [next_node]
                )
            )

    return [], 0


# ============================================================
# LOGICAL REASONING
# ============================================================

def logical_reasoning(patient_symptoms):

    results = {}

    for disease, symptoms in knowledge_base.items():

        matched = patient_symptoms.intersection(symptoms)

        if matched:
            results[disease] = matched

    return results


# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_patient():

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_var.get()
    patient_id = id_entry.get().strip()

    symptom_text = symptoms_entry.get().strip()

    if not name:
        messagebox.showwarning(
            "Missing Information",
            "Please enter the patient's name."
        )
        return

    if not age:
        messagebox.showwarning(
            "Missing Information",
            "Please enter the patient's age."
        )
        return

    if not symptom_text:

        messagebox.showwarning(
            "Missing Symptoms",
            "Please enter at least one symptom."
        )

        return

    patient_symptoms = set(
        symptom.strip().lower()
        for symptom in symptom_text.split(",")
        if symptom.strip()
    )

    logical_results = logical_reasoning(patient_symptoms)

    probabilities = bayesian_reasoning(patient_symptoms)

    if not probabilities:

        messagebox.showerror(
            "Analysis Error",
            "Unable to analyse the entered symptoms."
        )

        return

    top_disease = next(iter(probabilities))
    top_probability = probabilities[top_disease]

    path, path_cost = a_star_search()

    update_dashboard(
        name,
        age,
        gender,
        patient_id,
        patient_symptoms,
        logical_results,
        probabilities,
        top_disease,
        top_probability,
        path,
        path_cost
    )


# ============================================================
# UPDATE DASHBOARD
# ============================================================

def update_dashboard(
    name,
    age,
    gender,
    patient_id,
    patient_symptoms,
    logical_results,
    probabilities,
    top_disease,
    top_probability,
    path,
    path_cost
):

    # Clear result area

    for widget in result_frame.winfo_children():
        widget.destroy()

    # --------------------------------------------------------
    # PATIENT PROFILE
    # --------------------------------------------------------

    profile_card = tk.Frame(
        result_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    profile_card.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    profile_title = tk.Label(
        profile_card,
        text="👤  Patient Overview",
        font=("Segoe UI", 15, "bold"),
        bg=WHITE,
        fg=NAVY
    )

    profile_title.pack(
        anchor="w",
        padx=22,
        pady=(18, 10)
    )

    profile_info = tk.Frame(
        profile_card,
        bg=WHITE
    )

    profile_info.pack(
        fill="x",
        padx=22,
        pady=(0, 18)
    )

    create_info_box(
        profile_info,
        "PATIENT",
        name,
        0
    )

    create_info_box(
        profile_info,
        "AGE",
        age,
        1
    )

    create_info_box(
        profile_info,
        "GENDER",
        gender,
        2
    )

    create_info_box(
        profile_info,
        "PATIENT ID",
        patient_id if patient_id else "Not provided",
        3
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    kpi_frame = tk.Frame(
        result_frame,
        bg=BG
    )

    kpi_frame.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    create_kpi_card(
        kpi_frame,
        "🩺",
        "TOP CONDITION",
        top_disease,
        BLUE,
        0
    )

    create_kpi_card(
        kpi_frame,
        "📊",
        "AI MODEL ESTIMATE",
        f"{top_probability:.2f}%",
        PURPLE,
        1
    )

    create_kpi_card(
        kpi_frame,
        "🔎",
        "SYMPTOMS FOUND",
        str(len(patient_symptoms)),
        CYAN,
        2
    )

    create_kpi_card(
        kpi_frame,
        "🧠",
        "CONDITIONS CHECKED",
        str(len(probabilities)),
        GREEN,
        3
    )

    # --------------------------------------------------------
    # HEALTH SUMMARY
    # --------------------------------------------------------

    summary_card = tk.Frame(
        result_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    summary_card.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    tk.Label(
        summary_card,
        text="📊  AI Health Analysis",
        font=("Segoe UI", 16, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(
        anchor="w",
        padx=22,
        pady=(18, 4)
    )

    tk.Label(
        summary_card,
        text="Possible conditions based on the symptoms entered",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 15)
    )

    probability_frame = tk.Frame(
        summary_card,
        bg=WHITE
    )

    probability_frame.pack(
        fill="x",
        padx=22,
        pady=(0, 20)
    )

    # Show top 6 conditions

    for index, (disease, probability) in enumerate(
        list(probabilities.items())[:6]
    ):

        row = tk.Frame(
            probability_frame,
            bg=WHITE
        )

        row.pack(
            fill="x",
            pady=7
        )

        disease_label = tk.Label(
            row,
            text=disease,
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT,
            width=24,
            anchor="w"
        )

        disease_label.pack(
            side="left"
        )

        bar_bg = tk.Frame(
            row,
            bg="#E8EEF7",
            height=12
        )

        bar_bg.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        bar_bg.pack_propagate(False)

        bar_width = max(
            5,
            min(100, probability)
        )

        bar_color = (
            BLUE if index == 0
            else CYAN if index == 1
            else PURPLE
        )

        bar = tk.Frame(
            bar_bg,
            bg=bar_color,
            width=int(bar_width * 3)
        )

        bar.pack(
            side="left",
            fill="y"
        )

        value_label = tk.Label(
            row,
            text=f"{probability:.2f}%",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=TEXT,
            width=8,
            anchor="e"
        )

        value_label.pack(
            side="right"
        )

    # --------------------------------------------------------
    # SYMPTOMS
    # --------------------------------------------------------

    lower_frame = tk.Frame(
        result_frame,
        bg=BG
    )

    lower_frame.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    symptoms_card = tk.Frame(
        lower_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    symptoms_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 9)
    )

    tk.Label(
        symptoms_card,
        text="🩹  Symptoms Entered",
        font=("Segoe UI", 15, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(
        anchor="w",
        padx=20,
        pady=(18, 12)
    )

    chips_frame = tk.Frame(
        symptoms_card,
        bg=WHITE
    )

    chips_frame.pack(
        fill="x",
        padx=20,
        pady=(0, 20)
    )

    for symptom in patient_symptoms:

        chip = tk.Label(
            chips_frame,
            text="  " + symptom.replace("_", " ").title() + "  ",
            font=("Segoe UI", 9, "bold"),
            bg=LIGHT_BLUE,
            fg=BLUE,
            padx=6,
            pady=5
        )

        chip.pack(
            side="left",
            padx=4,
            pady=4
        )

    # --------------------------------------------------------
    # DECISION SUPPORT
    # --------------------------------------------------------

    decision_card = tk.Frame(
        lower_frame,
        bg=LIGHT_GREEN,
        highlightbackground="#A7F3D0",
        highlightthickness=1
    )

    decision_card.pack(
        side="right",
        fill="both",
        expand=True,
        padx=(9, 0)
    )

    tk.Label(
        decision_card,
        text="💡  AI Decision Support",
        font=("Segoe UI", 15, "bold"),
        bg=LIGHT_GREEN,
        fg="#047857"
    ).pack(
        anchor="w",
        padx=20,
        pady=(18, 10)
    )

    tk.Label(
        decision_card,
        text=f"Highest-scoring condition\n\n{top_disease}",
        font=("Segoe UI", 15, "bold"),
        bg=LIGHT_GREEN,
        fg="#065F46",
        justify="left"
    ).pack(
        anchor="w",
        padx=20
    )

    tk.Label(
        decision_card,
        text=(
            "\nFurther medical evaluation is recommended.\n"
            "This result is an AI model estimate."
        ),
        font=("Segoe UI", 10),
        bg=LIGHT_GREEN,
        fg="#047857",
        justify="left"
    ).pack(
        anchor="w",
        padx=20,
        pady=(4, 18)
    )

    # --------------------------------------------------------
    # A* JOURNEY
    # --------------------------------------------------------

    journey_card = tk.Frame(
        result_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    journey_card.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    tk.Label(
        journey_card,
        text="🧭  AI Diagnostic Journey",
        font=("Segoe UI", 16, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(
        anchor="w",
        padx=22,
        pady=(18, 3)
    )

    tk.Label(
        journey_card,
        text="A* search path used by the prototype",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 12)
    )

    journey_canvas = tk.Canvas(
        journey_card,
        height=120,
        bg=WHITE,
        highlightthickness=0
    )

    journey_canvas.pack(
        fill="x",
        padx=15,
        pady=(0, 10)
    )

    draw_journey(
        journey_canvas,
        path
    )

    tk.Label(
        journey_card,
        text=f"Total Path Cost: {path_cost}",
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=PURPLE
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 18)
    )

    # --------------------------------------------------------
    # LOGICAL REASONING
    # --------------------------------------------------------

    logic_card = tk.Frame(
        result_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    logic_card.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    tk.Label(
        logic_card,
        text="🧠  Logical Reasoning",
        font=("Segoe UI", 16, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(
        anchor="w",
        padx=22,
        pady=(18, 3)
    )

    tk.Label(
        logic_card,
        text="Symptoms matched with the healthcare knowledge base",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 12)
    )

    logic_text = tk.Text(
        logic_card,
        height=9,
        font=("Consolas", 10),
        bg="#F8FAFC",
        fg=TEXT,
        relief="flat",
        padx=15,
        pady=12
    )

    logic_text.pack(
        fill="x",
        padx=22,
        pady=(0, 20)
    )

    if logical_results:

        for disease, matched in logical_results.items():

            logic_text.insert(
                "end",
                f"{disease}\n"
            )

            logic_text.insert(
                "end",
                f"  Matched: {', '.join(sorted(matched))}\n"
            )

            logic_text.insert(
                "end",
                f"  Matches: {len(matched)}\n\n"
            )

    else:

        logic_text.insert(
            "end",
            "No matching condition found."
        )

    logic_text.config(
        state="disabled"
    )

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    disclaimer = tk.Frame(
        result_frame,
        bg=LIGHT_ORANGE,
        highlightbackground="#FDE68A",
        highlightthickness=1
    )

    disclaimer.pack(
        fill="x",
        padx=30,
        pady=(0, 30)
    )

    tk.Label(
        disclaimer,
        text="⚠️  Important",
        font=("Segoe UI", 11, "bold"),
        bg=LIGHT_ORANGE,
        fg="#92400E"
    ).pack(
        anchor="w",
        padx=18,
        pady=(12, 2)
    )

    tk.Label(
        disclaimer,
        text=(
            "This is an educational AI prototype. "
            "The displayed estimate is not a medical diagnosis "
            "and should not replace professional medical advice."
        ),
        font=("Segoe UI", 9),
        bg=LIGHT_ORANGE,
        fg="#92400E",
        wraplength=850,
        justify="left"
    ).pack(
        anchor="w",
        padx=18,
        pady=(0, 12)
    )

    # Scroll back to top

    canvas.yview_moveto(0)


# ============================================================
# INFO BOX
# ============================================================

def create_info_box(parent, title, value, column):

    box = tk.Frame(
        parent,
        bg="#F8FAFC"
    )

    box.grid(
        row=0,
        column=column,
        sticky="ew",
        padx=5
    )

    parent.grid_columnconfigure(
        column,
        weight=1
    )

    tk.Label(
        box,
        text=title,
        font=("Segoe UI", 8, "bold"),
        bg="#F8FAFC",
        fg=MUTED
    ).pack(
        anchor="w",
        padx=12,
        pady=(10, 2)
    )

    tk.Label(
        box,
        text=value,
        font=("Segoe UI", 11, "bold"),
        bg="#F8FAFC",
        fg=TEXT
    ).pack(
        anchor="w",
        padx=12,
        pady=(0, 10)
    )


# ============================================================
# KPI CARD
# ============================================================

def create_kpi_card(parent, icon, title, value, accent, column):

    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=5
    )

    parent.grid_columnconfigure(
        column,
        weight=1
    )

    tk.Label(
        card,
        text=icon,
        font=("Segoe UI Emoji", 20),
        bg=WHITE,
        fg=accent
    ).pack(
        anchor="w",
        padx=16,
        pady=(12, 0)
    )

    tk.Label(
        card,
        text=title,
        font=("Segoe UI", 8, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=16,
        pady=(4, 2)
    )

    tk.Label(
        card,
        text=value,
        font=("Segoe UI", 13, "bold"),
        bg=WHITE,
        fg=accent
    ).pack(
        anchor="w",
        padx=16,
        pady=(0, 14)
    )


# ============================================================
# A* JOURNEY DRAWING
# ============================================================

def draw_journey(canvas, path):

    if not path:
        return

    canvas.update_idletasks()

    width = canvas.winfo_width()

    if width < 500:
        width = 800

    count = len(path)

    spacing = width / (count + 1)

    y = 55

    for i, node in enumerate(path):

        x = spacing * (i + 1)

        # Connection line

        if i < count - 1:

            next_x = spacing * (i + 2)

            canvas.create_line(
                x + 14,
                y,
                next_x - 14,
                y,
                fill=CYAN,
                width=4
            )

        # Circle

        canvas.create_oval(
            x - 15,
            y - 15,
            x + 15,
            y + 15,
            fill=BLUE,
            outline=WHITE,
            width=3
        )

        # Number

        canvas.create_text(
            x,
            y,
            text=str(i + 1),
            fill=WHITE,
            font=("Segoe UI", 9, "bold")
        )

        # Label

        label = node.replace(
            " Assessment",
            ""
        ).replace(
            " Check",
            " Check"
        )

        canvas.create_text(
            x,
            y + 38,
            text=label,
            fill=TEXT,
            font=("Segoe UI", 9, "bold"),
            width=130
        )


# ============================================================
# NEW PATIENT
# ============================================================

def clear_patient():

    name_entry.delete(
        0,
        "end"
    )

    age_entry.delete(
        0,
        "end"
    )

    id_entry.delete(
        0,
        "end"
    )

    symptoms_entry.delete(
        0,
        "end"
    )

    gender_var.set(
        "Female"
    )

    for widget in result_frame.winfo_children():
        widget.destroy()

    create_welcome_message()


# ============================================================
# WELCOME MESSAGE
# ============================================================

def create_welcome_message():

    welcome = tk.Frame(
        result_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    welcome.pack(
        fill="x",
        padx=30,
        pady=30
    )

    tk.Label(
        welcome,
        text="👋  Ready for Analysis",
        font=("Segoe UI", 20, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(
        pady=(35, 8)
    )

    tk.Label(
        welcome,
        text=(
            "Enter patient information and symptoms on the left.\n"
            "Click  ANALYZE PATIENT  to start the AI assessment."
        ),
        font=("Segoe UI", 11),
        bg=WHITE,
        fg=MUTED,
        justify="center"
    ).pack(
        pady=(0, 35)
    )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "HealthAI - Smart Healthcare Decision Support"
)

root.geometry(
    "1250x850"
)

root.minsize(
    1050,
    700
)

root.configure(
    bg=BG
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=NAVY,
    height=85
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


brand_frame = tk.Frame(
    header,
    bg=NAVY
)

brand_frame.pack(
    side="left",
    padx=28
)

tk.Label(
    brand_frame,
    text="🩺",
    font=("Segoe UI Emoji", 28),
    bg=NAVY,
    fg=WHITE
).pack(
    side="left",
    padx=(0, 10)
)

title_frame = tk.Frame(
    brand_frame,
    bg=NAVY
)

title_frame.pack(
    side="left"
)

tk.Label(
    title_frame,
    text="HealthAI",
    font=("Segoe UI", 20, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(
    anchor="w"
)

tk.Label(
    title_frame,
    text="Smart Healthcare Decision Support",
    font=("Segoe UI", 9),
    bg=NAVY,
    fg="#CBD5E1"
).pack(
    anchor="w"
)


# System status

status_frame = tk.Frame(
    header,
    bg=NAVY
)

status_frame.pack(
    side="right",
    padx=28
)

tk.Label(
    status_frame,
    text="●  AI ENGINE READY",
    font=("Segoe UI", 9, "bold"),
    bg=NAVY,
    fg="#6EE7B7"
).pack(
    pady=(20, 2)
)

tk.Label(
    status_frame,
    text=datetime.now().strftime("%d %b %Y"),
    font=("Segoe UI", 8),
    bg=NAVY,
    fg="#CBD5E1"
).pack()


# ============================================================
# BODY
# ============================================================

body = tk.Frame(
    root,
    bg=BG
)

body.pack(
    fill="both",
    expand=True
)


# ============================================================
# LEFT SIDEBAR
# ============================================================

sidebar = tk.Frame(
    body,
    bg=WHITE,
    width=320,
    highlightbackground=BORDER,
    highlightthickness=1
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


tk.Label(
    sidebar,
    text="Patient Assessment",
    font=("Segoe UI", 17, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(
    anchor="w",
    padx=24,
    pady=(25, 4)
)

tk.Label(
    sidebar,
    text="Enter details to begin",
    font=("Segoe UI", 9),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=24,
    pady=(0, 20)
)


# Patient name

tk.Label(
    sidebar,
    text="PATIENT NAME",
    font=("Segoe UI", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=24
)

name_entry = tk.Entry(
    sidebar,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE
)

name_entry.pack(
    fill="x",
    padx=24,
    pady=(5, 15),
    ipady=9
)


# Age

tk.Label(
    sidebar,
    text="AGE",
    font=("Segoe UI", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=24
)

age_entry = tk.Entry(
    sidebar,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE
)

age_entry.pack(
    fill="x",
    padx=24,
    pady=(5, 15),
    ipady=9
)


# Gender

tk.Label(
    sidebar,
    text="GENDER",
    font=("Segoe UI", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=24
)

gender_var = tk.StringVar(
    value="Female"
)

gender_menu = tk.OptionMenu(
    sidebar,
    gender_var,
    "Female",
    "Male",
    "Other"
)

gender_menu.config(
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=0
)

gender_menu["menu"].config(
    font=("Segoe UI", 10)
)

gender_menu.pack(
    fill="x",
    padx=24,
    pady=(5, 15)
)


# Patient ID

tk.Label(
    sidebar,
    text="PATIENT ID",
    font=("Segoe UI", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=24
)

id_entry = tk.Entry(
    sidebar,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE
)

id_entry.pack(
    fill="x",
    padx=24,
    pady=(5, 15),
    ipady=9
)


# Symptoms

tk.Label(
    sidebar,
    text="SYMPTOMS",
    font=("Segoe UI", 8, "bold"),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=24
)

symptoms_entry = tk.Entry(
    sidebar,
    font=("Segoe UI", 10),
    bg="#F8FAFC",
    fg=TEXT,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER,
    highlightcolor=BLUE
)

symptoms_entry.pack(
    fill="x",
    padx=24,
    pady=(5, 3),
    ipady=9
)

tk.Label(
    sidebar,
    text="Example: fever,cough,fatigue",
    font=("Segoe UI", 8),
    bg=WHITE,
    fg=MUTED
).pack(
    anchor="w",
    padx=24,
    pady=(0, 18)
)


# Analyze button

analyze_button = tk.Button(
    sidebar,
    text="🔍  ANALYZE PATIENT",
    command=analyze_patient,
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#1D4ED8",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    pady=12
)

analyze_button.pack(
    fill="x",
    padx=24,
    pady=(5, 10)
)


# New patient button

new_button = tk.Button(
    sidebar,
    text="↻  NEW PATIENT",
    command=clear_patient,
    font=("Segoe UI", 10, "bold"),
    bg="#EFF6FF",
    fg=BLUE,
    activebackground="#DBEAFE",
    activeforeground=BLUE,
    relief="flat",
    cursor="hand2",
    pady=10
)

new_button.pack(
    fill="x",
    padx=24
)


# AI information

info_box = tk.Frame(
    sidebar,
    bg=LIGHT_PURPLE
)

info_box.pack(
    fill="x",
    padx=24,
    pady=25
)

tk.Label(
    info_box,
    text="🧠  AI METHODS",
    font=("Segoe UI", 9, "bold"),
    bg=LIGHT_PURPLE,
    fg=PURPLE
).pack(
    anchor="w",
    padx=14,
    pady=(12, 5)
)

tk.Label(
    info_box,
    text=(
        "• Logical Reasoning\n"
        "• Bayesian Reasoning\n"
        "• A* Search\n"
        "• Intelligent Agent"
    ),
    font=("Segoe UI", 8),
    bg=LIGHT_PURPLE,
    fg="#5B21B6",
    justify="left"
).pack(
    anchor="w",
    padx=14,
    pady=(0, 12)
)


# ============================================================
# RIGHT SCROLLABLE AREA
# ============================================================

right_container = tk.Frame(
    body,
    bg=BG
)

right_container.pack(
    side="right",
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    right_container,
    bg=BG,
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    right_container,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


result_frame = tk.Frame(
    canvas,
    bg=BG
)

canvas_window = canvas.create_window(
    (0, 0),
    window=result_frame,
    anchor="nw"
)


def configure_scroll(event):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_canvas(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


result_frame.bind(
    "<Configure>",
    configure_scroll
)

canvas.bind(
    "<Configure>",
    resize_canvas
)


# Mouse wheel scrolling

def mouse_scroll(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# Initial screen

create_welcome_message()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()