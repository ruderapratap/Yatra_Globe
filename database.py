import mysql.connector
from mysql.connector import Error
import streamlit as st
import hashlib

# ─────────────────────────────────────────────
#  DB CONFIG  –  apne MySQL credentials yahan
# ─────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # ← apna MySQL username
    "password": "Rudera@123",  # ← apna MySQL password
    "database": "yatraglobe",
    "port": 3306,
}


def get_connection():
    """Return a fresh MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None


def execute_query(query: str, params=None, fetch: bool = False):
    """
    Run a query.
    fetch=True  → return list of dicts
    fetch=False → commit and return lastrowid
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.lastrowid
    except Error as e:
        st.error(f"❌ Query Error: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_owner_login(username: str, password: str) -> bool:
    hashed = hash_password(password)
    rows = execute_query(
        "SELECT id FROM owner WHERE username=%s AND password_hash=%s",
        (username, hashed),
        fetch=True,
    )
    return bool(rows)


# ── Cities ────────────────────────────────────

def get_cities():
    return execute_query(
        "SELECT id, city_name FROM cities WHERE is_active=1 ORDER BY city_name",
        fetch=True,
    ) or []


def add_city(city_name: str):
    execute_query("INSERT INTO cities (city_name) VALUES (%s)", (city_name,))


def toggle_city(city_id: int, status: int):
    execute_query("UPDATE cities SET is_active=%s WHERE id=%s", (status, city_id))


# ── Destinations ──────────────────────────────

def get_destinations():
    return execute_query(
        "SELECT id, destination_name, description FROM destinations WHERE is_active=1 ORDER BY destination_name",
        fetch=True,
    ) or []


def add_destination(name: str, description: str):
    execute_query(
        "INSERT INTO destinations (destination_name, description) VALUES (%s, %s)",
        (name, description),
    )


def toggle_destination(dest_id: int, status: int):
    execute_query(
        "UPDATE destinations SET is_active=%s WHERE id=%s", (status, dest_id)
    )


# ── Bus Schedules ─────────────────────────────

def get_all_schedules():
    return execute_query(
        """
        SELECT bs.id, c.city_name AS from_city, d.destination_name AS to_destination,
               bs.departure_time, bs.arrival_time, bs.bus_type, bs.price, bs.is_active
        FROM bus_schedules bs
        JOIN cities c ON bs.from_city_id = c.id
        JOIN destinations d ON bs.to_destination_id = d.id
        ORDER BY c.city_name, d.destination_name, bs.departure_time
        """,
        fetch=True,
    ) or []


def get_schedules_for_route(from_city: str, to_dest: str):
    return execute_query(
        """
        SELECT bs.id, bs.departure_time, bs.arrival_time, bs.bus_type, bs.price
        FROM bus_schedules bs
        JOIN cities c ON bs.from_city_id = c.id
        JOIN destinations d ON bs.to_destination_id = d.id
        WHERE c.city_name=%s AND d.destination_name=%s AND bs.is_active=1
        ORDER BY bs.departure_time
        """,
        (from_city, to_dest),
        fetch=True,
    ) or []


def add_schedule(from_city_id, to_dest_id, dep_time, arr_time, bus_type, price):
    execute_query(
        """
        INSERT INTO bus_schedules
            (from_city_id, to_destination_id, departure_time, arrival_time, bus_type, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (from_city_id, to_dest_id, dep_time, arr_time, bus_type, price),
    )


def update_schedule_price(schedule_id: int, new_price: float):
    execute_query(
        "UPDATE bus_schedules SET price=%s WHERE id=%s", (new_price, schedule_id)
    )


def toggle_schedule(schedule_id: int, status: int):
    execute_query(
        "UPDATE bus_schedules SET is_active=%s WHERE id=%s", (status, schedule_id)
    )


# ── Food Pricing ──────────────────────────────

def get_food_pricing():
    return execute_query(
        "SELECT * FROM food_pricing WHERE is_active=1",
        fetch=True,
    ) or []


def get_food_price(food_type: str, meal_type: str) -> float:
    rows = execute_query(
        "SELECT price FROM food_pricing WHERE food_type=%s AND meal_type=%s AND is_active=1",
        (food_type, meal_type),
        fetch=True,
    )
    return float(rows[0]["price"]) if rows else 0.0


def update_food_price(food_id: int, new_price: float):
    execute_query(
        "UPDATE food_pricing SET price=%s WHERE id=%s", (new_price, food_id)
    )


# ── Hotel Pricing ─────────────────────────────

def get_hotel_pricing():
    return execute_query(
        "SELECT * FROM hotel_pricing WHERE is_active=1",
        fetch=True,
    ) or []


def get_hotel_price(category: str) -> float:
    rows = execute_query(
        "SELECT price_per_night FROM hotel_pricing WHERE hotel_category=%s AND is_active=1",
        (category,),
        fetch=True,
    )
    return float(rows[0]["price_per_night"]) if rows else 0.0


def update_hotel_price(hotel_id: int, new_price: float):
    execute_query(
        "UPDATE hotel_pricing SET price_per_night=%s WHERE id=%s",
        (new_price, hotel_id),
    )


# ── Bookings ──────────────────────────────────

def create_booking(data: dict):
    import random, string
    booking_id = "YG" + "".join(random.choices(string.digits, k=8))
    execute_query(
        """
        INSERT INTO bookings
            (booking_id, tourist_name, tourist_age, tourist_address, tourist_phone,
             tourist_email, num_tickets, pickup_city, destination, travel_date,
             bus_type, bus_schedule_id, food_preference, breakfast, lunch, dinner,
             hotel_category, num_hotel_nights, base_ticket_price, food_total,
             hotel_total, total_amount)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            booking_id,
            data["name"], data["age"], data["address"],
            data["phone"], data["email"], data["num_tickets"],
            data["pickup_city"], data["destination"], data["travel_date"],
            data["bus_type"], data.get("schedule_id"),
            data["food_preference"],
            int(data["breakfast"]), int(data["lunch"]), int(data["dinner"]),
            data["hotel_category"], data["num_hotel_nights"],
            data["base_ticket_price"], data["food_total"],
            data["hotel_total"], data["total_amount"],
        ),
    )
    return booking_id


def get_all_bookings():
    return execute_query(
        "SELECT * FROM bookings ORDER BY booking_date DESC",
        fetch=True,
    ) or []


def get_booking_by_id(booking_id: str):
    rows = execute_query(
        "SELECT * FROM bookings WHERE booking_id=%s", (booking_id,), fetch=True
    )
    return rows[0] if rows else None


def update_booking_status(booking_id: str, status: str):
    execute_query(
        "UPDATE bookings SET booking_status=%s WHERE booking_id=%s",
        (status, booking_id),
    )


def change_owner_password(username: str, new_password: str):
    hashed = hash_password(new_password)
    execute_query(
        "UPDATE owner SET password_hash=%s WHERE username=%s",
        (hashed, username),
    )
