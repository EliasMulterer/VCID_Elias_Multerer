import pymysql

# Diese Details sind für die Verbindung zu der Datenbank. Bitte anpassen je nach bereitstellung der Datenbank
db_user = 'root'
db_password = ''
db_connection_name = 'praxisarbeit-vcid-multerer:europe-west1:vicd'
db_name = 'cmdb'


# Verbindung zur Cloud SQL-Instanz herstellen:
def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    connection = pymysql.connect(user=db_user,
                             password=db_password,
                             database=db_name,
                            # unix_socket=unix_socket,
                             host='130.211.95.210',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

# Funktion zum Abrufen von Daten aus der Tabelle:
def getTable():
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `cmdb`"
            cursor.execute(sql)
            results = cursor.fetchall()
            print(results)
            response = {
                'Code': 200,
                'Results': results,
                'Error': None
            }
    except pymysql.MySQLError as e:
        response = {
                'Code': 400,
                'Results': None,
                'Error': getattr(e, 'args', [None])[1]
            }
    except:
        response = {
                'Code': 400,
                'Results': None,
                'Error': "Verbindung mit dem SQL-Server nicht erfolgreich."
            }
    return response
    
# Funktion zum Hinzufügen von Daten in die Tabelle:
def addItem(inventoryNum, hostName, deviceName, serialNum, date, MACAdress):
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            sql = f"INSERT INTO `cmdb` VALUES ({inventoryNum}, '{hostName}', '{deviceName}', '{serialNum}', '{date}', '{MACAdress}');"
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return 200
    except pymysql.MySQLError as e:
        return getattr(e, 'args', [None])[1]
    except:
        return "Verbindung mit dem SQL-Server nicht erfolgreich."

# Funktion zum Bearbeiten von Daten in der Tabelle:
def editItem(inventoryNum, hostName, deviceName, serialNum, date, MACAdress):
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            sql = f"UPDATE `cmdb` SET HostName = '{hostName}', DeviceName = '{deviceName}', SerialNumber = '{serialNum}', PurchaseDate = '{date}', MACAddress = '{MACAdress}' where InventoryNumber = {inventoryNum};"
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return 200
    except pymysql.MySQLError as e:
        return getattr(e, 'args', [None])[1]
    except:
        return "Verbindung mit dem SQL-Server nicht erfolgreich."
    
# Funktion zum Löschen von Daten aus der Tabelle:
def deleteItem(inventoryNum):
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            sql = f"DELETE FROM `cmdb` where InventoryNumber = {inventoryNum};"
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return 200
    except pymysql.MySQLError as e:
        return getattr(e, 'args', [None])[1]
    except:
        return "Verbindung mit dem SQL-Server nicht erfolgreich."

# Funktion zum Erstellen/Registrieren eines Benutzers in der Datenbank:
def createUser(username, name, email, password):
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            sql = f"INSERT INTO `Users` (Username, Name, Email, Password) VALUES ('{username}', '{name}', '{email}', md5('{password}'));"
            cursor.execute(sql)
            connection.commit()
            connection.close()
            return 200
    except pymysql.MySQLError as e:
        return getattr(e, 'args', [None])[1]
    except:
        return "Verbindung mit dem SQL-Server nicht erfolgreich."
    
# Funktion zum Abrufen eines Benutzers anhand des Benutzernamens:
def getUserFromUsername(username):
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM `Users` WHERE Username = '{username}';"
            cursor.execute(sql)
            result = cursor.fetchone()
            connection.close()
            if result is None:
                return 404
            return result
    except pymysql.MySQLError as e:
        return getattr(e, 'args', [None])[1]
    except:
        return "Verbindung mit dem SQL-Server nicht erfolgreich."
    
# Funktion zum Überprüfen, ob ein Benutzer in der Datenbank existiert:
def checkUser(username, password):
    try:
        connection = open_connection()
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM `Users` WHERE Username = '{username}' and Password = md5('{password}');"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                return 404
            connection.close()
            return result
    except pymysql.MySQLError as e:
        return getattr(e, 'args', [None])[1]
    except:
        return "Verbindung mit dem SQL-Server nicht erfolgreich."