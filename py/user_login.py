import streamlit as st

# Demo in-memory user storage
if "user_db" not in st.session_state:
    st.session_state["user_db"] = {"admin": "admin123"}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login_page():
    st.title("🔐 Login or Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username in st.session_state["user_db"] and st.session_state["user_db"][username] == password:
                st.session_state["authenticated"] = True
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username", key="new_user")
        new_pass = st.text_input("New Password", type="password", key="new_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
        if st.button("Register"):
            if new_user in st.session_state["user_db"]:
                st.warning("Username already exists.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif new_user == "" or new_pass == "":
                st.warning("Username and password cannot be empty.")
            else:
                st.session_state["user_db"][new_user] = new_pass
                st.success("Registration successful! You can now log in.")

if not st.session_state["authenticated"]:
    login_page()
else:
    st.success("✅ Logged in")
    st.write("You now have access to the report generator features.")
    # You can call your report generator function here.
