'''import streamlit as st
import requests

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="SmellSense AI")

st.title("SmellSense AI")
st.subheader("Automated Code Smell Detection Chatbot")

uploaded_file = st.file_uploader("Upload Java File", type=["java"])

if uploaded_file:

    st.write("Analyzing code...")

    response = requests.post(
        API_URL,
        files={"file": uploaded_file}
    )

    if response.status_code == 200:

        data = response.json()

        st.write("### Static Detection")
        st.write(data["static_engine"])

        st.write("### Metric Detection")
        st.write(data["metric_engine"])

        st.write("### LLM Semantic Detection")
        st.write(data["llm_engine"])

    else:

        st.write("Error analyzing file.")'''

import streamlit as st
import requests

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="SmellSense AI", layout="wide")

st.title("SmellSense AI")
st.subheader("Automated Code Smell Detection & Analysis")

uploaded_file = st.file_uploader("Upload Java File", type=["java"])

if uploaded_file:
    st.info("Analyzing code... Please wait.")
    
    # In a real scenario, we would first call Engine 1, 
    # then pass that to the analyze pipeline.
    # Assuming the API at API_URL now integrates the orchestrator 
    # OR we need to update the API to use the new orchestrator.
    # The user said "backend should output only the priority list as next engine will refactor".
    # This implies the /analyze endpoint might be updated.
    
    response = requests.post(
        API_URL,
        files={"file": uploaded_file}
    )

    if response.status_code == 200:
        data = response.json()
        
        # Check if we have the new 'priority_list' format
        if "priority_list" in data:
            st.success("Analysis Complete!")
            
            st.write("### 🚨 Priority List for Refactoring")
            
            for idx, item in enumerate(data["priority_list"], 1):
                priority_val = item["priority_score"]
                color = "red" if priority_val > 0.8 else "orange" if priority_val > 0.5 else "blue"
                
                # Header showing Number and Smell Name
                header = f"{idx}. {item['smell']} (Location: {item['location']})"
                
                with st.expander(f"**{header}** - Priority Score: :{color}[{item['ui_severity']}]"):
                    st.write(f"**📝 Explanation:** {item['explanation']}")
                    st.write(f"**📍 Location:** `{item['location']}`")
                    st.write("---")
                    st.write(f"**Category:** {item['category']} | **Severity:** {item['severity']}")
                    st.write(f"**Supported By:** {', '.join(item['supported_by'])}")
                    
                    if item.get("evidence"):
                        st.write("**Evidence:**")
                        for ev in item["evidence"]:
                            st.write(f"- {ev}")
        
        else:
            # Fallback to original display if format hasn't changed yet
            st.write("### Detected Smells (Raw Engine Output)")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Static Engine**")
                st.write(data.get("static_engine", []))
            with col2:
                st.write("**Metric Engine**")
                st.write(data.get("metric_engine", []))
            with col3:
                st.write("**LLM Engine**")
                st.write(data.get("llm_engine", []))
    else:
        st.error("Error analyzing file.")