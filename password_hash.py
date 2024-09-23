import streamlit_authenticator as stauth

password = input("Input Password: ")

hashed_passwords = stauth.Hasher(["password"]).generate()
print(hashed_passwords)