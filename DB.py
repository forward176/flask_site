import supabase
from our_secrets import url, key


def create_user(email: str, password: str) -> None:
    db = supabase.create_client(url, key)
    response = (
        db.table("users")
        .insert({ "email": email, "password": password})
        .execute()
    )


def is_user_exist(email: str):
    db = supabase.create_client(url, key)
    response = db.table("users").select("*").eq('email', email).execute()    
    return bool(response.data)


def check_password(email: str, password: str) -> bool:
    db = supabase.create_client(url, key)
    response = db.table("users").select("password").eq('email', email).execute()  
    return response.data[0]['password'] == password
