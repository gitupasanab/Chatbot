import streamlit as st
import pandas as pd
import sys
import os

# Add core to path for importing models and database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import get_db
from core.models import SupportTicket, Order, OrderTracking
from sqlalchemy.orm import Session
from sqlalchemy import text

st.set_page_config(page_title="Admin Dashboard", layout="wide")

ADMIN_USERNAME = "chatbot"
ADMIN_PASSWORD = "Upasana21"

# Initialize login state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# Logout function
def logout():
    st.session_state.admin_logged_in = False
    st.rerun()

# Login page
def login_page():
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(to right, #dbeafe, #fef3c7);  /* Soft blue to light yellow */
                height: 100vh;
            }
            .login-container {
                background-color: #fefce8;
                border: 2px solid #facc15;
                padding: 2rem;
                border-radius: 15px;
                width: 400px;
                margin: auto;
                margin-top: 120px;
                box-shadow: 0px 0px 20px rgba(0,0,0,0.2);
                text-align: center;
            }
            .login-title {
                font-size: 30px;
                font-weight: bold;
                color: #d97706;
                margin-bottom: 1.5rem;
            }
            .stTextInput input {
                background-color: #fff8dc !important;
                color: #000 !important;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 8px;
            }
            label {
                color: #374151 !important;
                font-weight: 600;
            }
            .stButton > button {
                background-color: #facc15;
                color: black;
                width: 100%;
                font-weight: bold;
                padding: 0.5rem;
                margin-top: 1rem;
                border-radius: 8px;
                transition: background-color 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #eab308;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # 🔐 Move the title INSIDE the white container
    st.markdown("""
        <div class='login-container'>
            <div class='login-title'>🔐 Admin Login</div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.success("Login successful!")
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")

    # Close the login container div
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- Secure Access ------------------
if st.session_state.admin_logged_in:

    st.sidebar.title("🧭 Admin Panel")
    section = st.sidebar.radio("Go to", ["Support Tickets", "Orders", "Analytics", "Feedback"])
    theme = st.sidebar.radio("Theme", ["calm", "Light"], index=0)
    st.sidebar.button("🔓 Logout", on_click=logout)

    if theme == "calm":
      st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #dbeafe, #fef3c7);  /* Soft blue to light yellow */
            color: #1f2937;  /* Tailwind Gray-800 for readable text */
        }

        .section-header {
            font-size: 32px;
            font-weight: bold;
            color: #d97706;  /* Amber-600 */
            margin-bottom: 20px;
        }

        .sub-heading {
            font-size: 18px;
            font-weight: 600;
            color: #92400e;  /* Warm brown */
            margin-top: 10px;
        }

        .detail-text {
            font-size: 15px;
            color: #374151;  /* Tailwind Gray-700 */
            margin-left: 10px;
            padding-left: 10px;
        }

        .stButton>button {
            background-color: #facc15 !important;  /* Amber-400 */
            color: #1f2937 !important;
            border-radius: 8px;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #eab308 !important;  /* Amber-500 */
            color: white !important;
        }

        .stExpanderHeader {
            color: #ca8a04 !important;  /* Amber-600 */
            font-weight: bold;
            font-size: 18px;
        }

        div[data-testid="metric-container"] {
            color: #1e293b !important;
            background-color: #fefce8 !important;  /* Light yellow background */
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

        header[data-testid="stHeader"] {
            background-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)


    # ---------------- Database Loader ------------------
    db: Session = next(get_db())

    # ---------------- Section: Support Tickets ------------------
    if section == "Support Tickets":
        st.markdown("<div class='section-header'>📩 Support Tickets</div>", unsafe_allow_html=True)
        tickets = db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).all()

        if not tickets:
            st.info("No support tickets submitted.")
        else:
            for ticket in tickets:
               with st.expander(f"📝 Ticket #{ticket.id} - {ticket.issue_type}"):
                 st.markdown(f"<div class='sub-heading'>👤 Name</div><div class='detail-text'>{ticket.name}</div>", unsafe_allow_html=True)
                 st.markdown(f"<div class='sub-heading'>📧 Email</div><div class='detail-text'>{ticket.email}</div>", unsafe_allow_html=True)
                 st.markdown(f"<div class='sub-heading'>📌 Issue Type</div><div class='detail-text'>{ticket.issue_type}</div>", unsafe_allow_html=True)
                 st.markdown(f"<div class='sub-heading'>📝 Description</div><div class='detail-text'>{ticket.description}</div>", unsafe_allow_html=True)
                 st.markdown(f"<div class='sub-heading'>🕒 Created At</div><div class='detail-text'>{ticket.created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

    # ---------------- Section: Orders ------------------
    elif section == "Orders":
        st.markdown("<div class='section-header'>📦 Orders Management</div>", unsafe_allow_html=True)
        orders = db.query(Order).all()

        if not orders:
            st.info("No orders available.")
        else:
            for order in orders:
                tracking = db.query(OrderTracking).filter(OrderTracking.tracking_number == order.tracking_number).first()
                with st.expander(f"📦 Order #{order.order_id} - User: {order.customer_name}"):
                 st.markdown(f"<div class='sub-heading'>🗓️ Order Date</div><div class='detail-text'>{order.order_date.strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)
                 st.markdown(f"<div class='sub-heading'>🚚 Status</div><div class='detail-text'>{order.order_status}</div>", unsafe_allow_html=True)
                 if tracking:
                  st.markdown(f"<div class='sub-heading'>📍 Tracking Status</div><div class='detail-text'>{tracking.status_update}</div>", unsafe_allow_html=True)
                  st.markdown(f"<div class='sub-heading'>📅 Updated At</div><div class='detail-text'>{tracking.last_updated.strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

    # ---------------- Section: Analytics ------------------
    elif section == "Analytics":
        st.markdown("<div class='section-header'>📊 Business Analytics</div>", unsafe_allow_html=True)

        total_tickets = db.query(SupportTicket).count()
        total_orders = db.query(Order).count()
        resolved_tickets = db.query(SupportTicket).filter(SupportTicket.issue_type.ilike('%resolved%')).count()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tickets", total_tickets)
        col2.metric("Total Orders", total_orders)
        col3.metric("Resolved Tickets", resolved_tickets)

        st.subheader("📈 Order Trends")
        df = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
            'Orders': [20, 45, 30, 60]
        })
        st.bar_chart(df.set_index('Month'))

    # ---------------- Section: Feedback ------------------
    elif section == "Feedback":
        st.markdown("<div class='section-header'>🗣️ Chatbot Feedback</div>", unsafe_allow_html=True)
        feedback_query = text("SELECT user_message, feedback, timestamp FROM chatbot_feedback ORDER BY timestamp DESC")
        result = db.execute(feedback_query).fetchall()

        if not result:
            st.info("No feedback has been submitted yet.")
        else:
            for i, row in enumerate(result, 1):
                with st.expander(f"💬 Feedback #{i} - {row[2].strftime('%Y-%m-%d %H:%M:%S')}"):
                 st.markdown(f"<div class='sub-heading'>🤖 Bot Message</div><div class='detail-text'>{row[0]}</div>", unsafe_allow_html=True)
                 emoji = "👍" if row[1] == "positive" else "👎"
                 st.markdown(f"<div class='sub-heading'>💬 Feedback</div><div class='detail-text'>{emoji} {row[1].capitalize()}</div>", unsafe_allow_html=True)

else:
    login_page()
