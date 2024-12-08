from database.connection import get_snowflake_connection
from shemas.auth import *
from utils.class_object import singleton

@singleton
class AuthController:
    def __init__(self) -> None:
        pass

    async def sign_up(self, params: SignUpParams):
        pass
        
        
    
    async def sign_in(self, params: SignInParams):
        conn = get_snowflake_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT * FROM Users WHERE email = %s
            """
            # Vérifiez les valeurs
            print("Executing SQL query:", query)
            print("With parameters:", (params.email,))

            # Exécutez la requête
            cursor.execute(query, [params.email])
            result = cursor.fetchone()
            if result:
                print("User found in Snowflake.")
                return {
                    "id": result[0],
                    "name": result[1],
                    "email": result[2],
                    "password": result[3],
                    "role": result[4]
                }
            else:
                print("User not found in Snowflake.")
                return None
        except Exception as e:
            print(f"Erreur lors de la recherche dans Snowflake : {e}")
            raise e
        finally:
            cursor.close()
            conn.close()
        
        
