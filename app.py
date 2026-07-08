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
    page_title="Aurora Office Furniture — AI Operations System",
    page_icon="🌿",
    layout="wide"
)

# Aurora Brand CSS — matches auroraofficefurniture.com.au
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #f8f9fa !important;
        color: #35383b !important;
    }
    .block-container { padding-top: 0 !important; max-width: 1200px; }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #0f2024 !important;
        letter-spacing: -0.02em !important;
    }
    hr { border-color: #e2e6ea !important; margin: 24px 0 !important; }
    p, li { color: #35383b !important; }

    .metric-card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px; margin: 8px 0 28px 0;
    }
    .metric-card {
        background: #ffffff; border: 1px solid #e2e6ea;
        border-radius: 10px; padding: 22px 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,90,106,0.12); }
    .metric-card.revenue { border-top: 4px solid #10b981; }
    .metric-card.pending { border-top: 4px solid #f39682; }
    .metric-card.orders  { border-top: 4px solid #005a6a; }
    .metric-card.average { border-top: 4px solid #6e969b; }
    .metric-label {
        font-size: 11px; font-weight: 700; color: #5a7380 !important;
        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;
    }
    .metric-value { font-size: 28px; font-weight: 800; color: #0f2024 !important; letter-spacing: -0.02em; }
    .metric-desc  { font-size: 11px; color: #5a7380 !important; margin-top: 6px; }

    .attention-card {
        background: #ffffff; border: 1px solid #e2e6ea; border-radius: 8px;
        padding: 14px 18px; margin-bottom: 10px;
        display: flex; align-items: center; justify-content: space-between;
        transition: box-shadow 0.2s ease;
    }
    .attention-card:hover { box-shadow: 0 2px 8px rgba(0,90,106,0.10); }
    .attention-card.critical { border-left: 4px solid #ef4444; }
    .attention-card.warning  { border-left: 4px solid #f39682; }
    .attention-title    { font-weight: 600; color: #0f2024 !important; font-size: 13px; }
    .attention-subtitle { color: #5a7380 !important; font-size: 11px; margin-top: 2px; }
    .badge { padding: 3px 8px; border-radius: 20px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
    .badge.urgent { background: #fee2e2; color: #b91c1c !important; }
    .badge.low    { background: #fff3e0; color: #b45309 !important; }

    .receivable-row {
        background: #ffffff; border: 1px solid #e2e6ea; border-radius: 8px;
        padding: 14px 18px; margin-bottom: 8px;
        display: flex; align-items: center; justify-content: space-between;
        transition: box-shadow 0.2s;
    }
    .receivable-row:hover { box-shadow: 0 2px 8px rgba(0,90,106,0.10); }
    .receivable-name    { font-weight: 600; color: #0f2024 !important; font-size: 13px; }
    .receivable-balance { font-size: 13px; font-weight: 700; color: #0f2024 !important; font-family: monospace; }

    div.stButton > button {
        background-color: #005a6a !important; color: #ffffff !important;
        border-radius: 6px !important; border: none !important;
        font-weight: 600 !important; padding: 10px 20px !important;
        width: 100% !important; font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
        transition: background-color 0.2s ease, transform 0.1s ease !important;
    }
    div.stButton > button:hover { background-color: #1d434c !important; transform: translateY(-1px); }

    div[data-testid="stExpander"] {
        background-color: #ffffff !important; border: 1px solid #e2e6ea !important;
        border-radius: 8px !important; margin-bottom: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stExpander"] details { border: none !important; }
    div[data-testid="stExpander"] summary {
        background-color: #ffffff !important; color: #0f2024 !important;
        font-weight: 600 !important; border-radius: 8px !important;
        font-size: 13px !important; padding: 12px 16px !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stExpander"] summary:hover { color: #005a6a !important; }
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        color: #35383b !important; font-size: 13px !important;
    }

    div[data-testid="stAlert"] {
        background-color: #e8f5f6 !important; border: 1px solid #b2d8dc !important;
        border-radius: 8px !important;
    }
    div[data-testid="stAlert"] p { color: #0f2024 !important; font-size: 13px !important; }

    div[data-testid="stChatMessage"] {
        background-color: #ffffff !important; border: 1px solid #e2e6ea !important;
        border-radius: 10px !important; padding: 14px 18px !important;
        margin-bottom: 10px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stChatMessage"] p {
        color: #35383b !important; font-size: 13px !important; line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
data = get_dashboard_data()
sales = data["sales_summary"]

# ==================== HEADER ====================
st.markdown("""
<div style="background:#0f2024; padding:16px 24px; margin:-1rem -4rem 2rem -4rem; display:flex; align-items:center; justify-content:space-between; border-bottom:3px solid #005a6a;">
  <div>
    <span style="font-size:20px; font-weight:800; color:#ffffff; font-family:Inter,sans-serif; letter-spacing:-0.03em;">
      aurora <span style="color:#f39682;">office furniture</span>
    </span>
    <span style="display:block; font-size:11px; color:#6e969b; letter-spacing:0.08em; text-transform:uppercase; margin-top:2px;">
      AI Operations System &bull; Internal Dashboard
    </span>
  </div>
  <div style="display:flex; gap:12px; align-items:center;">
    <span style="background:#1d434c; color:#fff; font-size:10px; font-weight:700; padding:4px 12px; border-radius:20px; letter-spacing:0.06em; text-transform:uppercase;">Live ERP Data</span>
    <span style="background:#f39682; color:#fff; font-size:10px; font-weight:700; padding:4px 12px; border-radius:20px; letter-spacing:0.06em; text-transform:uppercase;">AI Powered</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("## Operations Dashboard")
st.markdown("<p style='color:#5a7380; font-size:14px; margin-top:-8px; margin-bottom:24px;'>Real-time Odoo ERP telemetry • Canberra, Sydney, Melbourne</p>", unsafe_allow_html=True)
st.markdown("---")

# ==================== FINANCIAL TELEMETRY ====================
st.markdown("## Financial Overview")

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
st.markdown("## AI Business Audit")
st.markdown("<p style='color:#5a7380; font-size:13px; margin-top:-8px;'>Run a complete analysis of your Odoo ERP data to surface risks, priorities and growth opportunities.</p>", unsafe_allow_html=True)

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
    st.markdown("## Business Intelligence Report")
    
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
st.markdown("## AI Co-Pilot Q&A")
st.markdown("<p style='color:#5a7380; font-size:13px; margin-top:-8px;'>Query your Odoo operations data or ask for actionable business guidance.</p>", unsafe_allow_html=True)

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
st.markdown("<p style='font-size: 11px; font-weight: 700; color: #5a7380; margin-top: 16px; text-transform: uppercase; letter-spacing: 0.08em;'>Quick Queries</p>", unsafe_allow_html=True)

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
<div style="background:#0f2024; padding:24px 32px; margin:24px -4rem -4rem -4rem; text-align:center;">
    <p style="margin:0; font-weight:800; color:#ffffff; font-family:Inter,sans-serif; font-size:16px; letter-spacing:-0.02em;">
        aurora <span style="color:#f39682;">office furniture</span>
    </p>
    <p style="margin:6px 0 0 0; color:#6e969b; font-size:11px; letter-spacing:0.06em; text-transform:uppercase;">
        Canberra &bull; Sydney &bull; Melbourne &bull; Est. 1993
    </p>
    <p style="margin:4px 0 0 0; color:#5a7380; font-size:11px;">
        AI Operations System &mdash; Internal Use Only &mdash; Managing Director: Dean Grace
    </p>
    <p style="margin:8px 0 0 0; color:#3a5a63; font-size:10px;">
        &copy; 2026 Aurora Office Furniture (Aust) Pty Ltd &bull; ABN 34 659 801 662
    </p>
</div>
""", unsafe_allow_html=True)
