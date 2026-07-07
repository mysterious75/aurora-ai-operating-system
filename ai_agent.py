"""
Aurora AI Agent - Business Intelligence Analysis
Uses MiMo/Anthropic API for intelligent business insights
"""

import os
import json
import httpx
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration from .env
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")


async def call_ai(prompt: str, system: str = "") -> str:
    """Call MiMo/Anthropic API"""
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    messages = [{"role": "user", "content": prompt}]
    payload = {
        "model": MODEL,
        "max_tokens": 2000,
        "messages": messages,
    }
    if system:
        payload["system"] = system

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{BASE_URL}/v1/messages", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]


async def analyze_business_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """AI agent analyzes all business data and returns prioritized insights"""

    system_prompt = """You are an AI business analyst for Aurora Office Furniture, an Australian office furniture company.

Your job is to analyze business data and provide:
1. TOP 5 PRIORITY ACTIONS (ranked by business impact)
2. RISKS & ALERTS (things needing immediate attention)
3. OPPORTUNITIES (revenue growth, cost savings)
4. SUMMARY DASHBOARD (key metrics in plain English)

Be specific, actionable, and use Australian dollars (AUD). Focus on practical next steps a business manager can take TODAY."""

    # Prepare data summary for AI
    sales = data["sales_summary"]
    alerts = data["inventory_alerts"]
    receivables = data["receivables"]
    orders = data["orders"]

    # Format orders
    pending_orders = [o for o in orders if o["status"] in ["draft", "confirmed"]]
    order_text = "\n".join([
        f"- {o['customer']} ({o['customer_type']}): ${o['total']:,.2f} - {o['status'].upper()} - {o['days_since_order']} days ago"
        for o in pending_orders
    ])

    # Format alerts
    alert_text = "\n".join([
        f"- [{a['severity']}] {a['type']}: {a['product']} {'(Stock: ' + str(a.get('current', 0)) + ')' if 'current' in a else ''}"
        for a in alerts
    ])

    # Format receivables
    recv_text = "\n".join([
        f"- {r['customer']}: ${r['balance']:,.2f} ({r['utilization']}% of limit) - Risk: {r['risk']}"
        for r in receivables[:5]
    ])

    prompt = f"""ANALYZE THIS AURORA OFFICE FURNITURE BUSINESS DATA:

=== SALES SUMMARY ===
Total Revenue (Delivered): ${sales['total_revenue']:,.2f} AUD
Pending Revenue: ${sales['pending_revenue']:,.2f} AUD
Total Orders: {sales['total_orders']}
Average Order Value: ${sales['avg_order_value']:,.2f} AUD

=== INVENTORY ALERTS ===
{alert_text}

=== PENDING ORDERS ===
{order_text}

=== ACCOUNTS RECEIVABLE ===
{recv_text}

=== PRODUCTS ===
Total SKUs: {len(data['products'])}
Out of Stock: {len([p for p in data['products'] if p['stock'] == 0])}
Low Stock: {len([p for p in data['products'] if 0 < p['stock'] < p['min_stock']])}

Provide your analysis in this JSON format:
{{
    "priority_actions": [
        {{"rank": 1, "action": "...", "impact": "HIGH/MEDIUM/LOW", "effort": "...", "owner": "..."}},
        ...
    ],
    "risks": [
        {{"type": "...", "description": "...", "severity": "CRITICAL/HIGH/MEDIUM", "mitigation": "..."}},
        ...
    ],
    "opportunities": [
        {{"type": "...", "description": "...", "potential_value": "...", "timeline": "..."}},
        ...
    ],
    "dashboard_metrics": {{
        "revenue_status": "...",
        "inventory_health": "...",
        "cash_flow_risk": "...",
        "customer_satisfaction": "..."
    }},
    "executive_summary": "2-3 sentence summary for the Managing Director"
}}"""

    response = await call_ai(prompt, system_prompt)

    # Try to parse JSON from response
    try:
        # Find JSON in response
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(response[start:end])
    except json.JSONDecodeError:
        pass

    # Fallback: return raw text
    return {
        "executive_summary": response,
        "priority_actions": [],
        "risks": [],
        "opportunities": [],
        "dashboard_metrics": {}
    }


async def chat_with_agent(question: str, context: Dict[str, Any]) -> str:
    """Interactive Q&A about business data"""

    system_prompt = """You are Aurora AI Assistant - an intelligent business advisor for Aurora Office Furniture (Canberra, Australia).

You have access to the company's Odoo ERP data. Answer questions concisely with specific numbers and actionable advice.

Key context:
- Aurora is a family-run office furniture company (est. 1993)
- Offices in Canberra, Sydney, Melbourne
- MD: Dean Grace
- Uses Odoo ERP for operations
- Products: office chairs, desks, storage, accessories"""

    # Add relevant context
    sales = context["sales_summary"]
    context_text = f"""
Current Business Snapshot:
- Revenue: ${sales['total_revenue']:,.2f} AUD
- Pending Orders: {sales['pending_orders']}
- Out of Stock Items: {len([p for p in context['products'] if p['stock'] == 0])}
- Top Customer: {sales['top_customer']}
"""

    prompt = f"{context_text}\n\nUser Question: {question}"

    return await call_ai(prompt, system_prompt)
