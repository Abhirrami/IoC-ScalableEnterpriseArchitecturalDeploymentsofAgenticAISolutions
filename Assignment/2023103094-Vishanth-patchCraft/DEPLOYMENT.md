# 🚀 Step-by-Step Deployment Guide: Deploying PatchCraft AI to Hugging Face Spaces

This guide provides step-by-step instructions to deploy the **PatchCraft AI** Autonomous Vulnerability Remediation Agentic Assistant onto **Hugging Face Spaces** (or Streamlit Community Cloud) and share the live URL with your project guide (**Chandravadhana T.K. / Dr. K. Saravanan**).

---

## 🌟 Method 1: Hugging Face Spaces (Recommended - Free & 1-Click Live Hosting)

Hugging Face Spaces supports Streamlit applications out-of-the-box natively!

### Step 1: Create a Hugging Face Account & Space
1. Go to [Hugging Face](https://huggingface.co/) and click **Sign Up** (or Log In).
2. Click on your profile icon at the top right and select **+ New Space**.
3. Fill in the Space settings:
   - **Space Name:** `PatchCraft-AI-Agent` (or `2023103094-Vishanth-PatchCraft-AI`)
   - **License:** `mit`
   - **Select the Space SDK:** Select **Streamlit** 🎈
   - **Space Hardware:** `CPU basic • 2 vCPU • 16 GB` (Free)
   - **Visibility:** `Public` (so your guide can access it directly without logging in)
4. Click **Create Space**.

### Step 2: Upload Project Files to Hugging Face Space
You can upload the files via Git or directly via the Hugging Face Web UI:

#### Option A: Drag & Drop via Web UI (Easiest & Fastest)
1. On your newly created Space page, click **Files and versions** tab.
2. Click **Add file** -> **Upload files**.
3. Drag and drop all files from your project directory (`2023103094-Vishanth-PatchCraft_AI/`):
   - `README.md` (Contains HF Spaces metadata)
   - `app.py`
   - `requirements.txt`
   - `DELIVERABLES.md`
   - `PROMPT.md`
   - `Dockerfile`
   - Entire `src/` folder (`__init__.py`, `agent_engine.py`, `tools.py`, `guardrails.py`, `utils.py`)
4. Click **Commit changes to main**.

#### Option B: Via Git Command Line
```bash
# 1. Clone your Hugging Face Space repository
git clone https://huggingface.co/spaces/<YOUR-USERNAME>/PatchCraft-AI-Agent
cd PatchCraft-AI-Agent

# 2. Copy all files from your assignment folder into this folder

# 3. Commit and push
git add .
git commit -m "Deploy PatchCraft AI Streamlit Capstone App"
git push
```

### Step 3: View & Share your Live Space Link!
- Hugging Face will automatically build and start your Streamlit application in ~1 minute.
- Once building completes, your app will be live at:
  `https://huggingface.co/spaces/<YOUR-USERNAME>/PatchCraft-AI-Agent`
- Copy this link and send it to your course guide along with your `DELIVERABLES.md` document!

---

## 🎈 Method 2: Streamlit Community Cloud (Alternative Free Cloud Option)

1. Push your project folder `2023103094-Vishanth-PatchCraft_AI` to a GitHub repository (e.g., `https://github.com/<YOUR-USERNAME>/PatchCraft-AI`).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app**.
4. Select your GitHub repository, set **Main file path** to `app.py`, and click **Deploy!**
5. Your live app URL will be created instantly (e.g., `https://patchcraft-ai.streamlit.app`).

---

## 🐳 Method 3: Local Container Execution with Docker

If your guide requests local containerized execution:

```bash
# 1. Build the Docker image
docker build -t patchcraft-ai:v2 .

# 2. Run the Docker container
docker run -p 7860:7860 patchcraft-ai:v2

# 3. Open browser to http://localhost:7860
```

---

## 📋 Summary of Files Ready for Deployment

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit Web Entrypoint Dashboard |
| `requirements.txt` | Dependency specifications (`streamlit`, `pandas`, `plotly`) |
| `README.md` | Includes Hugging Face YAML metadata header |
| `DELIVERABLES.md` | All 5 Enterprise Capstone Architectural Specifications |
| `src/` | Modular agent engine, tools, guardrails, and telemetry utilities |
| `Dockerfile` | Container runtime config |
