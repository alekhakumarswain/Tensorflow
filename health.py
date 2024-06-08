import tensorflow as tf

# Data: Mapping symptoms to treatments
symptom_treatment_mapping = {
    'headache': 'Crocin',
    'fatigue': 'Rest and hydration',
    'hypertension': 'Medication for hypertension',
    'migraine': 'Migraine-specific medication'
}

# Model Architecture
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(len(symptom_treatment_mapping),)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(symptom_treatment_mapping), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Dummy training data
X_train = tf.constant([[1, 0, 0, 1], [0, 1, 1, 0]])  # Example input features (binary encoding of symptoms)
y_train = tf.constant([[0, 1, 0, 0], [1, 0, 1, 0]])  # Example target labels (binary encoding of treatments)

# Training the model (dummy data used here)
model.fit(X_train, y_train, epochs=10)

# User Interaction
name = input("Enter patient's name: ")
age = int(input("Enter patient's age: "))
gender = input("Enter patient's gender: ")
symptoms = input("Enter patient's symptoms (comma-separated): ").split(',')

# Encoding symptoms into input features
input_features = [1 if symptom.strip().lower() in symptoms else 0 for symptom in symptom_treatment_mapping.keys()]
input_features = tf.constant([input_features])

# Predict treatment recommendations
treatment_probabilities = model.predict(input_features)[0]

# Generate health report
generated_health_report = f"""
Patient Name: {name}
Age: {age}
Gender: {gender.capitalize()}

Medical History:
- Hypertension
- Migraine

Current Symptoms:
{"".join([f"- {symptom.strip()}\n" for symptom in symptoms])}

Assessment:
The patient presents with symptoms consistent with migraine and hypertension. Further evaluation and management are recommended.

Treatment Recommendations:
{"".join([f"{i+1}. {treatment}: {round(probability*100, 2)}%\n" for i, (symptom, treatment), probability in zip(enumerate(symptom_treatment_mapping.items()), treatment_probabilities)])}

Follow-up:
Schedule a follow-up appointment in 2 weeks to assess treatment effectiveness and adjust management as necessary.
"""

# Consultation Support Response
consultation_response = """
Doctor: Based on the patient's symptoms and medical history, I recommend the following treatment plan:
- Crocin for headache
- Rest and hydration for fatigue
- Medication for hypertension
- Migraine-specific medication for migraine

Let's schedule a follow-up appointment in 2 weeks to evaluate progress and make any necessary adjustments to the treatment plan.
"""

# Print generated health report
print("Generated Health Report:")
print(generated_health_report)

# Print consultation support response
print("\nConsultation Support Response:")
print(consultation_response)

