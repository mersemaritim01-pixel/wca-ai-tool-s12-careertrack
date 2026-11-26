# CareerTrack AI – Smart Job Application Tracker

**Track Applications. Remember Opportunities. Build Careers.**

## 1. Project Overview

CareerTrack AI is a Python-based AI-powered job application management system designed to help job seekers organise their applications, monitor recruitment progress, and receive personalised career assistance using Anthropic Claude AI.

The system combines job application tracking with an intelligent AI assistant that supports career guidance, interview preparation, and job application-related queries.

CareerTrack AI also incorporates conversation memory, allowing users to maintain context during AI interactions, save previous sessions, and retrieve session summaries.

## 2. Problem Statement

Job seekers often struggle to manage multiple job applications, remember application details, monitor recruitment progress, and keep track of previous career-related discussions.

Managing this information manually can result in missed opportunities, disorganised records, and difficulty following up on applications.

CareerTrack AI addresses these challenges by providing a centralised application management system with AI-powered career assistance.

## 3. Key Features

### Job Application Management
- Add new job applications.
- View all saved applications.
- Update existing application details.
- Delete job application records.
- Search applications by company name or job title.

### Application Status Tracking

The system supports six application statuses:

- Applied
- Under Review
- Interview
- Rejected
- Offer
- Withdrawn

### Application Summary
- View total job applications.
- Monitor active applications.
- View application status breakdowns.
- Track interviews, offers, rejections, and withdrawn applications.

### AI-Powered Career Assistance
- Receive AI-powered career guidance.
- Get assistance with interview preparation.
- Ask questions about saved job applications.
- Receive personalised responses using available application information and conversation context.
- Get suggested next actions.

### Conversation Memory and Session Management
- Maintain conversation history.
- Retain up to four conversation turns (eight messages).
- Save conversations in JSON format.
- Open previously saved sessions.
- Generate and save session summaries.
- Review key advice, discussion topics, and suggested next steps.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Anthropic Claude API | AI-powered career assistance |
| JSON | Application and conversation data storage |
| python-dotenv | Environment variable management |
| Git | Version control |
| GitHub | Source code hosting and collaboration |
| VS Code | Development environment |

**AI Model:** Claude Sonnet 4.6 (`claude-sonnet-4-6`).

## 5. Project Structure

```text
CareerTrack-AI/
│
├── main.py
├── job_tracker.py
├── ai_assistant.py
├── memory.py
├── summary.py
├── prompts.py
│
├── data/
│   └── applications.json
│
├── sessions/
│   └── saved session files
│
├── test_ai_assistant.py
├── test_job_tracker.py
├── test_memory.py
├── test_summary.py
│
├── .env
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

### Description of Main Modules

- **main.py:** Runs the application and connects the different modules.
- **job_tracker.py:** Handles adding, viewing, updating, deleting, searching, and storing job applications.
- **ai_assistant.py:** Handles Claude API integration, AI response validation, conversation interaction, and session summary generation.
- **memory.py:** Manages conversation history, session IDs, and JSON-based session storage.
- **summary.py:** Calculates and displays job application statistics.
- **prompts.py:** Contains the AI system instructions, summary instructions, and functions for preparing information sent to Claude.
- **test files:** Contain tests for the different application modules.

## 6. Installation and Setup

### Prerequisites

- Python installed on your computer.
- An Anthropic API key.
- Internet connectivity for AI-powered functionality.
- Git installed (for cloning the repository).

### Step 1: Clone the Repository

```bash
git clone https://github.com/mersemaritim01-pixel/wca-ai-tool-s12-careertrack.git
```

### Step 2: Navigate to the Project Directory

```bash
cd wca-ai-tool-s12-careertrack
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Anthropic API

Create a `.env` file in the project root directory and add your API key:

```env
Our API key is stored in .env

### Step 5: Run the Application

```bash
python main.py
winpty python main.py
```

## 7. AI Integration

CareerTrack AI integrates Anthropic Claude AI to provide intelligent career assistance.

The application uses the Claude Sonnet 4.6 model to:

- Answer job application-related questions.
- Provide career guidance and interview preparation.
- Use available job application records when responding.
- Maintain conversational context.
- Generate session summaries.

The AI integration is implemented in `ai_assistant.py`, while the system instructions and summary instructions are defined in `prompts.py`.

The application validates AI responses to ensure they follow the expected JSON structure. Invalid responses trigger a retry mechanism before a fallback response is returned.

## 8. Conversation Memory and Data Storage

CareerTrack AI uses JSON-based storage to maintain application records and conversation sessions.

**Job Application Storage**

Application records are stored in:

```text
data/applications.json
```

Each record contains:
- Unique application ID.
- Company name.
- Job title.
- Location.
- Application date.
- Application status.
- Notes.

**Conversation Storage**

Conversation sessions are stored in:

```text
sessions/
```

Each saved session can contain:
- Session ID.
- Session creation or saving information.
- User messages.
- AI assistant responses.
- Message timestamps.
- Generated session summary.

The conversation memory module retains up to four recent exchanges and supports saving and loading previous sessions.

## 9. Testing and Error Handling

The project includes test files for the main application components:

```text
test_ai_assistant.py
test_job_tracker.py
test_memory.py
test_summary.py
```

Run the tests using:

```bash
python test_memory.py
python test_job_tracker.py
python test_summary.py
python -m unittest test_ai_assistant.py
```

The application incorporates error handling through:

- Validation of required job application information.
- Validation of permitted application statuses.
- Validation of conversation messages.
- Validation of AI-generated JSON responses.
- Retry mechanisms for invalid AI responses.
- Fallback responses when AI response validation fails.

## 10. Data Privacy and Security

CareerTrack AI stores job application records and conversation history locally in JSON files.

The application sends the user's question, available application information, and recent conversation context to Anthropic Claude when generating AI responses.

Users should avoid entering passwords, API keys, or other highly sensitive personal information into conversations.

The Anthropic API key is configured through environment variables using a `.env` file, which should be excluded from version control.

Users should also protect access to their local project directory because saved application records and conversations may contain personal information.

## 11. Current Limitations

The current implementation operates as a Python command-line application.

Some features are not yet implemented, including:

- A web-based user interface.
- User registration and authentication.
- Automatic interview reminders.
- Scheduled follow-up notifications.
- Structured interview-date management.
- Online synchronisation of application records.

These features are potential areas for future development.

## 12. Future Improvements

Future development will focus on expanding CareerTrack AI into a more comprehensive career management platform through:

- **AI-powered CV Builder:** Generate professional CVs tailored to specific job opportunities.
- **Cover Letter Generator:** Create personalised cover letters.
- **Web-Based Application:** Develop an accessible web interface.
- **M-Pesa Payment Integration:** Introduce premium features and monetisation.
- **Job Search Integration:** Connect users with relevant job opportunities.
- **Application Analytics:** Provide more detailed application performance insights.
- **Notifications and Reminders:** Introduce interview reminders and application follow-up notifications.
- **User Authentication:** Enable secure individual user accounts.

## 13. Project Contributors

Developed collaboratively for **WECAN Season 12**.

1. Mercy Chepkurui
2. David  Muhuha Maina
3. Florence Muthoni Wanjiru

## 14.Team Responsibilities

Member 1: Core application and Claude AI integration .

Member 2: Job tracking and conversation memory.

Member 3: Session management, testing, and documentation.

Expected Outcome

To provide an efficient, intelligent, and centralized platform for managing job applications and improving the job search experience.

## 15. Project Information

| Item | Details |
|---|---|
| Project | CareerTrack AI |
| Programme | WECAN Season 12 |
| Programming Language | Python |
| AI Provider | Anthropic Claude |
| AI Model | Claude Sonnet 4.6 |
| Data Storage | JSON |
| Repository | GitHub |

---

**CareerTrack AI – Making Job Application Management Smarter.**

*Track Applications. Remember Opportunities. Build Careers.*
 
