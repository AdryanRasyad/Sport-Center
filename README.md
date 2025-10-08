TUGAS 3 :  Implementasi Form dan Data Delivery pada Django

1. Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
Data delivery menjadi bagian yang esensial dalam implementasi sebuah platform. Data delivery memastikan agar interaksi data atau pertukaran data berjalan dengan benar. Tanpa data delivery, informasi hanya tersimpan, tidak bisa ditampilkan atau dimanfaatkan pada webiste. Selain itu, data delivery memastikan pertukaran informasi berlangsung cepat, aman, konsisten, dan efisien sehingga pengalaman pengguna menjadi lebih baik serta platform dapat tetap berjalan meski jumlah pengguna meningkat.

2. Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?
Menurut saya, untuk pembuatan website saja, JSON lebih baik dibandingkan XML. Hal ini karena JSON lebih mudah dipahami, banyak bahasa pemrograman yang memiliki dukungan untuk membaca dan membuat JSON, serta berstuktur key dan value.

3. Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?
Method is_valid() pada form Django berfungsi untuk memastikan bahwa data yang dikirim user melalui form sesuai dengan aturan yang sudah didefinisikan di models.py. Jika tidak ada method tersebut, sembarang data dapat masuk ke database dan membuat error. 

4. Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?
csrf_token atau Cross Site Request Forgery token melindungi semua POST. Token dimasukkan ke setiap form yang terdapat di template, lalu dicek oleh server ketika data dikirim. Hal ini memastikan bahwa data form hanya berasal dari form yang memang kita buat. Jika tidak menambahkan csrf_token pada form Django, secara otomoatis server akan menolak request dari POST. Tanpa CSRF token, penyerang bisa melakukan Cross Site Request Forgery attack. Misalnya, saat kita login ke sebuah website dan website tersebut menggunakan cookie untuk autentikasi, penyerang dapat membuat halaman berisi form tersembunyi yang jika dibuka saat masih login, browser otomatis mengirim request ke server toko online dengan cookie yang valid. Hasilnya, uang dapat tertransfer tanpa disadari.

5. Penjelasan implementasi checklist secara step-by-step:

1) Menambahkan 4 fungsi views baru 
Pertama, pada views.py, import HttpResponse dan serializers. HttpResponse berfungsi untuk menyusun respon yang ingin dikembalikan oleh server ke user. Sedangkan, serializers akan digunakan untuk mentranslasikan model menjadi bentuk lain. Dalam hal ini, bentuk lain tersebut adalah xml dan json. Setelah itu, saya membuat fungsi:

def show_xml(request):
     product_list = Product.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

product_list = Product.objects.all() 
-> mengambil data dari tabel product di database yang hasilnya berupa quaryset.
xml_data = serializers.serialize("xml", product_list) dan json_data = serializers.serialize("json", product_list) 
-> Mengubah bentuk quaryset menjadi format xml dan json.
return HttpResponse(xml_data, content_type="application/xml") dan return HttpResponse(json_data, content_type="application/json")
-> Membungkus string XML dan JSON dalam HttpResponse supaya dapat dikirim ke browser.

def show_xml_by_id(request, product_id):
   try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, product_id):
   try:
        product_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)

Perbedaan dari kedua fungsi ini dari 2 fungsi sebelumnya adalah mengembalikan datanya menggunakan ID.
product_item = Product.objects.filter(pk=product_id) 
-> mencari data produk dengan primary key (pk) sama dengan product_id. Filter akan mengembalikan queryset, bukan data tunggal
xml_data = serializers.serialize("xml", product_item) dan json_data = serializers.serialize("json", [product_item])
-> Mengubah bentuk quaryset menjadi format xml dan json.
return HttpResponse(xml_data, content_type="application/xml") dan return HttpResponse(json_data, content_type="application/json")
-> Membungkus string XML dan JSON dalam HttpResponse supaya dapat dikirim ke browser.

2) Membuat routing URL
Sebelum menambahkan path, saya import semua fungsi yang sudah dibuat, yaitu show_xml, show_json, show_xml_by_id, show_json_by_id. Kemudian, saya menambahkan path :

path('xml/', show_xml, name='show_xml')
path('json/', show_json, name= 'show_json')
path('xml/<uuid:product_id>/', show_xml_by_id, name='show_xml_by_id')
path('json/<uuid:product_id>/', show_json_by_id, name='show_json_by_id')

3) Membuat halaman yang menampilkan data objek model yang memiliki tombol "Add" yang akan redirect ke halaman form, serta tombol "Detail" pada setiap data objek model yang akan menampilkan halaman detail objek.
Pada main.html, saya menambahkan tombol Add Product yang jika dipencet akan mengarah ke create_product yang terdapat di views.py. Lalu, di dalam loop produk, saya menambahkan tombol "Detail" yang mengarah ke show_products pada views.py. Dari create_product dan show_products, kedua fungsi ini akan me-render request ke create_product.html (untuk fungsi create_product) product_details.html (untuk fungsi show_products).

4) Membuat halaman form untuk menambahkan objek model pada app sebelumnya.
Pertama, saya membuat file create_product.html. Untuk menampilka form, saya menambahkan tag <form method="POST">, {% csrf_token %} untuk keamanan, dan {{ form.as_table }} untuk render form, serta menambahkan tombol submit 

5) Membuat halaman yang menampilkan detail dari setiap data objek model.
Pertama, saya membuat file product_detail.html. Di bagian atas, saya membuat tombol "Back to Catalog" yang jika diclick, akan kembali ke menu utama. Di bawahnya, saya menampilkan nama produk yang diikuti oleh kategori, label featured, dan tanggal produk dibuat, serta gambar thumbnail yang ditampilkan dengan ukuran lebar 300px. Selanjutnya, saya juga memasukkan deskripsi produk dan harga.

link pws : https://adryan-muhammad-sportcenter.pbp.cs.ui.ac.id


<img width="1440" height="900" alt="Screenshot 2025-09-17 at 07 56 17" src="https://github.com/user-attachments/assets/f4d3f9b5-0633-4571-b217-f308f3f0ef03" />
<img width="1440" height="900" alt="Screenshot 2025-09-17 at 07 57 01" src="https://github.com/user-attachments/assets/33ccc6e5-8776-4c11-8123-316394d8a52c" />
<img width="1440" height="900" alt="Screenshot 2025-09-17 at 07 57 31" src="https://github.com/user-attachments/assets/4762edc7-b381-413f-bfc1-3b48cc205b18" />
<img width="1440" height="900" alt="Screenshot 2025-09-17 at 07 55 56" src="https://github.com/user-attachments/assets/8edee3e4-bbab-45ec-8fa1-b2d35e25d582" />

TUGAS 4 : Implementasi Autentikasi, Session, dan Cookies pada Django

1. Django AuthenticationForm adalah form bawaan Django yang digunakan untuk proses login. Form ini ada di modul django.contrib.auth.forms yang berfungsi untuk meminta input username, password, serta melakukan validasi apakah kombinasi username dan password benar. kelebihan dari Django AuthenticationForm adalah tidak perlu membuat halaman login secara manual, keamanan yang baik, dan dapat dikustomisasi. Sedangkan, kekurangannya meliputi kesederhanaan cara login (hanya meminta username dan password) dan UI standar yang perlu dikostumisasi agar menarik.

2. Autentikasi adalah proses yang memverifikasi identitas pengguna. Sedangkan, otorisasi adalah proses menentukan hak akses pengguna setelah mereka terautentikasi. Dalam Django, autentikasi diimplementasikan melalui django.contrib.auth yang menyediakan model User, fungsi authenticate(), login(), logout(), serta form seperti AuthenticationForm untuk menangani login. Sementara itu, otorisasi diwujudkan dengan sistem permission dan group, yang memungkinkan pengecekan izin menggunakan user.has_perm(), serta pembatasan akses dengan dekorator seperti @login_required dan @permission_required.

3. Kelebihan dan Kekurangan :
     1) Session:
          - Kelebihan :
               Mudah diakses langsung oleh browser, sistem keamanannya lebih baik, dan kapasitas penyimpanan lebih besar dari cookie
          - Kekurangan :
               Menambah beban server karena data harus dikelola di server dan dara bisa hilang jika server restart atau session expired.
     2) Cookies
          - Kelebihan :
               Dapat menyimpan data lebih lama, tidak membebani server, cocok untuk menyimpan preferensi ringan.

4. Penggunaan cookies tidak sepenuhnya aman secara default karena ada beberapa risiko potensial seperti cookie theft (pencurian cookie melalui XSS), session hijacking (penggunaan cookie session oleh pihak ketiga), atau session fixation (pemaksaan pengguna memakai cookie tertentu). Django menangani hal tersebut dengan mengaktifkan atribut HttpOnly (mencegah akses cookie yang melalui JavaScript), Secure (agar cookie hanya dikirim melalui HTTPS jika diaktifkan), serta dukungan CSRF protection dan signed cookies (menggunakan kunci rahasia).

5. Langkah-langkah:
     - Registrasi
          1) Proses registrasi dimulai dengan import UserCreationForm dan messages pada views.py bawaan Django untuk menangani pendaftaran pengguna baru. Pada views.py, juga ditambahkan fungsi register. 
          2) Buat file html baru bernama register.html yang berfungsi untuk menampilkan form pada web. 
          3) Import register dan menambahkan path url ke dalam urlpatterns pada urls.py. 
     - Login
          1) Menambahkan import AuthenticationForm, authenticate, dan login pada view.py.
          2) Menambahkan fungsi login_user pada views.py. 
          3) Membuat file HTML baru dengan nama login.html yang berfungsi untuk menampilkan tampilan login untuk user.
          4) Import login_user dan menambahkan path url ke dalam urlpatterns pada urls.py. 
     - Logout
          1) Menambahkan import logout pada views.py
          2) Menambahkan fungsi logout_user
          3) Menambahkan kode untuk button logout pada main.html setelah tombol add product
          4) Import logout_user ke urls.py dan menambahkan path url ke urlpatters
     Supaya halaman main dan details ter-restriksi, import login_required pad  views.py dan tambahkan dekorator @login_required(login_url='/login') di atas fungsi show_main dan show_product.

     - Membuat dua (2) akun pengguna dengan masing-masing tiga (3) dummy data menggunakan model yang telah dibuat sebelumnya untuk setiap akun di lokal.
          1) Register 2 akun pengguna
          2) Login dengan username dan password yang sudah dibuat
          3) Setelah masuk, tekan tombol "add product"
          4) Isi nama barang, harga, deskripsi, jenis barang, is_featured, dan thumbnail
          4) Tekan "Add product"
          5) Lakukan secara berulang sampai 3 product dan ganti user yang belum dipakai untuk menambahkan product.
     
     - Menghubungkan model Product dengan User.
          1) Menambahkan field user pada models.py 
          2) Simpan request.user saat create product pada fungsi create_product views.py
          3) Modifikasi template product_detail.html dengan menambahkan product.user.username
     
     - Menampilkan detail informasi pengguna yang sedang logged in seperti username dan menerapkan cookies seperti last_login pada halaman utama aplikasi.
          1) Mengubah context pada show_main pada views.py -> 'name': request.user.username, 'last_login': request.COOKIES.get('last_login', 'Never')
          2) Menampilkan last_login pada main.html dengan <h5>Sesi terakhir login: {{ last_login }}</h5>

TUGAS 5

1.  Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!
     Jika terdapat beberapa CSS selector untuk suatu elemen HTML, maka prioritas utama adalah jika ada !important. Prioritas kedua adalah Inline Style di mana style diaplikasikan sebaris dengan elemen HTML yang bersangkutan. Ketiga adalah selector yang menargetkan elemen berdasarkan id uniknya. ID bersifat unik, hanya boleh ada satu nama ID yang sama per halaman. Prioritas berikutnya diikuti dengan class (Menargetkan elemen dengan class tertentu.), atribut (Menargetkan elemen berdasarkan atributnya.), dan pseudo-class (Menargetkan elemen dalam keadaan tertentu).
2. Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design, serta jelaskan mengapa!
     Responsive design menjadi konsep yang penting karena pengguna sekarang mengakses web dari berbagai perangkat. Apabila tampilan tidak menyesuaikan, pengguna bisa kesulitan membaca, menekan tombol, atau mengakses fitur. Akibatnya, user bisa cepat meninggalkan aplikasi (bounce rate tinggi).
     1) Contoh Aplikasi yang sudah menerapkan Responsive Design :
     - Tokopedia
     Jika dibuka di HP, tampilannya menyesuaikan dengan layar kecil, menampilkan ikon besar dan navigasi yang lebih sederhana. Sedankgan, jika dibuka di laptop, layout grid produk lebih lebar dan detail.
     2) Contoh Aplikasi yang belum menerapkan Responsive Design:
     - Pacil Web Service
     Jika dibuka di HP, tampilannya tidak menyesuaikan dengan layar kecil. Pengguna menjadi terganggu saat ingin aktivitas dalam web tersebut.

3. Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!
     Margin, border, dan padding adalah tiga konsep penting dalam CSS box model yang mengatur ruang di sekitar elemen HTML. Margin adalah ruang kosong di luar elemen yang memisahkan elemen tersebut dengan elemen lain di sekitarnya, sehingga berfungsi sebagai jarak antar elemen. Border adalah garis tepi yang membungkus konten dan padding, bisa memiliki ketebalan, warna, serta gaya (solid, dashed, dotted, dll.) untuk memperjelas batas elemen. Padding adalah ruang kosong di dalam elemen, tepat di antara konten (teks atau gambar) dan border yang berfungsi agar konten tidak menempel langsung pada tepi.
     Cara implementasi :
     .box {
          margin: 20px;         // jarak luar elemen
          border: 2px solid black;  // garis tepi hitam dengan ketebalan 2px 
          padding: 15px;        // jarak dalam antara konten dan border 
     }

4. Jelaskan konsep flex box dan grid layout beserta kegunaannya!
     Flexbox dan Grid Layout adalah dua sistem layout modern dalam CSS yang dirancang untuk mempermudah pengaturan posisi dan tata letak elemen di halaman web.
     1) Flexbox (Flexible Box Layout):
     Flexbox berfungsi untuk mengatur elemen dalam satu dimensi, yaitu baris (row) atau kolom (column). Konsep utamanya adalah membuat distribusi ruang yang fleksibel sehingga elemen dapat menyesuaikan ukuran layar secara otomatis. Flexbox cocok digunakan untuk mengatur item dalam navigasi, tombol, kartu produk, atau komponen yang tersusun dalam satu garis. 
     2) Grid Layout:
     Grid Layout memungkinkan pengaturan elemen dalam dua dimensi, yaitu baris (rows) dan kolom (columns) secara bersamaan. Dengan grid, kita bisa membagi halaman menjadi area-area tertentu, misalnya header, sidebar, content, dan footer, dengan kontrol yang presisi. Grid cocok dipakai untuk membangun struktur layout kompleks, seperti dashboard atau halaman majalah online.

5. Langkah-Langkah:
     - Implementasikan fungsi untuk menghapus dan mengedit product.
          1) Modifikasi views.py dengan menambahkan edit_product dan delete_product
          2) Menambahkan URL di urls.py untuk fungsi edit_product dan delete_product
          3) Membuat file edit_product.html untuk menampilkan halaman untuk edit product dan file 
          4) Tambahkan href link untuk edit product dan delete product.
     - Kustomisasi halaman login, register, tambah product, edit product, dan detail product semenarik mungkin.
          Menambahkan css pada login.html, register.html, create_product.html, edit_product.html, dan product_details.html seperti yang ada pada file tersebut.
     - Kustomisasi halaman daftar product menjadi lebih menarik dan responsive. Kemudian, perhatikan kondisi berikut:
          menggunakan pseudo-class CSS :hover yang memungkinkan perubahan gaya ketika kursor berada di atas elemen. Saya juga menggabungkannya dengan transition supaya fade-nya lebih halus.
     - Jika pada aplikasi belum ada product yang tersimpan, halaman daftar product akan menampilkan gambar dan pesan bahwa belum ada product yang terdaftar dan Jika sudah ada product yang tersimpan, halaman daftar product akan menampilkan detail setiap product dengan menggunakan card
          Menggunakan if dengan syarat apabila ada product yang tersimpan, maka tampilkan. Pesan ditampilkan beserta gambar bola yang terletak di static/image/bola.png
     - Untuk setiap card product, buatlah dua buah button untuk mengedit dan menghapus product pada card tersebut!
          Untuk menambahkan dua buah tombol Edit dan Hapus pada setiap card produk, langkah pertama adalah menempatkan elemen tombol di dalam card_product.html
     - Buatlah navigation bar (navbar) untuk fitur-fitur pada aplikasi yang responsive terhadap perbedaan ukuran device, khususnya mobile dan desktop.
          saya sudah membuat sebuah navigation bar (navbar) yang responsif dengan memanfaatkan Tailwind CSS dan sedikit JavaScript. Pada tampilan desktop (layar medium ke atas), menu navigasi ditampilkan dalam bentuk horizontal dengan link seperti Home dan Create Product, serta bagian user yang menampilkan identitas pengguna atau tombol Login/Register sesuai status autentikasi. Sementara itu, untuk tampilan mobile (layar kecil), menu utama disembunyikan dan diganti dengan tombol “hamburger” yang muncul di sisi kanan. Tombol ini dikendalikan oleh JavaScript sederhana yang menggunakan classList.toggle("hidden") untuk menampilkan atau menyembunyikan menu mobile. Bagian menu mobile juga menampilkan link navigasi dan user section, tetapi dengan layout vertikal yang lebih cocok untuk layar kecil.

TUGAS 6
1. Apa perbedaan antara synchronous request dan asynchronous request?
     Synchronous request adalah jenis permintaan di mana client harus menunggu server menyelesaikan proses dan mengirimkan respon terlebih dahulu sebelum dapat melanjutkan eksekusi kode berikutnya. Artinya, setiap request dijalankan secara berurutan, jika satu proses lama, maka proses lain akan ikut tertunda. Sedangkan Asynchronous request memungkinkan client untuk mengirim request ke server tanpa harus menunggu respon selesai terlebih dahulu.

2. Bagaimana AJAX bekerja di Django (alur request–response)?
     AJAX (Asynchronous JavaScript and XML) bekerja dengan cara mengirimkan request ke server secara asynchronous
     1) Request dari client
          Misal, client tekan tombol "Create Product".
     2) Browser mengirim request ke Django
          Request dikirim ke URL yang sudah didefinisikan di urls.py. Kemudian, fungsi add_product_entry_ajax di views.py menerima data dari request tersebut.
     3) Django memproses data di sisi server
          Fungsi view :
               - Menyimpan data produk baru ke database
               - Mengupdate atau menghapus data tertentu
               - Atau mengambil data dari model
     4) Server mengirim response kembali ke browser
     5) Browser menerima dan menampilkan hasil tanpa reload

3. Apa keuntungan menggunakan AJAX dibandingkan render biasa di Django?
     1) Tidak perlu reload seluruh halaman
     2) Performa lebih cepat
     3) Lebih interaktif dengan pengguna
     4) Dapat dikombinasikan dengan JSON API
4. Bagaimana cara memastikan keamanan saat menggunakan AJAX untuk fitur Login dan Register di Django?
     Dalam implementasi AJAX pada fitur Login dan Register di proyek ini, keamanan tetap dijaga dengan memanfaatkan mekanisme bawaan Django dan beberapa praktik tambahan.
     - Menggunakan sistem autentikasi bawaan Django
     - Validasi input & sanitasi data
     - Perlindungan CSRF (Cross Site Request Forgery)
     - Pembatasan akses menggunakan @login_required
5. Bagaimana AJAX mempengaruhi pengalaman pengguna (User Experience) pada website?
     Penggunaan AJAX secara signifikan meningkatkan User Experience (UX) karena membuat interaksi di website menjadi lebih cepat, interaktif, dan responsif tanpa perlu me-reload seluruh halaman. Dengan AJAX:
     - Pengguna bisa menambah, mengedit, dan menghapus produk secara langsung tanpa meninggalkan halaman utama.
     - Loading, Empty, dan Error state memberi umpan balik visual yang jelas saat data sedang dimuat atau gagal diambil
     - Toast Notification muncul setiap kali terjadi aksi (seperti create/update/delete/login/logout), memberi tahu pengguna hasil secara real time.
     - Tombol “Refresh Products” memungkinkan pengguna melihat daftar produk terbaru tanpa memuat ulang halaman browser, membuat pengalaman terasa mulus.

     
          
