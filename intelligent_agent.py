import csv
import heapq

# ==========================================
# 1. LOAD KNOWLEDGE BASE
# ==========================================

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


# ==========================================
# 2. GET PATIENT SYMPTOMS
# ==========================================

print("===== AI HEALTHCARE INTELLIGENT AGENT =====\n")

patient_input = input(
    "Enter patient symptoms (comma separated): "
)

patient_symptoms = set(
    symptom.strip().lower()
    for symptom in patient_input.split(",")
)


# ==========================================
# 3. LOGICAL REASONING
# ==========================================

results = {}

for disease, symptoms in knowledge_base.items():

    matched = patient_symptoms.intersection(symptoms)

    if matched:
        results[disease] = matched


print("\n===== LOGICAL REASONING =====\n")

if results:

    for disease, matched in results.items():

        print("Disease:", disease)
        print("Matched Symptoms:", ", ".join(matched))
        print("Number of Matches:", len(matched))
        print()

else:
    print("No matching disease found.")


# ==========================================
# 4. BAYESIAN REASONING
# ==========================================

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


# Normalize probabilities

total_probability = sum(probabilities.values())

if total_probability > 0:

    for disease in probabilities:

        probabilities[disease] = (
            probabilities[disease] / total_probability
        )


sorted_results = sorted(
    probabilities.items(),
    key=lambda x: x[1],
    reverse=True
)


print("===== BAYESIAN REASONING =====\n")

for disease, probability in sorted_results:

    print(
        f"{disease}: {probability * 100:.2f}%"
    )


best_disease = sorted_results[0][0]
best_probability = sorted_results[0][1]


# ==========================================
# 5. A* DIAGNOSTIC PATH
# ==========================================

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


# Map disease to A* goal

disease_to_goal = {

    "Flu": "Flu Assessment",
    "Pneumonia": "Pneumonia Assessment",
    "Malaria": "Malaria Assessment",
    "Migraine": "Migraine Assessment",
    "Typhoid": "Typhoid Assessment",
    "Gastritis": "Gastritis Assessment"
}


def a_star_search(start, goal):

    priority_queue = []

    heapq.heappush(
        priority_queue,
        (heuristic[start], 0, start, [start])
    )

    visited = set()

    while priority_queue:

        f, g, current, path = heapq.heappop(
            priority_queue
        )

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


# ==========================================
# 6. INTELLIGENT AGENT DECISION
# ==========================================

print("\n===== INTELLIGENT AGENT DECISION =====\n")

print(
    "Top Estimated Disease:",
    best_disease
)

print(
    f"Estimated Probability: "
    f"{best_probability * 100:.2f}%"
)


# Find A* path for supported disease

if best_disease in disease_to_goal:

    goal = disease_to_goal[best_disease]

    path, cost = a_star_search(
        "Start",
        goal
    )

    print("\nA* Diagnostic Path:")

    for step in path:

        print(" ->", step)

    print("Total Path Cost:", cost)

else:

    print(
        "\nNo A* diagnostic path available "
        "for this disease."
    )


# ==========================================
# 7. FINAL DECISION SUPPORT
# ==========================================

print("\n===== DECISION SUPPORT =====\n")

print(
    "The system identified",
    best_disease,
    "as the highest-scoring condition "
    "in this prototype."
)

print(
    "Further medical evaluation is recommended."
)

print(
    "\nNote: This system is an educational "
    "prototype and is not a clinical diagnosis."
)