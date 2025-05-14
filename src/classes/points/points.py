from src.db_connection import get_db_connection

class Points:
    """
    Points: Handles points-related operations and database interactions
    """
    @staticmethod
    def get_user_points(user_id):
        """Get total points for a user"""
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COALESCE(SUM(points_change), 0) AS total FROM points WHERE user_id = %s",
                    (user_id,)
                )
                result = cursor.fetchone()
                return result["total"] if result else 0
        except Exception as e:
            print("Error fetching user points:", e)
            return 0
        finally:
            conn.close()

    @staticmethod
    def get_points_history(user_id):
        """Get points transaction history for a user"""
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                query = """
                SELECT 
                    p.points_change, 
                    p.reason, 
                    p.transaction_date, 
                    COALESCE(e.title, 'System Award') AS event_name
                FROM 
                    points p
                LEFT JOIN 
                    events e ON p.event_id = e.event_id
                WHERE 
                    p.user_id = %s
                ORDER BY 
                    p.transaction_date DESC
                """
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
        except Exception as e:
            print("Database error:", e)
            return []
        finally:
            conn.close()
