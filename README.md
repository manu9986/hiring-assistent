# TalentScout Hiring Assistant 🤖

## Project Overview
The **TalentScout Hiring Assistant** is an AI-powered chatbot designed to streamline the hiring process by generating role-specific interview questions, evaluating candidate responses, and providing structured feedback. The chatbot ensures an interactive and insightful experience for both recruiters and candidates.

## Features
✅ **Candidate Information Collection** – Gathers candidate details (name, email, experience, tech stack, etc.).  
✅ **AI-Generated Interview Questions** – Dynamically generates 5 technical questions based on the candidate's role and experience.  
✅ **Automated Answer Evaluation** – Assesses responses, provides scores (0-10), and generates constructive feedback.  
✅ **PDF Report Generation** – Compiles candidate performance into a downloadable interview report.  
✅ **Seamless Streamlit Interface** – User-friendly, interactive web app for recruiters and candidates.  
✅ **Data Privacy Compliance** – Ensures GDPR-compliant data handling with no personal data storage.  

## Installation Instructions
### Prerequisites
- Python 3.8+
- A valid OpenAI API key (store in a `.env` file)

### Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/manu9986/hiring-assistent.git
   cd hiring-assistent
   ```
2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up your OpenAI API key**
   - Create a `.env` file in the project root and add:
     ```sh
     OPENAI_API_KEY=your_api_key_here
     ```
5. **Run the Streamlit app**
   ```sh
   streamlit run app.py
   ```

## Usage Guide
1. Enter your details (name, email, role, experience, tech stack, etc.).
2. The AI generates **5 role-specific technical questions**.
3. Answer each question in the provided text area.
4. Submit responses and receive **automated evaluation & feedback**.
5. Download a **PDF report** of your interview performance.
6. Optionally restart and take another interview.

## Technical Details
- **Framework:** Streamlit
- **Backend:** OpenAI GPT-3.5 Turbo
- **Data Processing:** Python (re, fpdf, dotenv, os)
- **Environment Management:** `.env` file for secure API handling
- **Deployment:** Compatible with Streamlit Sharing, Docker

## Prompt Design
- The AI dynamically generates questions based on **role, experience, and tech stack**.
- Avoids **repetitive or irrelevant** questions.
- Evaluates responses based on **correctness, clarity, and completeness**.

## Challenges & Solutions
### **1. API Rate Limits & Errors**
   - Implemented **error handling** and fallback mechanisms.
### **2. Ensuring Question Diversity**
   - Previous questions are stored and **excluded from future queries**.
### **3. Response Evaluation Consistency**
   - Used structured prompts to ensure **uniform scoring and feedback**.

## Future Enhancements 🚀
🔹 **Resume Upload & Parsing** – Extract skills and experiences from resumes.  
🔹 **Multilingual Support** – Generate questions in different languages.  
🔹 **Database Integration** – Store candidate responses for recruiter analysis.  
🔹 **Enhanced UI** – Improve design using **Streamlit components & animations**.  

## Contributing
Feel free to contribute by creating a pull request! 🚀

## License
MIT License © 2025 manu9986

