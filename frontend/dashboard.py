"""Streamlit Dashboard — Nutzungsstatistiken und Logs.

Dieses Modul zeigt eine Uebersicht ueber die bisherige Nutzung des
Budget Routers: Kosten, Modell-Verteilung und einzelne Requests.

Lernziele:
- Streamlit Layouts (st.columns, st.metric)
- Daten vom Backend abrufen (GET /stats)
- Einfache Diagramme mit st.bar_chart oder st.plotly_chart
- Tabellen mit st.dataframe

TODOs:
- Statistiken vom Backend laden (requests.get("http://localhost:8000/stats"))
- Kennzahlen anzeigen: Total Requests, Total Cost, Average Cost (st.metric)
- Balkendiagramm der Modell-Nutzung (model_usage)
- Log-Tabelle mit allen bisherigen Requests (GET /stats oder eigener Endpoint)
"""

import streamlit as st


def render_dashboard():
    """Rendere das Usage-Dashboard.

    TODO:
    1. st.title("Usage Dashboard")
    2. Stats vom Backend laden: requests.get("http://localhost:8000/stats").json()
    3. st.columns(3) fuer Kennzahlen (Total Requests, Total Cost, Avg Cost)
    4. st.bar_chart() fuer model_usage
    5. Optional: Log-Tabelle mit st.dataframe()
    """
    pass
