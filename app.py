"""
Aurora AI Operating System - Dashboard
Intelligent Business Analysis for Aurora Office Furniture
"""

import streamlit as st
import asyncio
import json
from datetime import datetime

from mock_odoo_data import get_dashboard_data, PRODUCTS, CUSTOMERS
from ai_agent import analyze_business_data, chat_with_agent

# Page config
st.set_page_config(
    page_title="Aurora AI Operating System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2d5a87;
    }
    .alert-critical { border-left: 4px solid #dc3545; background: #fff5f5; padding: 0.5rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
    .alert-high { border-left: 4px solid #fd7e14; background: #fff8f0; padding: 0.5rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
    .alert-medium { border-left: 4px solid #ffc107; background: #fffdf0; padding: 0.5rem 1rem; border-radius: 4px; margin: 0.5rem 0; }
    .stMetric { background: #f8f9fa; padding: 1rem; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; color:white;">🏢 Aurora AI Operating System</h1>
    <p style="margin:0; opacity:0.8;">Intelligent Business Analysis — Powered by AI</p>
    <p style="margin:0; font-size:0.8em; opacity:0.6;">Aurora Office Furniture (Aust) Pty Ltd • Canberra, Australia</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load data
data = get_dashboard_data()
sales = data["sales_summary"]

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")

    if st.button("🤖 Run AI Analysis", type="primary", use_container_width=True):
        with st.spinner("AI analyzing business data..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            st.session_state.analysis = loop.run_until_complete(analyze_business_data(data))
            loop.close()
        st.success("Analysis complete!")

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Products", len(PRODUCTS))
    st.metric("Active Customers", len(CUSTOMERS))
    st.metric("Out of Stock", len([p for p in PRODUCTS if p["stock"] == 0]))

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Aurora AI OS** demonstrates:
    - 🤖 AI-powered business analysis
    - 📊 Real-time Odoo data integration
    - ⚡ Prioritized action items
    - 💬 Interactive AI assistant
    """)

# Main content - Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🤖 AI Analysis", "📦 Inventory", "💬 AI Assistant"])

# Tab 1: Dashboard
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Revenue (Delivered)", f"${sales['total_revenue']:,.2f}")
    with col2:
        st.metric("⏳ Pending Revenue", f"${sales['pending_revenue']:,.2f}")
    with col3:
        st.metric("📋 Total Orders", sales['total_orders'])
    with col4:
        st.metric("📈 Avg Order Value", f"${sales['avg_order_value']:,.2f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Recent Orders")
        for order in data["orders"][:6]:
            status_color = {
                "draft": "🟡", "confirmed": "🔵",
                "delivered": "🟢", "invoiced": "🟣", "paid": "✅"
            }.get(order["status"], "⚪")

            with st.container():
                c1, c2, c3 = st.columns([3, 2, 1])
                c1.write(f"**{order['customer']}**")
                c2.write(f"${order['total']:,.2f}")
                c3.write(f"{status_color} {order['status']}")

    with col2:
        st.markdown("### ⚠️ Inventory Alerts")
        for alert in data["inventory_alerts"]:
            css_class = f"alert-{alert['severity'].lower()}"
            icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(alert["severity"], "⚪")
            st.markdown(f"""
            <div class="{css_class}">
                {icon} <strong>{alert['type']}</strong>: {alert['product']}
                {' — Stock: ' + str(alert.get('current', 0)) if 'current' in alert else ' — OUT OF STOCK'}
            </div>
            """, unsafe_allow_html=True)

    # Receivables
    st.markdown("### 💳 Accounts Receivable Risk")
    for r in data["receivables"]:
        risk_color = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}.get(r["risk"], "⚪")
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        col1.write(r["customer"])
        col2.write(f"${r['balance']:,.2f}")
        col3.progress(r["utilization"] / 100, text=f"{r['utilization']}% utilized")
        col4.write(f"{risk_color} {r['risk']}")

# Tab 2: AI Analysis
with tab2:
    if st.session_state.analysis:
        analysis = st.session_state.analysis

        # Executive Summary
        if "executive_summary" in analysis:
            st.markdown("### 📝 Executive Summary")
            st.info(analysis["executive_summary"])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Priority Actions")
            for action in analysis.get("priority_actions", []):
                impact_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(action.get("impact", ""), "⚪")
                with st.expander(f"{impact_emoji} #{action.get('rank', '?')}: {action.get('action', 'N/A')}"):
                    st.write(f"**Impact:** {action.get('impact', 'N/A')}")
                    st.write(f"**Effort:** {action.get('effort', 'N/A')}")
                    st.write(f"**Owner:** {action.get('owner', 'N/A')}")

        with col2:
            st.markdown("### ⚠️ Risks & Alerts")
            for risk in analysis.get("risks", []):
                severity_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(risk.get("severity", ""), "⚪")
                with st.expander(f"{severity_emoji} {risk.get('type', 'N/A')}: {risk.get('description', 'N/A')[:50]}..."):
                    st.write(f"**Severity:** {risk.get('severity', 'N/A')}")
                    st.write(f"**Description:** {risk.get('description', 'N/A')}")
                    st.write(f"**Mitigation:** {risk.get('mitigation', 'N/A')}")

        st.markdown("### 💡 Opportunities")
        for opp in analysis.get("opportunities", []):
            with st.expander(f"💰 {opp.get('type', 'N/A')}: {opp.get('description', 'N/A')[:50]}..."):
                st.write(f"**Potential Value:** {opp.get('potential_value', 'N/A')}")
                st.write(f"**Timeline:** {opp.get('timeline', 'N/A')}")
    else:
        st.info("👈 Click 'Run AI Analysis' in the sidebar to generate insights")

# Tab 3: Inventory
with tab3:
    st.markdown("### 📦 Product Inventory")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total SKUs", len(PRODUCTS))
    col2.metric("Out of Stock", len([p for p in PRODUCTS if p["stock"] == 0]))
    col3.metric("Low Stock", len([p for p in PRODUCTS if 0 < p["stock"] < p["min_stock"]]))

    # Product table
    for p in PRODUCTS:
        stock_status = "🔴" if p["stock"] == 0 else "🟠" if p["stock"] < p["min_stock"] else "🟢"

        with st.expander(f"{stock_status} {p['name']} — {p['category']}"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Price", f"${p['price']:,.2f}")
            c2.metric("Cost", f"${p['cost']:,.2f}")
            c3.metric("Stock", p['stock'])
            c4.metric("Min Stock", p['min_stock'])

            margin = ((p["price"] - p["cost"]) / p["price"]) * 100
            st.progress(margin / 100, text=f"Margin: {margin:.1f}%")

# Tab 4: AI Assistant
with tab4:
    st.markdown("### 💬 Ask Aurora AI")
    st.markdown("Ask questions about your business data in natural language.")

    # Chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if question := st.chat_input("Ask about sales, inventory, customers..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(chat_with_agent(question, data))
                loop.close()
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Sample questions
    st.markdown("#### 💡 Try asking:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- What are our biggest inventory risks?")
        st.markdown("- Which customers should we follow up with?")
    with col2:
        st.markdown("- What's our best-selling product category?")
        st.markdown("- How can we improve cash flow?")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8em;">
    <p>Aurora AI Operating System v1.0 | Built for Aurora Office Furniture (Aust) Pty Ltd</p>
    <p>Demo by: AI Automation Engineer | <a href="https://github.com/mysterious75">GitHub Portfolio</a></p>
</div>
""", unsafe_allow_html=True)
