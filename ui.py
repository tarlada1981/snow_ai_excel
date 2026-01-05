import streamlit as st
from excel_db import read_table
from change_checker import check_recent_changes
from kb_engine import search_kb
from incident_correlator import correlate_past_incidents
from ollama_engine import ask_ollama

st.set_page_config(page_title="AI Incident Analyzer", layout="wide")

st.title("🧠 AI Incident Analysis (ServiceNow Simulation)")

incidents = read_table("new incident")

incident_numbers = incidents["number"].tolist()
selected_inc = st.selectbox("Select Incident", incident_numbers)

incident = incidents[incidents["number"] == selected_inc].iloc[0]

st.subheader("📄 Incident Details")
st.write(f"**Incident:** {incident['number']}")
st.write(f"**CI:** {incident['cmdb_ci']}")
st.write(f"**Issue:** {incident['short_description']}")

if st.button("Analyze Incident"):
    output = ""

    # 1️⃣ Recent Changes
    changes = check_recent_changes(incident["cmdb_ci"])
    if not changes.empty:
        output += "🔧 **Recent Changes (Last 24h):**\n"
        for _, chg in changes.iterrows():
            output += f"- {chg['number']} | {chg['short_description']} | Risk: {chg['risk']}\n"
    else:
        output += "🔧 **No recent changes found**\n"

    # 2️⃣ Past Incident Correlation
    past = correlate_past_incidents(incident["cmdb_ci"])
    if not past.empty:
        output += "\n📊 **Past Incidents for this CI:**\n"
        for _, p in past.iterrows():
            output += f"- {p['number']} → {p['resolved_notes']}\n"
    else:
        output += "\n📊 **No past incidents found**\n"

    # 3️⃣ Knowledge Base + AI
    kb = search_kb(incident["short_description"])
    if not kb.empty:
        prompt = f"""
        Incident: {incident['short_description']}

        Past resolutions:
        {past[['resolved_notes']].to_string(index=False)}

        SOP:
        {kb.iloc[0]['text']}

        Provide step-by-step resolution and mention if this looks like a recurring issue.
        """
        ai_response = ask_ollama(prompt)
        output += "\n📘 **AI Suggested Resolution:**\n" + ai_response
    else:
        output += "\n📘 **No SOP found in KB**"

    st.subheader("🧾 AI Analysis Output")
    st.text_area("Result", output, height=400)
