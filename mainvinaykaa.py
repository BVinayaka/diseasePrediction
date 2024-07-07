from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from joblib import load
import requests

app = Flask(__name__)
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTkzN2YwYjgtZDQ2MS00OGJkLTg0NDItYTM5M2NhNWU0NTg0IiwidHlwZSI6ImFwaV90b2tlbiJ9.K1s4lp6Nl-7Bd4UFEfKDN_GQl-CIISWcJZxKLEMU9xc"
}



# Load pre-trained model
clf = load("C:/Users/vinay/Documents/Disease-Prediction-from-Symptoms-master/saved_model/decision_tree.joblib")

# Define symptoms
symptoms = {'itching': 0, 'skin_rash': 0, 'nodal_skin_eruptions': 0, 'continuous_sneezing': 0,
            'shivering': 0, 'chills': 0, 'joint_pain': 0, 'stomach_pain': 0, 'acidity': 0, 'ulcers_on_tongue': 0,
            'muscle_wasting': 0, 'vomiting': 0, 'burning_micturition': 0, 'spotting_ urination': 0, 'fatigue': 0,
            'weight_gain': 0, 'anxiety': 0, 'cold_hands_and_feets': 0, 'mood_swings': 0, 'weight_loss': 0,
            'restlessness': 0, 'lethargy': 0, 'patches_in_throat': 0, 'irregular_sugar_level': 0, 'cough': 0,
            'high_fever': 0, 'sunken_eyes': 0, 'breathlessness': 0, 'sweating': 0, 'dehydration': 0,
            'indigestion': 0, 'headache': 0, 'yellowish_skin': 0, 'dark_urine': 0, 'nausea': 0, 'loss_of_appetite': 0,
            'pain_behind_the_eyes': 0, 'back_pain': 0, 'constipation': 0, 'abdominal_pain': 0, 'diarrhoea': 0, 'mild_fever': 0,
            'yellow_urine': 0, 'yellowing_of_eyes': 0, 'acute_liver_failure': 0, 'fluid_overload': 0, 'swelling_of_stomach': 0,
            'swelled_lymph_nodes': 0, 'malaise': 0, 'blurred_and_distorted_vision': 0, 'phlegm': 0, 'throat_irritation': 0,
            'redness_of_eyes': 0, 'sinus_pressure': 0, 'runny_nose': 0, 'congestion': 0, 'chest_pain': 0, 'weakness_in_limbs': 0,
            'fast_heart_rate': 0, 'pain_during_bowel_movements': 0, 'pain_in_anal_region': 0, 'bloody_stool': 0,
            'irritation_in_anus': 0, 'neck_pain': 0, 'dizziness': 0, 'cramps': 0, 'bruising': 0, 'obesity': 0, 'swollen_legs': 0,
            'swollen_blood_vessels': 0, 'puffy_face_and_eyes': 0, 'enlarged_thyroid': 0, 'brittle_nails': 0, 'swollen_extremeties': 0,
            'excessive_hunger': 0, 'extra_marital_contacts': 0, 'drying_and_tingling_lips': 0, 'slurred_speech': 0,
            'knee_pain': 0, 'hip_joint_pain': 0, 'muscle_weakness': 0, 'stiff_neck': 0, 'swelling_joints': 0, 'movement_stiffness': 0,
            'spinning_movements': 0, 'loss_of_balance': 0, 'unsteadiness': 0, 'weakness_of_one_body_side': 0, 'loss_of_smell': 0,
            'bladder_discomfort': 0, 'foul_smell_of urine': 0, 'continuous_feel_of_urine': 0, 'passage_of_gases': 0, 'internal_itching': 0,
            'toxic_look_(typhos)': 0, 'depression': 0, 'irritability': 0, 'muscle_pain': 0, 'altered_sensorium': 0,
            'red_spots_over_body': 0, 'belly_pain': 0, 'abnormal_menstruation': 0, 'dischromic _patches': 0, 'watering_from_eyes': 0,
            'increased_appetite': 0, 'polyuria': 0, 'family_history': 0, 'mucoid_sputum': 0, 'rusty_sputum': 0, 'lack_of_concentration': 0,
            'visual_disturbances': 0, 'receiving_blood_transfusion': 0, 'receiving_unsterile_injections': 0, 'coma': 0,
            'stomach_bleeding': 0, 'distention_of_abdomen': 0, 'history_of_alcohol_consumption': 0, 'fluid_overload.1': 0,
            'blood_in_sputum': 0, 'prominent_veins_on_calf': 0, 'palpitations': 0, 'painful_walking': 0, 'pus_filled_pimples': 0,
            'blackheads': 0, 'scurring': 0, 'skin_peeling': 0, 'silver_like_dusting': 0, 'small_dents_in_nails': 0, 'inflammatory_nails': 0,
            'blister': 0, 'red_sore_around_nose': 0, 'yellow_crust_ooze': 0}

url = "https://api.edenai.run/v2/text/question_answer"

def get_disease_description(disease):
    question = "What are the details of the predicted disease?"
    context = f"The predicted disease is {disease} i need in senetnces."
    
    payload = {
        "providers": "openai",
        "texts": [context],
        "question": question,
        "examples_context": "In 2017, U.S. life expectancy was 78.6 years.",
        "examples": [["What is human life expectancy in the United States?", "78 years."]],
        "fallback_providers": "gpt-3.5-turbo"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result['openai']['answers'][0]
    else:
        return "Sorry, something went wrong."


def get_nearby_hospitals(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node["amenity"="hospital"](around:5000,{lat},{lon});
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    hospitals = []
    for element in data['elements']:
        name = element['tags'].get('name', 'No name available')
        lat = element['lat']
        lon = element['lon']
        hospitals.append({'name': name, 'lat': lat, 'lon': lon})
    return hospitals

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hospital', methods=['GET', 'POST'])
def hospital():
    hospitals = []
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        if latitude and longitude:
            hospitals = get_nearby_hospitals(latitude, longitude)
    return render_template('hospital.html', hospitals=hospitals)

@app.route('/disease')
def result_page():
    return render_template('disease.html')
@app.route('/predict', methods=['POST'])
def predict():
    # Get input symptoms from request
    input_symptoms = request.json
    print(input_symptoms)
    # If no symptoms are selected, return an error response
    if not input_symptoms:
        return jsonify({'error': 'Please select at least one symptom.'}), 400

    # Update symptom values
    input_data = symptoms.copy()
    for symptom in input_symptoms:
        if symptom in input_data:
            input_data[symptom] = 1

    # Prepare test data
    df_test = pd.DataFrame(columns=list(input_data.keys()))
    df_test.loc[0] = np.array(list(input_data.values()))

    # Predict the disease
    predicted_disease = clf.predict(df_test)
    description = get_disease_description(predicted_disease)
    
    return jsonify({
        'predicted_disease': predicted_disease[0],
        'description': description
    })

if __name__ == '__main__':
    app.run(debug=True)
