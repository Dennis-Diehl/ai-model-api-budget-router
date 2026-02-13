"""Streamlit Frontend — Chat Interface mit Backend-Integration.

Diese Streamlit-App verbindet sich mit dem FastAPI Backend und zeigt
echte AI-Antworten, Routing-Entscheidungen und Kosten an.

Lernziele:
- Streamlit Sidebar (st.sidebar, st.selectbox, st.slider)
- Chat Interface (st.chat_message, st.chat_input)
- Session State (st.session_state)
- Expandable Sections (st.expander)
- API Calls mit requests
- Error Handling
"""

import streamlit as st
import requests
import time

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Model names mapping für bessere Anzeige
MODEL_NAMES = {
    "llama-3.3-70b-versatile": "LLaMA 3.3 70B Versatile",
    "llama-3.1-8b-instant": "LLaMA 3.1 8B Instant",
    "openai/gpt-oss-120b": "GPT-OSS 120B",
    "openai/gpt-oss-20b": "GPT-OSS 20B",
}


def call_backend(prompt, task_type, budget, quality):
    """Ruft das Backend /route Endpoint auf.

    Args:
        prompt: User's eingabe
        task_type: Art der Aufgabe (general, code, email, summarize)
        budget: Maximales Budget in USD
        quality: Qualitätslevel (low, medium, high)

    Returns:
        dict: Backend response mit model, response, costs, tokens, routing_reason

    Raises:
        Exception: Bei Backend-Fehlern oder Verbindungsproblemen
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/route",
            json={
                "prompt": prompt,
                "task_type": task_type,
                "budget": budget,
                "quality": quality
            },
            timeout=60  # 60 Sekunden Timeout für LLM-Antworten
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        # Backend hat einen HTTP-Fehler zurückgegeben
        if e.response.status_code == 400:
            # Budget zu niedrig oder ungültige Eingabe
            error_detail = e.response.json().get('detail', 'Ungültige Anfrage')
            raise Exception(f"⚠️ {error_detail}")
        else:
            raise Exception(f"Backend-Fehler: {e}")
    except requests.Timeout:
        raise Exception("Anfrage hat zu lange gedauert. Bitte erneut versuchen.")
    except requests.ConnectionError:
        raise Exception("Keine Verbindung zum Backend. Stelle sicher, dass das Backend läuft.")
    except Exception as e:
        raise Exception(f"Verbindungsfehler: {str(e)}")


def init_session_state():
    """Initialisiert Session State für Chat-History und Spending Tracker."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_spent" not in st.session_state:
        st.session_state.session_spent = 0.0


def main():
    # Page config
    st.set_page_config(
        page_title="AI Model Budget Router",
        page_icon="🤖",
        layout="wide"
    )

    # Session State initialisieren
    init_session_state()

    # Header
    st.title("🤖 AI Model Budget Router")
    st.markdown(
        "Stelle eine Frage und lass den Router das beste Modell "
        "basierend auf deinem Budget und Qualitätsanforderungen auswählen."
    )

    # Sidebar Controls
    with st.sidebar:
        st.header("⚙️ Einstellungen")

        # Task Type Selector
        task_type = st.selectbox(
            "Task Type",
            ["general", "code", "email", "summarize"],
            index=0,
            help="Modelle haben unterschiedliche Stärken für verschiedene Aufgaben"
        )

        # Quality Selector
        quality = st.selectbox(
            "Quality Level",
            ["low", "medium", "high"],
            index=1,  # Default: medium
            help="Mindest-Qualitätsschwelle (low: 0, medium: 60, high: 75)"
        )

        # Budget Slider
        budget = st.slider(
            "Max Budget pro Request (USD)",
            min_value=0.0001,
            max_value=0.01,
            value=0.001,
            step=0.0001,
            format="$%.6f",
            help="Maximalbetrag, den du für diese Anfrage ausgeben möchtest"
        )


        st.divider()

        # Session Spending Tracker
        st.subheader("💰 Session Spending")
        st.metric(
            "Ausgegeben",
            f"${st.session_state.session_spent:.6f}",
            help="Gesamtkosten in dieser Session"
        )

    # Chat Interface
    # Zeige bisherige Chat-History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Zeige zusätzliche Details für Assistant-Nachrichten
            if message["role"] == "assistant" and "details" in message:
                details = message["details"]

                # Routing Details (expandable)
                with st.expander("🎯 Model Selection Details"):
                    model_id = details.get("model", "unknown")
                    model_name = MODEL_NAMES.get(model_id, model_id)
                    routing_reason = details.get("routing_reason", "N/A")

                    st.markdown(f"**Selected Model:** {model_name}")
                    st.info(routing_reason)

                # Cost Breakdown (expandable)
                with st.expander("💰 Cost Breakdown"):
                    estimated = details.get("estimated_cost", 0)
                    actual = details.get("actual_cost", 0)
                    tokens = details.get("tokens_used", 0)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Estimated", f"${estimated:.6f}")
                    with col2:
                        # Delta berechnen
                        delta = actual - estimated
                        delta_pct = (delta / estimated * 100) if estimated > 0 else 0
                        st.metric(
                            "Actual",
                            f"${actual:.6f}",
                            delta=f"{delta_pct:+.1f}%"
                        )
                    with col3:
                        st.metric("Tokens", f"{tokens:,}")

    # Chat Input
    if prompt := st.chat_input("Deine Frage..."):
        # User Message anzeigen
        with st.chat_message("user"):
            st.markdown(prompt)

        # User Message zu History hinzufügen
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Backend aufrufen und Antwort anzeigen
        with st.chat_message("assistant"):
            with st.spinner("Suche bestes Modell und generiere Antwort..."):
                try:
                    # Backend API Call
                    data = call_backend(prompt, task_type, budget, quality)

                    # Response anzeigen
                    response_text = data.get("response", "Keine Antwort erhalten")
                    st.markdown(response_text)

                    # Routing Details (expandable)
                    with st.expander("🎯 Model Selection Details", expanded=True):
                        model_id = data.get("model", "unknown")
                        model_name = MODEL_NAMES.get(model_id, model_id)
                        routing_reason = data.get("routing_reason", "N/A")

                        st.markdown(f"**Selected Model:** {model_name}")
                        st.info(routing_reason)

                    # Cost Breakdown (expandable)
                    with st.expander("💰 Cost Breakdown"):
                        estimated = data.get("estimated_cost", 0)
                        actual = data.get("actual_cost", 0)
                        tokens = data.get("tokens_used", 0)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Estimated", f"${estimated:.6f}")
                        with col2:
                            # Delta berechnen
                            delta = actual - estimated
                            delta_pct = (delta / estimated * 100) if estimated > 0 else 0
                            st.metric(
                                "Actual",
                                f"${actual:.6f}",
                                delta=f"{delta_pct:+.1f}%"
                            )
                        with col3:
                            st.metric("Tokens", f"{tokens:,}")

                    # Session Spending updaten
                    st.session_state.session_spent += actual

                    # Assistant Message zu History hinzufügen
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "details": {
                            "model": model_id,
                            "routing_reason": routing_reason,
                            "estimated_cost": estimated,
                            "actual_cost": actual,
                            "tokens_used": tokens
                        }
                    })

                    # Rerun um Sidebar zu updaten
                    st.rerun()

                except Exception as e:
                    # Fehler anzeigen
                    st.error(str(e))
                    st.markdown("**Hinweis:** Stelle sicher, dass:")
                    st.markdown("1. Das Backend läuft: `uvicorn backend.app:app --reload`")
                    st.markdown("2. GROQ_API_KEY gesetzt ist")
                    st.markdown("3. Dein Budget hoch genug ist")


if __name__ == "__main__":
    main()
