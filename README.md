1. Penjelasan setiap checklist:
- Membuat sebuah proyek django baru:
Pertama, saya membuat direktori sport-center. Selanjutnya, saya menginstal django dan beberapa dependencies lainnya yang diperlukan dengan menuliskannya pada file requirements.txt yang kemudian di-install melalui terminal. Setelah itu, saya membuatJe file .env dan .env.prod. .env digunakan untuk development lokal sehingga aplikasi akan menggunakan database SQLite. Sedangkan, .env.prod digunakan untuk production deployment. Dengan PRODUCTION=True, maka aplikasi akan menggunakan database PostgreSQL. Langkah selanjutnya adalah memodifikasi settings.py agar program dapat mengakses environment variables yang sudah dibuat pada .env dan .env.prod.Selain itu, saya juga menambahkan "localhost", "127.0.0.1" (perangkat saya sendiri) ke dalam list ALLOWED_HOST. Kemudian, saya menambahkan konfigurasi PRODUCTION yang berfungsi untuk membedakan antara development dan production. Adapun konfigurasi database yang saya tambahkan yang di mana jika PRODUCTION=True, maka Django akan memakai PostgreSQL yang kredensialnya serupa dengan environment variables. Jika PRODUCTION=False, maka Django akan memakai SQLite untuk development lokal. Langkah berikutnya adalah migrasi databse melalui terminal dengan perintah python3 manage.py migrate. Setelah itu server dijalankan dengan python3 manage.py runserver.
- Membuat aplikasi dengan nama "main" & Membuat model pada aplikasi main dengan nama Product:
Untuk membuat aplikasi baru bernama "main", saya menjalankan perintah python manage.py startapp main. Aplikasi ini perlu didaftarkan ke dalam proyek dengan cara menambahkan "main" pada INSTALLED_APPS yang terdapat di settings.py. Dalam direktori "main", saya menambahkan direktori template yang berisi main.html untuk menampilkan nama aplikasi, nama saya, dan kelas. Selanjutnya, dalam models.py, saya membuat CATEGORY_CHOICES dan fields name, price, description, thumbnail, category, serta is_featured. Setelah itu, saya migrasi model agar Django melacak perubahan model basis data. Lengkah berikutnya adalah menghubungkan view dengan template yang diawal dengan import render untuk render tampilan HTML. Saya juga menambahkan fungsi show_main yang mengatur permintaan HTTP dan mengembalikan tampilan yang sesuai. 
- Routing:
Dalam direktori main, saya membuat file urls.py yang isinya meng-import path dari django.urls dan show_main dari main.views (Akan dipanggil saat URL cocok dengan pola yang ditentukan). app_name = 'main' dipakai untuk memberi namespace unik pada URL sebuah aplikasi, supaya tidak bentrok jika ada banyak app di proyek Django, urlpatterns adalah daftar rute (route) yang didefinisikan dengan fungsi, dan untuk name=show_main sebenarnya opsional yang berguna untuk reverse URL nantinya. Terakhir, saya meng-import path dan include pada urls.py yang ada dalam direktori sport-center untuk mengimpor pola rute URL dari aplikasi main (include) dan mendefinisikan pola URL (path). Pada urlpatterns saya menambahkan path('', include('main.urls')) untuk mengarahkan semua request dengan URL ("").
- Membuat sebuah fungsi pada views.py
Pada aplikasi main, saya buka views.py dan membuat fungsi show_main yang menerima request lalu membuat dictionary context berisi data seperti nama dan kelas, kemudian mengirimkan data tersebut ke template main.html agar dapat ditampilkan di halaman web.
-Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py. :
Mengimpor views ke dalam urls.py pada aplikasi main dilakukan agar fungsi yang sudah dibuat dapat dipanggil melalui routing, misalnya dengan menggunakan path('', views.show_name, name='show_name')

2. ![S__7839747](https://github.com/user-attachments/assets/ee6e5d9b-e0a1-4c8a-9a93-f04fb99e5ae3)


3. Peran settings.py dalam proyek Django:
Peran settings.py adalah sebagai konfigurasi utama yang isinya pengaturan aplikasi, seperti konfigurasi database, daftar aplikasi yang digunakan, middleware, template, zona waktu, bahasa,serta pengaturan keamanan. Secara singkat, settings.py menentukan bagaimana proyek Django dijalankan baik di lingkungan development maupun production.

4. Bagaimana cara kerja migrasi database di Django?
Ketika kita menjalankan python manage.py makemigrations, Django membaca perubahan pada model dan membuat file migrasi. Setelah itu, saat kita jalankan python manage.py migrate, Django akan mengeksekusi file migrasi tersebut ke database.

5. Menurut saya Django menjadi framework yang digunakan untuk permulaan karena menggunakan bahasa python yang mudah dipahami pemula, menyediakan fitur bawaan sehingga tidak harus membuat kode dari awal, dan dapat beroprasi di berbagai OS (Windows, MacOS, dan Linux).

link PWS : https://adryan-muhammad-sportcenter.pbp.cs.ui.ac.id
