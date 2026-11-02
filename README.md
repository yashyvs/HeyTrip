
# HeyTrip ✈️

### Your AI-Powered Travel Planning Assistant

HeyTrip is an AI-powered conversational travel planning application that helps users plan trips through natural language interactions.

Instead of filling out lengthy travel forms, users can simply chat with HeyTrip. The assistant asks relevant questions one at a time, understands travel preferences, remembers previous responses, and generates a personalized travel itinerary after confirmation.

The goal is to make travel planning more interactive, intelligent, and convenient.

---

## ✨ Features

- **Conversational Trip Planning:** Interact with an AI assistant using natural language.
- **Multi-Turn Conversations:** The assistant remembers previously provided information throughout a conversation.
- **Step-by-Step Questioning:** Collects destination, origin, travel duration, number of travellers, budget, activities, and other preferences.
- **Flight Search:** Retrieves flight information using the Aviationstack API.
- **Hotel Discovery:** Uses Tavily search to discover relevant accommodation options.
- **AI-Generated Itinerary:** Generates a personalized itinerary based on collected travel details.
- **Trip Confirmation:** Summarizes travel preferences and asks for confirmation before generating the final plan.
- **Persistent Conversation State:** Uses PostgreSQL with LangGraph checkpointing to maintain conversation state.
- **Markdown-Based Responses:** Displays structured AI responses with headings, lists, links, and tables.

---

## 🛠️ Tech Stack

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- React Markdown
- Remark GFM

### Backend
- Python
- FastAPI
- LangChain
- LangGraph
- Groq LLM

### Database
- PostgreSQL
- LangGraph PostgreSQL Checkpointer

### External APIs
- Aviationstack API – Flight information
- Tavily API – Web search for accommodation and travel-related information

---

## 🏗️ Project Architecture

```text
HeyTrip/
│
├── backend/
│   ├── main.py
│   ├── api.py
│   ├── tools/
│   │   ├── flight_tool.py
│   │   └── tavily_tool.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── ChatPanel.tsx
│   │   │   ├── MessageList.tsx
│   │   │   └── ...
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   └── types.ts
│   │
│   ├── package.json
│   └── ...
│
└── README.md
```

---

## 🔄 How It Works

HeyTrip follows a conversational workflow powered by LangGraph.

### 1. Conversation Initialization
The user starts a conversation by describing the trip they want to plan.

Example:

> I want to plan a 5-day trip to Goa.

### 2. Information Collection
The AI identifies missing travel details and asks follow-up questions.

It collects information such as:

- Destination
- Starting location
- Travel duration
- Number of travellers
- Budget per person
- Preferred activities
- Travel dates
- Accommodation preferences

Users can provide multiple details in a single response.

### 3. Trip Confirmation
Once the required information is collected, the assistant summarizes the preferences and asks the user to confirm the trip details.

### 4. Information Retrieval
After confirmation, the workflow executes the relevant agents:

- Flight Agent: Retrieves flight information.
- Hotel Discovery: Searches for suitable accommodation.
- Itinerary Agent: Generates the personalized travel plan.

### 5. Final Itinerary
The assistant combines the retrieved information and generates a structured travel plan.

---

## 🧠 LangGraph Workflow

The application uses LangGraph to manage the conversational workflow and coordinate different tasks.

```text
          User Message
                |
                v
       Conversation Manager
                |
                v
       Extract Trip Details
                |
                v
       Check Missing Details
                |
          +-----+-----+
          |           |
        Missing     Complete
          |           |
          v           v
     Ask Next      Ask for
     Question     Confirmation
                      |
                      v
                 User Confirms
                      |
                      v
                 Flight Agent
                      |
                      v
                 Hotel Search
                      |
                      v
                Itinerary Agent
                      |
                      v
                 Final Response
```

PostgreSQL checkpointing is used to maintain graph state across multiple requests associated with the same conversation thread.

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3.11+
- Node.js and npm
- PostgreSQL
- Git

You will also need API keys for:

- Groq
- Tavily
- Aviationstack

### 1. Clone the Repository

```bash
git clone https://github.com/yashyvs/HeyTrip.git

cd HeyTrip
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key

DATABASE_URL=postgresql://username:password@localhost:5432/heytrip
```

Replace the placeholder values with your actual credentials.

Make sure PostgreSQL is running and the `heytrip` database exists.

### 4. Start the Backend

From the backend directory, run:

```bash
uvicorn api:api --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Install Markdown rendering packages if they are not already included:

```bash
npm install react-markdown remark-gfm
```

Create a `.env.local` file inside the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

The application will be available at:

```text
http://localhost:3000
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| GROQ_API_KEY | API key for Groq LLM |
| TAVILY_API_KEY | API key for Tavily search |
| AVIATIONSTACK_API_KEY | API key for Aviationstack |
| DATABASE_URL | PostgreSQL connection string |
| NEXT_PUBLIC_API_URL | FastAPI backend URL |

**Important:** Never commit `.env` or `.env.local` files to GitHub. Add them to `.gitignore`.

---

## 🚀 Future Improvements

- Voice-based conversations with speech-to-text and text-to-speech.
- Real-time flight and hotel availability.
- Integration with booking platforms for ticket and hotel reservations.
- Interactive maps and route visualization.
- User authentication and trip history.
- More specialized travel agents for activities, transportation, and recommendations.
- Deployment and production-ready infrastructure.

---

## 🎯 Project Objective

HeyTrip aims to move beyond traditional form-based travel planning by providing an intelligent conversational experience.

By combining LLMs, LangGraph, external APIs, and persistent conversation state, the application aims to simplify how users discover, plan, and organize their trips.

---

⭐ If you find this project interesting, consider giving it a star!
