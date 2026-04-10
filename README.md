# 📊 InstaLytics AI

> AI-powered Instagram Business Intelligence — real-time profile analysis, NLP sentiment, category classification, content themes & CRM-ready export.

![Stack](https://img.shields.io/badge/stack-Python%20%7C%20Streamlit-blue)
![NLP](https://img.shields.io/badge/Analysis-NLP%20%7C%20Sentiment-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

---

## 📌 Problem Statement

Businesses and marketers struggle to extract actionable insights from public Instagram profiles without expensive enterprise tools or complex scraping setups. Competitive analysis, audience sentiment tracking, and content theme identification are often manual and time-consuming processes. **InstaLytics AI** solves this by providing an automated, real-time intelligence platform that turns raw public profile data into structured, CRM-ready business insights using NLP and domain-specific AI classification.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📡 Live Scrapping | Real-time extraction of followers, bio, and media via robust API integration. |
| 🧠 NLP Analysis | Automated sentiment scoring of audience comments and post captions. |
| 🏷️ Smart Tagging | Automatic business category classification and service tag generation. |
| 🎯 Theme Detection | AI mapping of content strategies (Tutorials, BTS, Motivational, etc.). |
| 📤 CRM Export | One-click export of structured profile intelligence in JSON format. |
| 📈 Data Viz | High-fidelity interactive charts for watchtime, swipe rates, and engagement. |
| 💡 Strategy Hints | Automated, post-by-post actionable AI suggestions to improve creator performance. |

---

## 🏗️ Tech Stack

### Frontend & Dashboard
- **Streamlit** — Interactive web interface and state management.
- **Plotly** — Advanced data visualization and KPI gauges.
- **Vanilla CSS** — Custom glassmorphism and premium dark-mode styling.

### Backend & AI
- **Python 3.9+** — Core logic and processing engine.
- **RapidAPI (Instagram Scraper API2)** — Robust, real-time data extraction.
- **TextBlob** — Natural Language Processing for sentiment analysis.
- **Custom AI Classifiers** — Domain-specific logic for business categorization.

---

## 📂 Project Structure

```
SIMATS_ORIGIN_HACK/
├── backend/
│   ├── core/
│   │   ├── nlp_sentiment.py       # TextBlob-based sentiment engine
│   │   └── verifier.py            # Public profile meta-tag parsing logic
│   ├── data_extraction/
│   │   └── extractor.py           # RapidAPI integration with failover handling
│   ├── generators/
│   │   └── metrics_builder.py     # Synthesis of retention and activity KPIs
│   └── services/
│       └── pipeline.py            # Main business logic and AI classification
├── data/
│   ├── instagram_db.csv           # Offline database for demo mode
│   └── generate_csv.py            # Database utility scripts
├── frontend/
│   ├── app.py                     # Main Streamlit dashboard and UI
│   └── components/                # Modular UI elements (charts, suggestions)
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9+
- A valid RapidAPI Key (Optional, for real-time mode)

### 1. Clone & Install
```bash
git clone <repository-url>
cd SIMATS_ORIGIN_HACK
pip install -r requirements.txt
```

### 2. Environment Configuration
The application requires the project root to be in the Python path.
**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."
```
**Linux/macOS:**
```bash
export PYTHONPATH=$PYTHONPATH:.
```

### 3. Run the Application
```bash
streamlit run frontend/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧠 How It Works

### Profile Analysis Flow
1. **Input:** User provides an Instagram URL or username and an optional RapidAPI Key.
2. **Data Extraction:** `extractor.py` fetches real-time public data. If no key is provided, it falls back to the internal `instagram_db.csv` for demo handles.
3. **Intelligence Pipeline:** `pipeline.py` processes the raw data, running captions through the NLP engine and mapping keywords to business domains.
4. **Metric Synthesis:** `metrics_builder.py` calculates synthetic metrics (like estimated watchtime and swipe rates) anchored to real public engagement ratios.
5. **Visualization:** `frontend/app.py` renders the dashboard with interactive charts and AI-generated strategy directives.

---

## 📈 Scalability

- **Database Migration:** The current CSV/JSON storage can be upgraded to a scalable database like MongoDB or PostgreSQL for handling millions of profile reports.
- **Asynchronous Processing:** Scrapping tasks can be moved to Celery/Redis workers to handle concurrent analysis requests without blocking the UI.
- **Deployment:** The application is Docker-ready and can be deployed on AWS/GCP behind a load balancer for global availability.

---

## 💡 Feasibility

InstaLytics AI is highly feasible as it leverages existing high-availability APIs and lightweight Python frameworks. By moving the complex scraping and proxy management to a third-party service (RapidAPI), the core application remains lean, easy to maintain, and ready for production deployment with minimal infrastructure overhead.

---

## 🌟 Novelty

Unlike traditional "Instagram Downloaders," InstaLytics AI focuses on **Business Intelligence**. It doesn't just show data; it classifies the brand, identifies target audiences, and provides technical "Strategy Directives" (e.g., "Cut 30% of filler") based on synthesized performance metrics. This bridge between raw data and actionable advice is the core novel contribution.

---

## 🔧 Feature Depth

- **Recursive Classifier:** Uses both Instagram's native categories and caption NLP to determine industry domains.
- **Sentiment Logic:** Analyzes audience "vibe" across multiple posts to detect brand reputation shifts.
- **CRM Ready:** Produces deeply nested, structured JSON data that can be injected directly into Salesforce or HubSpot.
- **Edge Case Handling:** Includes robust URL parsing, missing thumbnail fallbacks, and multi-field ID matching to handle Instagram's dynamic API responses.

---

## ⚠️ Ethical Use & Disclaimer

This tool is designed for **public data analysis only**.

- **No Unauthorized Access:** This tool does not bypass privacy settings or access private accounts.
- **Compliance:** Users are responsible for complying with Instagram's Terms of Service and local data privacy laws.
- **Data Privacy:** This tool does not store user credentials. API keys are handled only during the active session.

---

## 📜 License

Licensed under the [Apache 2.0 License](LICENSE).

---

## 👤 Author

**Muthu**
🔗 [GitHub Profile](https://github.com/muthu27102005)
