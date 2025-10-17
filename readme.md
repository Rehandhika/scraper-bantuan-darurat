# Scraper Bantuan Darurat

Sistem web scraping otomatis untuk estimasi harga barang bantuan darurat dari Blibli dan Lazada berdasarkan standar BNPB.

## Fitur Utama

- Scraping otomatis 6 kategori bantuan (air, beras, mi instan, minyak goreng, gula, selimut)
- Filter lokasi 34 provinsi Indonesia
- Cleaning outlier dengan metode IQR
- Kalkulasi kebutuhan BNPB otomatis
- Export CSV detail produk & ringkasan biaya
- Anti-bot detection (undetected-chromedriver)

## Instalasi

git clone
cd scraper-bantuan-darurat
pip install -r requirements.txt

**Prasyarat:** Python 3.8+, Chrome browser

## Cara Pakai

Ikuti instruksi:
1. Input jumlah korban (contoh: 1000)
2. Input lokasi bencana (contoh: Jakarta Selatan)  
3. Pilih filter provinsi (0=nasional, 1=DKI Jakarta, dst.)

Sistem akan menghasilkan 2 file CSV:
- `detail_produk_[lokasi]_[provinsi]_[timestamp].csv` - Semua produk hasil scraping
- `ringkasan_biaya_[lokasi]_[provinsi]_[timestamp].csv` - Total biaya per kategori

## Teknologi
Python • Selenium • BeautifulSoup4 • Pandas • undetected-chromedriver

## Tim Pengembang
Rehandhika Arya Pratama dan Vicky Adi Saputro 
untuk Lomba Karya Tulis Ilmiah Red Compass 2025
