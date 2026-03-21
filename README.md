# 📋 Trainify AI — SOP to AI Training System

> Upload any Standard Operating Procedure document and instantly generate
> role-specific training content using AI.


## 🎯 What It Does

Takes any SOP document (PDF or TXT) as input and generates:

| Output | Description |
|---|---|
| 📌 Summary | 5–6 bullet points covering purpose, scope, roles and key steps |
| 📚 Training Guide | Step-by-step onboarding content with "Why it matters" context |
| ❓ Quiz | MCQ, True/False and Short Answer questions with answers |

---

## ⚙️ Key Features

- **Role-Based Output** — Content tailored for Intern, Employee, or Manager
- **Detail Level Control** — Choose Short, Medium, or Detailed output
- **Mistakes to Avoid** — Detailed mode adds common mistakes after each step
- **Clean Quiz UI** — Options in vertical layout, answers in green, explanations in blue
- **Download Everything** — Each section downloadable individually or as a full report
- **Free to Run** — Uses Groq API, no credit card or payment needed

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Groq API (LLaMA 3.3-70b) | AI content generation |
| PyPDF2 | PDF text extraction |
| python-dotenv | Secure API key management |

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/29nancy/SOP-AI-Trainer.git
cd sop-ai-trainer
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your free API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up free → API Keys → Create API Key
- Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure
```
sop-ai-trainer/
├── app.py              # Streamlit UI — all frontend logic
├── processor.py        # Groq API calls and prompt design
├── extractor.py        # PDF and TXT text extraction
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed to git)
├── sample_sop.txt      # Sample SOP for testing
└── README.md           # This file
```

---

## 💡 Sample Output

**Input:** Customer Complaint Handling SOP (txt)
**Role:** Intern | **Detail Level:** Medium

**Summary (excerpt):**
- The purpose of this SOP is to establish a standardized process for
  receiving and resolving customer complaints.
- All customer service representatives, team leads, and managers are
  covered under this procedure.

**Training Step (excerpt):**
Step 1: Receive and acknowledge the complaint professionally.
Why this matters: First impressions set the tone for the entire
resolution experience.

**Quiz Question (excerpt):**
Q1. What is the timeframe for logging a complaint in the CRM?
Answer: Within 5 minutes of receiving it.

---

## 🎨 UI Highlights

- Dark themed/Light themed, wide layout
- Role and detail level shown in metrics bar
- Each training step clearly separated
- Quiz answers always visible in color-coded boxes
- Full report download combines all 3 sections

---

## ⚠️ Limitations

- Scanned or image-based PDFs are not supported (text-based only)
- Very large documents are trimmed to first 5,000 characters for API limits
- Groq free tier has rate limits — wait a few seconds between generations

---

## 🔮 Future Improvements

- Support for multiple document uploads
- Export to PDF or DOCX format
- Add voice narration for training steps


**Code**
```
☑ app.py         — UI works end to end
☑ processor.py   — Groq API with role + detail prompts
☑ extractor.py   — PDF and TXT extraction
☑ requirements.txt
☑ sample_sop.txt — recruiter can test immediately
☑ README.md      — complete setup guide
```

