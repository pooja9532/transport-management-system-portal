import sqlite3

def create_tables():
    conn = sqlite3.connect("transport.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT,
            route_number TEXT,
            start_point TEXT,
            end_point TEXT,
            total_stops INTEGER,
            bus_number TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            roll_number TEXT,
            department TEXT,
            year TEXT,
            route TEXT,
            bus_number TEXT,
            pickup_stop TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_name TEXT,
            license_number TEXT,
            contact TEXT,
            assigned_route TEXT,
            experience TEXT,
            status TEXT DEFAULT 'On Duty'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            roll_number TEXT,
            semester TEXT,
            amount_due REAL,
            amount_paid REAL,
            payment_date TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route TEXT,
            bus_number TEXT,
            pickup_start TEXT,
            pickup_end TEXT,
            drop_start TEXT,
            drop_end TEXT,
            status TEXT DEFAULT 'On Time'
        )
    """)

    conn.commit()
    conn.close()
    print("All tables created")