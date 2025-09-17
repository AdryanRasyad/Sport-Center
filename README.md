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



