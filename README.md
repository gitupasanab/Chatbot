# E-Commerce Chatbot
An intelligent and interactive chatbot designed for an e-commerce platform to assist users with order tracking, payments, shipping, returns, discounts, product queries, and support tickets.

# Features
🔎 Track orders in real-time

💳 Provide payment methods (COD, UPI, etc.)

📦 Show shipping details and status

🎁 Display available discounts and offers

🛒 Recommend best-selling/top products

📄 Answer FAQs using a local dataset

🧠 Fallback to AI (Mistral model via Ollama) for general queries

🛠 Submit support tickets for unresolved issues

📊 Admin dashboard for analytics and ticket management

🌙 Light/Dark mode toggle in UI

# ⚙️ Technologies Used
1- Python

 2- FastAPI (backend)

3- Streamlit (frontend)

4- MySQL + SQLAlchemy (database)

5- Ollama + Mistral (AI fallback)

# How It Works
1- Users interact with the chatbot to get instant answers on various e-commerce-related queries.

2- If the query is not matched via logic or FAQ, it falls back to a local LLM model (Mistral) via Ollama.

3- Users can view top products or submit support tickets via the UI.

4- Admins can monitor tickets, orders, and analytics from the dashboard.

# Future Enhancements
🗣️ Add voice input/output

🌍 Support for multiple languages

🔐 Add user authentication

📱 Mobile responsiveness for UI


