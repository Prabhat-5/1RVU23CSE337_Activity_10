# -*- coding: utf-8 -*-
"""
Created on Sun May  5 17:08:50 2024

@author: Prabhat
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May  5 16:57:06 2024

@author: Prabhat
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = sqlite3.connect('tickets.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    passenger_name TEXT,
    destination TEXT,
    ticket_price REAL,
    seat_number INTEGER)''')
conn.commit()

@app.route('/')
def index():
    return render_template('1RVU23CSE337_Activity_10.html')

@app.route('/reserve_ticket', methods=['POST'])
def reserve_ticket():
    if request.method == 'POST':
        passenger_name = request.form['name']
        destination = request.form['destination']
        ticket_price = request.form['price']
        seat_number = request.form['seat_number']
        cursor.execute("INSERT INTO tickets (passenger_name, destination, ticket_price, seat_number) VALUES (?, ?, ?, ?)",
                       (passenger_name, destination, ticket_price, seat_number))
        conn.commit()
        flash('Ticket reserved successfully!', 'success')
        return redirect(url_for('index'))

@app.route('/cancel_ticket', methods=['POST'])
def cancel_ticket():
    if request.method == 'POST':
        passenger_name = request.form['name']
        cursor.execute("DELETE FROM tickets WHERE passenger_name=?", (passenger_name,))
        conn.commit()
        flash('Ticket canceled successfully!', 'success')
        return redirect(url_for('index'))

@app.route('/search_tickets', methods=['POST'])
def search_tickets():
    if request.method == 'POST':
        search_term = request.form['search']
        cursor.execute("SELECT * FROM tickets WHERE passenger_name LIKE ?", ('%' + search_term + '%',))
        tickets = cursor.fetchall()
        if tickets:
            return render_template('1RVU23CSE337_Activity_10.html', tickets=tickets)
        else:
            flash('No reservations found.', 'warning')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
