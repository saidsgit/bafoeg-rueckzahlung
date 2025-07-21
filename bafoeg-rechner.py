import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Layout Setup ---
st.set_page_config(page_title="BAföG-Zahlungscheck", layout="centered")

st.title("🎓 BAföG-Zahlungscheck")
st.subheader("Einmalzahlung vs. Raten – Was lohnt sich mehr?")

# --- Sidebar Eingaben ---
st.sidebar.header("🔧 Eingaben")

hoechstgrenze = st.sidebar.number_input("BAföG-Höchstgrenze (€)", value=10010.0, step=10.0)
rabatt_prozent = st.sidebar.slider("Rabatt bei Einmalzahlung (%)", 0, 50, 21)
quartalsrate = st.sidebar.number_input("Ratenzahlung pro Quartal (€)", value=390.0, step=10.0)
rendite = st.sidebar.slider("Anlagerendite (p.a. in %)", 0.0, 6.0, 3.0, step=0.1)

# --- Berechnungen ---
einmalzahlung = hoechstgrenze * (1 - rabatt_prozent / 100)
quartale = hoechstgrenze / quartalsrate
jahre = quartale / 4
endwert = einmalzahlung * (1 + rendite / 100) ** jahre
vorteil = endwert - hoechstgrenze

# --- Ergebnisse anzeigen ---
st.markdown("## 💰 Ergebnisvergleich")
col1, col2 = st.columns(2)

with col1:
    st.metric("Einmalzahlung", f"{einmalzahlung:,.2f} €")
    st.metric("Ratenzahlung gesamt", f"{hoechstgrenze:,.2f} €")
with col2:
    st.metric(f"Wert bei {rendite:.1f}% p.a.", f"{endwert:,.2f} €")
    st.metric("Finanzieller Vorteil", f"{vorteil:+,.2f} €")

# --- Vergleichstabelle bei verschiedenen Renditen ---
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

st.markdown("## 📊 Renditevergleich")
st.dataframe(df, use_container_width=True)

# --- Diagramm: Investition vs Rückzahlung über Zeit ---
st.markdown("## 📈 Entwicklung über die Zeit")

zeitpunkte = np.arange(0, quartale + 1)
jahre_zeit = zeitpunkte / 4

# Investitionswert zu jedem Quartal (Zinseszins quartalsweise)
vierteljahreszins = (1 + rendite / 100) ** 0.25 - 1
investitionswerte = einmalzahlung * (1 + vierteljahreszins) ** zeitpunkte

# Kumulierte Rückzahlung bis zu jedem Quartal
kumulierte_rueckzahlung = quartalsrate * zeitpunkte

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(jahre_zeit, investitionswerte, label="Investitionswert (Einmalzahlung)", color="green", linewidth=2)
ax.plot(jahre_zeit, kumulierte_rueckzahlung, label="Kumulierte Rückzahlung (Raten)", color="red", linewidth=2, linestyle="--")

ax.set_xlabel("Jahre")
ax.set_ylabel("Euro (€)")
ax.set_title("Entwicklung von Investition und Rückzahlung über die Zeit")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# --- Erklärung / Methodik ---
with st.expander("ℹ️ Wie wird gerechnet?"):
    st.markdown(f"""
    Die Berechnungen basieren auf folgendem Prinzip:

    - **Einmalzahlung** = BAföG-Höchstgrenze abzüglich des angegebenen Rabatts  
    - **Ratenzahlung** = volle Rückzahlungssumme bei vierteljährlicher Zahlung  
    - **Investition**: Annahme einer Verzinsung der Einmalzahlung zum angegebenen Zinssatz (p.a.), quartalsweise verzinst  
    - **Endwert** = Einmalzahlung × (1 + Zinssatz) ^ Jahre  
    - **Vorteil/Nachteil** = Differenz zwischen investiertem Endwert und der Summe der Ratenzahlungen  

    📌 Die Laufzeit ergibt sich aus der Anzahl der Quartalszahlungen:  
    **{quartale:.0f} Quartale = {jahre:.1f} Jahre**
    """)

st.markdown("---")
st.caption("Entwickler: Said")
