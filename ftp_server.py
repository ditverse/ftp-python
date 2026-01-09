import os
import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp_server():
    # --- 1. Konfigurasi Logging ---
    # Menampilkan log aktivitas server ke layar [cite: 11]
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "="*60)
    print(" SERVER FTP LOKAL BERJALAN ")
    print("="*60)

    # --- 2. Menyiapkan Folder Server ---
    share_folder_name = "data"
    current_dir = os.getcwd()
    server_dir = os.path.join(current_dir, share_folder_name)

    # Buat folder utama 'data' jika belum ada [cite: 22, 23]
    if not os.path.exists(server_dir):
        os.makedirs(server_dir)
        print(f" [+] Folder penyimpanan dibuat: {share_folder_name}")

    # Buat file dummy 'baca_saya.txt' untuk tes download [cite: 27]
    dummy_file = os.path.join(server_dir, "baca_saya.txt")
    if not os.path.exists(dummy_file):
        with open(dummy_file, "w") as f:
            f.write("Halo! Ini adalah file tes dari server.\nSilakan download file ini.")
        print(" [+] File 'baca_saya.txt' dibuat otomatis.")

    # Buat sub-folder 'Folder Tes' untuk tes navigasi [cite: 33]
    sub_folder = os.path.join(server_dir, "Folder Tes")
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
        print(" [+] Sub-Folder 'Folder Tes' dibuat.")
    
    print(f" Path Fisik Server: {server_dir}")

    # --- 3. Konfigurasi User (Authorizer) ---
    authorizer = DummyAuthorizer()
    
    # Menambahkan user: username='user', password='12345'
    # perm='elradfmw' memberikan akses penuh (read/write/delete/dll) [cite: 42]
    authorizer.add_user("user", "12345", server_dir, perm="elradfmw")

    # --- 4. Handler & Server ---
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "Selamat datang di Local FTP Server (Python)"  # [cite: 46]

    # Konfigurasi IP dan Port
    address = ("127.0.0.1", 2122) # [cite: 48, 49]
    
    try:
        server = FTPServer(address, handler)
        server.max_cons = 256 # Maksimal koneksi [cite: 52]
        server.max_cons_per_ip = 5 # Maksimal koneksi per IP [cite: 53]

        print("="*60)
        print(" SERVER SIAP MENERIMA KONEKSI")
        print(f" Alamat   : ftp://127.0.0.1:2122")
        print(" User     : user")
        print(" Pass     : 12345")
        print("="*60)
        print(" TEKAN CTRL+C UNTUK MEMATIKAN SERVER")
        
        server.serve_forever() # Jalankan server terus menerus [cite: 63]

    except OSError as ex:
        print(f" Gagal start server: {ex}")
        print(" Pastikan port 2122 tidak sedang dipakai aplikasi lain.")
    except KeyboardInterrupt:
        server.close_all()
        print("\n\n Server dimatikan.")

if __name__ == "__main__":
    start_ftp_server()