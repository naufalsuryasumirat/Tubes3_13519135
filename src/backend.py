import re
from kmp import kmp
from datetime import datetime, date
from app import convertmessage
import requestQueries as rq

keywords = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
keywordsHelp = ["opsi","help","dilakukan"]
keywordsUpdate = ["diundur"]


stopwords = ["pada", "tolong", "yakni", "aku", "di", "ke", "dari"]

def convert_date(input):
    con = datetime.strptime(input, '%d/%m/%Y').date()
    return con

def convert_database_date(input):
    con = datetime.strptime(input, '%y-%m-%d').date()
    return con

def convert_daftarTask(listOfEntry):
	if (not listOfEntry):
		return "Tidak ada"
	
	outputString = "[Daftar Deadline]\n"
	idx = 1
	for i in listOfEntry:
		outputString = outputString + str(idx) + ". " + convertEntryToString(i) + "\n"
		idx = idx + 1
	return outputString

def regExTanggal(inputString):
	#Return match object or none
	return re.search(r"([0-3][0-9](/|-)[0-1][0-9](/|-)([0-9]{4}|[0-9]{2}))|(([0-3][0-9]|[0-9])\s*(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)\s*([0-9]{4}|[0-9]{2}))", inputString.lower())

def convertEntryToString(entry):
    return "(ID: "+str(entry[1])+ ") "+ \
        str(entry[3])+" - "+entry[5] + " - " + \
             entry[4] + " - "+entry[6]

def regExTanggalFormat(inputString):
	#Return string
	date = re.search(r"([0-3][0-9](/|-)[0-1][0-9](/|-)([0-9]{4}|[0-9]{2}))|(([0-3][0-9]|[0-9])\s*(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)\s*([0-9]{4}|[0-9]{2}))", inputString.lower())
	if (not date):
		return None
	
	textMonth = re.search(r"([0-3][0-9]|[0-9])\s*(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)\s*([0-9]{4}|[0-9]{2})", inputString.lower())
	if (textMonth):
		if (len(textMonth.group(1)) == 1):
			date = "0" + textMonth.group(1)
		else:
			date = textMonth.group(1)
		if (textMonth.group(2) == "january" or textMonth.group(2) == "jan"):
			date = date + "/01"
		elif (textMonth.group(2) == "february" or textMonth.group(2) == "feb"):
			date = date + "/02"
		elif (textMonth.group(2) == "march" or textMonth.group(2) == "mar"):
			date = date + "/03"
		elif (textMonth.group(2) == "april" or textMonth.group(2) == "apr"):
			date = date + "/04"
		elif (textMonth.group(2) == "may"):
			date = date + "/05"
		elif (textMonth.group(2) == "june" or textMonth.group(2) == "jun"):
			date = date + "/06"
		elif (textMonth.group(2) == "july" or textMonth.group(2) == "jul"):
			date = date + "/07"
		elif (textMonth.group(2) == "august" or textMonth.group(2) == "aug"):
			date = date + "/08"
		elif (textMonth.group(2) == "september" or textMonth.group(2) == "sep"):
			date = date + "/09"
		elif (textMonth.group(2) == "october" or textMonth.group(2) == "oct"):
			date = date + "/10"
		elif (textMonth.group(2) == "november" or textMonth.group(2) == "nov"):
			date = date + "/11"
		elif (textMonth.group(2) == "december" or textMonth.group(2) == "dec"):
			date = date + "/12"

		date = date + "/"
		if (len(textMonth.group(3)) == 2):
			date = date + "20" + textMonth.group(3)
		else:
			date = date + textMonth.group(3)
	else:
		numberMonth = re.search(r"([0-3][0-9])(/|-)([0-1][0-9])(/|-)([0-9]{4}|[0-9]{2})",inputString.lower())
		date = numberMonth.group(1) + "/" +numberMonth.group(3) + "/"
		if (len(numberMonth.group(5)) == 2):
			date = date + "20" + numberMonth.group(3)
		else:
			date = date + numberMonth.group(5)

	return date

def removeStopWords(inputString, listOfString):
	for i in listOfString:
		inputString = inputString.replace(i, "")
	return inputString


#1.
def findTask(string, user_id):
	# tanggal = re.search(r"([0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9])|([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9])", string)
	# return tuple of string, isinya Tanggal yang di format, Kode Mata Kuliah, Jenis Tugas, Topik Tugas
	# Jika tidak ditemukan salah satu ini, return None

	# Cari tanggal
	# tanggal = re.search(r"([0-3][0-9](/|-)[0-1][0-9](/|-)([0-9]{4}|[0-9]{2}))|([0-3][0-9]\s*(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|september|sep|october|oct|november|nov|december|dec)\s*([0-9]{4}|[0-9]{2}))", string.lower())
	tanggal = regExTanggal(string)
	idxTanggalBegin = None
	if tanggal:
		# print(tanggal.group())
		idxTanggalBegin = tanggal.span()[0]
	else:
		# print("Tidak ditemukan match dalam "+string)
		return None
		

	#Cara mata kuliah, yang berisi 2 huruf dan 4 angka
	kodeMK = re.search(r"[a-zA-Z]{2}\d{4}", string)
	idxAkhirKode = None
	if kodeMK:
		# print(kodeMK.group())
		idxAkhirKode = kodeMK.span()[1]
	else:
		return None
	
	#Isi topik dengan apa kata setelah mata kuliah
	topik = None
	if (idxTanggalBegin and idxAkhirKode):
		topik = string[idxAkhirKode:idxTanggalBegin].strip()
		topik = removeStopWords(topik, stopwords)
		# print(topik)
	else:
		return None

	#Cari jenis berdasarakn keyword
	jenis = None
	for i in keywords:
		if kmp(i, string.lower()):
			jenis = i

	if jenis == None:
		return None
	rq.addDeadlineEntry(user_id, convert_date(regExTanggalFormat(tanggal.group())), jenis, kodeMK.group(),  topik)
	entry = rq.getLatestEntry(user_id)
	outputString = "[TASK BERHASIL DICATAT]\n" + convertEntryToString(entry)
	return outputString
    # print(tanggal.group())
	# print(kodeMK.group())
	# print(jenis)
	# print(topik)
    

# def regExDuaTanggal(input):
#     re.search(r"(\d+/\d+/\d+)*(\d+/\d+/\d+)", input)
#     return



#2.
def lihatDaftarTask(string, user_id):
	keywordSemuaTask = ["sejauh ini", "semua", "all", "so far"]

	##Flags for all
	semuaTask = False
	for i in keywordSemuaTask:
		if kmp(i, string.lower()):
			semuaTask = True


	##Flags for time period

	#Between 2 dates
	date1 = regExTanggal(string)
	date2 = None
	if (date1):
		slicedString = string.lower().replace(date1.group(),"")
		date2 = regExTanggal(slicedString) #Cannot use the index

	#N minggu ke depan
	NMingguDepan = re.search(r"(\d).*minggu.*depan",string.lower())
	#N hari ke depan
	NHariDepan = re.search(r"(\d).*hari.*depan",string.lower())
	#Hari ini
	HariIni = re.search(r"hari.*ini",string.lower())
	##Flag for jenis task
	jenis = None
	for i in keywords:
		if kmp(i, string.lower()):
			jenis = i

	if not (semuaTask or date1 or NMingguDepan or NHariDepan or HariIni or jenis):
		return None

	if semuaTask:
		print("Get All Tasks")
		return rq.getDeadlineEntries(user_id)
	else: # Process Time Period
		if (date1 and date2):
			print("Get Between " + regExTanggalFormat(date1.group()) + " " +regExTanggalFormat(date2.group()))
			if (jenis):
				return rq.getDeadlineBetweenType(user_id, convert_date(regExTanggalFormat(date1.group())), convert_date(regExTanggalFormat(date2.group())), jenis)
			else:
				return rq.getDeadlineBetween(user_id, convert_date(regExTanggalFormat(date1.group())), convert_date(regExTanggalFormat(date2.group())))
		elif (NMingguDepan):
			print("Get " + NMingguDepan.group(1)+ " Minggu depan")
			if (jenis):
				return rq.getDeadlineXWeeksType(user_id, NMingguDepan.group(1), jenis)
			else:
				return rq.getDeadlineXWeeks(user_id, NMingguDepan.group(1))
		elif (NHariDepan):
			# print("Get " + NHariDepan.group(1) + " Hari depan")
			if (jenis):
				return rq.getDeadlineXDaysType(user_id, NHariDepan.group(1), jenis)
			else:
				return rq.getDeadlineXDays(user_id, NHariDepan.group(1))
		elif (HariIni):
			# print("Get Hari ini")
			if (jenis):
				return rq.getDeadlineXDaysType(user_id, 0, jenis)
			else:
				return rq.getDeadlineXDays(user_id, 0)
            
		else:
			# print("Get semua tanggal")
			if (jenis):
				return rq.getDeadlineWithType(user_id, jenis)
			else:
				return rq.getDeadlineEntries(user_id)

		#Process Task
		# if (jenis):
		# 	print("Get type: "+jenis)
		# else:
		# 	print("Get all types")

#3.
# def findDeadlineMK(string, user_id): # Match langsung masuk ke query
# 	kodeMK = re.search(r"[a-zA-Z]{2}\d{4}", string)
# 	if (kodeMK):
# 		if (rq.getDeadlineMatkul(user_id, kodeMK.group())):
# 			first_row = rq.getDeadlineMatkul(user_id, kodeMK.group())[0]
# 			return first_row[3]
# 		else:
# 			return None
# 	else:
# 		return None
	
# 3
def findDeadLineMK(string, user_id):
	kodeMK = re.search(r"[a-zA-Z]{2}\d{4}", string)
	if (kodeMK):
		get = rq.getDeadlineMatkul(user_id, kodeMK.group())
		if (get):
			first_row = get[0]
			return convert_database_date(first_row[3])
		else:
			return None
	else:
		return None

#4
def regex_undur(input, user_id):
    for word in keywordsUpdate: # redundan, keyword hanya satu
        if not kmp(word, input): return None
    tgl = re.search(r"\s\d+/\d+/\d+\s")
    if tgl == None:
        return "Tolong untuk memasukkan tanggal dengan format yang benar"
    tgl = convert_date(tgl.group(0).strip())
    search = re.search(r"\stask\s\d*", input)
    if search == None: return None
    task = -1
    for c in search.group(0).split():
        if (c.isdigit()):
            task = c
    if rq.isTgsIDExist(user_id, task):
        rq.updateDeadlineEntry(user_id, task, tgl)
        return "Task dengan id " + task + " berhasil diundur menjadi " + tgl.strftime('%d-%m-%Y')
    else:
        return "Task tidak terdapat untuk diperbarui"

#5.
def taskDone(string, user_id):
	if (kmp("selesai", string.lower()) or kmp("done", string.lower())):
		ID = re.search(r"\d+", string)
		# print("Delete ID: "+ ID.group() + " For user: "+ str(user_id))
		taskToBeDeleted = rq.getTask(user_id, ID)
        # outputString = "(ID: "+str(taskToBeDeleted[1])+ ") "+str(taskToBeDeleted[3])+" - "+taskToBeDeleted[5] + " - " + taskToBeDeleted[4] + " - "+taskToBeDeleted[6]
		outputString = convertEntryToString(taskToBeDeleted)
		rq.removeDeadlineEntry(user_id, ID)
		return outputString
	else: return None

#6.
def opsi(string): 
	keywordsHelp = ["opsi","help","dilakukan"]

	isHelp = False
	for i in keywordsHelp:
		if (kmp(i,string.lower())):
			isHelp = True
			break
	
	if (isHelp):
		fitur = "[Fitur]\n"
		fitur = fitur+"1. Menambahkan task baru\n"
		fitur = fitur+"2. Melihat daftar task yang harus dikerjakan\n"
		fitur = fitur+"3. Menampilkan deadline dari suatu task tertentu\n"
		fitur = fitur+"4. Memperbaharui task tertentu\n"
		fitur = fitur+"5. Menandai bahwa suatu task sudah selesai kerjakan\n\n"


		katapenting = "[Daftar kata penting]\n"
		for i in range(len(keywords)):
			katapenting = katapenting+str(i+1)+". "+ str(keywords[i].title())+"\n"
		
		print(fitur+katapenting)
		return fitur+katapenting
	return None

def get_bot_message(message, user_id):
	msgOpsi = opsi(message)
	if msgOpsi: return msgOpsi
	msgDuaTanggal = lihatDaftarTask(message, user_id)
	if msgDuaTanggal: return convert_daftarTask(msgDuaTanggal) # Format
	find = findTask(message, user_id)
	if find: return find
	doneTask = taskDone(message, user_id)
	if doneTask: return doneTask
	undurTask = regex_undur(message, user_id)
	if undurTask: return undurTask
	findMK = findDeadLineMK(message, user_id)
	if findMK: return findMK
	return "Maaf, pesan tidak dikenali"

if __name__ == "__main__":
	txt1 = "Tubes IF2211 String Matching pada 14 April 2021"
	txt2 = "Halo bot, tolong ingetin kalau ada kuis IF3110 Bab 2 sampai 3 pada 22/04/2021"
	txt3 = "Halo bot, tolong ingetin kalau ada tubes IF2321 Topik String matching pada 22/05/2021"
	txt4 = "Apa saja deadline antara 03/04/2021 sampai 15/04/2021"
	print(regExTanggal(txt1))
	print(regExTanggal(txt1).group())
    # print(findTask(txt3))
	print(re.search(r"(\d\d/\d\d/\d\d)", txt4))
	print(re.search(r"(\d\d/\d\d/\d\d*\d\d/\d\d/\d\d)", txt4))
	print(re.search(r"[a-zA-Z]{2}\d{4}", txt1))
	print(convertmessage("Hello from the \nother side"))
	print(convert_date('03/04/2021'))
	print(convert_date('2021/04/03'))
	print(convert_date('03/04/2021'))
    