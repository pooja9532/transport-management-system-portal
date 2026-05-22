from flask import Flask, request, jsonify, render_template
import sqlite3
import csv
import io
from database import create_tables

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("transport.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/routes", methods=["GET"])
def get_routes():
    conn = get_db()
    rows = conn.execute("SELECT * FROM routes").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/routes", methods=["POST"])
def add_route():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO routes (route_name, route_number, start_point, end_point, total_stops, bus_number, status) VALUES (?,?,?,?,?,?,?)",
        (d["route_name"], d["route_number"], d["start_point"], d["end_point"], d["total_stops"], d["bus_number"], d["status"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Route added"})

@app.route("/api/routes/<int:id>", methods=["PUT"])
def update_route(id):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE routes SET route_name=?, route_number=?, start_point=?, end_point=?, total_stops=?, bus_number=?, status=? WHERE id=?",
        (d["route_name"], d["route_number"], d["start_point"], d["end_point"], d["total_stops"], d["bus_number"], d["status"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Route updated"})

@app.route("/api/routes/<int:id>", methods=["DELETE"])
def delete_route(id):
    conn = get_db()
    conn.execute("DELETE FROM routes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Route deleted"})

@app.route("/api/students", methods=["GET"])
def get_students():
    conn = get_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/students", methods=["POST"])
def add_student():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO students (student_name, roll_number, department, year, route, bus_number, pickup_stop, status) VALUES (?,?,?,?,?,?,?,?)",
        (d["student_name"], d["roll_number"], d["department"], d["year"], d["route"], d["bus_number"], d["pickup_stop"], d["status"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added"})

@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE students SET student_name=?, roll_number=?, department=?, year=?, route=?, bus_number=?, pickup_stop=?, status=? WHERE id=?",
        (d["student_name"], d["roll_number"], d["department"], d["year"], d["route"], d["bus_number"], d["pickup_stop"], d["status"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})

@app.route("/api/drivers", methods=["GET"])
def get_drivers():
    conn = get_db()
    rows = conn.execute("SELECT * FROM drivers").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/drivers", methods=["POST"])
def add_driver():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO drivers (driver_name, license_number, contact, assigned_route, experience, status) VALUES (?,?,?,?,?,?)",
        (d["driver_name"], d["license_number"], d["contact"], d["assigned_route"], d["experience"], d["status"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Driver added"})

@app.route("/api/drivers/<int:id>", methods=["PUT"])
def update_driver(id):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE drivers SET driver_name=?, license_number=?, contact=?, assigned_route=?, experience=?, status=? WHERE id=?",
        (d["driver_name"], d["license_number"], d["contact"], d["assigned_route"], d["experience"], d["status"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Driver updated"})

@app.route("/api/drivers/<int:id>", methods=["DELETE"])
def delete_driver(id):
    conn = get_db()
    conn.execute("DELETE FROM drivers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Driver deleted"})

@app.route("/api/fees", methods=["GET"])
def get_fees():
    conn = get_db()
    rows = conn.execute("SELECT * FROM fees").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/fees", methods=["POST"])
def add_fee():
    d = request.json
    due  = float(d.get("amount_due", 0))
    paid = float(d.get("amount_paid", 0))
    status = "Paid" if paid >= due else ("Partial" if paid > 0 else "Pending")
    conn = get_db()
    conn.execute("INSERT INTO fees (student_name, roll_number, semester, amount_due, amount_paid, payment_date, status) VALUES (?,?,?,?,?,?,?)",
        (d["student_name"], d["roll_number"], d["semester"], due, paid, d.get("payment_date", "-"), status))
    conn.commit()
    conn.close()
    return jsonify({"message": "Fee added"})

@app.route("/api/fees/<int:id>", methods=["PUT"])
def update_fee(id):
    d = request.json
    due  = float(d.get("amount_due", 0))
    paid = float(d.get("amount_paid", 0))
    status = "Paid" if paid >= due else ("Partial" if paid > 0 else "Pending")
    conn = get_db()
    conn.execute("UPDATE fees SET student_name=?, roll_number=?, semester=?, amount_due=?, amount_paid=?, payment_date=?, status=? WHERE id=?",
        (d["student_name"], d["roll_number"], d["semester"], due, paid, d.get("payment_date", "-"), status, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Fee updated"})

@app.route("/api/fees/<int:id>", methods=["DELETE"])
def delete_fee(id):
    conn = get_db()
    conn.execute("DELETE FROM fees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Fee deleted"})

@app.route("/api/schedules", methods=["GET"])
def get_schedules():
    conn = get_db()
    rows = conn.execute("SELECT * FROM schedules").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/schedules", methods=["POST"])
def add_schedule():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO schedules (route, bus_number, pickup_start, pickup_end, drop_start, drop_end, status) VALUES (?,?,?,?,?,?,?)",
        (d["route"], d["bus_number"], d["pickup_start"], d["pickup_end"], d["drop_start"], d["drop_end"], d["status"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Schedule added"})

@app.route("/api/schedules/<int:id>", methods=["PUT"])
def update_schedule(id):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE schedules SET route=?, bus_number=?, pickup_start=?, pickup_end=?, drop_start=?, drop_end=?, status=? WHERE id=?",
        (d["route"], d["bus_number"], d["pickup_start"], d["pickup_end"], d["drop_start"], d["drop_end"], d["status"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Schedule updated"})

@app.route("/api/schedules/<int:id>", methods=["DELETE"])
def delete_schedule(id):
    conn = get_db()
    conn.execute("DELETE FROM schedules WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Schedule deleted"})

@app.route("/api/upload", methods=["POST"])
def upload_csv():
    table   = request.form.get("table")
    file    = request.files.get("file")
    content = file.read().decode("utf-8")
    reader  = csv.DictReader(io.StringIO(content))
    rows    = list(reader)
    conn    = get_db()
    count   = 0

    for row in rows:
        row = {k.strip().lower().replace(" ", "_"): v.strip() for k, v in row.items()}
        try:
            if table == "students":
                conn.execute("INSERT INTO students (student_name, roll_number, department, year, route, bus_number, pickup_stop, status) VALUES (?,?,?,?,?,?,?,?)",
                    (row.get("student_name",""), row.get("roll_number",""), row.get("department",""), row.get("year",""), row.get("route",""), row.get("bus_number",""), row.get("pickup_stop",""), row.get("status","Active")))
            elif table == "routes":
                conn.execute("INSERT INTO routes (route_name, route_number, start_point, end_point, total_stops, bus_number, status) VALUES (?,?,?,?,?,?,?)",
                    (row.get("route_name",""), row.get("route_number",""), row.get("start_point",""), row.get("end_point",""), int(row.get("total_stops",0) or 0), row.get("bus_number",""), row.get("status","Active")))
            elif table == "drivers":
                conn.execute("INSERT INTO drivers (driver_name, license_number, contact, assigned_route, experience, status) VALUES (?,?,?,?,?,?)",
                    (row.get("driver_name",""), row.get("license_number",""), row.get("contact",""), row.get("assigned_route",""), row.get("experience",""), row.get("status","On Duty")))
            elif table == "fees":
                due  = float(row.get("amount_due", 0) or 0)
                paid = float(row.get("amount_paid", 0) or 0)
                status = "Paid" if paid >= due else ("Partial" if paid > 0 else "Pending")
                conn.execute("INSERT INTO fees (student_name, roll_number, semester, amount_due, amount_paid, payment_date, status) VALUES (?,?,?,?,?,?,?)",
                    (row.get("student_name",""), row.get("roll_number",""), row.get("semester",""), due, paid, row.get("payment_date","-"), status))
            elif table == "schedules":
                conn.execute("INSERT INTO schedules (route, bus_number, pickup_start, pickup_end, drop_start, drop_end, status) VALUES (?,?,?,?,?,?,?)",
                    (row.get("route",""), row.get("bus_number",""), row.get("pickup_start",""), row.get("pickup_end",""), row.get("drop_start",""), row.get("drop_end",""), row.get("status","On Time")))
            count += 1
        except Exception as e:
            print("Skipped row:", e)

    conn.commit()
    conn.close()
    return jsonify({"message": f"{count} records imported into {table}"})

if __name__ == "__main__":
    create_tables()
    print("Server running at http://localhost:5000")
    app.run(debug=True)



    