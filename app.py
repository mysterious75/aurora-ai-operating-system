"""
Aurora AI Operating System - Business Friendly Dashboard
Simple, clean, easy to understand for non-technical users
"""

import streamlit as st
import asyncio
from datetime import datetime

from mock_odoo_data import get_dashboard_data, PRODUCTS, CUSTOMERS
from ai_agent import analyze_business_data, chat_with_agent

# Page config
st.set_page_config(
    page_title="Aurora AI - Business Dashboard",
    page_icon="🏢",
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
    .big-font { font-size: 28px !important; font-weight: bold; }
    .medium-font { font-size: 18px !important; }
    .card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .green { border-left: 5px solid #28a745; }
    .yellow { border-left: 5px solid #ffc107; }
    .red { border-left: 5px solid #dc3545; }
    .blue { border-left: 5px solid #007bff; }
</style>
""", unsafe_allow_html=True)

# Load data
data = get_dashboard_data()
sales = data["sales_summary"]

# ==================== HEADER ====================
st.markdown("# 🏢 Aurora Office Furniture")
st.markdown("### AI Business Dashboard — Your Business at a Glance")
st.markdown("---")

# ==================== TOP METRICS ====================
st.markdown("## 💰 How is the Business Doing?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💵 Money Earned (Delivered Orders)",
        value=f"${sales['total_revenue']:,.0f}",
        help="Total revenue from orders that have been delivered to customers"
    )

with col2:
    st.metric(
        label="⏳ Money Coming (Pending Orders)",
        value=f"${sales['pending_revenue']:,.0f}",
        help="Revenue from orders that are confirmed but not yet delivered"
    )

with col3:
    st.metric(
        label="📦 Total Orders",
        value=sales['total_orders'],
        help="Number of orders in the system"
    )

with col4:
    st.metric(
        label="📊 Average Order Size",
        value=f"${sales['avg_order_value']:,.0f}",
        help="Average value per order"
    )

st.markdown("---")

# ==================== WHAT NEEDS ATTENTION ====================
st.markdown("## ⚠️ What Needs Your Attention?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 Out of Stock (Urgent!)")
    out_of_stock = [p for p in PRODUCTS if p["stock"] == 0]

    if out_of_stock:
        for p in out_of_stock:
            st.error(f"**{p['name']}** — {p['category']} — NEEDS RESTOCKING!")
    else:
        st.success("✅ All products are in stock!")

with col2:
    st.markdown("### 🟠 Low Stock (Order Soon)")
    low_stock = [p for p in PRODUCTS if 0 < p["stock"] < p["min_stock"]]

    if low_stock:
        for p in low_stock:
            st.warning(f"**{p['name']}** — Only {p['stock']} left (need {p['min_stock']})")
    else:
        st.success("✅ All stock levels are healthy!")

st.markdown("---")

# ==================== ORDERS OVERVIEW ====================
st.markdown("## 📋 Recent Orders — What's Happening?")

# Simple status explanation
st.info("""
**Order Status Guide:**
🟡 **Draft** = Customer interested, not confirmed yet
🔵 **Confirmed** = Order placed, waiting to ship
🟢 **Delivered** = Customer received it
🟣 **Invoiced** = Bill sent to customer
✅ **Paid** = Money received!
""")

for order in data["orders"][:8]:
    status_icon = {
        "draft": "🟡", "confirmed": "🔵",
        "delivered": "🟢", "invoiced": "🟣", "paid": "✅"
    }.get(order["status"], "⚪")

    with st.expander(f"{status_icon} {order['customer']} — ${order['total']:,.0f} — {order['status'].upper()}"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Customer Type:** {order['customer_type']}")
            st.write(f"**Location:** {order['customer_city']}")
            st.write(f"**Order Date:** {order['date']}")
        with col2:
            st.write(f"**Products:** {', '.join(order['products'])}")
            st.write(f"**Total Value:** ${order['total']:,.2f}")
            st.write(f"**Days Since Order:** {order['days_since_order']} days")

st.markdown("---")

# ==================== MONEY OWED ====================
st.markdown("## 💳 Who Owes Us Money?")

st.info("These customers have outstanding payments. Higher utilization = higher risk!")

for r in data["receivables"]:
    risk_color = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}.get(r["risk"], "⚪")

    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    with col1:
        st.write(f"**{r['customer']}**")
    with col2:
        st.write(f"${r['balance']:,.0f} owed")
    with col3:
        st.progress(r["utilization"] / 100)
        st.caption(f"{r['utilization']}% of credit limit used")
    with col4:
        st.write(f"{risk_color} {r['risk']}")

st.markdown("---")

# ==================== AI ANALYSIS ====================
st.markdown("## 🤖 AI Business Advisor")
st.markdown("Click the button below and our AI will analyze your business and tell you exactly what to do!")

if st.button("🤖 Analyze My Business", type="primary", use_container_width=True):
    with st.spinner("🔍 AI is analyzing your business data... Please wait 30 seconds..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        analysis = loop.run_until_complete(analyze_business_data(data))
        loop.close()
        st.session_state.analysis = analysis

    st.success("✅ Analysis Complete!")
    st.balloons()

# Show analysis if available
if "analysis" in st.session_state:
    analysis = st.session_state.analysis

    st.markdown("---")
    st.markdown("## 📊 AI Recommendations")

    # Executive Summary
    if "executive_summary" in analysis:
        st.markdown("### 📝 Summary for You")
        st.info(analysis["executive_summary"])

    # Priority Actions
    st.markdown("### 🎯 What Should You Do First? (Top 5)")
    for action in analysis.get("priority_actions", []):
        impact_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(action.get("impact", ""), "⚪")
        with st.expander(f"{impact_emoji} #{action.get('rank', '?')}: {action.get('action', 'N/A')}"):
            st.write(f"**Why it matters:** {action.get('impact', 'N/A')}")
            st.write(f"**How much work:** {action.get('effort', 'N/A')}")
            st.write(f"**Who should do it:** {action.get('owner', 'N/A')}")

    # Risks
    st.markdown("### ⚠️ Things That Could Go Wrong")
    for risk in analysis.get("risks", []):
        severity_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(risk.get("severity", ""), "⚪")
        with st.expander(f"{severity_emoji} {risk.get('type', 'N/A')}"):
            st.write(f"**What's the problem:** {risk.get('description', 'N/A')}")
            st.write(f"**How to fix it:** {risk.get('mitigation', 'N/A')}")

    # Opportunities
    st.markdown("### 💡 Ways to Make More Money")
    for opp in analysis.get("opportunities", []):
        with st.expander(f"💰 {opp.get('type', 'N/A')}"):
            st.write(f"**What to do:** {opp.get('description', 'N/A')}")
            st.write(f"**How much could we earn:** {opp.get('potential_value', 'N/A')}")
            st.write(f"**How long will it take:** {opp.get('timeline', 'N/A')}")

st.markdown("---")

# ==================== CHAT WITH AI ====================
st.markdown("## 💬 Ask the AI Anything")
st.markdown("Got a question about your business? Just type it below!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if question := st.chat_input("Example: Which products should I restock first?"):
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(chat_with_agent(question, data))
            loop.close()
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# Quick questions
st.markdown("### 💡 Try asking:")
col1, col2 = st.columns(2)
with col1:
    if st.button("What products are running low?"):
        st.session_state.chat_history.append({"role": "user", "content": "What products are running low?"})
        st.rerun()
    if st.button("Which customers owe us the most?"):
        st.session_state.chat_history.append({"role": "user", "content": "Which customers owe us the most?"})
        st.rerun()
with col2:
    if st.button("What should I focus on today?"):
        st.session_state.chat_history.append({"role": "user", "content": "What should I focus on today?"})
        st.rerun()
    if st.button("How can we increase sales?"):
        st.session_state.chat_history.append({"role": "user", "content": "How can we increase sales?"})
        st.rerun()

st.markdown("---")

# ==================== FOOTER ====================
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Aurora AI Operating System v1.0</strong></p>
    <p>Built for Aurora Office Furniture (Aust) Pty Ltd</p>
    <p>Managing Director: Dean Grace | Canberra, Australia</p>
</div>
""", unsafe_allow_html=True)
