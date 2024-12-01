from .connection import get_snowflake_connection

def insert_user(name: str, email: str, password_hash: str, role: str = "candidat"):
    connection = get_snowflake_connection()
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO Users (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """
        # Vérifiez les valeurs
        print("Executing SQL query:", query)
        print("With parameters:", (name, email, password_hash, role))
        
        # Exécutez la requête
        cursor.execute(query, [name, email, password_hash, role])
        connection.commit()  # Validez les modifications
        print("User successfully inserted into Snowflake.")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans Snowflake : {e}")
        raise e
    finally:
        cursor.close()
        connection.close()
