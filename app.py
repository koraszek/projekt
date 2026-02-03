odel = load_model_oczekiwanie()
    
    # Prosty układ - jeden pod drugim, żeby uniknąć błędów renderowania
dist = st.slider("Odległość (km)", 0.5, 20.0, 5.0)
meals = st.number_input("Liczba dań", 1, 10, 2)
rush = st.selectbox("Godzina szczytu?", ["Nie", "Tak"])
rain = st.selectbox("Deszcz", ["Nie", "Tak"])

if st.button("OBLICZ CZAS DOSTAWY"):
        # Konwersja na liczby 0/1 zgodnie z Twoim modelem
        val_rush = 1 if rush == "Tak" else 0
        val_rain = 1 if rain == "Tak" else 0
        
        # DataFrame - kolejność kolumn musi być idealna:
        # odleglosc, godzina_szczytu, deszcz, liczba_dan
        dane = pd.DataFrame([[dist, val_rush, val_rain, meals]], 
                            columns=['odleglosc', 'godzina_szczytu', 'deszcz', 'liczba_dan'])
        
        prognoza = model.predict(dane)[0]
        st.metric("Przewidywany czas", f"{prognoza:.1f} minut")
        st.balloons()
