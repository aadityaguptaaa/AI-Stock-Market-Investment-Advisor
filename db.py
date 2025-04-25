import mysql.connector
from mysql.connector import Error
from datetime import datetime

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="**",#replace with your username
            password="**",#replace with your password
            database="stock_prediction"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def register_user(user_id, username, password, city, phone, address):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users_data (user_id, user_name, password, city, phone_no, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (user_id, username, password, city, phone, address))
            conn.commit()
            return True
        except Error as e:
            print(f"Error registering user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def login_user(username, password):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT user_id FROM users_data WHERE user_name=%s AND password=%s
            ''', (username, password))
            result = cursor.fetchone()
            return result['user_id'] if result else None
        except Error as e:
            print(f"Error logging in: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def save_single_prediction(user_id, stock_name, time_period, predicted_profit):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Convert None values to appropriate SQL NULL
            time_period = time_period if time_period is not None else 0
            predicted_profit = predicted_profit if predicted_profit is not None else 0
            
            cursor.execute('''
                INSERT INTO single_predictions 
                (user_id, stock_name, time_period, predicted_profit)
                VALUES (%s, %s, %s, %s)
            ''', (
                user_id,
                stock_name,
                int(time_period),
                float(predicted_profit)
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error saving single prediction: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def save_recommendation_prediction(user_id, stock_name, investment_amount, time_period, predicted_profit):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Convert None values to appropriate SQL NULL
            investment_amount = investment_amount if investment_amount is not None else 0
            time_period = time_period if time_period is not None else 0
            predicted_profit = predicted_profit if predicted_profit is not None else 0
            
            cursor.execute('''
                INSERT INTO recommendation_predictions 
                (user_id, stock_name, investment_amount, time_period, predicted_profit)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                user_id,
                stock_name,
                float(investment_amount),
                int(time_period),
                float(predicted_profit)
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error saving recommendation prediction: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_user_single_predictions(user_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT 
                    stock_name,
                    time_period,
                    predicted_profit,
                    timestamp as prediction_time
                FROM single_predictions 
                WHERE user_id=%s 
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (user_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching single predictions: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_user_recommendation_predictions(user_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT 
                    stock_name,
                    investment_amount as amount,
                    time_period,
                    predicted_profit,
                    timestamp as prediction_time
                FROM recommendation_predictions 
                WHERE user_id=%s 
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (user_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching recommendation predictions: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def get_user_predictions(user_id):
    """Get all predictions for a user (both single and recommendation)"""
    single_predictions = get_user_single_predictions(user_id)
    for pred in single_predictions:
        pred['prediction_type'] = 'single'
        pred['amount'] = None  # Single predictions don't have amount
    
    recommendation_predictions = get_user_recommendation_predictions(user_id)
    for pred in recommendation_predictions:
        pred['prediction_type'] = 'recommendation'
    
    # Combine and sort by timestamp (newest first)
    all_predictions = single_predictions + recommendation_predictions
    all_predictions.sort(key=lambda x: x['prediction_time'], reverse=True)
    
    return all_predictions
