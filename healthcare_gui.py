import csv
import heapq
import tkinter as tk
from tkinter import ttk, messagebox


# =========================================================
# LOAD KNOWLEDGE BASE
# =========================================================

file_path = "../dataset/knowledge_rules.csv"

knowledge_base = {}

with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        disease = row["disease"]
        symptom = row["symptom"]

        if disease not in knowledge_base:
            knowledge_base[disease] = set()

        knowledge_base[disease].add(symptom)


# =========================================================
# A* GRAPH
# =========================================================

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
    ],

    "Flu Assessment": [],
    "Pneumonia Assessment": [],
    "Malaria Assessment": [],
    "Migraine Assessment": [],
    "Typhoid Assessment": [],
    "Gastritis Assessment": []
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


disease_to_goal = {
    "Flu": "Flu Assessment",
    "Pneumonia": "Pneumonia Assessment",
    "Malaria": "Malaria Assessment",
    "Migraine": "Migraine Assessment",
    "Typhoid": "Typhoid Assessment",
    "Gastritis": "Gastritis Assessment"
}


# =========================================================
# A* SEARCH
# =========================================================

def a_star_search(start, goal):

    priority_queue = []

    heapq.heappush(
        priority_queue,
        (heuristic[start], 0, start, [start])
    )

    visited = set()

    while priority_queue:

        f, g, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path, g

        for neighbor, cost in graph[current]:

            new_g = g + cost
            new_f = new_g + heuristic[neighbor]

            heapq.heappush(
                priority_queue,
                (
                    new_f,
                    new_g,
                    neighbor,
                    path + [neighbor]
                )
            )

    return None, None


# =========================================================
# ANALYSIS FUNCTION
# =========================================================

def analyze_patient(patient_input):

    patient_symptoms = set(
        symptom.strip().lower()
        for symptom in patient_input.split(",")
        if symptom.strip()
    )

    if not patient_symptoms:
        return None

    # -----------------------------------------------------
    # LOGICAL REASONING
    # -----------------------------------------------------

    logical_results = {}

    for disease, symptoms in knowledge_base.items():

        matched = patient_symptoms.intersection(symptoms)

        if matched:
            logical_results[disease] = matched

    # -----------------------------------------------------
    # BAYESIAN REASONING
    # -----------------------------------------------------

    probabilities = {}

    total_diseases = len(knowledge_base)

    for disease, symptoms in knowledge_base.items():

        prior = 1 / total_diseases

        likelihood = 1.0

        for symptom in patient_symptoms:

            if symptom in symptoms:
                likelihood *= 0.8
            else:
                likelihood *= 0.2

        probabilities[disease] = prior * likelihood

    total_probability = sum(probabilities.values())

    if total_probability > 0:

        for disease in probabilities:

            probabilities[disease] = (
                probabilities[disease]
                / total_probability
            )

    sorted_results = sorted(
        probabilities.items(),
        key=lambda x: x[1],
        reverse=True
    )

    best_disease = sorted_results[0][0]
    best_probability = sorted_results[0][1]

    # -----------------------------------------------------
    # A* PATH
    # -----------------------------------------------------

    path = None
    path_cost = None

    if best_disease in disease_to_goal:

        goal = disease_to_goal[best_disease]

        path, path_cost = a_star_search(
            "Start",
            goal
        )

    return (
        patient_symptoms,
        logical_results,
        sorted_results,
        best_disease,
        best_probability,
        path,
        path_cost
    )


# =========================================================
# GUI FUNCTIONS
# =========================================================

def analyze():

    symptoms = symptom_entry.get().strip()

    if not symptoms:

        messagebox.showwarning(
            "Input Required",
            "Please enter at least one symptom."
        )

        return

    result = analyze_patient(symptoms)

    if result is None:
        return

    (
        patient_symptoms,
        logical_results,
        probabilities,
        best_disease,
        best_probability,
        path,
        path_cost
    ) = result

    # Clear previous output
    output_text.delete("1.0", tk.END)

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    output_text.insert(
        tk.END,
        "===== AI HEALTHCARE ANALYSIS =====\n\n"
    )

    output_text.insert(
        tk.END,
        "Patient Symptoms:\n"
    )

    output_text.insert(
        tk.END,
        ", ".join(sorted(patient_symptoms))
        + "\n\n"
    )

    # -----------------------------------------------------
    # LOGICAL REASONING
    # -----------------------------------------------------

    output_text.insert(
        tk.END,
        "===== LOGICAL REASONING =====\n\n"
    )

    if logical_results:

        for disease, matched in logical_results.items():

            output_text.insert(
                tk.END,
                f"{disease}\n"
            )

            output_text.insert(
                tk.END,
                "Matched Symptoms: "
                + ", ".join(sorted(matched))
                + "\n"
            )

            output_text.insert(
                tk.END,
                f"Number of Matches: {len(matched)}\n\n"
            )

    else:

        output_text.insert(
            tk.END,
            "No matching disease found.\n\n"
        )

    # -----------------------------------------------------
    # BAYESIAN REASONING
    # -----------------------------------------------------

    output_text.insert(
        tk.END,
        "===== BAYESIAN PROBABILITIES =====\n\n"
    )

    for disease, probability in probabilities:

        output_text.insert(
            tk.END,
            f"{disease:<25} "
            f"{probability * 100:.2f}%\n"
        )

    # -----------------------------------------------------
    # A* SEARCH
    # -----------------------------------------------------

    output_text.insert(
        tk.END,
        "\n===== A* DIAGNOSTIC PATH =====\n\n"
    )

    if path:

        for i, step in enumerate(path):

            output_text.insert(
                tk.END,
                step
            )

            if i < len(path) - 1:
                output_text.insert(
                    tk.END,
                    "  →  "
                )

        output_text.insert(
            tk.END,
            f"\n\nTotal Path Cost: {path_cost}\n"
        )

    else:

        output_text.insert(
            tk.END,
            "No diagnostic path available.\n"
        )

    # -----------------------------------------------------
    # DECISION SUPPORT
    # -----------------------------------------------------

    output_text.insert(
        tk.END,
        "\n===== DECISION SUPPORT =====\n\n"
    )

    output_text.insert(
        tk.END,
        f"Top Estimated Condition: {best_disease}\n"
    )

    output_text.insert(
        tk.END,
        f"Estimated Probability: "
        f"{best_probability * 100:.2f}%\n\n"
    )

    output_text.insert(
        tk.END,
        "Further medical evaluation is recommended.\n\n"
    )

    output_text.insert(
        tk.END,
        "Note: This is an educational prototype "
        "and not a clinical diagnosis."
    )


def clear_all():

    symptom_entry.delete(0, tk.END)

    output_text.delete(
        "1.0",
        tk.END
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "AI-Based Smart Healthcare Diagnosis and Decision Support System"
)

root.geometry("1000x700")

root.minsize(850, 600)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="AI-Based Smart Healthcare Diagnosis\n"
         "and Decision Support System",
    font=("Arial", 20, "bold"),
    pady=15
)

title_label.pack()


subtitle_label = tk.Label(
    root,
    text="Intelligent Agent • Logical Reasoning • Bayesian Reasoning • A* Search",
    font=("Arial", 10)
)

subtitle_label.pack(
    pady=(0, 15)
)


# =========================================================
# INPUT FRAME
# =========================================================

input_frame = tk.Frame(
    root,
    padx=20,
    pady=10
)

input_frame.pack(
    fill="x"
)


symptom_label = tk.Label(
    input_frame,
    text="Enter Patient Symptoms:",
    font=("Arial", 12, "bold")
)

symptom_label.pack(
    anchor="w"
)


symptom_entry = tk.Entry(
    input_frame,
    font=("Arial", 12)
)

symptom_entry.pack(
    fill="x",
    pady=8
)


example_label = tk.Label(
    input_frame,
    text="Example: fever,cough,body_pain,fatigue",
    font=("Arial", 9)
)

example_label.pack(
    anchor="w"
)


# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(
    root,
    pady=10
)

button_frame.pack()


analyze_button = tk.Button(
    button_frame,
    text="ANALYZE",
    command=analyze,
    font=("Arial", 11, "bold"),
    width=15,
    padx=10,
    pady=6
)

analyze_button.pack(
    side="left",
    padx=8
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_all,
    font=("Arial", 11, "bold"),
    width=15,
    padx=10,
    pady=6
)

clear_button.pack(
    side="left",
    padx=8
)


# =========================================================
# OUTPUT FRAME
# =========================================================

output_frame = tk.Frame(
    root,
    padx=20,
    pady=10
)

output_frame.pack(
    fill="both",
    expand=True
)


output_text = tk.Text(
    output_frame,
    font=("Consolas", 11),
    wrap="word"
)

output_text.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar = ttk.Scrollbar(
    output_frame,
    orient="vertical",
    command=output_text.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

output_text.configure(
    yscrollcommand=scrollbar.set
)


# =========================================================
# FOOTER
# =========================================================

footer_label = tk.Label(
    root,
    text="Educational AI Prototype | Not for clinical diagnosis",
    font=("Arial", 9),
    pady=8
)

footer_label.pack()


# =========================================================
# START GUI
# =========================================================

root.mainloop()