# 🤖 AI Customer Support Agent (Enterprise)

An enterprise-grade AI Customer Support Agent built with **FastAPI**, **Ollama (Llama 3.2)**, **ChromaDB**, **SQLite**, **RAG (Retrieval-Augmented Generation)**, and **n8n** automation.

The system answers customer queries using a knowledge base, maintains conversation history, automatically escalates unresolved issues, prevents duplicate tickets, and integrates with Google Sheets and Gmail for enterprise support workflows.

---

## 🚀 Features

* ✅ FastAPI REST API
* ✅ Retrieval-Augmented Generation (RAG)
* ✅ Ollama (Llama 3.2) Local LLM
* ✅ ChromaDB Vector Database
* ✅ PDF Knowledge Base
* ✅ SQLite Conversation History
* ✅ Session-Based Memory
* ✅ Source References
* ✅ Intent Classification
* ✅ Automatic Ticket Escalation
* ✅ Duplicate Ticket Prevention
* ✅ Existing Ticket Reuse
* ✅ n8n Workflow Integration
* ✅ Google Sheets Ticket Logging
* ✅ Gmail Email Notifications
* ✅ Enterprise Service-Layer Architecture

---

# 🏗️ Architecture

![Architecture](docs/architecture.png)

---

# 🔄 Request Flow

```text
User
   │
   ▼
FastAPI (/chat)
   │
   ▼
RAG Service
   │
   ├── Conversation History (SQLite)
   ├── ChromaDB Similarity Search
   ├── Ollama (Llama 3.2)
   └── Intent Classification
          │
          ▼
Knowledge Found?
      │            │
     Yes          No
      │            │
      ▼            ▼
Generate      Ticket Service
Response           │
                   ▼
             Existing Ticket?
                │        │
               Yes      No
                │        │
                ▼        ▼
          Reuse Ticket  Create Ticket
                │
                ▼
             n8n Webhook
                │
        ┌───────┴────────┐
        ▼                ▼
 Google Sheets        Gmail
```

---

# 📂 Project Structure

```text
backend/
│
├── app.py
├── ingest.py
│
├── models/
│   └── schemas.py
│
├── services/
│   ├── database_service.py
│   ├── intent_service.py
│   ├── llm_service.py
│   ├── n8n_service.py
│   ├── rag_service.py
│   ├── ticket_service.py
│   └── vector_service.py
│
├── knowledge/
│   └── FAQs.pdf
│
├── database/
│
├── chroma_db/
│
└── requirements.txt
```

---

# ⚙️ Tech Stack

| Category        | Technology         |
| --------------- | ------------------ |
| Backend         | FastAPI            |
| Language        | Python             |
| LLM             | Ollama (Llama 3.2) |
| Embeddings      | nomic-embed-text   |
| Vector Database | ChromaDB           |
| Database        | SQLite             |
| AI Technique    | RAG                |
| Automation      | n8n                |
| Storage         | Google Sheets      |
| Notifications   | Gmail              |

---

# 📌 API Endpoint

### Chat

```http
POST /chat
```

Example Request

```json
{
  "session_id": "abc123",
  "question": "My student portal is showing an internal server error."
}
```

Example Response

```json
{
  "question": "My student portal is showing an internal server error.",
  "answer": "I couldn't find that information in the knowledge base.\n\nA support ticket has been created for you.\nTicket ID: #26",
  "sources": [],
  "ticket_created": true,
  "ticket_id": 26
}
```

---

# 🔄 n8n Automation

The application integrates with **n8n** to automate support operations.

Current workflow:

* Receive ticket via Webhook
* Log ticket in Google Sheets
* Send email notification through Gmail

---

# 📸 Screenshots

## Architecture

`docs/architecture.png`

## FastAPI Swagger

`docs/swagger.png`

## n8n Workflow

`docs/n8n-workflow.png`

## Google Sheets

`docs/google-sheets.png`

## Gmail Notification

`docs/gmail.png`

---

# 🔥 Enterprise Features

* Layered Architecture
* Service Layer Pattern
* Session Memory
* Knowledge Base Search
* Intent Classification
* Automatic Ticket Escalation
* Duplicate Ticket Prevention
* Existing Ticket Reuse
* Source Attribution
* Enterprise Automation with n8n

---

# 🚀 Future Enhancements

* JWT Authentication
* Admin Dashboard
* Ticket Status Management
* Customer Satisfaction Survey
* Slack / Microsoft Teams Integration
* Docker Deployment
* CI/CD Pipeline
* Unit & Integration Testing

---

# 👨‍💻 Author

**Muhammad Ovais**

Senior Software Engineer | AI Automation Engineer

* LinkedIn: https://www.linkedin.com/in/muhammadovais314/
* GitHub: https://github.com/muhammadovais314
