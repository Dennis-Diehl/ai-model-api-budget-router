"""Streamlit Frontend — Chat Interface with Backend Integration.

This Streamlit app connects to the FastAPI backend and displays
AI responses, routing decisions, and cost breakdowns.
"""

import streamlit as st
import requests


### Constants

BACKEND_URL = "http://localhost:8000"

# Human-readable display names for model IDs
MODEL_NAMES = {
    "llama-3.3-70b-versatile": "LLaMA 3.3 70B Versatile",
    "llama-3.1-8b-instant": "LLaMA 3.1 8B Instant",
    "openai/gpt-oss-120b": "GPT-OSS 120B",
    "openai/gpt-oss-20b": "GPT-OSS 20B",
}


### Backend Communication

def call_backend(prompt, task_type, budget, quality):
    """Call the backend /route endpoint and return the JSON response.

    Args:
        prompt: The user's input text
        task_type: Task category (general, code, email, summarize)
        budget: Maximum budget in USD
        quality: Quality level (low, medium, high)

    Returns:
        dict: Backend response with model, response, costs, tokens, routing_reason

    Raises:
        Exception: On backend errors or connection issues
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
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code == 400:
            error_detail = e.response.json().get('detail', 'Invalid request')
            raise Exception(f"⚠️ {error_detail}")
        else:
            raise Exception(f"Backend error: {e}")
    except requests.Timeout:
        raise Exception("Request timed out. Please try again.")
    except requests.ConnectionError:
        raise Exception("Cannot connect to backend. Make sure the backend is running.")
    except Exception as e:
        raise Exception(f"Connection error: {str(e)}")


### Session State

def init_session_state():
    """Initialize session state for chat history and spending tracker."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_spent" not in st.session_state:
        st.session_state.session_spent = 0.0


### UI Components

def render_routing_details(model_id, routing_reason):
    """Render the expandable model selection details section."""
    model_name = MODEL_NAMES.get(model_id, model_id)
    st.markdown(f"**Selected Model:** {model_name}")
    st.info(routing_reason)


def render_cost_breakdown(estimated, actual, tokens):
    """Render the expandable cost breakdown section with three metric columns."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Estimated", f"${estimated:.6f}")
    with col2:
        delta = actual - estimated
        delta_pct = (delta / estimated * 100) if estimated > 0 else 0
        st.metric("Actual", f"${actual:.6f}", delta=f"{delta_pct:+.1f}%")
    with col3:
        st.metric("Tokens", f"{tokens:,}")


def render_sidebar():
    """Render sidebar with settings and spending tracker. Returns user selections."""
    with st.sidebar:
        st.header("⚙️ Settings")

        # Task type selector
        task_type = st.selectbox(
            "Task Type",
            ["general", "code", "email", "summarize"],
            index=0,
            help="Models have different strengths for different tasks"
        )

        # Quality level selector
        quality = st.selectbox(
            "Quality Level",
            ["low", "medium", "high"],
            index=1,
            help="Minimum quality threshold (low: 0, medium: 60, high: 75)"
        )

        # Budget slider
        budget = st.slider(
            "Max Budget per Request (USD)",
            min_value=0.0001,
            max_value=0.01,
            value=0.001,
            step=0.0001,
            format="$%.6f",
            help="Maximum amount you want to spend on this request"
        )

        st.divider()

        # Session spending tracker
        st.subheader("💰 Session Spending")
        st.metric(
            "Total Spent",
            f"${st.session_state.session_spent:.6f}",
            help="Total cost accumulated in this session"
        )

    return task_type, quality, budget


def render_message_details(details):
    """Render routing and cost details for a message (used in chat history)."""
    with st.expander("🎯 Model Selection Details"):
        render_routing_details(
            details.get("model", "unknown"),
            details.get("routing_reason", "N/A")
        )
    with st.expander("💰 Cost Breakdown"):
        render_cost_breakdown(
            details.get("estimated_cost", 0),
            details.get("actual_cost", 0),
            details.get("tokens_used", 0)
        )


def render_chat_history():
    """Render all previous messages from session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and "details" in message:
                render_message_details(message["details"])


def handle_user_input(task_type, budget, quality):
    """Process new user input: send to backend, display response, update state."""
    if prompt := st.chat_input("Your question..."):
        # Display and store user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call backend and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Finding best model and generating response..."):
                try:
                    data = call_backend(prompt, task_type, budget, quality)

                    # Display response text
                    response_text = data.get("response", "No response received")
                    st.markdown(response_text)

                    # Extract details
                    model_id = data.get("model", "unknown")
                    routing_reason = data.get("routing_reason", "N/A")
                    estimated = data.get("estimated_cost", 0)
                    actual = data.get("actual_cost", 0)
                    tokens = data.get("tokens_used", 0)

                    # Display routing and cost details
                    with st.expander("🎯 Model Selection Details", expanded=True):
                        render_routing_details(model_id, routing_reason)
                    with st.expander("💰 Cost Breakdown"):
                        render_cost_breakdown(estimated, actual, tokens)

                    # Update session spending
                    st.session_state.session_spent += actual

                    # Store assistant message in history
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

                    # Rerun to update sidebar spending tracker
                    st.rerun()

                except Exception as e:
                    st.error(str(e))
                    st.markdown("**Troubleshooting:**")
                    st.markdown("1. Backend running? `uvicorn backend.app:app --reload`")
                    st.markdown("2. GROQ_API_KEY set?")
                    st.markdown("3. Budget high enough?")


### Main

def main():
    st.set_page_config(
        page_title="AI Model Budget Router",
        page_icon="🤖",
        layout="wide"
    )

    init_session_state()

    # Header
    st.title("🤖 AI Model Budget Router")
    st.markdown(
        "Ask a question and let the router pick the best model "
        "based on your budget and quality requirements."
    )

    # Sidebar (returns user selections)
    task_type, quality, budget = render_sidebar()

    # Chat history
    render_chat_history()

    # New message input
    handle_user_input(task_type, budget, quality)


if __name__ == "__main__":
    main()
