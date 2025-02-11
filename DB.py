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


def get_count_level(email: str) -> int :
    db = supabase.create_client(url, key)
    response = db.table("users").select("countLevel").eq('email', email).execute() 
    return response.data[0]['countLevel']


def update_count_level(email: str) -> None:
    db = supabase.create_client(url, key)
    db.table("users").update({"countLevel": get_count_level(email) + 1}).eq('email', email).execute()


def get_count_coins(email: str) -> int:
    db = supabase.create_client(url, key)
    response = db.table("users").select("countCoin").eq('email', email).execute() 
    return response.data[0]['countCoin']


def update_count_coins(email: str, new_count_coins: int) -> None:
    db = supabase.create_client(url, key)
    db.table("users").update({"countCoin": new_count_coins}).eq('email', email).execute()
