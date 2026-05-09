Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)
You are tasked with building an AI-powered restaurant recommendation service inspired by Zomato. The system should intelligently suggest restaurants based on user preferences by combining structured data with a Large Language Model (LLM).
Objective
Design and implement an application that:
Takes user preferences (such as location, budget, cuisine, and ratings)
Uses a real-world dataset of restaurants
Leverages an LLM to generate personalized, human-like recommendations
Displays clear and useful results to the user
System Workflow
Data Ingestion
Load and preprocess the Zomato dataset from Hugging Face (https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation )
Extract relevant fields such as restaurant name, location, cuisine, cost, rating, etc.
User Input
Collect user preferences:
Location (e.g., Delhi, Bangalore)
Budget (low, medium, high)
Cuisine (e.g., Italian, Chinese)
Minimum rating
Any additional preferences (e.g., family-friendly, quick service)
Integration Layer
Filter and prepare relevant restaurant data based on user input
Pass structured results into an LLM prompt
Design a prompt that helps the LLM reason and rank options
Recommendation Engine
Use the LLM to:
Rank restaurants
Provide explanations (why each recommendation fits)
Optionally summarize choices
Output Display
Present top recommendations in a user-friendly format:
Restaurant Name
Cuisine
Rating
Estimated Cost
AI-generated explanation

Diagram → 
Architecture

Phase-wise architecture: restaurant recommendation system
This document breaks the build into phases that map to the workflow in problemstatement.md: data ingestion → user input → integration (filter + prompt prep) → LLM recommendation → output display.
Phase 0 — Scope and foundations
Item
Outcome
Product slice
Basic web UI — source of user input and primary presentation of results for milestone 1 (see phase0-scope.md); CLI remains for dev/diagnostics.
Stack
Language/runtime, dependency manager, where secrets live (e.g. .env for API keys, never committed).
Dataset contract
Confirm Hugging Face dataset fields you will support in v1; document column → internal field mapping.
Non-goals
Explicitly defer (e.g. user accounts, live Zomato API, maps) to avoid scope creep.

Exit criteria: written assumptions (stack, v1 UI, supported preference fields) and a local way to run the app end-to-end once later phases exist.
Implemented artifacts: package src/milestone1/phase0/ (paths, scope, info/doctor commands), phase0-scope.md, dataset-contract.md, repo README.md, .env.example. CLI: milestone1 info / milestone1 doctor.

Phase 1 — Data ingestion and canonical model
Layer
Responsibility
Acquisition
Download or stream ManikaSaini/zomato-restaurant-recommendation; cache locally if useful for iteration.
Normalization
Clean types (ratings as numbers, cost as enum or numeric band), handle missing values, dedupe rows if needed.
Canonical schema
Internal Restaurant (or equivalent) with: name, location, cuisines, cost, rating, plus any extra columns you keep for prompts.

Exit criteria: a single module (or package) that loads data and returns a typed in-memory collection or queryable table; unit tests on parsing for a few sample rows.
Implemented: package src/milestone1/phase1_ingestion/ (Restaurant, load_restaurants / iter_restaurants, normalization, Hub revision pin, schema assertion). CLI: milestone1 ingest-smoke --limit N. Hub integration tests: RUN_HF_INTEGRATION=1 pytest -m integration.

Phase 2 — User preferences and validation
Component
Responsibility
Preference model
Structured fields: location, budget band, cuisine(s), minimum rating; optional free-text for “additional preferences.”
Validation
Reject or coerce invalid input (unknown location, rating out of range); clear error messages for the UI/CLI.

Exit criteria: preferences deserialize from form/API/CLI args into one object used by the filter layer; validation errors are user-visible.
Implemented: package src/milestone1/phase2_preferences/ (UserPreferences, preferences_from_mapping, optional allowed_city_names corpus check, allowed_cities_from_restaurants). CLI: milestone1 prefs-parse ... (prints JSON or field errors on stderr).

Phase 3 — Integration layer (retrieval + prompt assembly)
Component
Responsibility
Deterministic filter
Apply hard filters first: location, min rating, budget, cuisine overlap—reduce to top N candidates (cap for LLM context, e.g. 15–50).
Ranking hint (optional)
Pre-sort by rating or composite score so the LLM sees a sensible default order even before reasoning.
Prompt builder
System + user messages (or single structured prompt) including: user preferences as JSON or bullets; candidate table as markdown/JSON; instructions to only recommend from the list; output format (see Phase 4).

Exit criteria: given preferences + loaded dataset, produce a stable (candidates[], prompt_payload) without calling the LLM yet; tests for filter edge cases (no matches, too many matches).
Implemented: package src/milestone1/phase3_integration/ (filter_and_rank, build_prompt_payload, build_integration_output). CLI: milestone1 prompt-build.

Phase 4 — Recommendation engine (LLM)
Concern
Approach
Model I/O
Thin client: temperature, max tokens, timeout; inject API key from environment.
Grounding
Prompt requires the model to cite restaurant names from the candidate list only; refuse or return empty if nothing fits.
Structured output
Ask for JSON (e.g. rankings[] with restaurant_id, rank, explanation) or strict markdown sections—then parse and validate.
Resilience
Retry on transient errors; fallback: return deterministic top-k with template explanations if the LLM fails.

Exit criteria: end-to-end call returns ranked items with explanations; parser validates structure; failures degrade gracefully.
Implemented: package src/milestone1/phase4_llm/ (Gemini client, JSON rankings parse, deterministic fallback, recommend_with_gemini). CLI: milestone1 recommend. Secrets: GEMINI_API_KEY (see .env.example).

Phase 5 — Output and experience
Surface
Responsibility
Rendering
For each recommendation: name, cuisine, rating, estimated cost, AI explanation (per problem statement).
Empty states
“No restaurants match filters” vs “LLM could not justify picks”—different copy.
Observability (light)
Log latency, token usage if available, and filter counts (no PII in logs unless required).

Exit criteria: demo path from user input to readable results in one run; copy and layout match the minimum fields in the problem statement.
Implemented: package src/milestone1/phase5_output/ (markdown/plain rendering, empty-state copy, stderr telemetry JSON). CLI: milestone1 recommend-run (end-to-end readable output + telemetry).

Phase 6 — Backend (HTTP API)
Concern
Approach
Role
Thin HTTP service that owns server-side secrets (GEMINI_API_KEY), dataset access, and orchestration. The browser must not call Gemini or Hugging Face directly.
Contract
Stable JSON request/response for “recommend”: preferences body aligned with Phase 2 keys; response carries ranked items (ids + display fields + explanations), source (llm / fallback / no_candidates), filter/candidate counts, and optional non-sensitive telemetry fields for the UI.
Endpoints (v1 intent)
POST /api/v1/recommendations (or equivalent) — validate input, run load_restaurants (with limits/caching policy), recommend_with_gemini, return DTOs. GET /health — process up, keys configured (without exposing values). Optional: GET /api/v1/meta — e.g. sample allowed_cities cap for form hints.
Cross-cutting
Timeouts aligned with Phase 4; structured server logs (counts, latency, token totals—no raw user notes in info-level logs unless you explicitly choose to); CORS restricted to the dev frontend origin; request size limits on free-text fields (reuse Phase 2 max length).
Stack
Python-first is natural: e.g. FastAPI or Flask in src/ or a sibling package, sharing the installed milestone1 library. Alternative stacks (Node, etc.) are possible only if they duplicate contracts and call a Python sidecar—avoid unless required.

Exit criteria: frontend can complete one recommendation flow using only the API; API returns the same logical outcomes as milestone1 recommend / recommend-run for the same inputs (modulo caching).
Implemented: pending — document target layout here when added (e.g. src/milestone1/api/ or apps/api/).

Phase 7 — Frontend (web UI)
Concern
Approach
Role
Primary user-facing surface: preference form + results list, per phase0-scope.md.
Data flow
Browser only talks to the Phase 6 API. Map form fields to the API JSON schema (location, budget band, cuisines, minimum rating, optional additional text).
UI
Results show name, cuisines, rating, estimated cost, AI explanation for each row; reuse Phase 5 empty-state semantics (“no filter match” vs “model returned no grounded picks”) with clear, distinct copy.
UX
Loading states, validation errors inline, disabled submit while pending; optional “copy as Markdown” for demo.
Stack
Choose one and stay consistent: e.g. React + Vite (SPA) or HTMX + server templates (minimal JS). Host locally for milestone 1; no production SLA required in Phase 0.

Exit criteria: one demo path in the README: start API + UI, submit preferences, see ranked results or an intentional empty state.
Implemented: pending — e.g. apps/web/ or frontend/ + README section “Run the web app”.

Phase 8 — Deployment using Streamlit (optional)
Concern
Approach
Role
A single-process Python app (Streamlit) that exposes the same recommendation flow as the CLI/API: preferences in widgets → load corpus (Phase 1) → validate (Phase 2) → filter + prompt (Phase 3) → recommend_with_gemini (Phase 4) → render ranked cards with explanations (Phase 5 semantics). No Node build and no separate SPA host required for this path.
Secrets
GEMINI_API_KEY (and optional GEMINI_MODEL) via Streamlit secrets (st.secrets) on Streamlit Community Cloud or via environment variables when self-hosting—same rules as Phase 6: keys never ship to the browser client bundle; Streamlit runs logic server-side.
Deployment (free tier)
Streamlit Community Cloud: connect the GitHub repo, set the main file path (e.g. streamlit_app.py or src/milestone1/phase8_streamlit/app.py), add secrets in the dashboard, deploy. Cold starts and resource limits apply on the free tier; keep load_limit / candidate_cap conservative. Alternatives: Docker image (streamlit run …) on Render/Fly/other free allowances.
Relationship to Phase 6–7
Complementary: Phase 7 remains the primary product UI (browser + REST). Phase 8 is ideal for course demos, stakeholder previews, and fast sharing without operating Vite + CORS + two deployables. You may implement Streamlit without calling the HTTP API by importing milestone1 directly (duplication of orchestration is acceptable if thin); alternatively call POST /api/v1/recommendations if you want one orchestration path.
UX scope
Forms with st.selectbox / st.text_input / st.slider for location, cuisines, budget, minimum rating, and additional text; st.spinner while the model runs; st.expander for raw JSON or telemetry if useful. Match empty-state copy from Phase 5 where practical.

Exit criteria: README (or a short docs/streamlit-deploy.md) documents how to run locally (streamlit run …) and how to deploy to Community Cloud (repo layout, secrets names, branch); a reviewer can open the hosted URL and complete one successful recommendation or see an intentional empty state.
Implemented: package src/milestone1/phase8_streamlit/ (app.py), repo root streamlit_app.py (Cloud entrypoint), optional dependency [streamlit] in pyproject.toml, and streamlit-deploy.md.

Phase 8 — Deployment plan: Render (backend) + Vercel (frontend)
This document is the canonical guide for deploying Milestone 1 as two independent services:
Backend — FastAPI app from src/milestone1/phase6_api/ on Render.
Frontend — Vite + React SPA from frontend/ on Vercel.
The browser bundle is purely static and only talks to the Render URL over HTTPS. Provider keys (GEMINI_API_KEY, optional HF_TOKEN) live only on Render.

0. One-time prep in the repo
The repo already builds cleanly for both targets — Render reads pyproject.toml, Vercel reads frontend/package.json. Two small additions make the deploy reproducible without clicking around dashboards.
0.1 Pin a Python version for Render
Add a runtime.txt at the repo root so Render uses Python 3.11 (matches requires-python in pyproject.toml):
python-3.11.9

0.2 Optional: render.yaml (Infrastructure-as-Code)
Render can read a render.yaml blueprint at the repo root to provision the service automatically:
services:
  - type: web
    name: milestone1-api
    runtime: python
    plan: free
    buildCommand: pip install -e .
    startCommand: uvicorn milestone1.phase6_api.app:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    autoDeploy: true
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: GEMINI_MODEL
        sync: false
      - key: HF_TOKEN
        sync: false
      - key: CORS_ORIGINS
        sync: false

sync: false keeps secret values out of the repo; you set them in the Render dashboard.
0.3 Optional: frontend/vercel.json
Vercel auto-detects Vite, but a small config makes SPA fallback explicit and avoids surprises if you add client-side routing later:
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}


1. Deploy the backend on Render
1.1 Create the service
Push the repo to GitHub.
Render dashboard → New → Web Service → connect the GitHub repo.
If you committed render.yaml, choose Blueprint and Render fills in the rest. Otherwise use the manual settings below.
1.2 Manual settings (if not using render.yaml)
Field
Value
Environment
Python 3
Region
nearest free region
Branch
main
Root Directory
(blank — repo root)
Build Command
pip install -e .
Start Command
uvicorn milestone1.phase6_api.app:app --host 0.0.0.0 --port $PORT
Health Check Path
/health
Plan
Free (or paid for no cold starts)

milestone1.phase6_api.app:app exists at module scope in src/milestone1/phase6_api/app.py (app = create_app()), so uvicorn can import it without running the milestone1-api console script. The startup hook prewarms the city list in a background thread, so the first /api/v1/meta and /api/v1/recommendations calls do not pay the full Hugging Face load cost.
1.3 Environment variables on Render
Set in Environment → Environment Variables:
Var
Required?
Purpose
GEMINI_API_KEY
yes
Phase 4 LLM calls. Get from https://aistudio.google.com/app/apikey.
GEMINI_MODEL
optional
Override default Gemini model id (default: gemini-2.5-flash).
HF_TOKEN
optional
Higher Hugging Face Hub rate limits when streaming the dataset.
CORS_ORIGINS
yes (after Vercel deploy)
Comma-separated list of allowed browser origins. See §3.
PORT
auto
Render injects this; the app reads it via uvicorn ... --port $PORT.

Do not add API_HOST — the start command already binds 0.0.0.0.
1.4 Verify
After the first deploy, hit:
https://<service>.onrender.com/health → {"status":"ok","gemini_configured":true}
https://<service>.onrender.com/api/v1/meta?cities_cap=20 → JSON with a cities array
https://<service>.onrender.com/docs → Swagger UI
Note the service URL — it goes into the Vercel build env next.
Cold starts: Render free-tier services sleep after ~15 minutes of inactivity. The first request after sleep can take 30–60 s. The Phase 6 prewarm thread reduces post-startup latency but does not eliminate the dyno boot itself. If demos need snappy first hits, upgrade the plan or hit /health from an uptime pinger (Better Stack / cron-job.org).

2. Deploy the frontend on Vercel
2.1 Create the project
Vercel dashboard → Add New → Project → import the same GitHub repo.
Root Directory: frontend/ (critical — without this Vercel tries to build the Python project).
Framework Preset: Vite (auto-detected).
Build / Output should auto-fill from package.json:
Install: npm install
Build: npm run build
Output: dist
2.2 Environment variables on Vercel
Add under Settings → Environment Variables, scoped to Production (and Preview if you want previews to hit the same backend):
Var
Value
VITE_API_BASE_URL
https://<your-render-service>.onrender.com (no trailing slash)

Vite inlines VITE_* vars at build time, so a redeploy is needed to pick up changes (Vercel does this automatically on env-var save).
Never put GEMINI_API_KEY in any VITE_* var — frontend/src/lib/api.ts only ever calls ${VITE_API_BASE_URL}/..., and that boundary is what keeps provider keys server-side.
2.3 Verify
After deploy:
https://<project>.vercel.app/ loads the SPA.
DevTools → Network → submit the form → request goes to https://<render>.onrender.com/api/v1/recommendations and returns 200.
If the request is blocked by the browser with a CORS error, you have not yet completed §3.

3. Wire CORS on Render to the Vercel origin
src/milestone1/phase6_api/app.py reads CORS_ORIGINS (comma-separated). Set it on Render to the exact origins the browser will use:
CORS_ORIGINS=https://<project>.vercel.app,https://<project>-git-main-<team>.vercel.app

Common gotchas:
No trailing slash, no path. Origin only: https://foo.vercel.app, not https://foo.vercel.app/.
Custom domain? Add it too: CORS_ORIGINS=https://app.example.com,https://<project>.vercel.app.
Preview deploys get unique subdomains. Either disable preview-env builds, point them at a separate staging Render service, or temporarily widen CORS_ORIGINS while testing — never to * for a credentialed app.
After saving the env var, Render restarts the service. Re-test the SPA call from the browser.

4. Smoke-test checklist
Run these in order from the deployed Vercel URL:
Page loads, hero + form render, no console errors.
GET /api/v1/meta populates the city dropdown (visible on first paint, served by Render).
Submit form with a valid city → status badge shows source: llm and ranked cards render.
Submit with an obviously empty filter combo (e.g. min rating 5 + a quiet city) → renders the no candidates empty state copy from Phase 5.
Tail Render logs (Logs tab) — request lines appear with 200, telemetry JSON is logged on stderr.
If any step fails, see §5.

5. Troubleshooting
Symptom
Likely cause / fix
Browser shows CORS error
CORS_ORIGINS on Render does not include the exact Vercel origin. Update env var, wait for restart.
Failed to fetch from frontend
VITE_API_BASE_URL missing or wrong. Confirm value, then redeploy on Vercel.
gemini_configured: false from /health
GEMINI_API_KEY not set on Render, or has whitespace. Re-paste, redeploy.
First request hangs ~30 s
Render free-tier cold start. Ping /health first, or upgrade plan.
/api/v1/meta 500s with HF errors
Hugging Face throttle. Set HF_TOKEN on Render, or lower load_limit.
Vercel build fails on tsc --noEmit
Same TS error you would see locally — fix in frontend/, push, Vercel rebuilds.
Render build fails on pip install -e .
Confirm runtime.txt is python-3.11.x; Render's default Python may be too old.


6. Rollback
Backend: Render keeps a deploy history; Manual Deploy → Rollback to a previous build.
Frontend: Vercel’s Deployments tab → Promote to Production on a known-good build.
Both platforms support instant rollback without rebuilding.

7. Cost shape (free-tier)
Resource
Free tier
Notes
Render web service
750 hrs/month
Sleeps when idle (cold starts).
Vercel hobby
100 GB bandwidth, 6k build min/month
Static SPA is essentially free at this scale.
Gemini
Free dev quota
Keep candidate_cap modest in the API request body.
Hugging Face Hub
Anonymous
Add HF_TOKEN if you hit rate limits.

For demos and coursework, the free tiers are sufficient. For a graded review, hit /health once before the demo to wake the Render dyno.




Phase 11 — Production Deployment: Render (Backend) + Vercel (Frontend)
This phase covers deploying the current project structure to free-tier cloud platforms. The backend (FastAPI) runs on Render and the Next.js frontend runs on Vercel. All provider secrets stay server-side on Render; the browser only talks to the Render HTTPS URL.

Current project layout
Path	Role
backend/src/milestone0/app/main.py	FastAPI app entry point (uvicorn target)
backend/src/	Python source root (all milestones)
backend/pyproject.toml	Python dependency manifest
next-frontend/	Next.js 14 app (deployed to Vercel)
next-frontend/src/app/page.js	Reads NEXT_PUBLIC_API_URL for all backend calls
streamlit_app.py	Streamlit entry point (deployed to Streamlit Cloud separately)

Step 1 — Prepare the repo
1.1 Add render.yaml at the repo root
services:
  - type: web
    name: nextleap-api
    runtime: python
    plan: free
    rootDir: backend
    buildCommand: pip install -e .
    startCommand: uvicorn milestone0.app.main:app --app-dir src --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    autoDeploy: true
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: HF_TOKEN
        sync: false
      - key: CORS_ORIGINS
        sync: false

1.2 Add next-frontend/vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "framework": "nextjs"
}

1.3 Wire the API URL in next-frontend/src/app/page.js
Replace every hardcoded http://127.0.0.1:8000 with:
const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
This lets Vercel inject the live Render URL at build time while localhost still works in development.

Step 2 — Deploy the backend on Render
1. Push repo to GitHub.
2. Render dashboard → New → Blueprint → connect repo → Render reads render.yaml automatically.
3. Set environment variables in the Render dashboard:
Var	Required	Value
GEMINI_API_KEY	Yes	From https://aistudio.google.com/app/apikey
HF_TOKEN	Optional	Raises Hugging Face rate limits
CORS_ORIGINS	Yes (after step 3)	https://<your-project>.vercel.app

4. After first deploy, verify:
GET https://<service>.onrender.com/health → {"status":"ok","dataset_loaded":true}
GET https://<service>.onrender.com/api/locations → JSON array of neighbourhoods
POST https://<service>.onrender.com/api/recommend → ranked recommendations

Note: Free tier sleeps after 15 min of inactivity (30–60 s cold start). Use UptimeRobot to ping /health every 10 min to keep it warm, or upgrade to Render's $7/month paid tier.

Step 3 — Deploy the frontend on Vercel
1. Vercel dashboard → Add New Project → import the same GitHub repo.
2. Set Root Directory to next-frontend.
3. Framework preset: Next.js (auto-detected).
4. Add environment variable:
Var	Value
NEXT_PUBLIC_API_URL	https://<your-render-service>.onrender.com

5. Deploy. After build completes, verify:
https://<project>.vercel.app loads the biteAI UI.
Submitting the form calls the Render backend and returns recommendations.

Step 4 — Wire CORS
Once the Vercel URL is known, set CORS_ORIGINS on Render to the exact origin:
CORS_ORIGINS=https://<project>.vercel.app

In backend/src/milestone0/app/main.py update allow_origins to read from this env var:
import os
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, ...)

Save → Render restarts automatically → re-test from the Vercel URL.

Step 5 — Smoke-test checklist
1. Page loads, navbar, hero and feature cards render with no console errors.
2. Location dropdown populates from /api/locations.
3. Submit valid preferences → AI-ranked restaurant cards appear with rating, cuisine, price, reasoning.
4. Submit impossible filters (rating 5.0, obscure location) → "No restaurants matched" empty state.
5. Check Render logs → 200 lines appear for each request with latency.

Troubleshooting
Symptom	Fix
CORS error in browser	CORS_ORIGINS on Render doesn't match Vercel origin exactly. No trailing slash.
Failed to fetch	NEXT_PUBLIC_API_URL missing or wrong. Update in Vercel env vars and redeploy.
dataset_loaded: false	Cold start still in progress. Wait 60 s and retry /health.
Gemini returns empty recommendations	GEMINI_API_KEY not set or invalid on Render. Re-paste and redeploy.
Vercel build fails	Check next-frontend/ for TypeScript or ESLint errors locally first.

Cost on free tiers
Resource	Free allowance	Notes
Render web service	750 hrs/month	Sleeps when idle
Vercel hobby plan	100 GB bandwidth, 6 000 build-minutes	Static + SSR, essentially free at demo scale
Gemini API	Free dev quota	Keep candidate_cap ≤ 25
Hugging Face Hub	Anonymous access	Set HF_TOKEN if rate-limited

Phase 9 — Hardening and handoff (optional but recommended)
Automated tests for filters, prompt shape, JSON parsing (fixtures with fake LLM responses), and API contract tests (golden JSON for happy/empty/error paths).
README: install, set GEMINI_API_KEY, run API + UI, CLI fallbacks, and limitations (dataset revision, rate limits, candidate cap).
Cost/latency notes: candidate cap, model id, when to raise load limits, caching strategy for repeated queries (optional in-process LRU of recent Hub windows—only if measured need).

Phase 10 — Streamlit Community Cloud Deployment (Free Tier)
Concern
Approach
Role
Single-process deployment to Streamlit Community Cloud for easy sharing and demos. Eliminates need for separate backend/frontend deployment and CORS configuration.
Deployment Strategy
Streamlit Community Cloud hosts Python web apps directly from GitHub repositories with built-in secrets management and automatic deployment on push.
Secrets Management
GEMINI_API_KEY configured via Streamlit dashboard (st.secrets) - never exposed in browser client bundle. Streamlit runs all logic server-side.
Configuration Files
streamlit_app.py (repo root) - main entry point for Cloud deployment
requirements.txt or pyproject.toml - dependencies including streamlit
.streamlit/config.toml - optional app configuration (theme, layout)
Deployment Steps
1. Push code to GitHub repository
2. Connect repository to Streamlit Community Cloud
3. Set main file path: streamlit_app.py
4. Add GEMINI_API_KEY in Streamlit secrets dashboard
5. Deploy - automatic URL generation
Environment Variables
GEMINI_API_KEY (required) - Gemini API key from Google AI Studio
Optional: GEMINI_MODEL, HF_TOKEN for enhanced functionality
Performance Considerations
Free tier limitations: cold starts (~30s), resource caps, concurrent user limits
Optimize dataset loading with @st.cache_resource for faster subsequent loads
Limit candidate_cap to manage memory usage and API costs
Exit Criteria
README documents Streamlit deployment steps with screenshots
Reviewer can open hosted Streamlit URL and complete successful recommendation flow
Shareable link works without local setup or API key configuration
Implemented: streamlit_app.py, deployment documentation, and working Community Cloud instance.
