import streamlit as st
import database as d

def render_login():
    """Render authentication and return the authenticated user's ID."""
    st.title("Welcome to Document Assistant")
    st.caption("Sign in to access your documents and conversation history.")

    sign_in, register = st.tabs(["Log in", "Create account"])
    with sign_in:
        adhar_card_no = st.number_input("Aadhaar card number", min_value=1, step=1, key="login_adhar")
        email = st.text_input("Email", key="login_email")
        if st.button("Log in", type="primary", key="login_submit"):
            if d.authenticate(adhar_card_no, email.strip()):
                st.session_state["current_user"] = int(adhar_card_no)
                st.rerun()
            st.error("Aadhaar card number and email do not match.")

    with register:
        with st.form("register_form"):
            adhar_card_no = st.number_input("Aadhaar card number", min_value=1, step=1, key="register_adhar")
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
            email = st.text_input("Email", key="register_email")
            phno = st.text_input("Phone number")
            submitted = st.form_submit_button("Create account", type="primary")
        if submitted:
            try:
                d.create_user(
                    adhar_card_no,
                    name.strip(),
                    age,
                    email.strip(),
                    phno.strip(),
                )
                st.session_state["current_user"] = int(adhar_card_no)
                st.rerun()
            except Exception as exc:
                d.conn.rollback()
                st.error(f"Could not create account: {exc}")

    return st.session_state.get("current_user")



