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
                    topik TEXT NOT NULL,
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

# Mendapatkan tgs_id terakhir untuk suatu user
def getLatestTgsID(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT tgs_id FROM t_dln WHERE user_id = ?
                    ORDER BY tgs_id DESC LIMIT 1""", (user_id,))
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return rows[0][0]

# Mendapatkan entry terbaru untuk suatu user
def getLatestEntry(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ?
                    ORDER BY tgs_id DESC LIMIT 1""", (user_id,))
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return rows[0]

# Menambahkan deadline tugas baru untuk suatu user
# Mengembalikan False jika entry sudah terdapat, true jika belum
# user_id = integer, date = datetime (yyyy-mm-dd), type = keyword, matkul = kode/nama
def addDeadlineEntry(user_id, date, tipe, matkul, topik):
    if isEntryExist(user_id, date, tipe, matkul): return False
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    tgs_id = getTgsCount(user_id) + 1
    if (getLatestTgsID(user_id) != None):
        tgs_id = getLatestTgsID(user_id) + 1
    insert = (tgs_id, user_id, date.strftime("%y-%m-%d"), tipe, matkul, topik)
    cursor.execute("""INSERT INTO t_dln(tgs_id, user_id, tanggal, type, matkul, topik)
                    VALUES (?, ?, ?, ?, ?, ?)""", insert)
    cursor.connection.commit()
    return True

# Mencari jika tgs_id ada untuk suatu user
def isTgsIDExist(user_id, tgs_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, tgs_id)
    cursor.execute("SELECT * FROM t_dln WHERE user_id = ? AND tgs_id = ?", entry)
    rows = cursor.fetchall()
    return len(rows) > 0

# Mengecek jika sudah terdapat entry yang persis
def isEntryExist(user_id, date, tipe, matkul):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, date.strftime("%y-%m-%d"), tipe, matkul)
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
    cursor.execute("""SELECT * FROM t_dln 
                    WHERE user_id = ? AND type = ?""", entry)
    return cursor.fetchall()

# Mendapatkan deadline matkul X
def getDeadlineMatkul(user_id, matkul):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, matkul)
    cursor.execute("""SELECT * FROM t_dln 
                    WHERE user_id = ? AND matkul = ?""", entry)
    return cursor.fetchall()

# Mendapatkan deadline matkul X dengan tipe Y
def getDeadlineMatkulType(user_id, matkul, tipe):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, matkul, tipe)
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ? 
                AND matkul = ? AND type = ?""", entry)
    return cursor.fetchall()

# Mendapatkan deadline antara date1 dan date2 dengan date1 <= date2
# Mengembalikan None jika tidak terdapat deadline pada timeframe
def getDeadlineBetween(user_id, date1, date2):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if (date1 <= date2): 
        entry = (user_id, date1.strftime("%y-%m-%d"), date2.strftime("%y-%m-%d"))
    else:
        entry = (user_id, date2.strftime("%y-%m-%d"), date1.strftime("%y-%m-%d"))
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
    entry = (user_id, date.strftime("%y-%m-%d"))
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ?
                    AND tanggal = ?""", entry)
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return rows

# Mendapatkan list deadline untuk x hari ke depan untuk suatu user
def getDeadlineXDays(user_id, x_day):
    now = date.today()
    future = now + timedelta(days = x_day)
    return getDeadlineBetween(user_id, now, future)

# Mendapatkan list deadline untuk x minggu ke depan untuk suatu user
def getDeadlineXWeeks(user_id, x_week):
    now = date.today()
    future = now + timedelta(weeks = x_week)
    return getDeadlineBetween(user_id, now, future)

# Mendapatkan list deadline untuk x bulan ke depan untuk suatu user
def getDeadlineXMonths(user_id, x_month):
    now = date.today()
    future = now + relativedelta(months = x_month)
    return getDeadlineBetween(user_id, now, future)

# Mendapatkan list deadline untuk x tahun ke depan untuk suatu user
def getDeadlineXYears(user_id, x_year):
    now = date.today()
    future = now + relativedelta(years = x_year)
    return getDeadlineBetween(user_id, now, future)

# Mendapatkan info task berdasarkan user_id dan tgs_id
def getTask(user_id, tgs_id):
    if not isTgsIDExist(user_id, tgs_id): return None
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, tgs_id)
    command = "SELECT * FROM t_dln WHERE user_id = ? AND tgs_id = ?"
    cursor.execute(command, entry)
    rows = cursor.fetchall()
    return rows[0]

def getDeadlineBetweenType(user_id, date1, date2, tipe):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    if (date1 <= date2): 
        entry = (user_id, tipe, date1.strftime("%y-%m-%d"), date2.strftime("%y-%m-%d"))
    else:
        entry = (user_id, tipe, date2.strftime("%y-%m-%d"), date1.strftime("%y-%m-%d"))
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ? AND type = ?
                AND tanggal >= ? AND tanggal <= ?""", entry)
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return rows

def getDeadlineOnXDateType(user_id, date, tipe):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, date.strftime("%y-%m-%d"), tipe)
    cursor.execute("""SELECT * FROM t_dln WHERE user_id = ?
                    AND tanggal = ? AND type = ?""", entry)
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return rows

def getDeadlineXDaysType(user_id, x_day, tipe):
    now = date.today()
    future = now + timedelta(days = x_day)
    return getDeadlineBetweenType(user_id, now, future, tipe)

def getDeadlineXWeeksType(user_id, x_week, tipe):
    now = date.today()
    future = now + timedelta(weeks = x_week)
    return getDeadlineBetweenType(user_id, now, future, tipe)

def getDeadlineXMonthsType(user_id, x_month, tipe):
    now = date.today()
    future = now + relativedelta(months = x_month)
    return getDeadlineBetweenType(user_id, now, future, tipe)

def getDeadlineXYearsType(user_id, x_year, tipe):
    now = date.today()
    future = now + relativedelta(years = x_year)
    return getDeadlineBetweenType(user_id, now, future, tipe)

# Menghilangkan deadline
def removeDeadlineEntry(user_id, tgs_id):
    if not isTgsIDExist(user_id, tgs_id): return False
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (user_id, tgs_id)
    cursor.execute("""DELETE FROM t_dln WHERE user_id = ?
                    AND tgs_id = ?""", entry)
    cursor.connection.commit()
    return True

# Mengupdate deadline suatu tugas
def updateDeadlineEntry(user_id, tgs_id, date):
    if not isTgsIDExist(user_id, tgs_id): return False
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    entry = (date, user_id, tgs_id)
    command = """UPDATE t_akun SET tanggal = ? 
                WHERE user_id = ? AND tgs_id = ?"""
    cursor.execute(command, entry)
    cursor.connection.commit()
    return True

if __name__ == "__main__":
    print("running requestQueries")
    # createDeadlineDatabase()
    date = date(2021, 4, 26)
    print(date.strftime("%y-%m-%d"))
    print(addDeadlineEntry(1, (date + timedelta(weeks = 5)), "Tubes", "IF2230", "Placeholder topik"))
    print("Added")
    showAllDeadlineEntries()
    print("getDeadlineMatkul IF2230")
    print(getDeadlineMatkul(1, "IF2230"))
    print("getDeadlineWithType Tubes")
    print(getDeadlineWithType(1, "Tubes"))
    print("getDeadlineBetween ga dapet")
    print(getDeadlineBetween(1, date.today() - timedelta(weeks=4), date.today()))
    print("getDeadlineBetween")
    print(getDeadlineBetween(1, date.today() + timedelta(weeks=7), date.today()))
    print("getDeadlineOnXDate")
    print(getDeadlineOnXDate(1, (date.today() + timedelta(weeks=5))))
    print("getDeadlineXDays, 365")
    print(getDeadlineXDays(1, 365))
    print("getDeadlineXDays, 7")
    print(getDeadlineXDays(1, 7))
    print("getDeadlineXWeeks, 7")
    print(getDeadlineXWeeks(1, 7))
    print("getDeadlineXWeeks, 2")
    print(getDeadlineXWeeks(1, 2))
    print("getDeadlineXMonths, 4")
    print(getDeadlineXMonths(1, 4))
    print("getDeadlineXMonths, 1")
    print(getDeadlineXMonths(1, 1))
    print("getDeadlineXYears, 1")
    print(getDeadlineXYears(1, 1))
    print("getDeadlineXYears, 0")
    print(getDeadlineXYears(1, 0))
    print(addDeadlineEntry(1, (date + timedelta(weeks = 3)), "Tucil", "IF2210", "Placeholder topik"))
    print("Added")
    print("All entries")
    showAllDeadlineEntries()
    print("All entries for 1")
    showDeadlineEntries(1)
    addDeadlineEntry(2, date + timedelta(weeks=4), "PR", "IF2220", "Placeholder topik")
    showAllDeadlineEntries()
    print("deadline for 1")
    showDeadlineEntries(1)
    print("deadline for 2")
    showDeadlineEntries(2)
    print(getLatestTgsID(1))
    print(getLatestTgsID(2))
    print(addDeadlineEntry(1, (date + timedelta(weeks = 5)), "Tucil", "IF2250", "Placeholder topik"))
    print(addDeadlineEntry(1, (date + timedelta(weeks = 6)), "Tucil", "IF2350", "Placeholder topik"))
    print(addDeadlineEntry(2, (date + timedelta(weeks = 2)), "Tucil", "IF2150", "Placeholder topik"))
    showAllDeadlineEntries()
    print("deadline for 1")
    showDeadlineEntries(1)
    print("deadline for 2")
    showDeadlineEntries(2)
    print(removeDeadlineEntry(1, 1))
    print(addDeadlineEntry(1, (date + timedelta(weeks = 5)), "Tucil", "IF2750", "Placeholder topik"))
    print("all")
    showAllDeadlineEntries()
    print(1)
    showDeadlineEntries(1)
    print(2)
    showDeadlineEntries(2)