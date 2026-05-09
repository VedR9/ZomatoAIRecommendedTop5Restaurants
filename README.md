# NextLeapPractice

Phase 0 implementation# Zomato AI Guide

A restaurant recommendation system powered by Gemini AI that helps users discover their next favorite meal based on location, budget, cuisine preferences, and ratings.

## Features

- **AI-Powered Recommendations**: Uses Gemini LLM to provide intelligent restaurant suggestions
- **Location-Based Filtering**: Find restaurants in specific areas (Bangalore)
- **Budget Preferences**: Filter by low, medium, or high budget ranges
- **Cuisine Selection**: Search for specific cuisines or get recommendations across all types
- **Rating Filters**: Ensure quality with minimum rating requirements
- **Real-Time Processing**: Fast response times with cached results
- **Modern UI**: Clean, responsive interface with glass morphism design

## Architecture

This project follows a phased development approach:

- **Phase 0**: Environment setup and basic structure
- **Phase 1**: Restaurant data ingestion from Hugging Face
- **Phase 2**: Data validation and filtering
- **Phase 3**: Retrieval and filtering logic
- **Phase 4**: LLM integration with Gemini for recommendations
- **Phase 5**: User interface and experience improvements
- **Phase 6**: FastAPI backend deployment
- **Phase 7**: Next.js frontend (primary UI) 
- **Phase 8**: Streamlit deployment (optional)
- **Phase 9**: Production hardening
- **Phase 10**: Streamlit Community Cloud deployment

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/VedR9/ZOmatoAIRecommendedTop5Restaurants.git
cd ZOmatoAIRecommendedTop5Restaurants
```

2. Set up Python environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Start the backend:
```bash
uvicorn src.milestone0.app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup (Phase 7)

1. Navigate to frontend directory:
```bash
cd next-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Run the Web App (Phase 7 Demo)

### One-Command Demo

```bash
# Terminal 1: Start backend
cd backend && source .venv/bin/activate && uvicorn src.milestone0.app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Start frontend
cd next-frontend && npm run dev
```

### Step-by-Step Demo

1. **Start Backend**: Run the FastAPI server on port 8000
2. **Start Frontend**: Run the Next.js development server on port 3000
3. **Enter Preferences**: 
   - Select location from dropdown (Indiranagar, Koramangala, etc.)
   - Choose budget band (Low/Medium/High)
   - Add cuisines (optional, comma-separated)
   - Set minimum rating (0-5)
4. **Get Recommendations**: Click "Find Restaurants" to receive AI-powered suggestions
5. **View Results**: See ranked restaurants with detailed AI reasoning
6. **Copy Results**: Use "Copy as Markdown" for demo purposes

## Phase 7 Frontend Features

### Primary User Interface
- **Modern Design**: Glass morphism effects with gradient backgrounds
- **Responsive Layout**: Mobile-friendly with tablet/desktop optimizations
- **Location Dropdown**: Pre-populated with Bangalore locations
- **Form Validation**: Inline error messages and disabled submit while loading
- **Loading States**: Smooth animations and visual feedback
- **Error Handling**: Graceful fallbacks for API issues

### Enhanced User Experience
- **Smart Filtering**: Real-time validation and preference management
- **AI Reasoning**: Detailed explanations for each recommendation
- **Copy to Clipboard**: Export results as Markdown for demos
- **Empty States**: Clear messaging for different scenarios
- **Accessibility**: WCAG AA compliance with keyboard navigation

## API Documentation

### Endpoints

- `GET /health` - Health check endpoint
- `POST /api/recommend` - Get restaurant recommendations
- `GET /api/phase0/info` - System information

### Recommendation Request

```json
{
  "location": "Indiranagar",
  "budget_band": "medium",
  "cuisines": ["Italian", "Cafe"],
  "minimum_rating": 4.2
}
```

### Recommendation Response

```json
{
  "recommendations": [
    {
      "rank": 1,
      "restaurant_name": "The Pizza Bakery",
      "reasoning": "This restaurant offers Italian cuisine with a high rating of 4.5 and fits your medium budget."
    }
  ]
}
```

## Deployment

### Phase 7 Production Deployment

#### Render + Vercel (Recommended)

1. **Backend (Render)**:
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn src.milestone0.app.main:app --host 0.0.0.0 --port $PORT`
   - Add `GEMINI_API_KEY` environment variable

2. **Frontend (Vercel)**:
   - Connect GitHub repository
   - Set build command: `npm run build`
   - Set output directory: `.next`
   - Configure environment variable for backend URL

#### Streamlit Community Cloud (Alternative)

1. Push code to GitHub repository
2. Connect repository to Streamlit Community Cloud
3. Set main file path: `streamlit_app.py`
4. Add `GEMINI_API_KEY` in Streamlit secrets dashboard
5. Deploy

## UI Generation

For generating enhanced UI designs, use the comprehensive prompt in `docs/ui-generation-prompt.md` with Google Stitch or similar AI design tools.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Restaurant data from [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- Gemini AI API from [Google AI Studio](https://aistudio.google.com/)
- Built with FastAPI, Next.js, and Streamlit

## Phase 0 Exit Criteria Mapping
- Working scaffold: yes
- README with run instructions: yes
- Lint/test baseline: yes
- Environment variables defined and not committed: yes (`.env.example` + `.gitignore`)
