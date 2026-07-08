"""
Aurora AI Operating System - Premium Business Dashboard
Classic, professional, high-fidelity dark-mode telemetry
"""

import streamlit as st
import asyncio
from datetime import datetime

from mock_odoo_data import get_dashboard_data, PRODUCTS, CUSTOMERS
from ai_agent import analyze_business_data, chat_with_agent

# Page config
st.set_page_config(
    page_title="Aurora AI - Operations Dashboard",
    page_icon="🏢",
    layout="wide"
)

# Custom Design System - Slate Dark / Classic Corporate Theme CSS
st.markdown("""
<style>
    /* Import Premium Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global reset for container text */
    .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0B0F19;
        color: #F8FAFC;
    }

    /* Style titles and subheaders */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Header border line styling */
    hr {
        border-color: #1E293B !important;
        margin: 20px 0 !important;
    }

    /* Custom Metric Cards Grid */
    .metric-card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin: 20px 0 30px 0;
    }

    .metric-card {
        background: #151D30;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #3B82F6;
    }

    .metric-card.revenue {
        border-left: 4px solid #10B981;
    }
    .metric-card.pending {
        border-left: 4px solid #F59E0B;
    }
    .metric-card.orders {
        border-left: 4px solid #3B82F6;
    }
    .metric-card.average {
        border-left: 4px solid #8B5CF6;
    }

    .metric-label {
        font-size: 12px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.01em;
    }

    .metric-desc {
        font-size: 11px;
        color: #64748B;
        margin-top: 6px;
    }

    /* Custom Attention Alerts Grid */
    .attention-card {
        background: #151D30;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: border-color 0.2s ease;
    }
    
    .attention-card:hover {
        border-color: #334155;
    }

    .attention-card.critical {
        border-left: 4px solid #EF4444;
    }

    .attention-card.warning {
        border-left: 4px solid #F59E0B;
    }

    .attention-title {
        font-weight: 600;
        color: #F8FAFC;
        font-size: 14px;
    }

    .attention-subtitle {
        color: #94A3B8;
        font-size: 12px;
        margin-top: 3px;
    }

    .badge {
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge.urgent {
        background-color: rgba(239, 68, 68, 0.12);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }

    .badge.low {
        background-color: rgba(245, 158, 11, 0.12);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.25);
    }

    /* Custom Receivables Row styling */
    .receivable-row {
        background: #151D30;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: border-color 0.2s ease;
    }
    
    .receivable-row:hover {
        border-color: #334155;
    }

    .receivable-name {
        font-weight: 600;
        color: #F8FAFC;
        font-size: 14px;
    }

    .receivable-balance {
        font-family: monospace;
        font-size: 14px;
        font-weight: 700;
        color: #F8FAFC;
    }

    /* Custom AI Report styling */
    .report-container {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 24px;
        margin-top: 15px;
    }

    .report-section {
        border-bottom: 1px solid #1E293B;
        padding-bottom: 20px;
        margin-bottom: 20px;
    }

    .report-section:last-child {
        border-bottom: none;
        padding-bottom: 0;
        margin-bottom: 0;
    }

    /* Refine Streamlit native components (Buttons, Expanders, Info Banners) */
    div.stButton > button {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        width: 100% !important;
        transition: background-color 0.2s ease, transform 0.1s ease !important;
        font-size: 14px !important;
    }
    div.stButton > button:hover {
        background-color: #2563EB !important;
        transform: translateY(-1px);
    }
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* Expander card custom style rules */
    div[data-testid="stExpander"] {
        background-color: #151D30 !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="stExpander"] details {
        border: none !important;
    }
    div[data-testid="stExpander"] summary {
        background-color: #151D30 !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #3B82F6 !important;
    }
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        color: #E2E8F0 !important;
        font-size: 13px !important;
    }

    /* Customize Streamlit alerts / banners */
    div[data-testid="stAlert"] {
        background-color: #151D30 !important;
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }
    div[data-testid="stAlert"] p {
        color: #E2E8F0 !important;
        font-size: 13px !important;
    }

    /* Custom Chat bubbles */
    div[data-testid="stChatMessage"] {
        background-color: #151D30 !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"][data-test-user="user"] {
        background-color: #1E293B !important;
        border-color: #3B82F630 !important;
    }
    div[data-testid="stChatMessage"] p {
        color: #E2E8F0 !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
data = get_dashboard_data()
sales = data["sales_summary"]

# ==================== HEADER ====================
st.markdown("# 🏢 Aurora Office Furniture")
st.markdown("<p style='color: #94A3B8; font-size: 16px; margin-top: -10px; margin-bottom: 24px;'>Enterprise Operations Control Dashboard & Intelligent AI Co-Pilot</p>", unsafe_allow_html=True)
st.markdown("---")

# ==================== FINANCIAL TELEMETRY ====================
st.markdown("## 💰 Financial Telemetry")

metrics_html = f"""
<div class="metric-card-container">
  <div class="metric-card revenue">
    <div class="metric-label">💵 Money Earned</div>
    <div class="metric-value">${sales['total_revenue']:,.2f} AUD</div>
    <div class="metric-desc">Total billing from delivered, invoiced, and paid orders</div>
  </div>
  <div class="metric-card pending">
    <div class="metric-label">⏳ Money Coming</div>
    <div class="metric-value">${sales['pending_revenue']:,.2f} AUD</div>
    <div class="metric-desc">Value of active draft and confirmed pending orders</div>
  </div>
  <div class="metric-card orders">
    <div class="metric-label">📦 Total Orders</div>
    <div class="metric-value">{sales['total_orders']}</div>
    <div class="metric-desc">Total orders registered in Odoo system</div>
  </div>
  <div class="metric-card average">
    <div class="metric-label">📊 Avg Order Size</div>
    <div class="metric-value">${sales['avg_order_value']:,.2f} AUD</div>
    <div class="metric-desc">Average gross invoice value per sale</div>
  </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)

# ==================== STOCK TELEMETRY ====================
st.markdown("## 📦 Inventory Operations")
st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-top: -12px; margin-bottom: 20px;'>Live warehouse alerts and replenishment tracking.</p>", unsafe_allow_html=True)

# Custom stock alerts
out_of_stock = [p for p in PRODUCTS if p["stock"] == 0]
low_stock = [p for p in PRODUCTS if 0 < p["stock"] < p["min_stock"]]

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🔴 Out of Stock (Urgent)")
    if out_of_stock:
        for p in out_of_stock:
            html = f"""
            <div class="attention-card critical">
              <div>
                <div class="attention-title">{p['name']}</div>
                <div class="attention-subtitle">{p['category']}</div>
              </div>
              <div class="badge urgent">Urgent Restock</div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="attention-card" style="border-left: 4px solid #10B981;"><div class="attention-title">✅ All products are in stock!</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🟠 Low Stock (Order Soon)")
    if low_stock:
        for p in low_stock:
            html = f"""
            <div class="attention-card warning">
              <div>
                <div class="attention-title">{p['name']}</div>
                <div class="attention-subtitle">Current stock: {p['stock']} (Target: {p['min_stock']})</div>
              </div>
              <div class="badge low">Low Stock</div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="attention-card" style="border-left: 4px solid #10B981;"><div class="attention-title">✅ All stock levels are healthy!</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ==================== RECENT ORDERS ====================
st.markdown("## 📋 Recent Orders Log")
st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-top: -12px; margin-bottom: 20px;'>Expand items to view order line items and client profile.</p>", unsafe_allow_html=True)

st.info("""
**Order Status Legend:**
🟡 **Draft** - Pending verification | 🔵 **Confirmed** - Ready for dispatch | 🟢 **Delivered** - Transit completed | 🟣 **Invoiced** - Awaiting payment | ✅ **Paid** - Settled
""")

for order in data["orders"][:8]:
    status_icon = {
        "draft": "🟡", "confirmed": "🔵",
        "delivered": "🟢", "invoiced": "🟣", "paid": "✅"
    }.get(order["status"], "⚪")

    with st.expander(f"{status_icon} {order['customer']} — ${order['total']:,.2f} — {order['status'].upper()}"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Customer Type:** {order['customer_type']}")
            st.write(f"**Location:** {order['customer_city']}")
            st.write(f"**Order Date:** {order['date']}")
        with col2:
            st.write(f"**Products:** {', '.join(order['products'])}")
            st.write(f"**Total Value:** ${order['total']:,.2f} AUD")
            st.write(f"**Days Since Logged:** {order['days_since_order']} days ago")

st.markdown("---")

# ==================== RECEIVABLES & CREDIT ====================
st.markdown("## 💳 Receivables & Credit Accounts")
st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-top: -12px; margin-bottom: 20px;'>Review credit utilization and payment aging risks for active business accounts.</p>", unsafe_allow_html=True)

receivables_html = ""
for r in data["receivables"]:
    risk_text_color = "#FCA5A5" if r["risk"] == "HIGH" else "#FCD34D" if r["risk"] == "MEDIUM" else "#A7F3D0"
    risk_bg_color = "rgba(239, 68, 68, 0.12)" if r["risk"] == "HIGH" else "rgba(245, 158, 11, 0.12)" if r["risk"] == "MEDIUM" else "rgba(16, 185, 129, 0.12)"
    
    receivables_html += f"""
    <div class="receivable-row">
      <div style="flex: 2;">
        <span class="receivable-name">{r['customer']}</span>
      </div>
      <div style="flex: 1; text-align: right; padding-right: 25px;">
        <span class="receivable-balance">${r['balance']:,.2f} AUD</span>
      </div>
      <div style="flex: 2; display: flex; align-items: center; gap: 12px;">
        <div style="flex: 1; background: #1E293B; height: 6px; border-radius: 3px; overflow: hidden;">
          <div style="background: #3B82F6; width: {min(r['utilization'], 100)}%; height: 100%;"></div>
        </div>
        <span style="font-size: 12px; color: #94A3B8; width: 45px; font-weight: 500;">{r['utilization']}%</span>
      </div>
      <div style="width: 120px; text-align: right;">
        <span class="badge" style="background: {risk_bg_color}; color: {risk_text_color}; border: 1px solid {risk_text_color}25;">{r['risk']} RISK</span>
      </div>
    </div>
    """
st.markdown(receivables_html, unsafe_allow_html=True)

st.markdown("---")

# ==================== AI ANALYSIS REPORT ====================
st.markdown("## 🤖 AI Business Advisor")
st.markdown("Initiate a comprehensive business analysis audit. The AI agent will ingest financial and inventory tables to identify strategic risks and growth optimizations.")

if st.button("🤖 Run AI Business Audit", type="primary"):
    with st.spinner("🔍 Executing AI business model diagnostics..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        analysis = loop.run_until_complete(analyze_business_data(data))
        loop.close()
        st.session_state.analysis = analysis
    st.success("✅ Analysis Complete!")

# Show analysis if available
if "analysis" in st.session_state:
    analysis = st.session_state.analysis
    
    st.markdown("---")
    st.markdown("## 📊 AI Recommendation Report")
    
    # Executive Summary
    if "executive_summary" in analysis:
        st.markdown("### 📝 Executive Summary")
        st.info(analysis["executive_summary"])

    # Priority Actions
    st.markdown("### 🎯 Prioritized Action Items")
    for action in analysis.get("priority_actions", []):
        impact_emoji = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}.get(action.get("impact", "").upper(), "⚪")
        with st.expander(f"{impact_emoji} Action #{action.get('rank', '?')}: {action.get('action')}"):
            st.write(f"**Impact:** {action.get('impact')} | **Complexity:** {action.get('effort')} | **Assignee:** {action.get('owner')}")

    # Risks and Opportunities Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚠️ Core Operational Risks")
        for risk in analysis.get("risks", []):
            with st.expander(f"🔴 {risk.get('type')}"):
                st.write(f"**Description:** {risk.get('description')}")
                st.write(f"**Mitigation Plan:** {risk.get('mitigation')}")
                
    with col2:
        st.markdown("### 💡 Strategic Opportunities")
        for opp in analysis.get("opportunities", []):
            with st.expander(f"🟢 {opp.get('type')}"):
                st.write(f"**Strategy:** {opp.get('description')}")
                st.write(f"**Potential Value:** {opp.get('potential_value')} | **Timeline:** {opp.get('timeline')}")

st.markdown("---")

# ==================== CO-PILOT CHAT INTERFACE ====================
st.markdown("## 💬 AI Co-Pilot Q&A")
st.markdown("Query the active Odoo database or ask the assistant for workflow action items in natural language.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if question := st.chat_input("Query: e.g., Which customers owe us the most money?"):
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Consulting operations logs..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(chat_with_agent(question, data))
            loop.close()
        st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# Quick actions query buttons
st.markdown("<p style='font-size: 13px; font-weight: 600; color: #94A3B8; margin-top: 15px;'>Quick Queries:</p>", unsafe_allow_html=True)

def ask_quick_question(question):
    """Handle quick question button click"""
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.spinner("🤖 Consulting operations logs..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(chat_with_agent(question, data))
        loop.close()
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

col1, col2 = st.columns(2)
with col1:
    if st.button("📦 Which products are currently running low in warehouse?"):
        ask_quick_question("Which products are currently running low in warehouse?")
    if st.button("💳 List outstanding customer accounts sorted by risk."):
        ask_quick_question("List outstanding customer accounts sorted by risk.")
with col2:
    if st.button("🎯 Outline operations priorities for MD today."):
        ask_quick_question("Outline operations priorities for MD today.")
    if st.button("💰 Propose sales strategies to increase gross margins."):
        ask_quick_question("Propose sales strategies to increase gross margins.")

st.markdown("---")

# ==================== FOOTER ====================
st.markdown("""
<div style="text-align: center; color: #64748B; padding: 20px 0 10px 0; font-size: 12px; border-top: 1px solid #1E293B;">
    <p style="margin: 0; font-weight: 700; color: #94A3B8;">Aurora AI Operating System v1.0.0</p>
    <p style="margin: 4px 0 0 0;">Engineered for Aurora Office Furniture (Aust) Pty Ltd</p>
    <p style="margin: 2px 0 0 0;">Canberra • Sydney • Melbourne | Managing Director: Dean Grace</p>
</div>
""", unsafe_allow_html=True)
