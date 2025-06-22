
import streamlit as st
from generate import generate_mcqs
from export import export_to_doc
from utils import extract_text_from_pdf

def display_mcq(mcqs):
    st.title("Multiple Choice Questions")

    # Ensure correct initialization of answer tracking
    if 'user_answers' not in st.session_state or len(st.session_state.user_answers) != len(mcqs):
        st.session_state.user_answers = [None] * len(mcqs)

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    if st.button("Reset Choices"):
        for idx in range(len(mcqs)):
            st.session_state.pop(f"q_{idx}", None)
        st.session_state.user_answers = [None] * len(mcqs)
        st.session_state.submitted = False
        st.rerun()

    # 🔧 Form with submit button inside
    with st.form("mcq_form"):
        for idx, mcq in enumerate(mcqs):
            st.subheader(mcq['question'])
            options = mcq['choices']
            st.session_state.user_answers[idx] = st.radio(
                f"Select your answer for Question {idx+1}:",
                options,
                key=f"q_{idx}"
            )

        # ✅ Submit button placed inside the form block
        submitted = st.form_submit_button("Submit All Answers")
        if submitted:
            st.session_state.submitted = True

    # 🧠 Evaluation
    if st.session_state.submitted:
        correct = 0
        for idx, mcq in enumerate(mcqs):
            user_answer = st.session_state.user_answers[idx]
            correct_answer = mcq['answer']

            if user_answer == correct_answer:
                st.success(f"Question {idx+1}: Correct! The answer is {correct_answer}")
                correct += 1
            else:
                st.error(f"Question {idx+1}: Incorrect. The correct answer is {correct_answer}")

            # Show explanation if present
            if "explanation" in mcq:
                st.markdown(f"**🧠 Explanation:** {mcq['explanation']}")

        st.info(f"🎯 Final Score: {correct}/{len(mcqs)}")

    # 📄 Export option
    if st.button("Export to DOC"):
        doc_buffer = export_to_doc(mcqs)
        st.download_button(
            label="Download DOC",
            data=doc_buffer,
            file_name="mcqs.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


def main():
    st.sidebar.title("Quiz-N-learn")
    st.sidebar.write("This Web app displays 10 multiple-choice questions generated from PDF.")

    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)

        if st.sidebar.button("Generate New Questions"):
            st.session_state.pop('mcqs', None)
            st.session_state.user_answers = [None] * 5
            st.session_state.submitted = False
            for idx in range(10):
                st.session_state.pop(f"q_{idx}", None)
            st.rerun()

        if 'mcqs' not in st.session_state:
            with st.spinner('Generating MCQs...'):
                st.session_state.mcqs = generate_mcqs(pdf_text)

        if st.session_state.mcqs:
            st.sidebar.success("MCQs generated successfully!")
            display_mcq(st.session_state.mcqs)
        else:
            st.sidebar.error("Failed to generate MCQs.")
    else:
        st.sidebar.info("Upload a PDF to generate MCQs.")

if __name__ == "__main__":
    main()
