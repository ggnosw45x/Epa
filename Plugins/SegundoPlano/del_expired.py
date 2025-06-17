from Plugins.Func import connect_to_db, db_lock
import threading
import time
from pyrogram import Client
from datetime import datetime

def calculate_remaining_days(fecha_registro, dias):
    current_time = datetime.now().timestamp()
    remaining_seconds = (fecha_registro + (dias * 24 * 60 * 60)) - current_time
    remaining_days = remaining_seconds / (24 * 60 * 60)
    return remaining_days

def update_expired_users():
    while True:
        with db_lock:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, rango, fecha_registro, dias FROM users")
            users_data = cursor.fetchall()

            for user_id, rango, fecha_registro, dias in users_data:
                if dias is None or fecha_registro is None:
                    continue

                dias = int(dias)
                fecha_registro = float(fecha_registro)
                remaining_days = calculate_remaining_days(fecha_registro, dias)

                if remaining_days <= 0:
                    cursor.execute("UPDATE users SET rango = ?, antispam = ?, dias = ? WHERE user_id = ?",
                                   ("Free", 60, 0, user_id))
                    conn.commit()
            conn.close()

        time.sleep(5)

thread_update = threading.Thread(target=update_expired_users)
thread_update.start()
