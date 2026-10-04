import csv
import math

# Load disease-symptom knowledge base
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


# Get patient symptoms
patient_input = input(
    "Enter patient symptoms (comma separated): "
)

patient_symptoms = set(
    symptom.strip().lower()
    for symptom in patient_input.split(",")
)


# Calculate Bayesian score
probabilities = {}

total_diseases = len(knowledge_base)

for disease, symptoms in knowledge_base.items():

    matched = patient_symptoms.intersection(symptoms)

    # Prior probability
    prior = 1 / total_diseases

    # Calculate likelihood
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


# Sort diseases by probability
sorted_results = sorted(
    probabilities.items(),
    key=lambda x: x[1],
    reverse=True
)


# Display result
print("\n===== BAYESIAN REASONING RESULT =====\n")

for disease, probability in sorted_results:
    print(
        f"{disease}: {probability * 100:.2f}%"
    )

print("\n===== MOST LIKELY RESULT =====")

best_disease, best_probability = sorted_results[0]

print("Disease:", best_disease)
print(
    f"Estimated Probability: {best_probability * 100:.2f}%"
)

print(
    "\nNote: This is an educational prototype "
    "and not a clinical diagnosis."
)