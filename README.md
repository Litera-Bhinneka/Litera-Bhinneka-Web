# Litera - Web
Aplikasi pertukaran buku berbasis website dengan fitur daftar katalog buku, review buku, permintaan pertukaran buku secara online, rekomendasi buku, dan informasi pengguna. 

# Link
Link to Website: [LINK](http://litera-b06-tk-tutorial.pbp.cs.ui.ac.id)

## Anggota Kelompok👥
- Andhika Reihan Hervito (2206826324)
- Catherine Hana Natalie (2206083123)
- Ghana Ahmada Yudistira (2206824760)
- Muhammad Rafli Darmawan (2206828052)
- Muhammad Raihan Akbar (2206827674)

## Cerita Aplikasi dan Manfaat 🍃
Aplikasi ini dirancang sebagai platform pertukaran buku yang menyediakan fitur-fitur dengan antarmuka intuitif untuk menjelajahi, memilih, dan bertukar buku dengan mudah kepada pengguna. Dengan fitur-fitur seperti daftar katalog buku, permintaan pertukaran buku secara online, ulasan pengguna, rekomendasi buku, dan informasi pengguna, aplikasi ini memfasilitasi pertukaran buku yang efisien dan bermakna. Melalui aplikasi ini, pengguna dapat berbagi pengetahuan dengan pengguna lainnya dan mendukung budaya literasi dalam bentuk yang ramah lingkungan dan ekonomis. Aplikasi ini bisa menjadi kontribusi yang besar dalam meningkatkan tingkat literasi para pengguna.

Aplikasi ini menawarkan kemudahan bagi pengguna untuk menemukan buku yang mereka cari dengan cepat dan mudah melalui daftar katalog buku yang lengkap. Selain itu, pengguna dapat berinteraksi dengan komunitas pembaca lainnya, berbagi ulasan dan tanggapan, serta mendapatkan inspirasi dari pengalaman membaca orang lain. Selain itu, pengguna juga dapat memperluas koleksi buku mereka tanpa biaya tambahan dengan menukar buku yang sudah mereka baca dengan buku baru yang diinginkan.

Melalui fitur-fitur yang disediakan, aplikasi ini tidak hanya mempermudah pertukaran buku, tetapi juga memberikan manfaat yang signifikan bagi pengguna dan masyarakat secara keseluruhan.

## Daftar Modul 📃
### 1. Homepage - Andhika Reihan Hervito dan Ghana Ahmad Yudistira
Di halaman ini, pengguna dapat melihat pilihan modul yang tersedia melalui desain *card*.

### 2. Halaman Login dan Register - Andhika Reihan Hervito dan Ghana Ahmada Yudistira
Pada halaman ini, terdapat formulir untuk masuk ke sistem aplikasi, yang dapat diakses oleh administrator dan pengguna yang telah masuk ke dalam akun mereka. Selain itu, terdapat opsi untuk membuat akun baru dengan mengklik tautan yang mengarahkan pengguna ke halaman pendaftaran.

### 3. Book Catalog - Catherine Hana Natalie
Dalam modul `Book Catalog`, pengguna dapat menjelajahi daftar buku yang tersedia untuk pertukaran dan melakukan pencarian berdasarkan judul, penulis, atau kategori. Mereka memiliki akses ke informasi detail buku, termasuk deskripsi, penulis, dan status ketersediaan. Pengguna dapat menambahkan buku yang tidak terdapat katalog. Di sisi lain, admin memiliki kontrol penuh atas katalog buku dengan kemampuan untuk menambahkan buku baru, mengelola status ketersediaan buku, dan menghapus buku dari katalog.

### 4. Book Exchange - Muhammad Raihan Akbar
Dalam modul `Book Exchange`, pengguna memiliki kemampuan untuk membuat permintaan pertukaran buku dengan pengguna lain melalui sistem permintaan online. Pengguna mengisi detail buku yang ingin ditukar dan mengirimkan permintaan kepada pemilik buku yang diinginkan. Setelahnya, pengguna dapat melihat permintaan yang diterima dan memiliki opsi untuk menerima atau menolaknya. Jika permintaan diterima, pertukaran buku dapat dilakukan dengan pengguna yang diminta. Pengguna yang menerima permintaan harus mengonfirmasi pertukaran, mengikuti petunjuk langkah demi langkah yang diberikan oleh sistem, termasuk lokasi pertemuan, waktu, dan instruksi khusus jika ada.

### 5. Review Buku - Ghana Ahmada Yudistira
Dalam modul `Review Buku`, pengguna memiliki beberapa fungsi penting. Pertama, mereka dapat melihat semua ulasan dan komentar pengguna lain mengenai buku tertentu, termasuk penilaian bintang, memberi mereka wawasan sebelum membaca buku tersebut. Pengguna juga dapat menulis ulasan dan memberikan penilaian bintang terhadap buku yang telah mereka baca, memberikan komentar, kesan, serta saran kepada pengguna lain yang mungkin tertarik dengan buku tersebut. Selain itu, pengguna memiliki kemampuan untuk memberikan respon atau tanggapan terhadap ulasan yang diposting oleh pengguna lain, memungkinkan interaksi dan berbagi pengalaman di antara komunitas pembaca. Pengguna juga dapat melihat peringkat buku berdasarkan ulasan pengguna, yang dihitung berdasarkan rata-rata penilaian bintang.

### 6. Rekomendasi Buku - Andhika Reihan Hervito
Dalam modul `Rekomendasi Buku`, Pengguna memiliki opsi untuk membuat rekomendasi buku. Rekomendasi ini terdiri dari dua buku, sehingga jika pengguna menikmati suatu buku A, kemungkinan besar pengguna juga akan menyukai suatu buku B yang direkomendasi oleh pengguna lain. Selain itu, pengguna juga bisa membuat rekomendasi baru yang nantinya akan tampil di laman tersebut.

### 7. Informasi Pengguna - Muhammad Rafli Darmawan
Dalam modul `Informasi Pengguna`,  Pengguna juga memiliki opsi untuk menambahkan buku yang diminati ke dalam wishlist mereka untuk ditukar di masa mendatang, dan pengguna memiliki kemampuan untuk melihat buku-buku yang mereka simpan dalam *wishlist*, memberikan gambaran tentang buku-buku yang menarik minat mereka. Mereka juga dapat melihat koleksi buku yang dimiliki, memberikan wawasan tentang buku-buku yang telah mereka baca atau miliki. Selain itu, pengguna memiliki akses ke histori pertukaran buku, memungkinkan mereka melihat catatan transaksi pertukaran sebelumnya.


## Sumber Dataset Katalog Buku 📚
Kaggle: https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews?select=Books_rating.csv

Sumber dataset katalog buku mengenai Amazon Book Reviews dari Kaggle menyediakan berbagai atribut buku, seperti tampilan cover buku, nama penulis buku, kategori buku, rating buku, dan reviews buku. Atribut buku yang disediakan dari dataset dibutuhkan untuk menjalankan modul-modul yang sudah dipaparkan sebelumnya.

## Peran Pengguna👤

### 1. User

User memiliki otoritas untuk mengakses welcome page, menambahkan buku ke katalog, menambahkan buku ke dalam inventori user tersebut, menulis *review* buku, membuat rekomendasi dan menawarkan pertukaran buku ke user lain.

### 2. Admin

Admin atau administrator berperan sebagai pemegang kendali website dan memiliki akses penuh untuk memodifikasi buku, rekomendasi, dan melihat user database melalui dashboard admin.

### 3. Guest

Guest atau user yang belum log in hanya memiliki kekuatan mengakses yang paling rendah

## User Diagram 📊

![User Diagram](assets/images/user_story.png)
