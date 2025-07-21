import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Dark Mode Umschalter ---
dark_mode = st.sidebar.checkbox("🌙 Dark Mode aktivieren", value=False)

if dark_mode:
    bg_color = "#121212"
    text_color = "#FFFFFF"
    grid_color = "#333333"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    grid_color = "#DDDDDD"

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {bg_color};
        color: {text_color};
        transition: background-color 0.5s, color 0.5s;
    }}
    .st-bb {{
        background-color: {bg_color};
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Layout ---
st.set_page_config(page_title="BAföG-Zahlungscheck", layout="centered")

st.title("🎓 BAföG-Zahlungscheck (for Säbbeboi)")
st.subheader("Einmalzahlung vs. Raten – Was lohnt sich mehr?")

# --- Sidebar Eingaben ---
st.sidebar.header("🔧 Eingaben")

hoechstgrenze = st.sidebar.number_input("BAföG-Höchstgrenze (€)", value=10010.0, step=10.0)
rabatt_prozent = st.sidebar.slider("Rabatt bei Einmalzahlung (%)", 0, 50, 21)
quartalsrate = st.sidebar.number_input("Ratenzahlung pro Quartal (€)", value=390.0, step=10.0)
rendite = st.sidebar.slider("Anlagerendite (p.a. in %)", 0.0, 6.0, 3.0, step=0.1)

# --- Info-Fenster mit Anlagearten und Renditen ---
with st.expander("ℹ️ Typische Renditen nach Anlageart"):
    st.markdown("""
    | Anlageart              | Durchschnittliche Rendite p.a. | Quellen / Hinweise                         |
    |-----------------------|-------------------------------|-------------------------------------------|
    | Tagesgeldkonto         | 0,1 % – 0,5 %                 | Deutsche Bundesbank, 2024                  |
    | Festgeld               | 0,5 % – 1,5 %                 | Bundesfinanzministerium, aktuelle Angebote|
    | Staatsanleihen (10J)   | ca. 1,0 % – 2,0 %             | Bundesanleihe Renditekurven                |
    | Aktien (DAX)           | ca. 7 % – 8 % (Langfristig)  | Historische Renditen, Deutsche Börse       |
    | Immobilien (Miete)     | ca. 3 % – 5 % (Netto)         | Statistisches Bundesamt, Marktdaten        |

    **Erläuterung:**  
    Die hier angegebenen Renditen sind historische oder aktuell marktübliche Durchschnittswerte.  
    Die tatsächliche Rendite kann stark schwanken, insbesondere bei Aktien und Immobilien.  
    Eine sichere Verzinsung (z.B. Tagesgeld) ist in der Regel deutlich niedriger, aber auch weniger riskant.

    Nutze diese Werte als grobe Orientierung bei der Bewertung deiner Anlagerendite im Tool.
    """)

# --- Berechnungen ---
einmalzahlung = hoechstgrenze * (1 - rabatt_prozent / 100)
quartale = hoechstgrenze / quartalsrate
jahre = quartale / 4

# Berechnung mit quartalsweisem Zins
vierteljahreszins = (1 + rendite / 100) ** 0.25 - 1
endwert = einmalzahlung * (1 + vierteljahreszins) ** quartale
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
    vierteljahreszins_temp = (1 + zins) ** 0.25 - 1
    ew = einmalzahlung * (1 + vierteljahreszins_temp) ** quartale
    diff = ew - hoechstgrenze
    tabelle.append({
        "Rendite p.a.": f"{zins:.2%}",
        "Endwert Investition": f"{ew:,.2f} €",
        "Vorteil/Nachteil gegenüber Ratenzahlung": f"{diff:,.2f} €"
    })

df = pd.DataFrame(tabelle)

st.markdown("## 📊 Renditevergleich")
st.dataframe(df, use_container_width=True)

# --- Interaktives Diagramm mit Plotly ---
zeitpunkte = np.arange(0, quartale + 1)
jahre_zeit = zeitpunkte / 4

investitionswerte = einmalzahlung * (1 + vierteljahreszins) ** zeitpunkte
kumulierte_rueckzahlung = quartalsrate * zeitpunkte

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=jahre_zeit, y=investitionswerte,
    mode='lines+markers',
    name='Investitionswert (Einmalzahlung)',
    line=dict(color='green', width=3),
    marker=dict(size=6)
))

fig.add_trace(go.Scatter(
    x=jahre_zeit, y=kumulierte_rueckzahlung,
    mode='lines+markers',
    name='Kumulierte Rückzahlung (Raten)',
    line=dict(color='red', width=3, dash='dash'),
    marker=dict(size=6)
))

fig.update_layout(
    title='Entwicklung von Investition und Rückzahlung über die Zeit',
    xaxis_title='Jahre',
    yaxis_title='Euro (€)',
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font=dict(color=text_color),
    hovermode='x unified',
    legend=dict(x=0.02, y=0.98)
)

st.plotly_chart(fig, use_container_width=True)

# --- FAQ Bereich ---
st.markdown("## ❓ Häufige Fragen (FAQ)")
with st.expander("Was passiert, wenn ich BAföG nicht rechtzeitig zurückzahle?"):
    st.write("""
    Wird BAföG nicht fristgerecht zurückgezahlt, können Mahngebühren und Zinsen anfallen.  
    Im schlimmsten Fall drohen Vollstreckungsmaßnahmen.
    """)
with st.expander("Wie errechnet sich der Rabatt bei Einmalzahlung?"):
    st.write("""
    Der Rabatt ist eine pauschale Vergünstigung, die das Bundesverwaltungsamt für eine frühzeitige Rückzahlung gewährt.  
    Aktuell liegt er bei ca. 21 % der Rückzahlungssumme.
    """)
with st.expander("Kann ich den Rückzahlungszeitraum verlängern?"):
    st.write("""
    Ja, auf Antrag kann die Rückzahlung gestundet oder in Raten verlängert werden, z.B. bei geringem Einkommen.
    """)
with st.expander("Wie kann ich die Anlagerendite realistisch einschätzen?"):
    st.write("""
    Nutze konservative Werte für risikoarme Anlagen (Tagesgeld, Festgeld) und höhere Renditen für Aktien oder Immobilien.  
    Denk daran: Höhere Rendite bedeutet meist höheres Risiko.
    """)

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
