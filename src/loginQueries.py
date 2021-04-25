import sqlite3
import requestQueries as rq

# Membuat Tabel User jika belum ada
def createUserDatabase():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS 
                    t_akun(user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
    )""")
    return

# Mengecek jika email sudah terdapat pada database User, jika sudah terdapat dikembalikan True, jika tidak dikembalikan False
def isEmailExist(email):
    connectionUser = sqlite3.connect('database.db')
    cursor = connectionUser.cursor()
    command = "SELECT user_id FROM t_akun WHERE t_akun.email = ?"
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return (len(rows) > 0)

# Menghitung banyak user pada database User
def userCount():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * from t_akun")
    return len(cursor.fetchall())

def addUserEntry(name, email, password):
    if (isEmailExist(email)): return False
        # Tidak menambahkan entry jika sudah terdapat user dengan email yang sama 
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    user = (name, email, password)
    commandInsert = """INSERT INTO t_akun(name, email, password) 
                    VALUES (?, ?, ?)"""
    cursor.execute(commandInsert, user)
    cursor.connection.commit()
    return True

# Menampilkan tabel user
def showUserEntries():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    command = "SELECT * FROM t_akun"
    cursor.execute(command)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Table t_akun Empty")
        return
    for row in rows:
        print(row)
    return

# Mendapatkan info yang digunakan untuk login (password)
# Mengembalikan False jika user belum terdaftar
def getLoginInfo(email):
    if not isEmailExist(email): return False # Mengembalikan False jika user belum terdaftar
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    command = """SELECT password FROM t_akun WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return rows[0][0] # Mengembalikan password

# Mengambil nama user dengan input email
def getName(email):
    if not isEmailExist(email): return None
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    command = """SELECT name FROM t_akun WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return rows[0][0]

# Mengambil id user dengan input email
def getUserID(email):
    if not isEmailExist(email): return None
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    command = "SELECT user_id FROM t_akun WHERE email = ?"
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return rows[0][0]

if __name__ == "__main__":
    print("running loginQueries")