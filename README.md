<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql" />
  <img src="https://img.shields.io/badge/Ollama-AI-000000?logo=ollama" />
  <img src="https://img.shields.io/badge/Modern-UI-FF6B6B" />
</p>

# 📚 EduMetric – AI-Powered Assignment Grading System
### *(FastAPI • JWT Auth • RBAC • Ollama AI • PostgreSQL • PDF Extraction • Modern UI)*

A production-ready full-stack application that automates assignment grading using local AI (Ollama). Teachers upload assignments, students submit answers (text or PDF), and AI evaluates them instantly with detailed feedback.

This project demonstrates **real-world backend engineering** with role-based access control, PDF processing, and AI integration.

---

## 🔥 Features

- 🔐 **JWT Authentication**: Secure token-based auth with role management
- 👥 **Role-Based Access Control**: Separate workflows for Teachers & Students
- 🤖 **AI-Powered Grading**: Local Ollama LLM evaluates submissions with feedback
- 📄 **PDF Support**: Upload assignments and submit answers via PDF
- ✍️ **Text Submissions**: Direct text input for assignment answers
- 📊 **Submission Tracking**: Students view grades and feedback history
- 👨‍🏫 **Teacher Dashboard**: Create assignments, view submissions, grade manually
- 📈 **Assignment Analytics**: Track submission status and student performance
- 🎨 **Modern UI**: Glassmorphic design with smooth animations
- 🗄️ **PostgreSQL Storage**: Persistent data with SQLAlchemy ORM
- 📱 **Responsive Design**: Mobile-friendly interface

---

## 🎓 How It Works

### **For Teachers:**
1. **Create Assignment** – Manually input or upload PDF
2. **View Submissions** – See all student submissions in table format
3. **AI Grading** – Click to auto-grade with Ollama AI
4. **Review Results** – Check marks, feedback, and student answers

### **For Students:**
1. **Browse Assignments** – View assignment details and requirements
2. **Submit Answers** – Type directly or upload PDF
3. **Track Status** – See submission status (Pending/Evaluated)
4. **View Grades** – Check marks obtained and AI feedback

---

## 🧰 Tech Stack

### **Backend**
- **FastAPI** – High-performance async API framework
- **SQLAlchemy(Async)** – Database operations
- **PostgreSQL** – Relational database
- **JWT** – Secure authentication tokens
- **Ollama (Phi model)** – Local AI for grading
- **pdfplumber** – PDF text extraction
- **Pydantic** – Data validation

### **Frontend**
- **HTML5/CSS3** – Modern semantic markup
- **Vanilla JavaScript** – No frameworks, pure JS
- **Fetch API** – REST API communication
- **CSS Animations** – Smooth transitions and effects
- **Responsive Design** – Mobile-first approach

### **Security**
- Password hashing with bcrypt
- JWT token validation
- Role-based route protection
- SQL injection prevention

---

## 🔐 Authentication Flow

1. User registers as Teacher or Student
2. Login returns JWT access token
3. Token stored in browser `localStorage`
4. All API requests include `Authorization: Bearer <token>`
5. Backend validates token and role permissions

```
Register → Login → JWT → Protected Routes → Response
```

---

## 🤖 AI Grading Flow

1. Student submits assignment answers
2. Teacher clicks "Grade" button
3. Backend sends each section to Ollama AI:
   - Compares student answer vs reference
   - Assigns score (0 to max marks)
   - Generates feedback (1-2 lines)
4. AI returns Marks and Feedback
5. Results saved to database
6. Student sees grade and feedback
   
---

## 🚀 Getting Started

### 1️⃣ Prerequisites

- **Python 3.13+**
- **PostgreSQL** (local or cloud)
- **Ollama** with Phi model installed

Install Ollama and pull the model:
```bash
# Install Ollama from https://ollama.ai
ollama pull phi
ollama serve
```

### 2️⃣ Clone Repository

```bash
git clone https://github.com/your-username/EduMetric.git
cd EduMetric/Project
```

### 3️⃣ Install Dependencies

```bash
python -m venv myvenv
myvenv\Scripts\activate  # Windows
source myvenv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Create `.env` file in project root (not included in repo):

```env
# App Config
APP_NAME=EduMetric
DEBUG=True

# JWT Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/edumetric

# Ollama (ensure running on localhost:11434)
```

### 5️⃣ Initialize Database

Create the database in PostgreSQL first:
```bash
psql -U postgres
CREATE DATABASE edumetric;
\q
```

Then initialize tables:
```bash
python -c "from app.db.init_db import init_db; import asyncio; asyncio.run(init_db())"
```

### 6️⃣ Run the Application

```bash
uvicorn app.main:app --reload --port 8000
```

### 7️⃣ Access the App

- 🌐 **Frontend**: http://localhost:8000/home.html
- 📚 **API Docs**: http://localhost:8000/docs
- 🔑 **Login**: http://localhost:8000/login.html

---

## 📁 Project Structure

```
EduMetric/
├── app/
│   ├── api/                   # API routes
│   │   ├── routers_auth.py           # Login/Register
│   │   ├── routers_assignment.py     # CRUD assignments
│   │   ├── routers_assignment_pdf.py # PDF uploads
│   │   ├── routers_grading.py        # AI grading
│   │   └── routers_submission.py     # Student submissions
│   ├── core/                  # Core functionality
│   │   ├── config.py                 # Settings
│   │   ├── dependencies.py           # Auth dependencies
│   │   ├── rbac.py                   # Role checks
│   │   ├── security.py               # JWT & password
│   │   ├── constants.py               # JWT & password
│   │   └── exceptions.py             # Exception Handling
│   ├── db/                    # Database
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py
│   │   ├── assignment.py
│   │   └── submission.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py
│   │   ├── assignment.py
│   │   └── submission.py
│   ├── services/              # Business logic
│   │   ├── grading_service.py        # Ollama AI integration
│   │   ├── pdf_extractor.py          # PDF text extraction
│   │   └── text_parser.py            # Parse sections
│   ├── utils/                 # Utility functions
│   └── main.py                # FastAPI app
├── frontend/
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript files
│   └── *.html                 # HTML pages
└── requirements.txt
```

---

## 🎨 Frontend Pages

### **Public Pages**
- `home.html` – Landing page
- `login.html` – User login
- `register.html` – User registration

### **Student Pages**
- `dashboard.html` – Student dashboard
- `assignments.html` – Browse assignments
- `assignment-detail.html` – View assignment reference
- `submit.html` – Submit text answers
- `submit-pdf.html` – Submit PDF answers
- `my-submissions.html` – View submission history
- `submission-detail.html` – View grades & feedback

### **Teacher Pages**
- `dashboard.html` – Teacher dashboard
- `create-assignment.html` – Manual assignment creation
- `upload-pdf.html` – Upload PDF assignment
- `view-submissions.html` – View all submissions
- `grading.html` – AI grading interface

---

## 🎯 API Endpoints

### **Authentication**
- `POST /auth/register/{role}` – Register user
- `POST /auth/login` – Login & get JWT
- `GET /auth/me` – Get current user

### **Assignments**
- `GET /assignments` – List all assignments
- `POST /assignments` – Create assignment (Teacher)
- `POST /assignments/upload-pdf` – Upload PDF (Teacher)
- `POST /assignments/extract-pdf-preview` – Preview PDF extraction

### **Submissions**
- `POST /assignments/{id}/submit` – Submit text answers
- `POST /assignments/{id}/submit-pdf` – Submit PDF
- `GET /submissions/my-submissions` – Student's submissions
- `GET /submissions/{id}` – Get submission details
- `GET /submissions/assignment/{id}` – All submissions for assignment

### **Grading**
- `POST /grading/assignments/{aid}/submissions/{sid}` – AI grade submission

---

## 🧩 Key Learnings

- ✅ **Role-Based Access Control** (RBAC) implementation
- ✅ **JWT authentication** with FastAPI
- ✅ **Ollama AI integration** for local LLM inference
- ✅ **PDF text extraction** with pdfplumber
- ✅ **Text parsing** for structured content
- ✅ **Database design** with relationships
- ✅ **Modern frontend** with vanilla JavaScript
- ✅ **API design** following REST principles
- ✅ **Error handling** and validation
- ✅ **Clean architecture** with separation of concerns

---

## 🔮 Future Improvements

- 📊 **Analytics Dashboard** with charts (marks distribution, submission trends)
- 🔄 **Real-time notifications** (WebSockets for grade updates)
- 📄 **Pagination** for large submission lists
- 🧪 **Unit & Integration Tests** with pytest
- 🐳 **Docker Compose** for easy deployment
- ☁️ **Cloud Deployment** (Render/Railway/AWS)
- 📝 **Rich text editor** for submissions
- 🎨 **Dark mode** toggle
- 🔍 **Search & filter** for assignments
- 📧 **Email notifications** for grades
- 📱 **Mobile app** (React Native/Flutter)
- 🤖 **Multiple AI models** (GPT, Claude, Gemini support)
- 📈 **Performance monitoring** with Prometheus
- 🔒 **Rate limiting** for API endpoints

---

## 🛠️ Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
ollama serve
```

### Database Connection Error
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Create database manually if needed
psql -U postgres
CREATE DATABASE edumetric;
```

### PDF Extraction Fails
- Ensure PDF is text-based (not scanned image)
- Check file size (large PDFs may timeout)
- Verify pdfplumber is installed correctly

---

## ⚠️ Disclaimer

This project is **for educational purposes** to demonstrate full-stack development with AI integration. Not recommended for production without proper security hardening, testing, and scalability improvements.

---

## 👨‍💻 Author

Made with ❤️ by **Shounak**

---

## ⭐ If you found this project useful, please ⭐ the repository!

---
