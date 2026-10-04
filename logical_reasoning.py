import csv

# Load knowledge base from CSV
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


# Get symptoms from the patient
patient_input = input(
    "Enter patient symptoms (comma separated): "
)

patient_symptoms = set(
    symptom.strip().lower()
    for symptom in patient_input.split(",")
)


# Logical reasoning
results = {}

for disease, symptoms in knowledge_base.items():

    matched_symptoms = patient_symptoms.intersection(symptoms)

    if matched_symptoms:
        results[disease] = matched_symptoms


# Display results
print("\n===== LOGICAL REASONING RESULT =====\n")

if results:
    for disease, matched in results.items():
        print("Disease:", disease)
        print("Matched Symptoms:", ", ".join(matched))
        print("Number of Matches:", len(matched))
        print()
else:
    print("No matching disease found.")