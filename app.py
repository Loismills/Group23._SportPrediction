import streamlit as st
import pickle
import numpy as np



model = pickle.load(open('/Users/naakoshie/Downloads/model.pkl', 'rb'))


st.title("Player Rating Predictor")


potential= st.number_input('potential', min_value=0.0, step=0.01, key='potential')
wage_eur = st.number_input('wage_eur', min_value=0.0, step=0.01, key='wage_eur')
passing = st.number_input('passing', min_value=0.0, step=0.01, key='passing')
dribbling = st.number_input('dribbling', min_value=0.0, step=0.01, key='dribbling')
movement_reactions = st.number_input('movement_reactions', min_value=0.0, step=0.01, key='movement_reactions')
mentality_composure = st.number_input('mentality_composure', min_value=0.0, step=0.01, key='mentality_composure')
lf = st.number_input('lf', min_value=0.0, step=0.01, key='lf')
cf = st.number_input('cf', min_value=0.0, step=0.01, key='cf')
rf = st.number_input('rf', min_value=0.0, step=0.01, key='rf')
lam = st.number_input('lam', min_value=0.0, step=0.01, key='lam')
cam = st.number_input('cam', min_value=0.0, step=0.01, key='cam')
ram = st.number_input('ram', min_value=0.0, step=0.01, key='ram')
lm = st.number_input('lm', min_value=0.0, step=0.01, key='lm')
lcm = st.number_input('lcm', min_value=0.0, step=0.01, key='lcm')
cm = st.number_input('cm', min_value=0.0, step=0.01, key='cm')
rcm = st.number_input('rcm', min_value=0.0, step=0.01, key='rcm')
rm = st.number_input('rm', min_value=0.0, step=0.01, key='rm')


if st.button("Predict"):
    input_data = np.array([[potential, wage_eur, passing, dribbling, movement_reactions, mentality_composure, lf, cf, rf, lam, cam, ram, lm, lcm, cm, rcm, rm]])

    prediction = model.predict(input_data)[0]
    confidence_score = model.predict(input_data).max() * 100

    st.write(f"Player Rating Prediction: {prediction:.2f}")
    st.write(f"Confidence Score: {confidence_score:.2f}%")
user_feedback = st.radio("Do you agree with the prediction?", ["Yes", "No"])
if user_feedback == "Yes":
    st.write("Thank you for your feedback!")
else:
    st.write("We appreciate your input. Please provide more details for better accuracy.")
