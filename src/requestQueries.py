import sqlite3
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import loginQueries as lq

# Membuat tabel deadline tugas jika belum ada
def createDeadlineDatabase():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS
                    t_dln(dln_id INTEGER PRIMARY KEY,
                    tgs_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    tanggal DATE NOT NULL,
                    type TEXT NOT NULL,
                    matkul TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES t_akun(user_id)
    )""")
    return

# Mendapatkan jumlah tugas yang ada untuk suatu user
def getTgsCount(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_dln WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    return len(rows)

# Menambahkan deadline tugas baru untuk suatu user
# Mengembalikan False jika entry sudah terdapat, true jika belum
# user_id = integer, date = datetime (yyyy-mm-dd), type = keyword, matkul = kode/nama
def addDeadlineEntry(user_id, date, tipe, matkul):
    if isEntryExist: return False
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    tgs_id = getTgsCount(user_id) + 1
    insert = (tgs_id, user_id, date, tipe, matkul)
    cursor.execute("""INSERT INTO t_dln(tgs_id, user_id, tanggal, type, matkul)
                    VALUES (?, ?, ?, ?, ?)""", insert)
    cursor.connection.commit()
    return True

# Mengecek jika sudah terdapat entry yang persis
def isEntryExist(user_id, date, tipe, matkul):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, date, tipe, matkul)
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ? 
                    AND tanggal = ? AND type = ? AND matkul = ?""", entry)
    rows = cursor.fetchall()
    return len(rows) > 0

# Mendapatkan list yang berisi deadline user dengan id = user_id
def getDeadlineEntries(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_dln WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    if (len(rows) == 0): return None
    return rows

# Memperlihatkan deadline untuk user_id tertentu
def showDeadlineEntries(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_dln WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Tidak ada deadline untuk user dengan id " + user_id)
        return
    for row in rows:
        print(row)
    return

# Memperlihatkan seluruh entry pada tabel deadline
def showAllDeadlineEntries():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_dln")
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Tabel deadline empty")
        return
    for row in rows:
        print(row)
    return

# Mendapatkan deadline dengan type = tipe
def getDeadlineWithType(user_id, tipe):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, tipe)
    cursor.execute("""SELECT tanggal, matkul FROM t_dln 
                    WHERE user_id = ? AND type = ?""", entry)
    return cursor.fetchall()

# Mendapatkan deadline matkul X
def getDeadlineMatkul(user_id, matkul):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, matkul)
    cursor.execute("""SELECT tanggal, tipe FROM t_dln 
                    WHERE user_id = ? AND matkul = ?""", entry)
    return cursor.fetchall()

# Mendapatkan deadline matkul X dengan tipe Y
def getDeadlineMatkulType(user_id, matkul, tipe):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, matkul, tipe)
    cursor.execute("""SELECT tanggal FROM t_dln WHERE user_id = ? 
                AND matkul = ? AND type = ?""", entry)
    return cursor.fetchall()

# Mendapatkan deadline antara date1 dan date2 dengan date1 <= date2
# Mengembalikan None jika tidak terdapat deadline pada timeframe
def getDeadlineBetween(user_id, date1, date2):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, date1, date2)
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ?
                AND tanggal >= ? AND tanggal <= ?""", entry)
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return rows

# Mendapatkan deadline yang terdapat pada tanggal = date untuk suatu user
# Mengembalikan None jika tidak terdapat deadline pada waktu yang diberikan
def getDeadlineOnXDate(user_id, date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, date)
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ?
                    AND tanggal = ?""", entry)
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return rows

# Mendapatkan list deadline untuk x hari ke depan untuk suatu user
def getDeadlineXDays(user_id, x_day):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    now = date.today()
    future = now + timedelta(days = x_day)
    return getDeadlineBetween(now, future)

# Mendapatkan list deadline untuk x minggu ke depan untuk suatu user
def getDeadlineXWeeks(user_id, x_week):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    now = date.today()
    future = now + timedelta(weeks = x_week)
    return getDeadlineBetween(now, future)

# Mendapatkan list deadline untuk x bulan ke depan untuk suatu user
def getDeadlineXMonths(user_id, x_month):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    now = date.today()
    future = now + relativedelta(months = x_month)
    return getDeadlineBetween(now, future)

# Mendapatkan list deadline untuk x tahun ke depan untuk suatu user
def getDeadlineXYears(user_id, x_year):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    now = date.today()
    future = now + relativedelta(years = x_year)
    return getDeadlineBetween(now, future)

if __name__ == "__main__":
    print("running requestQueries")
    createDeadlineDatabase()
    