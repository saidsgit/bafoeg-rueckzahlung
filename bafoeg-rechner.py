import streamlit as st
import pandas as pd
import numpy as np

st.title("🎓 BAföG-Rückzahlungsvergleich: Einmalzahlung vs. Raten")

# Eingaben
st.sidebar.header("🔧 Eingaben")

hoechstgrenze = st.sidebar.number_input("BAföG-Höchstgrenze (z. B. 10.010 €)", value=10010.0, step=10.0)
rabatt_prozent = st.sidebar.slider("Rabatt bei Einmalzahlung (%)", min_value=0, max_value=50, value=21)
quartalsrate = st.sidebar.number_input("Ratenzahlung pro Quartal (€)", value=390.0, step=10.0)
rendite = st.sidebar.slider("Anlagerendite (p.a. in %)", min_value=0.0, max_value=6.0, value=3.0, step=0.1)

# Berechnungen
einmalzahlung = hoechstgrenze * (1 - rabatt_prozent / 100)
quartale = hoechstgrenze / quartalsrate
jahre = quartale / 4

# Investitionswert
endwert = einmalzahlung * (1 + rendite / 100) ** jahre
vorteil = endwert - hoechstgrenze

# Ergebnisse
st.markdown("### 💡 Vergleich")
st.write(f"**Einmalzahlung:** {einmalzahlung:,.2f} €")
st.write(f"**Ratenzahlung gesamt:** {hoechstgrenze:,.2f} € über ca. {jahre:.1f} Jahre")
st.write(f"**Investierter Einmalbetrag bei {rendite:.1f}% Rendite:** {endwert:,.2f} €")
st.write(f"**Vorteil gegenüber Ratenzahlung:** {vorteil:,.2f} €")

# Tabelle: verschiedene Renditen
zinsraten = np.arange(0.00, 0.065, 0.005)
tabelle = []

for zins in zinsraten:
    ew = einmalzahlung * (1 + zins) ** jahre
    diff = ew - hoechstgrenze
    tabelle.append({
        "Rendite p.a.": f"{zins:.2%}",
        "Endwert Investition": f"{ew:,.2f} €",
        "Vorteil/Nachteil gegenüber Ratenzahlung": f"{diff:,.2f} €"
    })

df = pd.DataFrame(tabelle)
st.markdown("### 📊 Renditevergleichstabelle")
st.dataframe(df, use_container_width=True)
