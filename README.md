# NexaCart 🛒✨
**AI-Powered E-Commerce Platform**

NexaCart is a modern, full-featured e-commerce platform built with Django and Django REST Framework. It goes beyond traditional shopping by integrating a powerful AI layer powered by **Google Gemini**, offering natural language product search, personalized recommendations, and a safe, tool-based AI shopping assistant.

This project was built as a final-year academic project.

---

## 🌟 Key Features

### 1. AI Shopping Assistant (NexaBot)
- **Multi-turn Chat**: Engages users in natural conversation.
- **Tool-Calling Architecture**: The AI can dynamically call Python tools to fetch real-time data from the database (e.g., checking order status, searching products).
- **Guardrails**: Built-in regex guards to prevent prompt injection and redact PII/secrets.
- **Context-Aware**: Injects user preferences and cart data directly into the system prompt for hyper-personalized responses.

### 2. Personalized Recommender Engine
- **Behavior Tracking**: Logs views, searches, cart additions, and purchases via asynchronous Celery tasks to avoid blocking the main thread.
- **Preference Profiling**: Builds a dynamic user profile (affinity scores) based on interaction history.
- **Recommendations API**: Serves Top-K personalized products with cold-start fallbacks.
- **Offline Evaluation**: Includes a script (`evaluate_recommender.py`) to benchmark the engine using standard ranking metrics like **Precision@K** and **NDCG**.

### 3. Natural Language Search
- Parses complex user queries ("laptop for coding under 70000") using the Gemini API.
- Extracts structured parameters (Category, Max Price, Keywords) and applies them to the Django ORM for precise filtering.

### 4. Staff Management Dashboard & Product Catalog
- **Product Management**: Staff can browse live catalog items, filter by category/stock, add new products with specifications, and edit or delete items.
- **Integrated AI Price Consultation**: While creating new products, staff can consult the AI to evaluate category peer reviews and suggested launch pricing.

### 5. AI Review-Based Price Recommendation Engine
- **Review Sentiment Intelligence**: Uses **Google Gemini 3.8 Flash** to deeply analyze customer feedback on product quality, build materials, and perceived price-to-value friction.
- **Price Elasticity & Sentiment Analysis**: Detects whether items are overpriced, fair value, or underpriced, calculating sentiment distribution and elasticity scores (0-100).
- **Strategic Pricing & 1-Click Application**: Provides optimal psychological pricing (e.g. ₹59,999 vs ₹64,999) with explicit review citations and expected conversion impact. Staff can apply recommended prices with a single click.

### 6. Customer Reviews & Value Sentiment
- Verified customer review streaming and submission on storefront product pages.
- Direct feedback loop feeding the AI commercial pricing model.

### 7. Premium UI/UX
- Built with **Vanilla CSS** employing a modern, glassmorphic design language.
- Features dynamic dark mode, smooth micro-animations, and a responsive floating chatbot widget.

---

## 🏗️ Architecture & Tech Stack

- **Backend**: Django 5.1, Django REST Framework
- **Database**: SQLite (Development)
- **Async Workers**: Celery + Redis (Message Broker)
- **AI Integration**: `google-generativeai` SDK (Gemini 3.1 Pro)
- **Frontend**: Django Templates, Vanilla CSS, Vanilla JS, Chart.js

---

## 🚀 Setup Instructions

1. **Clone the repository**
2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or .\venv\Scripts\Activate.ps1 on Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements/base.txt
   ```
4. **Environment Variables**:
   Create a `.env` file in the root directory and add:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key
   REDIS_URL=redis://localhost:6379/0
   ```
5. **Run Redis**:
   Ensure a local Redis server is running on port 6379 (via Docker or natively).
6. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```
7. **Seed the Database** (Optional but recommended):
   Populates the database with 50 products, 10 users, and synthetic order/interaction data.
   ```bash
   python seed_data.py
   ```
8. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
9. **Start Celery Worker**:
   ```bash
   celery -A config worker -l INFO
   ```

---

## 📊 Evaluation
You can evaluate the recommender engine's performance on the seeded dataset:
```bash
python evaluate_recommender.py
```
*Outputs Mean Precision@5, Precision@10, and NDCG@10.*
