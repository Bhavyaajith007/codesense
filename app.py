import streamlit as st
from orchestrator import analyze_code

# --- Page Config ---
st.set_page_config(
    page_title="CodeSense",
    page_icon="🔍",
    layout="wide"
)

# --- Header ---
st.title("🔍 CodeSense")
st.markdown("*AI-powered code review, bug detection, and test generation*")
st.divider()

# --- Input Section ---
col1, col2 = st.columns([3, 1])

with col1:
    code_input = st.text_area(
        "Paste your Python code here",
        height=250,
        placeholder="""def divide(a, b):
    return a / b

def get_first(items):
    return items[0]"""
    )

with col2:
    traceback_input = st.text_area(
        "Paste error traceback (optional)",
        height=150,
        placeholder="Traceback (most recent call last):\n  ..."
    )
    analyze_btn = st.button("🚀 Analyze Code", use_container_width=True, type="primary")

# --- Analysis ---
if analyze_btn:
    if not code_input.strip():
        st.warning("Please paste some code first!")
    else:
        with st.spinner("Running all agents..."):
            result = analyze_code(code_input, traceback_input)

        st.divider()

        # --- Score Banner ---
        score = result.quality_report.overall_score
        grade = result.quality_report.grade
        bugs = result.bug_report.total_bugs
        tests = result.test_suite.total_tests

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Quality Score", f"{score}/100")
        m2.metric("Grade", grade)
        m3.metric("Bugs Found", bugs)
        m4.metric("Tests Generated", tests)

        st.divider()

        # --- Tabs ---
        tab1, tab2, tab3, tab4 = st.tabs([
            "🐛 Bugs", "📊 Quality", "✅ Tests", "💡 Error Explainer"
        ])

        # Bug Tab
        with tab1:
            st.subheader(f"Bug Report — {result.bug_report.overall_verdict}")
            if result.bug_report.bugs:
                for i, bug in enumerate(result.bug_report.bugs, 1):
                    color = "🔴" if bug.severity == "high" else "🟡" if bug.severity == "medium" else "🟢"
                    with st.expander(f"{color} Bug {i} — {bug.description[:60]}..."):
                        st.markdown(f"**Location:** `{bug.line}`")
                        st.markdown(f"**Severity:** `{bug.severity}`")
                        st.markdown(f"**Problem:** {bug.description}")
                        st.markdown(f"**Fix:** {bug.fix}")
            else:
                st.success("No bugs found! Clean code 🎉")

        # Quality Tab
        with tab2:
            st.subheader(f"Quality Score: {score}/100 — Grade {grade}")
            for cat in result.quality_report.categories:
                st.markdown(f"**{cat.category}**")
                st.progress(cat.score / 100)
                st.caption(cat.feedback)
            st.divider()
            c1, c2 = st.columns(2)
            c1.success(f"💪 Strength: {result.quality_report.top_strength}")
            c2.warning(f"⚠️ Improve: {result.quality_report.top_improvement}")

        # Tests Tab
        with tab3:
            st.subheader(f"{tests} Tests Generated")
            st.caption(f"Setup: {result.test_suite.setup_notes}")
            full_test_code = "import pytest\n\n"
            for test in result.test_suite.test_cases:
                full_test_code += test.code + "\n\n"
            st.code(full_test_code, language="python")
            st.download_button(
                "⬇️ Download test file",
                full_test_code,
                file_name="test_generated.py",
                mime="text/plain"
            )

        # Error Explainer Tab
        with tab4:
            if result.error_explanation:
                st.subheader(f"Error: {result.error_explanation.error_type}")
                st.markdown(f"**What happened:** {result.error_explanation.plain_english}")
                st.markdown(f"**Root cause:** {result.error_explanation.root_cause}")
                st.markdown(f"**Fix:** {result.error_explanation.fix}")
                st.info(f"💡 Prevention: {result.error_explanation.prevention}")
            else:
                st.info("Paste a traceback in the input box to get an error explanation.")