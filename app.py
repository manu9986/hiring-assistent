import streamlit as st
from openai import OpenAI
import os
import re
from fpdf import FPDF
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables for secure API key handling
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client securely
if not OPENAI_API_KEY:
    st.error("OpenAI API key is missing. Please check your .env file.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_questions(job_role, tech_stack, experience, previous_questions=[]):
    """Generates technical interview questions tailored to the candidate's profile."""
    prompt = f"""
    You are an AI recruiter generating technical interview questions.

    - Role: **{job_role}**
    - Experience: **{experience} years**
    - Tech Stack: **{', '.join(tech_stack)}**
    - Avoid these previous questions: **{'; '.join(previous_questions)}**

    Generate **5** new technical questions:
    - Relevant to both the role and tech stack.
    - Increasing in difficulty.
    - Avoid yes/no questions.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI recruiter generating interview questions."},
                {"role": "user", "content": prompt}
            ]
        )
        raw_questions = response.choices[0].message.content
        questions = re.findall(r"\d+\.\s*(.*)", raw_questions)  # Extract numbered questions
        return questions if questions else [raw_questions]  # Fallback if regex fails
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

def evaluate_answer(question, answer):
    """Evaluates the answer and provides a score (0-10) and feedback."""
    eval_prompt = f"""
    Evaluate this answer for a technical interview.

    Question: {question}
    Candidate's Answer: {answer}

    - Assign a score (0-10) based on correctness, clarity, and completeness.
    - Provide constructive feedback.

    Format:
    Score: (0-10)
    Feedback: (Detailed feedback)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI technical recruiter."},
                {"role": "user", "content": eval_prompt}
            ]
        )
        evaluation = response.choices[0].message.content
        score_match = re.search(r"Score:\s*(\d+)", evaluation)
        feedback_match = re.search(r"Feedback:\s*(.*)", evaluation, re.DOTALL)

        score = int(score_match.group(1)) if score_match else 0
        feedback = feedback_match.group(1).strip() if feedback_match else "No feedback provided."

        return score, feedback
    except Exception as e:
        st.error(f"Error evaluating answer: {e}")
        return 0, "Evaluation failed."

def generate_pdf(full_name, email, questions, answers, scores, feedbacks):
    """Generates a downloadable PDF report."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)

    pdf.cell(200, 10, "TalentScout Interview Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Candidate: {full_name}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.ln(10)

    for i, (q, ans, score, feedback) in enumerate(zip(questions, answers, scores, feedbacks), 1):
        pdf.set_font("Arial", style="B", size=12)
        pdf.multi_cell(0, 10, f"Q{i}: {q}")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Answer: {ans if ans.strip() else 'No answer provided'}")
        pdf.multi_cell(0, 10, f"Score: {score}/10")
        pdf.multi_cell(0, 10, f"Feedback: {feedback}")
        pdf.ln(5)

    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

st.title("TalentScout Hiring Assistant 🤖")
st.write("Hello! I’ll guide you through your technical interview screening.")

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "responses" not in st.session_state:
    st.session_state.responses = []
if "scores" not in st.session_state:
    st.session_state.scores = []
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if st.session_state.stage == "greeting" or not st.session_state.form_submitted:
    # Collect Candidate Information
    with st.form("candidate_form"):
        st.subheader("📄 Candidate Information")

        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email Address", placeholder="johndoe@email.com")
            phone = st.text_input("Phone Number", placeholder="+1 234 567 890")

        with col2:
            experience = st.slider("Years of Experience", 0, 20, 1)
            position = st.text_input("Desired Position", placeholder="Software Engineer")
            location = st.text_input("Current Location", placeholder="Bengaluru, Karnataka")

        tech_stack = [tech.strip() for tech in st.text_area("Tech Stack (comma-separated)", placeholder="Python, Django, React").split(',') if tech.strip()]

        submit = st.form_submit_button("Submit 🔥")

    if submit:
        if not full_name or not email or not tech_stack or not position:
            st.error("Please fill in all required fields: Full Name, Email, Tech Stack, and Desired Position.")
        else:
            st.session_state.full_name = full_name
            st.session_state.email = email
            st.session_state.questions = generate_questions(position, tech_stack, experience)
            st.session_state.stage = "question_answering"
            st.session_state.form_submitted = True
            st.session_state.responses = [""] * len(st.session_state.questions)
            st.session_state.scores = [0] * len(st.session_state.questions)
            st.session_state.feedbacks = [""] * len(st.session_state.questions)
            st.rerun()  # Force refresh without redirecting


if st.session_state.stage == "question_answering":
    with st.form("answers_form"):
        st.subheader("✍️ Answer the Following Questions")
        for i, q in enumerate(st.session_state.questions):
            st.write(f"**Q{i+1}:** {q.strip()}")
            st.session_state.responses[i] = st.text_area(
                f"Your Answer to Q{i+1}:",
                value=st.session_state.responses[i],
                key=f"answer_{i}",
                placeholder="Type your answer here..."
            )
        submit_answers = st.form_submit_button("Submit Answers")

    if submit_answers:
        st.success("Evaluating responses...")

        for i, (q, ans) in enumerate(zip(st.session_state.questions, st.session_state.responses)):
            if ans.strip():  # Only evaluate if the answer is not empty
                score, feedback = evaluate_answer(q, ans)
                st.session_state.scores[i] = score
                st.session_state.feedbacks[i] = feedback
            else:
                st.session_state.scores[i] = 0
                st.session_state.feedbacks[i] = "No answer provided."

        st.success("Evaluation complete! Here are your results:")

        for i, (q, ans, score, feedback) in enumerate(zip(st.session_state.questions, st.session_state.responses, st.session_state.scores, st.session_state.feedbacks)):
            st.subheader(f"🔹 Question {i+1}")
            st.write(f"**{q.strip()}**")

            st.progress(score / 10)  # Show score as a progress bar

            if score >= 8:
                st.success(f"🌟 Score: {score}/10")
            elif score >= 5:
                st.warning(f"⚡ Score: {score}/10")
            else:
                st.error(f"❌ Score: {score}/10")

            st.write(f"💡 **Feedback:** {feedback}")
            st.divider()

        pdf_report = generate_pdf(st.session_state.get('full_name', ''), st.session_state.get('email', ''), st.session_state.questions, st.session_state.responses, st.session_state.scores, st.session_state.feedbacks)

        # Display Thank You Message and Download Button
        st.success("Thank you for completing the interview! You can download your report below.")

        download_clicked = st.download_button(
            label="📄 Download Your Interview Report",
            data=pdf_report,
            file_name=f"{st.session_state.get('full_name', 'interview')}_report.pdf",
            mime="application/pdf",
            help="Click to download your interview assessment report."
        )



        
exit_clicked = st.button("❌ Exit Interview & Fill Form Again")

if exit_clicked:
    # Reset specific session state variables
    st.session_state.clear()  # Clears all stored values in session state
    st.rerun()  # Ensures Streamlit restarts fresh
            



