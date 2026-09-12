# AI Job Application Assistant

An AI-powered backend API that helps users analyze job vacancies, track job applications, generate cover letters, and create PDF job analysis reports.

## Features

- User registration and login
- JWT authentication
- Job creation
- AI-powered job description analysis
- Job analysis stored in PostgreSQL
- PDF job analysis report generation
- Job application tracking
- AI-generated cover letters
- Cover letter caching to avoid unnecessary repeated AI requests

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Gemini AI
- ReportLab
- Pydantic
- Uvicorn

## Project Structure

```text
app/
├── auth/
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── security.py
│
├── routes/
│   ├── jobs.py
│   └── applications.py
│
├── services/
│   ├── ai.py
│   └── pdf.py
│
├── database.py
├── models.py
├── schemas.py
└── main.py
```

## Main API Endpoints

### Authentication

```text
POST /auth/register
POST /auth/login
```

### Jobs

```text
POST /jobs
POST /jobs/{job_id}/analyze
GET /jobs/{job_id}/report
```

### Applications

```text
POST /applications
GET /applications
POST /applications/{application_id}/cover-letter
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit the `.env` file to GitHub.

## Installation

Clone the repository:

```bash
git clone https://github.com/arkankalevi/ai-job-application-assistant.git
cd ai-job-application-assistant
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the API

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## Basic Usage Flow

```text
Register
   ↓
Login
   ↓
Get JWT token
   ↓
Create Job
   ↓
Analyze Job with Gemini
   ↓
Generate PDF Report
   ↓
Create Job Application
   ↓
Generate Cover Letter
```

## AI Features

The application uses Gemini AI to analyze job descriptions and generate personalized cover letters.

### Job Analysis

The AI analyzes a job vacancy and provides:

1. Required Skills
2. Key Responsibilities
3. Difficulty Level
4. Recommended Preparation

The analysis is stored in the database and can be reused without making an unnecessary repeated AI request.

### Cover Letter Generation

The application can generate a professional cover letter based on:

- Job title
- Company
- Job description

The generated cover letter is stored in the database and can be reused through the application.

The AI is instructed not to invent the user's experience, education, or achievements.

## Authentication

The API uses JWT-based authentication to protect user-specific endpoints.

Users must register and log in before accessing protected features.

After successful login, the API returns an access token that can be used in Swagger through the **Authorize** button.

## Database

The application uses PostgreSQL with SQLAlchemy as the ORM.

The main database tables are:

```text
users
jobs
job_applications
job_analyses
cover_letters
```

## PDF Report

The application can generate a PDF report containing the AI analysis of a job vacancy.

The report includes:

- Job title
- Company
- AI analysis

The generated report can be downloaded from the API response.

## Reviewer Notes

This project demonstrates a complete backend workflow for an AI-powered job application assistant, including authentication, database operations, AI integration, application tracking, cover letter generation, and PDF report generation.

The API can be tested using the FastAPI Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

## Repository

GitHub:

https://github.com/arkankalevi/ai-job-application-assistant