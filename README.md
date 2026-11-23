# wca-ai-tool-s12-careertrack

**CareerTrack AI – Smart Job Application Tracker**

*Track Applications. Remember Opportunities. Build Careers.*

An AI-powered Job Application Tracker built with Python and Anthropic Claude API to help job seekers organize applications, track interviews, manage follow-ups, and receive intelligent career assistance through conversation memory.

## 1. Project Overview

CareerTrack AI is a Python-based AI-powered job application management system designed to help job seekers organize, manage, and monitor their job applications.

It integrates Anthropic Claude AI to provide intelligent career assistance, answer questions about saved applications, maintain conversation memory, and generate session summaries.

## 2. Problem Statement

Job seekers often struggle to manage multiple job applications, remember deadlines, track interview dates, and follow up with potential employers.

CareerTrack AI addresses these challenges through a centralized application tracking system supported by AI-powered career assistance.

## 3. Project Objectives

- Simplify job application management.
- Monitor application progress.
- Manage interview dates and follow-ups.
- Provide AI-powered career assistance.
- Maintain conversation history and memory.
- Generate AI session summaries.

## 4. Key Features

**Job Application Management**
- Add, view, update, and delete applications.
- Search saved applications.
- Track application progress.

**Application Status Tracking**
- Applied
- Shortlisted
- Interview
- Rejected
- Offered

**Interview and Follow-up Management**
- Record interview dates.
- Manage follow-up information.
- Monitor recruitment progress.

**AI-Powered Assistant**
- Claude AI integration.
- Personalized career guidance.
- Assistance with saved job applications.
- Context-aware conversations.

**Session Management**
- Create new AI sessions.
- Retrieve previous sessions.
- Maintain conversation history.
- Generate session summaries.

## 5. Technologies Used

- Python
- Anthropic Claude API
- JSON
- python-dotenv
- Git and GitHub

## 6. Project Structure

```text
wca-ai-tool-s12-careertrack/
│
├── main.py
├── ai_assistant.py
├── memory.py
├── job_tracker.py
├── summary.py
├── prompts.py
│
├── data/
├── sessions/
│
├── test_memory.py
├── test_job_tracker.py
├── test_summary.py
├── test_ai_assistant.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 7. Installation and Setup

**Clone the repository**

```bash
git clone https://github.com/mersemaritim01-pixel/wca-ai-tool-s12-careertrack.git
```

**Navigate to the project folder**

```bash
cd wca-ai-tool-s12-careertrack
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Configure environment variables**

Create a `.env` file in the project directory and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

Keep your API key private. Never upload your `.env` file to GitHub.

## 8. Running the Application

Start CareerTrack AI using:

```bash
python main.py
```

## 9. Application Menu

The application provides the following options:

1. Add Job Application
2. View All Applications
3. Update Application
4. Delete Application
5. Search Applications
6. View Application Summary
7. Ask CareerTrack AI
8. Exit

## 10. Testing

Run individual tests using:

```bash
python test_memory.py
python test_job_tracker.py
python test_summary.py
python -m unittest test_ai_assistant.py
```

## 11. Current Development Status

CareerTrack AI has implemented job application management, AI integration with Anthropic Claude, conversation memory, session management, and AI-powered session summaries.

Further development will focus on expanding its functionality and transitioning towards a web-based platform.

## 12. Contributors

Developed collaboratively by:

1. Mercy Chepkurui
2. David David Muhuha Maina
3. Florence Njeri Mucuthi

**Programme:** WECAN Season 12

## 13. Future Improvements

- AI-powered CV builder.
- AI-generated cover letters.
- Web-based application interface.
- M-Pesa payment integration.
- Job search integration.
- Application reminders and notifications.
- Downloadable application reports.

---

**CareerTrack AI – Making Job Application Management Smarter.**