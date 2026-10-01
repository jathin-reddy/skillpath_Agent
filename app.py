import streamlit as st
from agent import SkillPathAgent

st.set_page_config(page_title="SkillPath Bharat", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:2rem;max-width:1200px}
.hero{padding:1.5rem;border-radius:18px;background:linear-gradient(135deg,#eef4ff,#f8f5ff);border:1px solid #dfe6f5;margin-bottom:1.5rem}
.hero h1{margin:0}.muted{color:#6b7280}.card{padding:1rem;border:1px solid #e5e7eb;border-radius:14px;background:#fff;margin-bottom:.7rem}
</style>
""", unsafe_allow_html=True)

ROLES = [
    "Machine Learning Engineer",
    "Python Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Data Analyst",
    "Data Scientist",
    "AI Engineer",
    "Data Engineer",
    "Cloud / DevOps Engineer",
    "Cybersecurity Analyst",
    "Mobile App Developer",
    "QA / Test Engineer",
    "UI/UX Designer",
    "Blockchain Developer",
    "Business Analyst",
    "Other",
]

st.markdown("""
<div class="hero">
<h1>🎓 SkillPath Bharat</h1>
<p><b>Agentic AI for Career Readiness & Future Skills</b></p>
<p class="muted">Analyze skills → identify gaps → build a personalized action plan → assess readiness → take the next step.</p>
</div>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None

with st.sidebar:
    st.header("🎯 Learner Profile")
    st.caption("Enter your information to generate a personalized learning pathway.")

    # Blank by default; the learner provides their own name.
    learner_name = st.text_input("Your name", value="", placeholder="Enter your name")

    # Education is selectable. Custom typing appears only for Other.
    education = st.selectbox(
        "Education",
        ["B.Tech / Engineering", "Degree", "Diploma", "Intermediate", "Other"],
    )

    education_value = education
    education_other = ""
    if education == "Other":
        education_other = st.text_input(
            "Enter your education",
            placeholder="e.g., BCA, MCA, B.Sc Computer Science",
        )
        education_value = education_other.strip()

    # Current stage is selection-only.
    current_stage = st.selectbox(
        "Current stage",
        ["1st Year", "2nd Year", "3rd Year", "Final Year", "Graduate / Job Seeker"],
    )

    # Blank by default; the learner enters their own current skills.
    skills = st.text_area(
        "Current skills",
        value="",
        placeholder="e.g., Python, SQL, Git, Machine Learning",
        help="Enter your current skills separated by commas.",
    )

    # Target pathway has 15 predefined roles. Custom typing appears only for Other.
    target = st.selectbox("Target pathway", ROLES)

    target_value = target
    target_other = ""
    if target == "Other":
        target_other = st.text_input(
            "Enter your target career",
            placeholder="e.g., Product Manager, AI Researcher",
        )
        target_value = target_other.strip()

    # Requested range: 1 to 15 hours/day.
    hours = st.slider(
        "Available learning time (hours/day)",
        min_value=1,
        max_value=15,
        value=3,
        step=1,
    )

    # Blank by default; the learner provides their own goal.
    goal = st.text_area(
        "Main goal",
        value="",
        placeholder="e.g., Become placement-ready and build strong AI/ML projects.",
    )

    st.divider()
    run = st.button(
        "🚀 Run SkillPath Agent",
        type="primary",
        use_container_width=True,
    )

if run:
    if not learner_name.strip():
        st.warning("Please enter your name.")
        st.stop()

    if not skills.strip():
        st.warning("Please enter your current skills.")
        st.stop()

    if education == "Other" and not education_value:
        st.warning("Please enter your education.")
        st.stop()

    if target == "Other" and not target_value:
        st.warning("Please enter your target career.")
        st.stop()

    if not goal.strip():
        st.warning("Please enter your main goal.")
        st.stop()

    profile = {
        "name": learner_name.strip(),
        "education": education_value,
        "current_stage": current_stage,
        "skills": skills,
        "target": target_value,
        "hours": hours,
        "goal": goal.strip(),
    }

    with st.spinner("Agent is analyzing your profile and building your personalized pathway..."):
        st.session_state.result = SkillPathAgent().run(profile)

result = st.session_state.result

if result:
    st.success("Agent run completed — your personalized career-readiness pathway is ready.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Readiness score", f"{result['readiness_score']}/100")
    c2.metric("Skill gaps", len(result["skill_gaps"]))
    c3.metric("Daily plan", f"{result['daily_hours']} hrs")

    st.subheader("🧠 Agent Decision")
    st.info(result["decision"])

    st.subheader("🔎 Priority Skill Gaps")
    for gap in result["skill_gaps"]:
        icon = "🔴" if gap["priority"] == "High" else ("🟡" if gap["priority"] == "Medium" else "🟢")
        st.markdown(
            f'<div class="card">{icon} <b>{gap["skill"]}</b> '
            f'<span class="muted">Priority: {gap["priority"]} · Current: {gap["current"]} · Target: {gap["target"]}</span></div>',
            unsafe_allow_html=True,
        )

    st.subheader("📅 Personalized 7-Day Action Plan")
    for day in result["plan"]:
        with st.expander(f"Day {day['day']} — {day['focus']}"):
            st.write(f"**Time:** {day['time']} hours")
            st.write(f"**Actions:** {day['actions']}")
            st.write(f"**Deliverable:** {day['deliverable']}")

    st.subheader("⚡ Next Action")
    st.success(result["next_action"])

    st.subheader("🔄 Agent Workflow Trace")
    st.code(
        "INPUT → PROFILE ANALYZER → GAP ANALYZER → READINESS SCORING → "
        "ROADMAP PLANNER → ASSESSMENT TOOL → ACTION RECOMMENDER → OUTCOME"
    )
else:
    st.markdown("""
    <div class="card">
    <h3>👋 Start your personalized pathway</h3>
    <p>Enter your name, skills and main goal, choose your education, current stage and target pathway, then run the agent.</p>
    <p class="muted">Education and target pathway show a custom input only when <b>Other</b> is selected. Learning time supports <b>1–15 hours/day</b>.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("BharatAgentic Hackathon • EdTech & Future Skills • SkillPath Bharat")
