import streamlit as st
from extractor import extract_text
from processor import generate_summary, generate_training, generate_quiz

# ── Page Configuration ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SOP AI Trainer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; }
    .stDownloadButton button { width: 100%; margin-top: 1rem; }
    .config-box {
        background: #1e1e2e;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("SOP AI Trainer")

    st.divider()
    st.markdown("### How to Use")
    st.markdown("""
    1. Upload your SOP (PDF or TXT)
    2. Select **Role** and **Detail Level**
    3. Preview the extracted text
    4. Click **Generate Training Content**
    5. View results in the 3 tabs i.e. Summary, Training Guide and Quiz 
    6. Download any output (or all)
    """)
    

# ── Main Header ───────────────────────────────────────────────────────────────

st.title("Trainify AI")
st.markdown(
    "Upload any **Standard Operating Procedure** and instantly generate "
    "a structured summary, employee training guide, and evaluation quiz."
)
st.divider()

# ── File Upload ───────────────────────────────────────────────────────────────

col_upload, col_info = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload your SOP document",
        type=["pdf", "txt"],
        help="Supports PDF (text-based) and plain text .txt files"
    )

with col_info:
    st.info(
        "**Supported Formats**\n\n"
        "✅ PDF (text-based)\n\n"
        "✅ Plain Text (.txt)\n\n"
        "❌ Scanned / image PDFs"
    )


# ── Configuration Panel ───────────────────────────────────────────────────────

st.subheader("")
col1, col2 = st.columns(2)

with col1:
    role = st.selectbox(
        "👤 Target Role",
        options=["Intern", "Employee", "Manager"],
        help="Content tone and complexity will be tailored to this role"
    )
    role_descriptions = {
        "Intern": "🟢 Simple language, every term explained, encouraging tone",
        "Employee": "🔵 Professional tone, assumes basic workplace knowledge",
        "Manager": "🔴 Concise, focuses on oversight, compliance and team impact"
    }
    st.caption(role_descriptions[role])

with col2:
    detail_level = st.selectbox(
        "📊 Detail Level",
        options=["Short", "Medium", "Detailed"],
        index=1,
        help="Controls depth of training content and quiz complexity"
    )
    detail_descriptions = {
        "Short": "⚡ Quick overview, 4-5 steps, 2 quiz questions",
        "Medium": "📋 Balanced content, 6-8 steps, 4 quiz questions + why it matters",
        "Detailed": "📚 Full depth, 8-10 steps, 5 questions + mistakes to avoid"
    }
    st.caption(detail_descriptions[detail_level])

st.divider()



# ── Document Processing ───────────────────────────────────────────────────────

if uploaded_file is not None:

    with st.spinner("Reading your document..."):
        try:
            sop_text = extract_text(uploaded_file)
        except ValueError as e:
            st.error(f"❌ {str(e)}")
            st.stop()

    # Document stats
    word_count = len(sop_text.split())
    char_count = len(sop_text)

    m1, m2 = st.columns(2)
    m1.metric("📄 File", uploaded_file.name[:20])
    m2.metric("📝 Words", f"{word_count:,}")

    # Preview
    with st.expander("🔍 Preview extracted text"):
        preview = sop_text[:800] + ("..." if len(sop_text) > 800 else "")
        st.text_area("Extracted content", preview, height=200, disabled=True)

    st.success("✅ Document loaded successfully and ready to process.")
    st.divider()

    # ── Generate Button ───────────────────────────────────────────────────────

    if st.button("🚀 Generate Training Content", type="primary", use_container_width=True):

        summary, training, quiz = None, None, None

        with st.status("AI is analysing your SOP...", expanded=True) as status:

            st.write("📌 Generating structured summary...")
            try:
                summary = generate_summary(sop_text,role,detail_level)
                st.write("✅ Summary done")
            except RuntimeError as e:
                status.update(label="Failed", state="error")
                st.error(str(e))
                st.stop()

            st.write("📚 Building step-by-step training guide...")
            try:
                training = generate_training(sop_text,role, detail_level)
                st.write("✅ Training guide done")
            except RuntimeError as e:
                status.update(label="Failed", state="error")
                st.error(str(e))
                st.stop()

            st.write("❓ Creating quiz questions...")
            try:
                quiz = generate_quiz(sop_text,role, detail_level)
                st.write("✅ Quiz done")
            except RuntimeError as e:
                status.update(label="Failed", state="error")
                st.error(str(e))
                st.stop()

            status.update(
                label="✅ All content generated!",
                state="complete",
                expanded=False
            )

        # ── Results Tabs ──────────────────────────────────────────────────────

        st.divider()
        st.subheader("Your Generated Training Content")

        tab1, tab2, tab3 = st.tabs(["📌 Summary", "📚 Training Guide", "❓ Quiz"])

        with tab1:
            st.markdown("### Key Takeaways from the SOP")
            st.divider()
            # Split bullets into separate lines and render each one
            lines = summary.split("•")
            for line in lines:
                line = line.strip()
                if line:
                    st.markdown(f"• {line}")
                    st.markdown("")
            st.download_button(
                "⬇️ Download Summary",
                data=summary,
                file_name="sop_summary.txt",
                mime="text/plain",
                use_container_width=True
            )

        with tab2:
            st.markdown("### Step-by-Step Training Guide")
            st.divider()
            import re

            # Split on "Step X:" and render each on its own line
            steps = re.split(r'(?=Step \d+:)', training.strip())

            for section in steps:
                section = section.strip()
                if section:
                    st.markdown(section)
                    st.markdown("")

            st.download_button(
                "⬇️ Download Training Guide",
                data=training,
                file_name="sop_training_guide.txt",
                mime="text/plain",
                use_container_width=True
            )

        with tab3:
            st.markdown("### Evaluation Quiz")
            st.divider()
            
            import re
            # Split quiz into question blocks
            question_blocks = re.split(r'\n(?=Q\d+\.)', quiz.strip())

            for i, block in enumerate(question_blocks):
                if not block.strip():
                    continue

                lines = block.strip().split("\n")

                question_text = ""
                question_type = ""
                options_list = []
                answer_text = ""
                explanation_text = ""

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if re.match(r'^Q\d+\.', line):
                        question_text = line
                    elif line.startswith("Type:"):
                        question_type = line.replace("Type:", "").strip()
                    elif line.startswith("Options:"):
                        options_raw = line.replace("Options:", "").strip()
                        options_list = re.split(r'\s+(?=[A-D]\))', options_raw)
                    elif line.startswith("Answer:"):
                        answer_text = line.replace("Answer:", "").strip()
                    elif line.startswith("Explanation:"):
                        explanation_text = line.replace("Explanation:", "").strip()


                # ── Render the question ───────────────────────────────────────────

                st.markdown(f"#### {question_text}")
                st.caption(f"📝 {question_type}")

                # Options (MCQ)
                if options_list:
                    for opt in options_list:
                        opt = opt.strip()
                        if opt:
                            st.markdown(
                                f'<div style="padding: 6px 12px; margin: 4px 0; '
                                f'background: #1e1e2e; border-radius: 6px; '
                                f'border-left: 3px solid #555;">{opt}</div>',
                                unsafe_allow_html=True
                            )

                # True/False display
                if "true" in question_type.lower() or "false" in question_type.lower():
                    col_t, col_f = st.columns(2)
                    with col_t:
                        st.markdown(
                            '<div style="text-align:center; padding: 6px; '
                            'background:#1e1e2e; border-radius:6px; '
                            'border: 1px solid #555;">✔️ True</div>',
                            unsafe_allow_html=True
                        )
                    with col_f:
                        st.markdown(
                            '<div style="text-align:center; padding: 6px; '
                            'background:#1e1e2e; border-radius:6px; '
                            'border: 1px solid #555;">❌ False</div>',
                            unsafe_allow_html=True
                        )

                # ── Answer ────────────────────────────────────────────────────────
                if answer_text:
                    st.markdown(
                        f'<div style="padding: 10px 16px; margin-top: 10px; '
                        f'background:#0a2e1a; border-radius: 6px; '
                        f'border-left: 4px solid #00c853;">'
                        f'<span style="color:#00c853; font-weight:bold;">'
                        f'✅ Answer: {answer_text}</span></div>',
                        unsafe_allow_html=True
                    )

                # ── Explanation ───────────────────────────────────────────────────
                if explanation_text:
                    st.markdown(
                        f'<div style="padding: 10px 16px; margin-top: 6px; '
                        f'background:#0a1a2e; border-radius: 6px; '
                        f'border-left: 4px solid #82b1ff;">'
                        f'<span style="color:#82b1ff;">'
                        f'💡 {explanation_text}</span></div>',
                        unsafe_allow_html=True
                    )

                st.markdown("<br>", unsafe_allow_html=True)

            st.divider()
            st.download_button(
                "⬇️ Download Quiz",
                data=quiz,
                file_name="sop_quiz.txt",
                mime="text/plain",
                use_container_width=True
            )

        # ── Full Report Download ──────────────────────────────────────────────

        st.divider()
        full_report = f"""SOP AI TRAINING SYSTEM — COMPLETE REPORT
Source file: {uploaded_file.name}
Role: {role}
Detail Level: {detail_level}
{'=' * 60}

SECTION 1: SUMMARY
{'=' * 60}
{summary}

SECTION 2: TRAINING GUIDE
{'=' * 60}
{training}

SECTION 3: QUIZ
{'=' * 60}
{quiz}
"""
        st.download_button(
            "📦 Download Full Report (All 3 Sections)",
            data=full_report,
            file_name="sop_full_report.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )



