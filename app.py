import streamlit as st
import requests
import json

st.set_page_config(
    page_title="SOP → AI Training System",
    page_icon="📋",
    layout="centered"
)

SAMPLE_SOP = """Employee Onboarding SOP
Version: 2.1 | Department: Human Resources

Purpose:
This SOP outlines the standard process for onboarding new employees to ensure a smooth transition and productive start.

Scope:
Applies to all full-time and part-time employees joining the organization.

Procedure:

Step 1 - Pre-joining Preparation (3 days before joining)
- HR sends welcome email with joining details and documents checklist
- IT team sets up laptop, email account, and software access
- Reporting manager arranges workspace and team introduction
- Offer letter, NDA, and policy documents sent for digital signature

Step 2 - Day 1: Orientation
- New employee reports to HR at 9:00 AM
- Complete documentation: ID proof, bank details, PAN card
- Company introduction: vision, mission, values, org structure
- Office tour and introduction to key personnel
- Issue employee ID card and access badge

Step 3 - Week 1: Department Induction
- Reporting manager conducts role briefing and goal-setting session
- New employee attends team meetings and shadow sessions
- Access granted to all role-specific tools and platforms
- Buddy/mentor assigned for first 30 days

Step 4 - First 30 Days: Performance Check-in
- Weekly 1:1 meetings with manager
- Mid-point review at Day 15
- Completion of mandatory compliance training modules
- Feedback form submitted by employee at end of Day 30

Responsible Parties:
- HR Manager: Steps 1, 2
- IT Department: Step 1 (tech setup)
- Reporting Manager: Steps 3, 4

Key Policy Notes:
- All documents must be submitted within 3 business days of joining
- Failure to complete compliance training within 30 days results in system access suspension"""


def analyze_sop(api_key: str, sop_text: str) -> dict:
    prompt = f"""You are an expert training content creator. Analyze the following SOP document and return ONLY a valid JSON object. No markdown, no explanation, just raw JSON.

{{
  "title": "SOP title here",
  "department": "Department name here",
  "summary": {{
    "purpose": "1-2 sentence purpose of this SOP",
    "scope": "Who this SOP applies to",
    "key_points": ["Key point 1","Key point 2","Key point 3","Key point 4","Key point 5"]
  }},
  "training_steps": [
    {{
      "step": 1,
      "title": "Step title",
      "description": "Clear description of what happens in this step",
      "action_items": ["Specific action 1","Specific action 2","Specific action 3"]
    }}
  ],
  "responsible_parties": ["Role 1", "Role 2", "Role 3"],
  "quiz": [
    {{
      "question": "Question text here?",
      "options": ["A. Option one", "B. Option two", "C. Option three", "D. Option four"],
      "answer": "A",
      "explanation": "Why this answer is correct"
    }}
  ]
}}

Generate 4 to 5 training steps and exactly 4 quiz questions.

SOP Document:
{sop_text}"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )

    data = response.json()

    if "error" in data:
        raise Exception(data["error"]["message"])

    raw = data["choices"][0]["message"]["content"].strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def build_export_text(r: dict) -> str:
    lines = []
    lines.append("SOP TRAINING PACKAGE")
    lines.append("=" * 50)
    lines.append(f"Document   : {r.get('title', '')}")
    lines.append(f"Department : {r.get('department', '')}")
    lines.append("")
    lines.append("--- SUMMARY ---")
    s = r.get("summary", {})
    lines.append(f"Purpose : {s.get('purpose', '')}")
    lines.append(f"Scope   : {s.get('scope', '')}")
    lines.append("")
    lines.append("Key Points:")
    for i, point in enumerate(s.get("key_points", []), 1):
        lines.append(f"  {i}. {point}")
    lines.append("")
    lines.append("--- TRAINING STEPS ---")
    for step in r.get("training_steps", []):
        lines.append(f"\nStep {step['step']}: {step['title']}")
        lines.append(step.get("description", ""))
        for action in step.get("action_items", []):
            lines.append(f"  - {action}")
    lines.append("")
    lines.append("--- QUIZ ---")
    for i, q in enumerate(r.get("quiz", []), 1):
        lines.append(f"\nQ{i}: {q['question']}")
        for opt in q.get("options", []):
            lines.append(f"  {opt}")
        lines.append(f"Answer: {q['answer']} — {q.get('explanation', '')}")
    return "\n".join(lines)


# ── UI: Header ────────────────────────────────────────────────────────────────
st.title("📋 SOP → AI Training System")
st.markdown("Convert any **Standard Operating Procedure** into structured training content and quiz questions instantly using AI.")
st.divider()

# ── UI: Inputs ────────────────────────────────────────────────────────────────
api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...")
st.caption("Get your FREE API key at [console.groq.com](https://console.groq.com) — no credit card needed!")

st.markdown("#### 📄 SOP Document")

if st.button("Load Sample SOP (Employee Onboarding)"):
    st.session_state["sop_text"] = SAMPLE_SOP

sop_text = st.text_area(
    label="Paste your SOP here",
    value=st.session_state.get("sop_text", ""),
    height=280,
    placeholder="Paste your Standard Operating Procedure here...\n\nExample: Employee Onboarding SOP, Customer Support SOP, Quality Control SOP, etc."
)

st.divider()

# ── UI: Generate ──────────────────────────────────────────────────────────────
if st.button("✦ Generate Training Content", use_container_width=True, type="primary"):
    if not api_key:
        st.error("Please enter your Groq API key.")
    elif not sop_text.strip():
        st.error("Please paste an SOP document first.")
    else:
        with st.spinner("AI is analyzing your SOP and building training content..."):
            try:
                result = analyze_sop(api_key, sop_text)
                st.session_state["result"] = result
                st.success("Training content generated successfully!")
            except json.JSONDecodeError:
                st.error("Could not parse the response. Please try again.")
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

# ── UI: Results ───────────────────────────────────────────────────────────────
if "result" in st.session_state:
    r = st.session_state["result"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📄 Document", r.get("title", "SOP")[:18])
    col2.metric("🏢 Department", r.get("department", "General")[:14])
    col3.metric("📚 Steps", len(r.get("training_steps", [])))
    col4.metric("🎯 Questions", len(r.get("quiz", [])))

    st.divider()

    tab1, tab2, tab3 = st.tabs(["📋  Summary", "📚  Training Content", "🎯  Quiz"])

    # ── Tab 1: Summary ────────────────────────────────────────────────────────
    with tab1:
        s = r.get("summary", {})

        st.subheader("Purpose")
        st.write(s.get("purpose", ""))

        st.subheader("Scope")
        st.write(s.get("scope", ""))

        st.subheader("Key Points")
        for i, point in enumerate(s.get("key_points", []), 1):
            st.markdown(f"**{i}.** {point}")

        parties = r.get("responsible_parties", [])
        if parties:
            st.subheader("Responsible Parties")
            cols = st.columns(len(parties))
            for i, party in enumerate(parties):
                cols[i].info(party)

    # ── Tab 2: Training Content ───────────────────────────────────────────────
    with tab2:
        for step in r.get("training_steps", []):
            with st.expander(f"**Step {step['step']}: {step['title']}**", expanded=True):
                st.write(step.get("description", ""))
                items = step.get("action_items", [])
                if items:
                    st.markdown("**Action Items:**")
                    for action in items:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;✅ {action}")

    # ── Tab 3: Quiz ───────────────────────────────────────────────────────────
    with tab3:
        st.markdown("Test your understanding of the SOP:")
        st.write("")
        for i, q in enumerate(r.get("quiz", []), 1):
            st.markdown(f"**Q{i}. {q['question']}**")
            for opt in q.get("options", []):
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{opt}")
            with st.expander("Show Answer"):
                st.success(f"**Answer: {q['answer']}** — {q.get('explanation', '')}")
            st.write("")

    # ── Export ────────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📥 Export")
    export_text = build_export_text(r)
    st.download_button(
        label="⬇️ Download Training Package (.txt)",
        data=export_text,
        file_name="sop_training_package.txt",
        mime="text/plain",
        use_container_width=True
    )