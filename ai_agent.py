"""
Aurora AI Agent - Business Intelligence Analysis
Uses MiMo/Anthropic API for intelligent business insights
"""

import os
import json
import httpx
from typing import Dict, Any, List

# Load .env file if it exists (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# API Configuration - works with both .env file and HuggingFace Secrets
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")


async def call_ai(prompt: str, system: str = "", max_tokens: int = 2000) -> str:
    """Call MiMo/Anthropic API"""
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    messages = [{"role": "user", "content": prompt}]
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
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

    system_prompt = "You are a business analyst. Return ONLY valid JSON. No markdown code blocks. No explanation. Just the JSON object."

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
        f"- [{a['severity']}] {a['type']}: {a['product']}"
        for a in alerts
    ])

    # Format receivables
    recv_text = "\n".join([
        f"- {r['customer']}: ${r['balance']:,.2f} ({r['utilization']}% of limit) - Risk: {r['risk']}"
        for r in receivables[:5]
    ])

    prompt = f"""Analyze this Aurora Office Furniture business data:

SALES: Revenue ${sales['total_revenue']:,.0f}, Pending ${sales['pending_revenue']:,.0f}, Orders {sales['total_orders']}, Avg ${sales['avg_order_value']:,.0f}

INVENTORY ALERTS:
{alert_text}

PENDING ORDERS:
{order_text}

RECEIVABLES:
{recv_text}

PRODUCTS: {len(data['products'])} total, {len([p for p in data['products'] if p['stock'] == 0])} out of stock, {len([p for p in data['products'] if 0 < p['stock'] < p['min_stock']])} low stock

Return this exact JSON structure:
{{
  "executive_summary": "2 sentence summary for Managing Director",
  "priority_actions": [
    {{"rank": 1, "action": "Action text", "impact": "HIGH", "effort": "Low/Medium/High", "owner": "Role"}}
  ],
  "risks": [
    {{"type": "Risk type", "description": "Description", "severity": "HIGH", "mitigation": "How to fix"}}
  ],
  "opportunities": [
    {{"type": "Opportunity", "description": "Description", "potential_value": "Value", "timeline": "Timeline"}}
  ]
}}"""

    response = await call_ai(prompt, system_prompt, max_tokens=4000)

    # Try to parse JSON from response
    try:
        # Remove markdown code block if present
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        elif clean_response.startswith("```"):
            clean_response = clean_response[3:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()

        # Find JSON in response - try multiple approaches
        # Approach 1: Find first { to last }
        start = clean_response.find("{")
        end = clean_response.rfind("}") + 1
        if start != -1 and end != -1:
            json_str = clean_response[start:end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # Try fixing common JSON issues
                # Remove trailing commas before } or ]
                import re
                json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
                return json.loads(json_str)
    except (json.JSONDecodeError, Exception) as e:
        pass

    # Fallback: return raw text
    return {
        "executive_summary": response[:500] if len(response) > 500 else response,
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
