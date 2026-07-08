import streamlit as st

st.set_page_config(page_title="Aurora AI Test", page_icon="🏢", layout="wide")

st.title("🏢 Aurora AI Operating System")
st.success("✅ App is loading correctly!")

st.markdown("### Test Status")
st.write("If you can see this, Streamlit is working on HuggingFace Spaces.")

import os
api_key = os.environ.get("ANTHROPIC_API_KEY", "NOT SET")
base_url = os.environ.get("ANTHROPIC_BASE_URL", "NOT SET")

st.markdown("### Environment Variables")
st.write(f"API Key: {'✅ Set' if api_key != 'NOT SET' else '❌ Not Set'}")
st.write(f"Base URL: {base_url}")
