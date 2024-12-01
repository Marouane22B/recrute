from .connection import get_snowflake_connection

def insert_user(name: str, email: str, password_hash: str):
    connection = get_snowflake_connection()
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO Users (name, email, password_hash)
            VALUES (?, ?, ?)
        """
        cursor.execute(query, (name, email, password_hash))
        connection.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion de l'utilisateur : {e}")
        raise e
    finally:
        cursor.close()
        connection.close()
