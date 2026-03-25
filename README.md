[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mRmkZGKe)
# Network Programming - Assignment G01

## Anggota Kelompok
| Nama           | NRP        | Kelas     |
| ---            | ---        | ----------|
| Akmal Yusuf    | 5025241212 | C         |
|                |            |           |

## Link Youtube (Unlisted)
Link ditaruh di bawah ini
```
https://youtu.be/zw4ebf-N-JY
```

## Penjelasan Program
Proyek ini adalah implementasi sistem Client-Server berbasis protokol TCP menggunakan bahasa pemrograman Python. Proyek ini mendemonstrasikan empat arsitektur server yang berbeda untuk menangani blocking I/O, serta implementasi client berbasis multithreading.

Terdapat beberapa file dummy yang dapat digunakan untuk mendemonstrasikan program yang tersimpan pada folder `files` dan `saved`. Folder `files` dimaksudkan untuk dimiliki oleh server, sedangkan folder `saved` adalah milik client. Penggunaan folder bertujuan untuk menjaga kerapian files.

How to run:
1. Menjalankan Server
Buka terminal dan jalankan salah satu dari empat skrip server yang tersedia. Contoh:
```
python3 server-threads.py
```
2. Menjalankan Klien
Buka terminal baru (bisa buka beberapa terminal sekaligus untuk menyimulasikan banyak klien), lalu jalankan:
```
python3 client.py
```

3. Daftar Perintah (Commands) di Klien
- Ketik pesan biasa: Pesan akan di-broadcast ke seluruh klien lain yang terhubung.
- `/list`: Melihat daftar file yang tersedia di folder `files/` milik server.
- `/download <nama_file>`: Mengunduh file dari server dan menyimpannya ke folder `saved/` klien. (Contoh: /download beluga.png)
- `/upload <nama_file>`: Mengunggah file dari folder `saved/` klien ke folder files/ server. (Contoh: /upload gokil.jpg)


## Screenshot Hasil

### Syncronus Server
Test Broadcast
<img width="1524" height="161" alt="image" src="https://github.com/user-attachments/assets/48b0fea4-a8a3-4d84-8cf0-82adc56fcd41" />

Test Download and Upload
<img width="1454" height="307" alt="image" src="https://github.com/user-attachments/assets/964526be-98c0-49e0-87fd-5a3c31c50113" />

Before 

<img width="297" height="167" alt="image" src="https://github.com/user-attachments/assets/a930ed4e-303a-4c63-b414-15072978a4f7" />

After

<img width="302" height="214" alt="image" src="https://github.com/user-attachments/assets/eb97fe4f-310a-4f89-a7a4-8a9ce2996f1f" />


### Select Server

<img width="1514" height="192" alt="image" src="https://github.com/user-attachments/assets/99cd770d-c8af-46b1-a9cf-0c8cc93fee7d" />

<img width="1515" height="255" alt="image" src="https://github.com/user-attachments/assets/e9a11835-9a96-4d6d-9e45-a7bee62366fd" />

Before

<img width="306" height="167" alt="image" src="https://github.com/user-attachments/assets/4dcdb43e-a973-4047-94aa-53ec75cac345" />

After

<img width="1523" height="320" alt="image" src="https://github.com/user-attachments/assets/080f4e10-9ecf-467c-978a-7fccfc5b6b54" />

<img width="311" height="217" alt="image" src="https://github.com/user-attachments/assets/685b705a-8bcf-47a6-8685-9ab2e264e39f" />

<img width="1529" height="371" alt="image" src="https://github.com/user-attachments/assets/f88f3664-e003-4b48-846e-d617142e1f40" />

### Poll Server

<img width="1520" height="239" alt="image" src="https://github.com/user-attachments/assets/f3dc322d-ad3e-4c4a-b738-81cbfdf606e8" />

<img width="1606" height="292" alt="image" src="https://github.com/user-attachments/assets/39cd34f3-c9d2-466a-8926-015802433715" />

<img width="304" height="215" alt="image" src="https://github.com/user-attachments/assets/7578a8f5-ded9-4e7b-80f6-a4add0c5cc43" />

### Threads Server

<img width="1527" height="425" alt="image" src="https://github.com/user-attachments/assets/123dfaa1-cd2b-40fa-bcca-ea5ada5b70c5" />

<img width="312" height="164" alt="image" src="https://github.com/user-attachments/assets/5a1196a5-6b15-4e50-b4eb-66d53fd5e4e0" />


<img width="314" height="211" alt="image" src="https://github.com/user-attachments/assets/a9dee70f-a0e4-4628-b7e8-10e5205ea7d8" />

