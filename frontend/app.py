"""Streamlit Frontend — Hauptanwendung.

Dies ist die Hauptseite der Streamlit-App, ueber die Nutzer Prompts
an den Budget Router senden koennen.

Lernziele:
- Streamlit Grundlagen (st.title, st.text_area, st.slider, st.button)
- HTTP Requests an das eigene Backend (requests.post)
- Ergebnisse darstellen (st.write, st.json, st.metric)

TODOs:
- Seitentitel und Beschreibung anzeigen
- Prompt-Eingabefeld (st.text_area)
- Task-Type Auswahl (st.selectbox: "general", "code", "creative", "analysis")
- Budget-Slider (st.slider fuer max Budget pro Request in USD)
- Quality-Slider (st.slider fuer minimale Qualitaet 0-100)
- Absende-Button der POST /route aufruft
- Ergebnis-Anzeige: Modell, Antwort, Kosten, Tokens, Routing-Grund
"""

import streamlit as st


def main():
    """Rendere die Streamlit-Hauptseite.

    TODO:
    1. st.title("AI Model Budget Router")
    2. Prompt-Eingabe mit st.text_area()
    3. Sidebar mit Task-Type, Budget-Slider, Quality-Slider
    4. Button zum Absenden -> requests.post("http://localhost:8000/route", json={...})
    5. Antwort anzeigen mit st.write() / st.json() / st.metric()
    """
    pass


if __name__ == "__main__":
    main()
