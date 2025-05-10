from flask import Flask, render_template, redirect, request, send_from_directory
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'rijumonroy@gmail.com' 
app.config['MAIL_PASSWORD'] = 'xpmgxdennrfljaie'  # Make sure this is an App Password

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/view_resume")
def view_resume():
    return send_from_directory(directory="static/images", path="Rijumon Roy resume .pdf")

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Store to SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contact (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        subject TEXT,
                        message TEXT NOT NULL)''')
    cursor.execute("INSERT INTO contact (name, email, subject, message) VALUES (?, ?, ?, ?)",
                   (name, email, subject, message))
    conn.commit()
    conn.close()

    # Try sending email
    try:
        msg = Message(subject=f"New Contact Form Submission: {subject}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['rijumonroy@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        mail.send(msg)
    except Exception as e:
        print("Email sending failed:", e)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
