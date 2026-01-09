import ftplib
import os
import sys

# Konfigurasi Koneksi [cite: 74, 76]
FTP_HOST = "127.0.0.1"
FTP_PORT = 2122

def clear():
    # Membersihkan layar terminal [cite: 79]
    os.system("cls" if os.name == "nt" else "clear")

def garis():
    print("="*60)

def pause():
    input("\nTekan ENTER untuk lanjut...")

def cek_koneksi():
    # Fungsi untuk memastikan server aktif sebelum login [cite: 88]
    garis()
    print(" CEK KONEKSI FTP SERVER")
    garis()
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT, timeout=5)
        print(" [STATUS] Server FTP TERHUBUNG")
        ftp.quit() # Tutup koneksi sementara
        return True
    except Exception as e:
        print(" [STATUS] Server FTP TIDAK TERHUBUNG")
        print(f" Error: {e}")
        return False

def login_ftp():
    # Fungsi untuk login ke server [cite: 101]
    ftp = ftplib.FTP()
    try:
        ftp.connect(FTP_HOST, FTP_PORT)
        print("\n LOGIN FTP")
        user = input(" Username: ") # Masukkan 'user'
        pwd = input(" Password: ")  # Masukkan '12345'
        
        ftp.login(user, pwd)
        print(" [LOGIN BERHASIL]")
        print(" Pesan Server:", ftp.getwelcome())
        return ftp
    except Exception as e:
        print("\n [LOGIN GAGAL]")
        print(f" Error: {e}")
        try:
            ftp.quit()
        except:
            pass
        return None

def menu(ftp, home_dir):
    while True:
        clear()
        print(" MENU CLIENT FTP")
        garis()
        print(f" Direktori saat ini: {ftp.pwd()}") # [cite: 120]
        garis()
        print(" 1. Cek Direktori Server (List)")
        print(" 2. Pindah Folder (Change Directory)")
        print(" 3. Kembali ke Awal (Home)")
        print(" 4. Download File")
        print(" 5. Upload File")
        print(" 0. Keluar")
        garis()
        
        pilihan = input(" Pilihan (0-5): ")

        if pilihan == '1':
            # LIST FILE [cite: 145]
            print("\n [ISI DIREKTORI SERVER]")
            try:
                ftp.dir() # Menampilkan daftar file lengkap
            except Exception as e:
                print(f" Gagal mengambil list: {e}")
            pause()

        elif pilihan == '2':
            # PINDAH FOLDER [cite: 151]
            folder = input(" Masukkan nama folder tujuan: ")
            try:
                ftp.cwd(folder) # Change Working Directory
                print(f" [BERHASIL] Sekarang di: {ftp.pwd()}")
            except Exception as e:
                print(" [GAGAL] Folder tidak ditemukan.")
            pause()

        elif pilihan == '3':
            # KEMBALI KE HOME [cite: 160]
            try:
                ftp.cwd(home_dir)
                print(f" [HOME] Kembali ke: {ftp.pwd()}")
            except Exception as e:
                print(f" Gagal: {e}")
            pause()

        elif pilihan == '4':
            # DOWNLOAD FILE [cite: 164]
            print("\n [DOWNLOAD FILE]")
            # Tampilkan dulu isinya agar user mudah memilih
            ftp.dir() 
            nama_file = input(" Masukkan nama file yang akan di-download: ")
            try:
                # Membuka file lokal mode write binary (wb)
                with open(nama_file, "wb") as f:
                    # Perintah RETR (Retrieve) [cite: 177]
                    ftp.retrbinary(f"RETR {nama_file}", f.write)
                print(" [BERHASIL] File berhasil di-download.")
            except Exception as e:
                print(f" [GAGAL] File tidak dapat di-download: {e}")
                # Hapus file kosong jika gagal
                if os.path.exists(nama_file):
                    os.remove(nama_file)
            pause()

        elif pilihan == '5':
            # UPLOAD FILE [cite: 180]
            print("\n [UPLOAD FILE]")
            print(" Daftar File Lokal:")
            # List file di komputer client
            lokal_files = [f for f in os.listdir() if os.path.isfile(f)]
            for f in lokal_files:
                print(f" - {f}")
            
            nama_file = input(" Masukkan nama file lokal untuk di-upload: ")
            
            if not os.path.exists(nama_file):
                 print(" [ERROR] File lokal tidak ditemukan.")
            else:
                try:
                    # Membuka file lokal mode read binary (rb)
                    with open(nama_file, "rb") as f:
                        # Perintah STOR (Store) [cite: 202]
                        ftp.storbinary(f"STOR {nama_file}", f)
                    print(" [BERHASIL] File berhasil di-upload.")
                except Exception as e:
                     print(f" [GAGAL] Upload gagal: {e}")
            pause()

        elif pilihan == '0':
            print(" Menutup koneksi...")
            try:
                ftp.quit()
            except:
                pass
            break
        
        else:
            print(" Pilihan tidak valid.")
            pause()

def main():
    clear()
    # Step 1: Cek Server
    if not cek_koneksi():
        pause()
        return

    pause()
    clear()
    
    # Step 2: Login
    ftp = login_ftp()
    if ftp:
        # Simpan direktori awal sebagai home
        home_dir = ftp.pwd()
        menu(ftp, home_dir)

if __name__ == "__main__":
    main()