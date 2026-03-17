import io

import requests
import streamlit as st

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="SmellSense AI", layout="wide")


def inject_custom_css():
    st.markdown(
        """
    <style>
        .stApp {
            background: linear-gradient(180deg, #fcfaff 0%, #f8f4ff 100%);
        }

        h1, h2, h3, .stSubheader, p, label {
            color: #3b2f4a !important;
        }

        [data-testid="stFileUploader"] {
            background-color: #f6f0ff;
            border: 2px dashed #d8c4f0;
            border-radius: 14px;
            padding: 20px;
        }

        button[data-baseweb="tab"] {
            background-color: #efe4ff !important;
            color: #5b4b73 !important;
            border: none !important;
            border-radius: 10px !important;
            margin-right: 5px !important;
            padding: 10px 25px !important;
            transition: all 0.2s ease !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #b794f4 !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
        }

        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }

        textarea, input {
            background-color: #fcfaff !important;
            border: 1px solid #d9c7f3 !important;
            border-radius: 10px !important;
            color: #3b2f4a !important;
        }

        [data-testid="stExpander"] {
            background-color: #f3ebff !important;
            border-radius: 14px !important;
            border: 1px solid #e3d3f8 !important;
            margin-bottom: 15px !important;
            padding: 0 !important;
            box-shadow: 0 2px 8px rgba(120, 90, 160, 0.08) !important;
            overflow: hidden !important;
        }

        [data-testid="stExpander"] summary {
            background-color: #f3ebff !important;
            color: #5a3f7a !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            padding: 12px 15px !important;
            list-style: none !important;
            transition: background-color 0.2s ease !important;
        }

        [data-testid="stExpander"] summary:hover,
        [data-testid="stExpander"] summary:focus,
        [data-testid="stExpander"] summary:active,
        [data-testid="stExpander"][aria-expanded="true"] summary,
        details[open] > summary {
            background-color: #f3ebff !important;
            color: #5a3f7a !important;
            outline: none !important;
            box-shadow: none !important;
        }

        .streamlit-expanderContent {
            background-color: #fbf8ff !important;
            border-top: 1px solid #e7d9fa !important;
            padding: 15px !important;
            color: #4d3f63 !important;
        }

        div.stButton > button {
            background-color: #b794f4 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.2s ease !important;
        }

        div.stButton > button:hover {
            background-color: #a87fe8 !important;
            box-shadow: 0 4px 12px rgba(167, 127, 232, 0.25) !important;
        }

        div[data-testid="stFileUploader"] section button {
            background-color: #ffffff !important;
            color: #5b4b73 !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }

        div[data-testid="stFileUploader"] section button:hover {
            background-color: #f8f4ff !important;
        }

        [data-testid="stExpander"]:hover {
            border-color: #cfb4f4 !important;
            box-shadow: 0 4px 10px rgba(140, 110, 190, 0.12) !important;
        }

        [data-testid="stAlert"], [data-testid="stNotification"] {
            border-radius: 12px !important;
            background-color: #f3ebff !important;
            color: #5a3f7a !important;
            border: 1px solid #e3d3f8 !important;
        }

        [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stNotification"] [data-testid="stMarkdownContainer"] p {
            color: #5a3f7a !important;
        }

        hr {
            border: none;
            border-top: 1px solid #e8dcfa;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def detect_language(file_name: str) -> str:
    return "java" if str(file_name).lower().endswith(".java") else "python"


inject_custom_css()

st.title("SmellSense AI")
st.subheader("Automated Code Smell Detection, Analysis, and Refactoring")
st.write("---")

col1, col2, col3 = st.columns([1, 1, 1], gap="large")

with col1:
    st.markdown("### Upload or Paste Code")

    tab1, tab2 = st.tabs(["Upload File", "Paste Code"])

    source_code = None
    file_name = "pasted_code.java"

    with tab1:
        uploaded_file = st.file_uploader("Upload Java File", type=["java"], key="uploader")
        if uploaded_file:
            source_code = uploaded_file.getvalue().decode("utf-8")
            file_name = uploaded_file.name

    with tab2:
        pasted_code = st.text_area(
            "Paste your Java code here:",
            height=300,
            placeholder="public class Example { ... }",
            key="paster",
        )
        if pasted_code:
            source_code = pasted_code
            file_name = "manual_input.java"

    analysis_data = None
    if source_code and st.button("Analyze code", use_container_width=True):
        st.info("Analyzing code... Please wait.")
        files = {"file": (file_name, io.BytesIO(source_code.encode("utf-8")), "text/plain")}

        try:
            response = requests.post(API_URL, files=files, timeout=600)
            if response.status_code == 200:
                analysis_data = response.json()
                st.success("Analysis complete.")
                st.session_state["analysis_results"] = analysis_data
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as exc:
            st.error(f"Connection error: {exc}")

if "analysis_results" in st.session_state:
    analysis_data = st.session_state["analysis_results"]

with col2:
    st.markdown("### Priority List")
    if analysis_data and "priority_list" in analysis_data:
        for idx, item in enumerate(analysis_data["priority_list"], 1):
            priority_val = item.get("priority_score", 0)
            ui_severity = item.get("ui_severity", "N/A")

            if priority_val > 0.8:
                badge_color = "red"
            elif priority_val > 0.5:
                badge_color = "orange"
            else:
                badge_color = "blue"

            header = f"{idx}. {item['smell']} - Priority: :{badge_color}[{ui_severity}]"
            with st.expander(header):
                st.markdown(f"**Explanation:** {item.get('explanation', 'N/A')}")
                st.markdown(f"**Location:** `{item.get('location', 'unknown')}`")
                st.write("---")
                st.caption(
                    f"Category: {item.get('category', 'General')} | Engines: {', '.join(item.get('supported_by', []))}"
                )
    elif analysis_data:
        st.info("Raw output detected. Please check the API format.")
        st.write(analysis_data)
    else:
        st.write("Results will appear here after analysis.")

with col3:
    st.markdown("### Refactored Code")
    if analysis_data and analysis_data.get("refactoring"):
        refactoring = analysis_data["refactoring"]
        summary = refactoring.get("summary", {})
        st.caption(
            " | ".join(
                [
                    f"Smells received: {summary.get('smells_received', 0)}",
                    f"Refactored: {summary.get('smells_refactored', 0)}",
                    f"Failures: {summary.get('failures', 0)}",
                ]
            )
        )

        for idx, item in enumerate(refactoring.get("results", []), 1):
            header = f"{idx}. {item.get('smell_type', 'Unknown')} -> {item.get('strategy', 'unknown')}"
            with st.expander(header):
                st.markdown(f"**Status:** `{item.get('status', 'unknown')}`")
                st.markdown(f"**Severity:** `{item.get('severity', 'N/A')}`")
                st.markdown(f"**Location:** `{item.get('location', 'unknown')}`")
                st.markdown(f"**Rationale:** {item.get('rationale', 'N/A')}")

                validation = item.get("validation", {})
                st.caption(
                    " | ".join(
                        [
                            f"Syntax: {validation.get('syntax', False)}",
                            f"Compile: {validation.get('compile', 'N/A')}",
                            f"Structural: {validation.get('structural', 'N/A')}",
                        ]
                    )
                )

                metrics = item.get("metrics") or {}
                if metrics:
                    st.json(metrics, expanded=False)

                refactored_code = item.get("refactored_code")
                if refactored_code:
                    st.code(refactored_code, language=detect_language(refactoring.get("file_name", "")))
                else:
                    st.warning("No refactored code was produced for this smell.")

                errors = validation.get("errors") or []
                if errors:
                    st.error("\n".join(errors))
    else:
        st.info("Refactoring results will appear here after analysis.")
