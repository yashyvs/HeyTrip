# ✈️ HeyTrip

HeyTrip is an AI-powered travel planning assistant that helps users plan trips through a conversational interface. Instead of filling out forms, users can interact with the AI, share their travel preferences, and receive personalized trip recommendations and itineraries.

This project is currently under development and focuses on building a multi-agent travel planning workflow using LangGraph.

---

## Features

- 💬 Conversational AI trip planning
- 🗺️ Destination preference extraction
- 🧠 Context-aware conversations
- ⚡ Real-time communication using Socket.IO
- 📋 AI-generated travel itineraries
- 🎯 Interactive suggestion chips for guided conversations
- 🔍 Search integration (DuckDuckGo - WIP)

---

## Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- FastAPI
- LangGraph
- LangChain
- Hugging Face Inference Endpoint

---

## Project Structure

```
HeyTrip/

├── frontend/
│   ├── app/
│   ├── components/
│   ├── services/
│   ├── types/
│   └── public/
│
├── backend/
│   ├── agents/
│   ├── graph/
│   ├── memory/
│   ├── models/
│   ├── tools/
│   ├── main.py
│   └── requirements.txt
│
└── README.md
```

---

## Workflow

```
User

↓

Frontend (Next.js)

↓

Socket.IO

↓

FastAPI

↓

LangGraph

↓

Extractor Agent

↓

Conversation / Planner Routing

↓

Recommendation & Search Tools

↓

Itinerary Generation

↓

Response to Frontend
```

---

## Current Agents

- Extractor Agent
- Conversation Agent
- Router Agent
- Recommendation Agent *(Work in Progress)*
- Itinerary Agent *(Work in Progress)*

---

## Current Tools

- DuckDuckGo Search Tool *(Work in Progress)*

Future integrations:

- Google Places API
- Weather API
- Hotel & Flight APIs
- Maps Integration

---

## Installation

### Clone Repository

```bash
git clone https://github.com/<yashyvs>/HeyTrip.git
cd HeyTrip
```

---

### Backend

```bash
cd backend

python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

Run backend

```bash
uvicorn main:socket_app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Future Improvements

- Multi-agent planning workflow
- Real-time travel search
- Flight and hotel recommendations
- Budget optimization
- Voice conversations
- Collaborative trip planning
- Interactive itinerary timeline
- Maps integration

---

## Status

This project is currently under development as part of an AI-based travel planning system using LangGraph and FastAPI.