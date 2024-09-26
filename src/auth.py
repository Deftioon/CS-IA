import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.switch_page_button import switch_page

def authenticate(yaml_path: str) -> None:

    # st.set_page_config(initial_sidebar_state="expanded")


    with open(f"{yaml_path}", "r") as file:
        config = yaml.load(file, Loader=SafeLoader)
        
    #stauth.Hasher.hash_passwords(config['credentials'])

    # link page to sidebar
    st.sidebar.page_link("pages/sidebar_test.py", label="Sidebar Test")

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login(key='Login', location='main')
    print(name, authentication_status, username)

    if authentication_status:   
        authenticator.logout('Logout', 'main')
        if name == 'deftioon':
            # st.switch_page("pages/admin.py")
            switch_page("admin")
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
