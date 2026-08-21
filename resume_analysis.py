import streamlit as st 
from utils import extract_pdf, create_vector_store 
 
from langchain_community.llms import Ollama 
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.runnables import RunnablePassthrough 
 
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

/* Main Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: white;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 18px;
    margin-bottom: 35px;
}

/* Section Titles */
.section-title {
    font-size: 22px;
    font-weight: 600;
    color: white;
    margin-bottom: 15px;
}

/* Analyze Button */
.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: 600;
}

/* Text Area */
textarea {
    background-color: #262833 !important;
    color: white !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background-color: #262833;
    border-radius: 10px;
    padding: 10px;
}

/* File Uploader Text */
[data-testid="stFileUploader"] label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown(
    '<div class="title">📄 Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume against a job description using AI</div>',
    unsafe_allow_html=True
)


# ---------------- INPUT SECTION ----------------

col1, col2 = st.columns(2)


# -------- RESUME --------

with col1:

    st.markdown(
        '<div class="section-title">📄 Upload Resume</div>',
        unsafe_allow_html=True
    )

    resume_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )


# -------- JOB DESCRIPTION --------

with col2:

    st.markdown(
        '<div class="section-title">💼 Job Description</div>',
        unsafe_allow_html=True
    )

    jd_text = st.text_area(
        "Paste the Job Description here",
        height=200,
        placeholder="Paste the job description here..."
    )


# ---------------- ANALYZE BUTTON ----------------

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Analyze Resume"):

    if resume_file and jd_text:

        with st.spinner("Analyzing your resume..."):

            # Extract Resume 
            resume_text = extract_pdf(resume_file) 
 
            # Combine resume text + JD 
            combine_text = resume_text + "\n\n" + jd_text 
 
            # Create vector store 
            vectorstore = create_vector_store(combine_text) 
 
            # Retriever 
            retriever = vectorstore.as_retriever() 
 
            llm = Ollama(model="gemma2:2b") 
 
 
            # Prompt template Design
            prompt = ChatPromptTemplate.from_template(""" 
            You are an AI placement coach for help4code. 
            COntext: 
            {context} 
 
            Question: 
            {question} 
 
            1. Skill gap analysis 
            2. Missing technologies and skills 
            3. ATS score (0-100) 
            4. Technical interview questions 
            5. Resume improvement suggestions 
            6. Strengths of the candidate 
            7. Weaknesses of the candidate 
            8. Recommended skills to learn 
            9. Job role suitability analysis 
            10. Recommended job roles 
            11. Required technologies for the target job role 
            12. Comparison between candidate skills and job requirements 
            13. Missing keywords for ATS optimization 
            14. Resume formatting and structure suggestions 
            15. Project improvement suggestions 
            """)


            chain = ( 
                { 
                    "context": retriever, 
                    "question": RunnablePassthrough() 
                } 
                | prompt 
                | llm 
                | StrOutputParser() 
            ) 
 
            response = chain.invoke(
                "Analyze resume against job description"
            )

        # ---------------- RESULT ----------------

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">📊 Analysis Result</div>',
            unsafe_allow_html=True
        )

        st.write(response)

    else:

        st.warning(
            "⚠️ Please upload a resume and job description."
        )