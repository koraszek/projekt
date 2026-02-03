import streamlit as st
import pandas as pd
import xgboost as xgb
import os

# Definicja modelu na samym początku
@st.cache_resource
def load_model_oczekiwanie():
    if os.path.exists('model_oczekiwanie.json'):
        m = xgb.XGBRegressor()
        m.load_model('model_oczekiwanie.json')
        return m
    return None

st.title("Kalkulator czasu oczekiwania na dostawę")

model = load_model_oczekiwanie()
    
    # Prosty układ - jeden pod drugim, żeby uniknąć błędów renderowania
dist = st.slider("Odległość (km)", 0.5, 20.0, 5.0)
meals = st.number_input("Liczba dań", 1, 10, 2)
rush = st.selectbox("Godzina szczytu?", ["Nie", "Tak"])
rain = st.selectbox("Deszcz", ["Nie", "Tak"])
day = st.selectbox("Weekend lub święto?", ["Nie", "Tak"])
time = st.selectbox("Pora dnia", ["Rano", "Przedpołudnie (Lunch)", "Popołudnie", "Wieczór"])

if st.button("OBLICZ CZAS DOSTAWY"):
    # Konwersja na liczby 0/1 zgodnie z Twoim modelem
    val_rush = 1 if rush == "Tak" else 0
    val_rain = 1 if rain == "Tak" else 0
    val_day = 1 if day == "Tak" else 0

    time_map = {
        "Rano": 0,
        "Przedpołudnie (Lunch)": 1,
        "Popołudnie": 2,
        "Wieczór (18-22)": 3
    }

    val_time = time_map[time]

        # DataFrame - kolejność kolumn musi być idealna:
        # odleglosc, godzina_szczytu, deszcz, liczba_dan
        dane = pd.DataFrame([[dist, val_rush, val_rain, meals, day, time]], 
                            columns=['odleglosc', 'godzina_szczytu', 'deszcz', 'liczba_dan', 'weekend_swieto', 'pora_dnia'])
        
        prognoza = model.predict(dane)[0]
        st.metric("Przewidywany czas", f"{prognoza:.1f} minut")
        st.balloons()
