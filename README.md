# Travel Itinerary Backend

REST API built with FastAPI that generates personalized travel itineraries using AI. The system has a three-tier model priority: local fine-tuned model (GPU) → HuggingFace Inference API → Groq fallback.

## Architecture

```
POST /generate
      │
      ▼
 GPU available? ──yes──► Fine-tuned Llama 3.2 1B (local)
      │
      no
      │
      ▼
 HF_TOKEN set? ──yes──► HuggingFace Inference API (Llama 3.2 1B)
      │
      no
      │
      ▼
    Groq API (llama-3.3-70b-versatile)
```

## Endpoints

### `GET /`
Health check.

**Response:**
```json
{ "message": "Travel Planner API funcionando ✅" }
```

### `POST /generate`
Generates a personalized travel itinerary.

**Request body:**
```json
{
  "destination": "París, Francia",
  "start_date": "2025-07-01",
  "end_date": "2025-07-05",
  "budget": "moderado",
  "traveler_type": "pareja",
  "pace": "equilibrado",
  "interests": ["cultura", "gastronomía"],
  "budget_amount": 2000
}
```

| Field | Type | Options |
|-------|------|---------|
| `budget` | string | `economico`, `moderado`, `lujo` |
| `traveler_type` | string | `solo`, `pareja`, `familia`, `amigos` |
| `pace` | string | `relajado`, `equilibrado`, `intensivo` |
| `interests` | string[] | cultura, historia, gastronomía, arte, aventura, naturaleza, playa, fotografía, vida nocturna, senderismo, arqueología, bienestar |
| `budget_amount` | int | optional, amount in USD |

**Response:**
```json
{
  "destination": "París, Francia",
  "total_days": 4,
  "budget_level": "moderado",
  "traveler_type": "pareja",
  "days": [
    {
      "day": 1,
      "title": "Llegada y primer paseo",
      "activities": [
        {
          "time": "09:00",
          "name": "Torre Eiffel",
          "description": "Visita al icónico monumento parisino",
          "type": "cultural",
          "tip": "Compra las entradas online para evitar filas"
        }
      ],
      "restaurants": ["Café de Flore", "Le Procope"],
      "local_tips": ["Usa el metro, es más rápido que el taxi"]
    }
  ]
}
```

## Local Setup

### Requirements
- Python 3.10+
- Groq API key → [console.groq.com](https://console.groq.com)
- (Optional) HuggingFace token for the inference API
- (Optional) CUDA GPU for the local model

### Installation

```bash
git clone https://github.com/danielfevargas/travel-itinerary-backend.git
cd travel-itinerary-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-prod.txt
```

### Environment variables

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token  # optional
```

### Run

```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

## Deployment (Render)

1. Connect this repository in Render
2. Set **Build Command**: `pip install -r requirements-prod.txt`
3. Set **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables: `GROQ_API_KEY`, `HF_TOKEN` (optional)

> Render has no GPU, so it always uses the Groq fallback.

## Fine-tuned Model

The local model is a Llama 3.2 1B fine-tuned on travel itinerary data, available on HuggingFace:
[Danielfevargas16/travel-planner-llama](https://huggingface.co/Danielfevargas16/travel-planner-llama)

To use it locally, place the model files in `./travel-model-final/` and install `requirements.txt` (includes PyTorch with CUDA).

## Project Structure

```
travel-itinerary-backend/
├── app/
│   ├── main.py          # FastAPI app and routes
│   ├── generator.py     # Model priority logic and itinerary generation
│   ├── local_model.py   # Fine-tuned Llama 3.2 1B inference
│   ├── hf_model.py      # HuggingFace Inference API
│   ├── rag.py           # Business rules context (budget, pace, traveler type)
│   └── data/
│       └── destinations.json  # Planning rules by budget/pace/traveler type
├── requirements.txt      # Full deps with PyTorch (GPU)
├── requirements-prod.txt # Lightweight deps for deployment
└── .env                  # API keys (not committed)
```
