import csv

# Load knowledge rules
file_path = "../dataset/knowledge_rules.csv"

knowledge_base = {}

with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        disease = row["disease"]
        symptom = row["symptom"]

        if disease not in knowledge_base:
            knowledge_base[disease] = []

        knowledge_base[disease].append(symptom)

# Display Knowledge Base
print("===== HEALTHCARE KNOWLEDGE BASE =====\n")

for disease, symptoms in knowledge_base.items():
    print("Disease:", disease)
    print("Symptoms:", ", ".join(symptoms))
    print()