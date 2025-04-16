# Trigger update from Notepad final cleanup

import streamlit as st
import yaml
import pandas as pd
import os
import traceback
import streamlit_authenticator as stauth

# Load credentials safely
if not os.path.exists("auth_config.yaml"):
    st.error("🚨 auth_config.yaml not found in the current working directory.")
    st.stop()

with open("auth_config.yaml") as file:
    config = yaml.safe_load(file)

# Initialize authenticator
try:
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
except Exception:
    st.error("🚨 Failed to initialize authenticator.")
    st.stop()

# Render login interface
st.header("🔐 Please Log In to Continue")

try:
    authenticator.login(location="main")

    if authenticator.authentication_status is None:
        st.stop()

except Exception as e:
    st.error("🚨 Login process failed.")
    st.text(traceback.format_exc())
    st.stop()

# Post-login dashboard
if authenticator.authentication_status:
    st.set_page_config(page_title="KSV Strategy Dashboard", layout="wide")
    st.title("📊 Visage Strategy Dashboard")
    st.success(f"Welcome back, {authenticator.name}!")

    authenticator.logout("Logout", "sidebar")

    file_path = "ksv_strategy_results.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df)

        st.subheader("Strategy Overview")
        st.line_chart(df.set_index("date")["strategy_returns"])
    else:
        st.warning("Strategy results file not found. Please push results from model first.")

elif authenticator.authentication_status is False:
    st.error("❌ Incorrect username or password")


