from src.db_connection import get_db_connection

class Rewards:
    """
    Rewards: Handles rewards-related operations and database interactions
    """
    @staticmethod
    def get_all_rewards():
        """Get all available rewards"""
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM rewards")
                return cursor.fetchall()
        except Exception as e:
            print("Error fetching rewards:", e)
            return []
        finally:
            conn.close()
    
    @staticmethod
    def redeem_reward(user_id, reward_id, points_required):
        """Redeem a reward and deduct points"""
        try:
            conn = get_db_connection()
            if not conn:
                return False
                
            with conn.cursor() as cursor:
                cursor.execute("SELECT name FROM rewards WHERE reward_id = %s", (reward_id,))
                reward = cursor.fetchone()
                if not reward:
                    return False
                
                insert_query = """
                INSERT INTO points (user_id, event_id, reason, points_change, transaction_date)
                VALUES (%s, NULL, %s, %s, NOW())
                """
                cursor.execute(insert_query, (
                    user_id,
                    f"Redeemed: {reward['name']}", 
                    -points_required
                ))
                conn.commit()
                return True
        except Exception as e:
            print("Database error:", e)
            return False
        finally:
            conn.close()
