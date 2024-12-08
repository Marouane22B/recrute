from database.connection import get_snowflake_connection
from shemas.auth import *
from utils.class_object import singleton
from werkzeug.security import generate_password_hash,check_password_hash




@singleton
class AuthController:
    def __init__(self) -> None:
        pass
    from werkzeug.security import generate_password_hash

    async def sign_up(self, params: SignUpParams):
        connection = get_snowflake_connection()
        try:
            cursor = connection.cursor()

            # Requête SQL pour insérer un nouvel utilisateur
            query = """
                INSERT INTO Users (name, email, password_hash, role)
                VALUES (%s, %s, %s, 'condidat')
            """

            # Préparation des paramètres
            name = params.name
            email = params.email
            password_hash = generate_password_hash(params.password)  # Hachage sécurisé du mot de passe

            # Vérifiez les valeurs
            print("Executing SQL query:", query)
            print("With parameters:", (name, email, password_hash))

            # Exécutez la requête
            cursor.execute(query, (name, email, password_hash))
            connection.commit()  # Validez les modifications

            print("User successfully inserted into Snowflake.")

            # Récupérer l'identifiant de l'utilisateur inséré (si supporté par Snowflake)
            # Note : Snowflake ne retourne pas `inserted_id` comme certaines bases de données
            inserted_id_query = "SELECT MAX(USER_ID) FROM Users WHERE email = %s"
            cursor.execute(inserted_id_query, (email,))
            inserted_id = cursor.fetchone()[0]

            # Retournez un message de confirmation
            return {
                "id": inserted_id,
                "name": params.name,
                "email": params.email,
                "password": "",
                "role": "condidat",
                "plan": 0
            }

        except Exception as e:
            print(f"Erreur lors de l'insertion dans Snowflake : {e}")
            raise e

        finally:
            cursor.close()
            connection.close()

            
            
        
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
                    "role": result[4],
                    "plan": result[8]
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
        
    async def update_user_plan(self, user_id: int, new_plan: int):
        """
        Met à jour le plan d'un utilisateur dans la table Users de Snowflake.

        Args:
            user_id (int): L'identifiant de l'utilisateur dont le plan doit être mis à jour.
            new_plan (int): La nouvelle valeur du plan.

        Returns:
            dict: Détails de l'utilisateur après la mise à jour ou un message d'erreur.
        """
        conn = get_snowflake_connection()
        try:
            cursor = conn.cursor()

            # 1️⃣ Requête pour mettre à jour le plan de l'utilisateur
            update_query = """
                UPDATE Users
                SET plan = %s
                WHERE user_id = %s;
            """
            
            # Affiche la requête et les paramètres
            print("Executing SQL query:", update_query)
            print("With parameters:", (new_plan, user_id))
            
            # Exécuter la requête d'UPDATE
            cursor.execute(update_query, [new_plan, user_id])

            # 2️⃣ Requête pour récupérer l'utilisateur mis à jour
            select_query = """
                SELECT user_id, name, email, plan 
                FROM Users 
                WHERE user_id = %s;
            """
            
            print("Executing SQL query:", select_query)
            print("With parameters:", (user_id,))
            
            # Exécute la requête SELECT
            cursor.execute(select_query, [user_id])
            result = cursor.fetchone()

            if result:
                print("User's plan updated successfully.")
                return {
                    "id": result[0],
                    "name": result[1],
                    "email": result[2],
                    "plan": result[3]
                }
            else:
                print("User not found or no rows updated in Snowflake.")
                return {"status": "error", "message": "User not found or no changes made."}

        except Exception as e:
            print(f"Erreur lors de la mise à jour du plan de l'utilisateur dans Snowflake : {e}")
            raise e

        finally:
            cursor.close()
            conn.close()
