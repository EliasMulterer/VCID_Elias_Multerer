import pymysql

# These are the details for connecting to your database. Kindly set them accordingly when deploying:
db_user = 'root'
db_password = ''
db_connection_name = 'praxisarbeit-vcid-multerer:europe-west1:vicd'
db_name = 'cmdb'


# Conneting to the cloud SQL instance:
def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    connection = pymysql.connect(user=db_user,
                             password=db_password,
                             database=db_name,
                            # unix_socket=unix_socket,
                             host='130.211.95.210',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

# Function to get Data from Table:
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
                'Error': "Connection with SQL Server Not Successful."
            }
    return response
    
# Function to Add Data in table:
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
        return "Connection with SQL Server Not Successful."

# Function to Edit Data in Table:
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
        return "Connection with SQL Server Not Successful."
    
# Function to Delete Data from Table:
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
        return "Connection with SQL Server Not Successful."

# Function to Create/Register User in Database:
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
        return "Connection with SQL Server Not Successful."
    
# Function to get User from Username:
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
        return "Connection with SQL Server Not Successful."
    
# Function to Check if User exist in Database:
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
        return "Connection with SQL Server Not Successful."