import streamlit as st
import os

st.set_page_config(page_title="Aurora AI OS", page_icon="🏢", layout="wide")

st.title("🏢 Aurora AI Operating System")
st.success("✅ App loaded successfully!")

st.markdown("---")

# Check environment variables
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
base_url = os.environ.get("ANTHROPIC_BASE_URL", "")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Environment Status")
    st.write(f"API Key: {'✅ Set' if api_key else '❌ Not Set'}")
    st.write(f"Base URL: {'✅ Set' if base_url else '❌ Not Set'}")

with col2:
    st.markdown("### Quick Stats")
    st.metric("Products", "15")
    st.metric("Customers", "10")
    st.metric("Alerts", "6")

st.markdown("---")
st.markdown("### Test AI Connection")

if st.button("Test API"):
    if api_key:
        st.info("Testing API connection...")
        try:
            import httpx
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            payload = {
                "model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Say hello in 3 words"}],
            }
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(f"{base_url}/v1/messages", json=payload, headers=headers)
                if resp.status_code == 200:
                    st.success("✅ API Connection Working!")
                    st.json(resp.json())
                else:
                    st.error(f"❌ API Error: {resp.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("API key not configured")

st.markdown("---")
st.markdown("**Aurora AI Operating System v1.0** | Built for Aurora Office Furniture")
