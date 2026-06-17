from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database Table
def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_table()


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        # Health Prediction Logic

        if float(glucose) > 140:
            remarks = "High Diabetes Risk"

        elif float(cholesterol) > 200:
            remarks = "High Cholesterol Risk"

        elif float(haemoglobin) < 12:
            remarks = "Low Haemoglobin"

        else:
            remarks = "Normal"

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO patients
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks))

        conn.commit()
        conn.close()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return render_template('index.html', patients=patients)


@app.route('/delete/<int:id>')
def delete_patient(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)