import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from io import BytesIO
from fpdf import FPDF


# Load environment variables from a .env file if available
load_dotenv()

# Set the OpenAI API key (ensure it’s stored securely)
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Define the system instruction
system_inst = """
You are an academic advisor AI assisting students in choosing a university major.
The user will provide details about their interests, strengths, and career goals, and based on this,
you need to recommend a suitable major for them.

The output should be an analysis and recommendation of different fields with focus on one in a string format and at least recommend one major.
Limit tokens to 500, dont repeat the answers of the question. can suggest from the taylors university courses if the recommended course not available in taylors just
suggest the name.
School of Architecture, Building and Design
Become an innovative architect shaping cities in Asia & beyond. Develop your creativity at Taylor's top architecture school to solve local & global challenges.

Bachelor of Science (Honours) in Architecture
Bachelor of Arts (Honours) in Interior Architecture
Bachelor of Quantity Surveying (Honours)
Bachelor of Science (Honours) in Sustainable Digital Construction Management
Master of Architecture
Master of Science in Virtual Design and Construction
Doctor of Philosophy in Architecture
School of Biosciences
Master in-demand bioscience skills at Taylor's. Our top-notch research labs and expert faculty equip you for careers in biotechnology, medical science & more.

Bachelor of Biomedical Science (Honours)
Bachelor of Food Science (Honours)
Bachelor of Biotechnology (Honours)
Bachelor of Applied Health Sciences (Honours)
Master of Science
Doctor of Philosophy in Science
Taylor's Business School
Taylor's leads as the top business school in Malaysia that offers dual awards with UWE & QUT, supported by strong industry links and innovative education.

Bachelor of Business (Honours)
Bachelor of Business (Honours) in International Business and Marketing
Bachelor of Accounting and Finance (Honours)
Bachelor of Banking and Finance (Honours)
Bachelor of Finance and Economics (Honours)
Bachelor of Actuarial Studies (Honours)
Bachelor of Entrepreneurship (Honours) in Team Entrepreneurship
Bachelor in Accounting (FinTech) (Honours)
Master of Business Administration
Master of Management
Master of Business Administration (100% Online)
Doctor of Business Administration
Doctor of Philosophy in Business
School of Food Studies and Gastronomy
A leading School for culinary arts studies in Southeast Asia with research-led teaching & Michelin-star internships, matching the growth in food studies.

Bachelor of Culinary Management (Honours)
Bachelor of Science (Honours) in Culinology
Bachelor of Patisserie Arts (Honours)
Master of Food Studies and Gastronomy
Master of Food Studies
Doctor of Philosophy In Food Studies
Taylor's Culinary Insitute
Taylor's Culinary Institute offers a world-class experience with its global curriculum and Michelin-starred internships to train future leaders of the industry.

Diploma in Hotel Management
Diploma in Culinary Arts
Advanced Diploma in Patisserie and Gastronomic Cuisine
School of Media and Communication
Renowned both locally and globally, students at Taylor’s School of Media and Communication will benefit from industry networks with valuable opportunities.

Bachelor of Mass Communication (Honours) in Advertising and Brand Management
Bachelor of Mass Communication (Honours) (Digital Media Production)
Bachelor of Mass Communication (Honours)
Bachelor of Mass Communication (Honours) in Public Relations and Event Management
Bachelor of Mass Communication (Honours) in Public Relations and Marketing
Master of Communication
Doctor of Philosophy in Media and Communication Studies
School of Computer Science
The School of Computer Science programmes build innovative technopreneurs and tech graduates skilled in data science, cybersecurity and cloud computing.

Bachelor of Computer Science (Honours)
Bachelor of Software Engineering (Honours)
Bachelor of Information Technology (Honours)
Master of Applied Computing (Coursework)
Master of Computer Science
Master of Applied Computing (100% Online)
Doctor of Philosophy in Computer Science
The Design School at Taylor's
Think outside the box across various design disciplines including Interior Design, Interior Architecture, Graphic Design, Creative Media and Animation.

Bachelor of Interactive Spatial Design (Honours)
Bachelor of Fashion Design Technology (Honours)
Bachelor of Design (Honours) In Creative Media
Master of Design
Doctor of Philosophy In Design Management
School of Education
Earn a degree in primary education at Taylor’s University; the first teacher development programme aiming to raise the standard of teaching in Malaysia.

Bachelor of Education (Honours)
Master of Teaching and Learning
Postgraduate Certificate in Teaching And Learning
Master of Education
Postgraduate Certificate in Education (100% online)
Master of Teaching and Learning (100% online)
Doctor Of Philosophy In Education
School of Engineering
The School of Engineering is SEA's 1st to offer the Grand Challenge Scholars Programme; Malaysia's 1st to use the CDIO™ Initiative for project-based learning.

Bachelor of Chemical Engineering (Honours)
Bachelor of Electrical and Electronic Engineering (Honours)
Bachelor of Mechanical Engineering (Honours)
Bachelor of Mechatronics Engineering (Honours)
Master of Science in Engineering
Doctor of Philosophy in Engineering
School of Hospitality, Tourism and Events
Leaders for hospitality education in SEA, we're an award-winning school for hospitality, tourism & events with high-quality teaching & impactful research.

Bachelor of International Hospitality Management (Honours)
Bachelor of International Events Management (Honours)
Bachelor of International Tourism Management (Honours)
Master of Global Hospitality Management (100% Online)
Master of International Hospitality Management
Master of Science in Tourism
Doctor of Philosophy In Hospitality & Tourism
School of Law and Governance
Get an LL.B. degree with CLP Recognition at a leading law school, learn Malaysian & UK law in a Dual Jurisdiction programme and transfer to our UK partners.

Bachelor of Laws (Honours)
Master of Laws in Healthcare and Medical Law
Master of Laws
Doctor of Philosophy in Law
School of Liberal Arts and Sciences
The multidisciplinary School of Liberal Arts & Sciences offers holistic and diverse education covering fields such as arts, humanities, and social sciences.

American Degree Transfer Program
Bachelor of Performing Arts (Honours)
Bachelor of Psychology (Honours)
Bachelor of Social Science (Honours) in International Relations
Intensive English
Master of Counselling
Master of Clinical Psychology
Doctor of Philosophy in Social Sciences
School of Pharmacy
The School of Pharmacy, fully accredited by the Malaysian Pharmacy Board, raises pharmaceutical education standards, producing excellent professionals.

Bachelor of Pharmacy with Honours
Bachelor of Pharmaceutical Science (Honours)
Master of Philosophy in Pharmaceutical Science
Master of Philosophy in Pharmacy
Doctor of Philosophy in Pharmaceutical Science
School of Medicine
Our leading medical school offers innovative teaching methods and personalised attention from specialists across undergraduate and postgraduate programmes.

Bachelor of Medicine, Bachelor of Surgery (MBBS)
Master of Science in Medical Science
Doctor of Philosophy in Medical Science
"""
def recommend_major_with_openai(student_profile):
    prompt = f"""
    Based on the following student profile, recommend a suitable university major:

    Interests: {student_profile.get('interests')}
    Strengths: {student_profile.get('strengths')}
    Career Goals: {student_profile.get('career_goals')}
    Skills: {student_profile.get('skills')}
    Confident Skills: {student_profile.get('confident_skills')}
    Proud Moments: {student_profile.get('proud_moments')}
    Work Preference: {student_profile.get('work_preference')}
    Learning Preference: {student_profile.get('learning_preference')}
    Collaboration Preference: {student_profile.get('collaboration_preference')}
    Difficult Aspects: {student_profile.get('difficult_aspects')}
    Setback Response: {student_profile.get('setback_response')}
    Learning Style: {student_profile.get('learning_style')}
    """

    # Generate recommendation with OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_inst},
            {"role": "user", "content": prompt}
        ]
    )

    # Return the recommendation text
    recommendation = response.choices[0].message.content.strip()
    return recommendation


def create_pdf(student_profile, recommendation):
    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)
    
    # Title
    pdf.cell(0, 10, "University Major Recommendation", ln=True, align="C")
    pdf.ln(10)

    # Add student profile
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Student Profile", ln=True)
    pdf.set_font("Arial", size=12)
    
    for key, value in student_profile.items():
        if value:
            pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)

    # Add recommendation
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Recommended Major:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, recommendation)

    # Save to a BytesIO stream
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    return pdf_buffer

# Initialize page in session state
if "page" not in st.session_state:
    st.session_state["page"] = 1  # Start on page 1

def go_to_next_page():
    st.session_state["page"] += 1

def go_to_first_page():
    st.session_state["page"] = 1

# Page 1: Front Page
if st.session_state["page"] == 1:
    st.markdown(
        """
        <style>
        .header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2B6CB0;
            text-align: center;
            padding-top: 2rem;
        }
        .subheader {
            font-size: 1.2rem;
            color: #4A5568;
            text-align: center;
            margin-top: -10px;
            padding-bottom: 2rem;
        }
        .center-btn {
            display: flex;
            justify-content: center;
            padding-top: 1rem;
        }
        .stButton>button {
            background-color: #3182CE;
            color: #FFFFFF;
            border: None;
            font-size: 1rem;
            padding: 0.75rem 1.5rem;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div class='header'>Education Consult</div>", unsafe_allow_html=True)
    st.markdown("<div class='subheader'>An education consultant directing students toward their dream courses</div>", unsafe_allow_html=True)
    
    # Get Started Button
    if st.button("Get Started", key="get_started"):
        st.session_state["page"] = 2  # Go to page 2

# Page 2: Questionnaire
elif st.session_state["page"] == 2:
    st.title("🎓 University Major Recommendation")
    st.write("Answer a few questions, and our AI will help guide your academic future.")
    
    st.subheader("Your Profile")
    
    st.markdown("### Personal Interests and Strengths")
    interests = st.text_input("💡 What activities or subjects do you enjoy most?", 
                              help="Mention subjects you like even if they're challenging.",
                              placeholder="E.g., Mathematics, Arts, Coding, etc.")
    strengths = st.text_input("📈 What are some of your strengths?",
                              help="List areas where you excel.",
                              placeholder="E.g., Logical thinking, public speaking.")

    st.markdown("### Career Goals and Skills")
    career_goals = st.text_input("🎯 What are your career goals?", 
                                 placeholder="E.g., Tech industry, leadership role.")
    skills = st.text_input("🔧 What are some skills you have?", 
                           placeholder="E.g., Programming, critical thinking.")

    # Optional Questions
    with st.expander("More About You (Optional)", expanded=False):
        confident_skills = st.text_input("What abilities or competencies do you feel most confident in?")
        proud_moments = st.text_input("Describe a time when you felt truly proud of an accomplishment.")
        work_preference = st.text_input("What work environment do you prefer?")
        learning_preference = st.text_input("Preferred learning experience (e.g., hands-on, research).")
        collaboration_preference = st.text_input("Do you prefer working independently or in a team?")
        difficult_aspects = st.text_input("Describe any challenging tasks you've overcome.")
        setback_response = st.text_input("How do you handle setbacks?")
        learning_style = st.text_input("Effective learning style for mastering new topics.")

    # Store profile data in session state
    st.session_state["student_profile"] = {
        "interests": interests,
        "strengths": strengths,
        "career_goals": career_goals,
        "skills": skills,
        "confident_skills": confident_skills,
        "proud_moments": proud_moments,
        "work_preference": work_preference,
        "learning_preference": learning_preference,
        "collaboration_preference": collaboration_preference,
        "difficult_aspects": difficult_aspects,
        "setback_response": setback_response,
        "learning_style": learning_style
    }

    # Proceed to the next page to get the recommendation
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Get Recommendation"):
            st.session_state["page"] = 3  # Go to page 3
    with col2:
        if st.button("Back to Start"):
            st.session_state["page"] = 1  # Go to the first page

# Page 3: Display Recommendation
elif st.session_state["page"] == 3:
    st.subheader("🎓 Recommended Major")
    st.write("Based on your inputs, here’s a major that aligns with your profile: ")
    
    with st.spinner("Generating your recommended major..."):
        try:
            # Generate recommendation
            recommendation = recommend_major_with_openai(st.session_state["student_profile"])
            st.success(recommendation)

            # Generate and download PDF
            pdf_buffer = create_pdf(st.session_state["student_profile"], recommendation)
            st.download_button(
                label="📄 Download Recommendation as PDF",
                data=pdf_buffer,
                file_name="recommendation.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Back to Start button at the bottom
    if st.button("Back to Start"):
        st.session_state["page"] = 1  # Go to the first pag