import sqlite3
import os
import platform
from datetime import datetime
from dateutil.relativedelta import *

clear = lambda: os.system('cls')
sesi = []

class Database:
	def __init__(self):
		# Untuk connect ke database
		self.mydb = sqlite3.connect("barang.db")
		self.mycursor = self.mydb.cursor()

class Sistem(Database):
	def __init__(self, query=None, value=None):
		Database.__init__(self)
		self.query = query
		self.value = value

	def create(self):
		self.mycursor.executemany(self.query, self.value)
		self.mydb.commit()

	def fetchAll(self):
		self.mycursor.execute(self.query)
		return self.mycursor.fetchall()

	def fetchOne(self):
		self.mycursor.execute(self.query, self.value)
		return self.mycursor.fetchone()

	def update(self):
		self.mycursor.execute(self.query, self.value)
		self.mydb.commit()

	def delete(self):
		self.mycursor.execute(self.query, self.value)
		self.mydb.commit()

class Akun(Sistem):
	tabelAkun = "akun"

	def __init__(self, query=None, value=None):
		Sistem.__init__(self, query, value)

	def login(self, username, password):
		self.query = f"SELECT idAkun, username, nama FROM {self.tabelAkun} WHERE username = ? AND password = ?"
		self.value = (username, password)

		hasil = self.fetchOne()

		clear()

		if(hasil):
			sesi.append(hasil)
		else:
			print("Username atau password salah")

		return hasil

	def register(self, value):
		self.query = f"INSERT INTO {self.tabelAkun} (username, password, nama) VALUES (?, ?, ?)"
		self.value = value

		self.create()
		print("Berhasil mendaftar")

class Jenis(Sistem):
	# Private Variabel
	__namaTabel = "jenis_barang"

	def __init__(self, query=None, value=None):
		Sistem.__init__(self, query, value)

	def input(self, value):
		self.query = f"INSERT INTO {self.__namaTabel} (namaJenis) VALUES (?)"
		self.value = value

		self.create()
		print("Berhasil menginput data")

	def ambil(self):
		self.query = f"SELECT * FROM {self.__namaTabel}"
		hasil = self.fetchAll()

		if(hasil):
			print("=== Jenis Barang ===")

			for x in range(0, len(hasil)):
				print(f"{x+1}. {hasil[x][1]} (ID: {hasil[x][0]})")
		else:
			print("=== Jenis Barang ===")
			print("Tidak ada data")

		return hasil

	def ambilSatu(self, inputan):
		self.query = f"SELECT * FROM {self.__namaTabel} where idJenis = ?"
		self.value = (inputan,)

		return self.fetchOne()

	def ubah(self, inputan):
		self.query = f"UPDATE {self.__namaTabel} SET namaJenis = ? WHERE idJenis = ?"
		self.value = inputan

		self.update()
		print("Berhasil mengubah data")

	def hapus(self, inputan):
		self.query = f"DELETE FROM {self.__namaTabel} WHERE idJenis = ?"
		self.value = (inputan,)

		self.delete()
		print("Berhasil menghapus data")

class Jasa(Sistem):
	# Private Variabel
	__namaTabel = "jasa"

	def __init__(self, query=None, value=None):
		Sistem.__init__(self, query, value)

	def input(self, value):
		self.query = f"INSERT INTO {self.__namaTabel} (idJenis, namaBarang, jumlahBarang, namaCustomer, alamat, tanggalMasuk, tanggalAmbil, biaya, statusBarang) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
		self.value = value

		self.create()
		print("Berhasil menginput data")

	def ambil(self):
		self.query = f"SELECT a.idJasa, b.namaJenis, a.namaBarang, a.jumlahBarang, a.alamat, a.tanggalMasuk, a.tanggalAmbil, a.biaya, a.statusBarang FROM {self.__namaTabel} a INNER JOIN jenis_barang b using(idJenis)"
		hasil = self.fetchAll()

		if(hasil):
			print("=== Riwayat Jasa ===")

			for x in range(0, len(hasil)):
				if(hasil[x][8] == "0"):
					status = "Masih dalam penitipan"
				else:
					status = "Telah diambil"

				print(f"{x+1}. Nama Barang: {hasil[x][2]} | Jenis: {hasil[x][1]} | Jumlah: {hasil[x][3]} | Alamat Pengguna: {hasil[x][4]} | Tanggal Masuk: {hasil[x][5]} | Tanggal Ambil: {hasil[x][6]} | Biaya: Rp {hasil[x][7]} | Status: {status} (ID: {hasil[x][0]})")
		else:
			print("=== Riwayat Jasa ===")
			print("Tidak ada data")

		return hasil

	def ambilSatu(self, inputan):
		self.query = f"SELECT a.idJasa, b.namaJenis, a.namaBarang, a.jumlahBarang, a.alamat, a.tanggalMasuk, a.tanggalAmbil, a.biaya, a.statusBarang FROM {self.__namaTabel} a INNER JOIN jenis_barang b using(idJenis) WHERE idJasa = ?"
		self.value = (inputan,)

		return self.fetchOne()

	def prosesTransaksi(self, inputan):
		self.query = f"UPDATE {self.__namaTabel} SET statusBarang = ? WHERE idJasa = ?"
		self.value = inputan

		self.update()
		print("Berhasil mengubah data")

	def hapus(self, inputan):
		self.query = f"DELETE FROM {self.__namaTabel} WHERE idJasa = ?"
		self.value = (inputan,)

		self.delete()
		print("Berhasil menghapus data")

def jenisBarang():
	print("Jenis Barang")
	print("1. Tambah\n2. Tampilkan\n3. Ubah\n4. Hapus")
	menu = int(input("Pilih Menu: "))

	clear()

	if(menu == 1):
		data = []
		banyakData = int(input("Masukkan banyak data yang akan diinput: "))

		for x in range(0, banyakData):
			print(f"===== Jenis #{x+1} =====")
			input1 = input("Input nama jenis barang: ")

			# Tuple single item
			data.append((input1,))

		clear()
		Jenis().input(data)
	elif(menu == 2):
		Jenis().ambil()
	elif(menu == 3):
		cekData = Jenis().ambil()

		# Cek jika data ada
		if(cekData):
			inputan = int(input("Masukkan ID yang akan diubah: "))
			dataAda = Jenis().ambilSatu(inputan)

			if(dataAda):
				input1 = input("Input nama jenis barang: ")

				data = (input1, inputan)

				clear()
				Jenis().ubah(data)
			else:
				clear()
				print(f"ID {inputan} tidak ada.")
		else:
			pass
	elif(menu == 4):
		cekData = Jenis().ambil()

		if(cekData):
			inputan = int(input("Masukkan id yang akan dihapus: "))
			dataAda = Jenis().ambilSatu(inputan)

			if(dataAda):
				clear()
				Jenis().hapus(inputan)
			else:
				clear()
				print(f"ID {inputan} tidak ada.")
		else:
			pass
	else:
		pass

def jasa():
	print("Manajemen Jasa")
	print("1. Tambah\n2. Lihat Riwayat Transaksi\n3. Proses Transaksi\n4. Hapus")
	menu = int(input("Pilih Menu: "))

	clear()
	
	if(menu == 1):
		data = []

		Jenis().ambil()
		input1 = input("Input ID jenis barang: ")
		jenis = Jenis().ambilSatu(input1)

		if(jenis):
			input2 = input("Input nama barang: ")
			input3 = input("Input jumlah barang: ")
			input4 = input("Input nama customer: ")
			input5 = input("Input alamat: ")
			input6 = int(input("Input lama penitipan (bulan): "))
			
			biayaTotal = input6 * 75000
			statusBarang = "0"

			tanggalAwal = datetime.today().strftime('%Y-%m-%d')
			initialDate = datetime.strptime(str(tanggalAwal), '%Y-%m-%d')
			modifiedDate = initialDate + relativedelta(months=+input6)
			tanggalAmbil = datetime.strftime(modifiedDate, '%Y-%m-%d')

			data.append((input1, input2, input3, input4, input5, tanggalAwal, tanggalAmbil, biayaTotal, statusBarang))

			clear()
			Jasa().input(data)
		else:
			print("ID jenis tidak ditemukan")
	elif(menu == 2):
		Jasa().ambil()
	elif(menu == 3):
		cekData = Jasa().ambil()

		if(cekData):
			inputan = int(input("Masukkan ID yang akan diproses: "))
			dataAda = Jasa().ambilSatu(inputan)

			if(dataAda):
				input1 = input("Input status barang (0 = Masih Dalam Masa Penitipan | 1 = Telah Diambil): ")

				data = (input1, inputan)

				clear()
				Jasa().prosesTransaksi(data)
			else:
				clear()
				print(f"ID {inputan} tidak ada.")
		else:
			pass
	elif(menu == 4):
		cekData = Jasa().ambil()

		if(cekData):
			inputan = int(input("Masukkan id yang akan dihapus: "))
			dataAda = Jasa().ambilSatu(inputan)

			if(dataAda):
				clear()
				Jasa().hapus(inputan)
			else:
				clear()
				print(f"ID {inputan} tidak ada.")
		else:
			pass
	else:
		pass

while True:
	# Jika Array sesi tidak ada isinya
	if(len(sesi) == 0):
		print(f"Selamat Datang!")
		print("1. Login")
		print("2. Registrasi User")
		menu = int(input("Pilih menu: "))

		clear()

		if(menu == 1):
			username = input("Input username: ")
			password = input("Input password: ")

			clear()
			Akun().login(username, password)
		elif(menu == 2):
			username = input("Input username: ")
			password = input("Input password: ")
			nama = input("Input nama: ")

			data = [(username, password, nama)]

			clear()
			Akun().register(data)
		else:
			print("Menu tidak valid")
	else:
		# Jika sudah login
		print(f"Selamat Datang! {sesi[0][2]}")
		print("1. Manajemen Jenis")
		print("2. Manajemen Jasa")
		print("3. Logout")
		menu = int(input("Pilih menu: "))

		clear()

		if(menu == 1):
			jenisBarang()
		elif(menu == 2):
			jasa()
		elif(menu == 3):
			sesi = []

			clear()
			print("Berhasil logout")
		else:
			exit()