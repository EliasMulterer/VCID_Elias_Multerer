import os
import pymysql
import io
import csv
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session, Response, send_file

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Alle Funktionen bezüglich der Datenbank sind in der Datei "db.py" enthalten.
from db import getTable, addItem, editItem, deleteItem, createUser, getUserFromUsername, checkUser

# Index/Home Page/Add Item:
@app.route('/', methods = ['GET', 'POST'])
def index():
    if session.get('loggedin') is None or False or session.get('username') is None:
        flash("Bitte zuerst Anmelden.") # Den Benutzer zur Anmeldung auffordern.
        return redirect(url_for('login'))

    table = getTable()
    if table['Code'] == 200:
        tableResults = table['Results']
    else:
        flash(table['Error']) # Fehlermeldung anzeigen
        tableResults = []

    if request.method == "POST":
        inventoryNum = request.form.get('inventoryNum')
        hostName = request.form.get('hostName')
        deviceName = request.form.get('device')
        serial = request.form.get('serialNum')
        date = request.form.get('date')
        mac = request.form.get('macAddress')
        if not inventoryNum or not hostName or not deviceName or not serial or not date or not mac:
            flash('Bitte alle Felder ausfüllen.') # Benutzer auffordern, alle Felder auszufüllen.
            return render_template('index.html', Table = tableResults, current_username = session.get('username'), inventoryNum=inventoryNum, hostName=hostName, deviceName=deviceName, serial=serial, date=date, mac=mac)
        
        # Eintragen der Daten in die Datenbank:
        response = addItem(inventoryNum, hostName, deviceName, serial, date, mac)

        if response == 200:
            flash("Daten erfolgreich eingegeben.", "success") # Erfolgsmeldung anzeigen
            return redirect(url_for('index'))
        elif "Duplicate entry" in response:
            flash("Fehler: Inventarnummer bereits vorhanden. Bitte nochmals versuchen.") # Fehlermeldung anzeigen
            return render_template('index.html', Table = tableResults, current_username = session.get('username'), inventoryNum=inventoryNum, hostName=hostName, deviceName=deviceName, serial=serial, date=date, mac=mac)
        else:
            flash(response) # Fehlermeldung anzeigen
            return render_template('index.html', Table = tableResults, current_username = session.get('username'), inventoryNum=inventoryNum, hostName=hostName, deviceName=deviceName, serial=serial, date=date, mac=mac)

    return render_template('index.html', Table = tableResults, current_username = session.get('username'))


# Edit Page:
@app.route('/edit/<int:num>', methods=['GET', 'POST'])
def edit(num):
    if session.get('loggedin') is None or False or session.get('username') is None:
        return redirect(url_for('login'))

    table = getTable()
    if table['Code'] == 200:
        tableResults = table['Results']
    else:
        flash(table['Error']) # Fehlermeldung anzeigen
        tableResults = []

    if request.method == 'POST':
        hostName = request.form.get('hostName')
        deviceName = request.form.get('device')
        serial = request.form.get('serialNum')
        date = request.form.get('date')
        mac = request.form.get('macAddress')
        
        response = editItem(num, hostName, deviceName, serial, date, mac)
        if response == 200:
            flash("Eintrag erfolgreich angepasst.", "success") # Erfolgsmeldung anzeigen
            return redirect(url_for('index'))
        else:
            flash(response) # Fehlermeldung anzeigen
            return render_template('edit.html', Table = tableResults)
    
    return render_template('edit.html', Table = tableResults, itemToEdit = num)


# Route to delete an item:
@app.route('/delete/<int:num>')
def delete(num):
    response = deleteItem(num)

    if response == 200:
        flash("Eintrag erfolgreich gelöscht.", "success")
    else:
        flash(response)

    return redirect(url_for('index'))

#CSV Export
@app.route('/export', methods=['GET'])
def export():
    if session.get('loggedin') is None or session.get('username') is None:
        flash("Bitte zuerst Anmelden.")
        return redirect(url_for('login'))

    table = getTable()
    if table['Code'] != 200:
        flash(table['Error'])
        return redirect(url_for('index'))

    tableResults = table['Results']

    # Erstellen eines StringIO-Objekts im Speicher
    output = io.StringIO()
    writer = csv.writer(output)

    # Schreiben der Spaltenüberschriften, basierend auf den Schlüsseln des ersten Eintrags
    if tableResults:
        writer.writerow(tableResults[0].keys())
    # Schreiben der Datenzeilen
    for row in tableResults:
        writer.writerow(row.values())

    # Zurücksetzen des Cursors des StringIO-Objekts auf den Anfang
    output.seek(0)

    # Erstellen und Senden der Antwort
    return Response(
        output.getvalue(), 
        mimetype="text/csv", 
        headers={"Content-disposition": "attachment; filename=export.csv"})


# Login Page:
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('loggedin') is True:
        flash("Sie sind bereits angemeldet.")
        return redirect(url_for('index'))
    
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Bitte alle Felder ausfüllen.") # Benutzer auffordern, alle Felder auszufüllen.
            return render_template('login.html', username=username, password=password)

        response = checkUser(username, password)
        if response == 404:
            flash('User oder Passwort nicht korrekt. Bitte erneut versuchen.') # Fehlermeldung anzeigen
        else:
            try:
                session['loggedin'] = True
                session['username'] = response['Username']
                return redirect(url_for('index'))
            except:
                flash(f'Da ist leider etwas schief gelaufen. Bitte erneut versuchen. {response}') # Fehlermeldung anzeigen

    return render_template('login.html')

# Signup Page:
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not username or not name or not email or not password1 or not password2:
            flash("Bitte alle Felder ausfüllen.") # Benutzer auffordern, alle Felder auszufüllen.
            return render_template('signup.html', username=username, name=name, email=email, password1=password1, password2=password2)

        if password1 != password2:
            flash("Passwörter stimmen nicht überein. Bitte erneut versuchen.") # Fehlermeldung anzeigen
            return render_template('signup.html', username=username, name=name, email=email, password1=password1, password2=password2)

        response = createUser(username, name, email, password1)
        if response == 200:
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('index'))
        elif "Duplicate entry" in response:
            flash('Ein Benutzer mit diesem Usernamen existiert bereits. Bitte einen anderen Usernamen nehmen.') # Fehlermeldung anzeigens
        else:
            flash(f'Da ist etwas scheif gelaufen. Bitte erneut versuchen. {response}') # Fehlermeldung anzeigen
        return render_template('signup.html', username=username, name=name, email=email, password1=password1, password2=password2)

    return render_template('signup.html')


# Route to Logout the User:
@app.route('/logout')
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)