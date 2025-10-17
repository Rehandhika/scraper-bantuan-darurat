import time
import pandas as pd
import undetected_chromedriver as uc
import re
from datetime import datetime
import statistics
from urllib.parse import quote_plus
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup



PROVINSI_INDONESIA = {
    1: {"nama": "DKI Jakarta", "blibli": "DKI+Jakarta", "lazada": "A-ID-1"},
    2: {"nama": "Jawa Barat", "blibli": "Jawa+Barat", "lazada": "A-ID-2"},
    3: {"nama": "Jawa Tengah", "blibli": "Jawa+Tengah", "lazada": "A-ID-3"},
    4: {"nama": "Jawa Timur", "blibli": "Jawa+Timur", "lazada": "A-ID-4"},
    5: {"nama": "Banten", "blibli": "Banten", "lazada": "A-ID-1"},
    6: {"nama": "DI Yogyakarta", "blibli": "DI+Yogyakarta", "lazada": "A-ID-3"},
    7: {"nama": "Bali", "blibli": "Bali", "lazada": "A-ID-5"},
    8: {"nama": "Sumatera Utara", "blibli": "Sumatera+Utara", "lazada": "A-ID-6"},
    9: {"nama": "Sumatera Selatan", "blibli": "Sumatera+Selatan", "lazada": "A-ID-8"},
    10: {"nama": "Sumatera Barat", "blibli": "Sumatera+Barat", "lazada": "A-ID-11"},
    11: {"nama": "Lampung", "blibli": "Lampung", "lazada": "A-ID-8"},
    12: {"nama": "Riau", "blibli": "Riau", "lazada": "A-ID-7"},
    13: {"nama": "Jambi", "blibli": "Jambi", "lazada": "A-ID-10"},
    14: {"nama": "Bengkulu", "blibli": "Bengkulu", "lazada": "A-ID-8"},
    15: {"nama": "Aceh", "blibli": "Aceh", "lazada": "A-ID-9"},
    16: {"nama": "Kalimantan Barat", "blibli": "Kalimantan+Barat", "lazada": "A-ID-13"},
    17: {"nama": "Kalimantan Tengah", "blibli": "Kalimantan+Tengah", "lazada": "A-ID-13"},
    18: {"nama": "Kalimantan Selatan", "blibli": "Kalimantan+Selatan", "lazada": "A-ID-13"},
    19: {"nama": "Kalimantan Timur", "blibli": "Kalimantan+Timur", "lazada": "A-ID-13"},
    20: {"nama": "Kalimantan Utara", "blibli": "Kalimantan+Utara", "lazada": "A-ID-13"},
    21: {"nama": "Sulawesi Utara", "blibli": "Sulawesi+Utara", "lazada": "A-ID-14"},
    22: {"nama": "Sulawesi Tengah", "blibli": "Sulawesi+Tengah", "lazada": "A-ID-14"},
    23: {"nama": "Sulawesi Selatan", "blibli": "Sulawesi+Selatan", "lazada": "A-ID-14"},
    24: {"nama": "Sulawesi Tenggara", "blibli": "Sulawesi+Tenggara", "lazada": "A-ID-14"},
    25: {"nama": "Gorontalo", "blibli": "Gorontalo", "lazada": "A-ID-14"},
    26: {"nama": "Sulawesi Barat", "blibli": "Sulawesi+Barat", "lazada": "A-ID-14"},
    27: {"nama": "Nusa Tenggara Barat", "blibli": "Nusa+Tenggara+Barat", "lazada": "A-ID-15"},
    28: {"nama": "Nusa Tenggara Timur", "blibli": "Nusa+Tenggara+Timur", "lazada": "A-ID-15"},
    29: {"nama": "Maluku", "blibli": "Maluku", "lazada": "A-ID-16"},
    30: {"nama": "Maluku Utara", "blibli": "Maluku+Utara", "lazada": "A-ID-16"},
    31: {"nama": "Papua", "blibli": "Papua", "lazada": "A-ID-16"},
    32: {"nama": "Papua Barat", "blibli": "Papua+Barat", "lazada": "A-ID-16"},
    33: {"nama": "Papua Selatan", "blibli": "Papua+Selatan", "lazada": "A-ID-16"},
    34: {"nama": "Papua Tengah", "blibli": "Papua+Tengah", "lazada": "A-ID-16"}
}


STANDAR_BNPB = {
    "air_mineral": {
        "nama": "Air Mineral", "kebutuhan_per_jiwa_per_hari": 2.5, "satuan": "liter",
        "keyword": "air mineral 600ml dus", "konversi": 14.4, "prioritas": 1
    },
    "beras": {
        "nama": "Beras", "kebutuhan_per_jiwa_per_hari": 0.4, "satuan": "kg",
        "keyword": "beras 5kg", "konversi": 5.0, "prioritas": 2
    },
    "mi_instan": {
        "nama": "Mi Instan", "kebutuhan_per_jiwa_per_hari": 3, "satuan": "bungkus",
        "keyword": "indomie 1 dus", "konversi": 40, "prioritas": 3
    },
    "minyak_goreng": {
        "nama": "Minyak Goreng", "kebutuhan_per_keluarga_3_hari": 1.0, "satuan": "liter",
        "keyword": "minyak goreng 2 liter", "konversi": 2.0, "prioritas": 4
    },
    "gula_pasir": {
        "nama": "Gula Pasir", "kebutuhan_per_keluarga_3_hari": 1.0, "satuan": "kg",
        "keyword": "gula pasir 1kg", "konversi": 1.0, "prioritas": 5
    },
    "selimut": {
        "nama": "Selimut", "kebutuhan_per_keluarga": 2, "satuan": "buah",
        "keyword": "selimut tebal", "konversi": 1.0, "prioritas": 6
    }
}


HARGA_FALLBACK = {
    "air_mineral": 40000, "beras": 65000, "mi_instan": 120000,
    "minyak_goreng": 28000, "gula_pasir": 15000, "selimut": 45000
}



def tampilkan_provinsi():
    print("\n" + "="*80)
    print("📍 DAFTAR PROVINSI INDONESIA")
    print("="*80)
    
    for idx, prov in PROVINSI_INDONESIA.items():
        print(f"  {idx:2d}. {prov['nama']}")
    
    print("\n   0. Nasional (Tanpa Filter Lokasi)")
    print("="*80)



def pilih_provinsi():
    tampilkan_provinsi()
    
    while True:
        try:
            pilihan = input("\nPilih nomor provinsi (0-34): ").strip()
            if not pilihan:
                continue
            
            pilihan = int(pilihan)
            
            if pilihan == 0:
                print("✅ Menggunakan harga Nasional")
                return None
            elif pilihan in PROVINSI_INDONESIA:
                prov = PROVINSI_INDONESIA[pilihan]
                print(f"✅ Filter lokasi: {prov['nama']}")
                return pilihan
            else:
                print("❌ Pilihan tidak valid! Pilih 0-34")
        except ValueError:
            print("❌ Input harus angka!")
        except KeyboardInterrupt:
            print("\n⚠️ Dibatalkan")
            return None



def bersihkan_harga(teks):
    if not teks:
        return 0
    
    angka = re.sub(r'\D', '', teks)
    if not angka:
        return 0
    
    try:
        harga = int(angka)
        return harga if harga >= 5000 else 0
    except:
        return 0



def remove_outliers_iqr(data, multiplier=1.5):
    if len(data) < 4:
        return data, [], {}
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    q1 = sorted_data[n // 4]
    q2 = sorted_data[n // 2]
    q3 = sorted_data[(3 * n) // 4]
    
    iqr = q3 - q1
    lower_fence = q1 - (multiplier * iqr)
    upper_fence = q3 + (multiplier * iqr)
    
    cleaned = [x for x in sorted_data if lower_fence <= x <= upper_fence]
    outliers = [x for x in sorted_data if x < lower_fence or x > upper_fence]
    
    stats = {
        'q1': q1, 'q2': q2, 'q3': q3, 'iqr': iqr,
        'lower_fence': lower_fence, 'upper_fence': upper_fence,
        'total_original': len(data), 'total_cleaned': len(cleaned),
        'outliers_removed': len(outliers),
        'outliers_pct': (len(outliers) / len(data)) * 100 if data else 0
    }
    
    return cleaned, outliers, stats



def scrape_blibli(keyword, provinsi_id, num_pages=3):
    print(f"\n🔵 BLIBLI - {keyword}")
    
    if provinsi_id:
        prov = PROVINSI_INDONESIA[provinsi_id]
        location = prov['blibli']
        print(f"   📍 Lokasi: {prov['nama']}")
    else:
        location = None
        print(f"   📍 Lokasi: Nasional")
    
    print(f"   📄 Target: {num_pages} halaman")
    
    all_products = []
    driver = None
    
    try:
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = uc.Chrome(options=options, use_subprocess=True)
        driver.set_page_load_timeout(60)
        
        keyword_encoded = quote_plus(keyword)
        
        for page in range(1, num_pages + 1):
            if page == 1:
                url = f"https://www.blibli.com/cari/{keyword_encoded}"
                if location:
                    url += f"?location={location}"
            else:
                start = (page - 1) * 36
                url = f"https://www.blibli.com/cari/{keyword_encoded}?page={page}&start={start}"
                if location:
                    url += f"&location={location}"
            
            print(f"   📄 Halaman {page}/{num_pages} - Loading...")
            driver.get(url)
            
            wait_time = 20 if page == 1 else 12
            time.sleep(wait_time)
            
            for i in range(5):
                driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {(i+1)*20}/100);")
                time.sleep(2)
            
            time.sleep(5)
            
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rp') and string-length(text()) > 2]"))
                )
            except:
                pass
            
            product_cards = driver.find_elements(
                By.XPATH,
                "//div[contains(@data-testid, 'product-list-container')]"
            )
            
            if not product_cards:
                product_cards = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'product') and .//a[@href]]"
                )
            
            success_count = 0
            for idx, card in enumerate(product_cards, 1):
                try:
                    try:
                        link_elem = card.find_element(By.TAG_NAME, "a")
                        link = link_elem.get_attribute("href")
                    except:
                        link = ""
                    
                    nama = ""
                    nama_strategies = [
                        ".//div[contains(@class, 'els-product__title-wrapper')]//span[@data-v-1c3396be]",
                        ".//span[@data-v-1c3396be and contains(@class, 'multiline-title')]",
                        ".//span[@data-v-1c3396be and string-length(text()) > 10]",
                        ".//div[contains(@class, 'product') and contains(@class, 'title')]//span",
                        ".//h2//span"
                    ]
                    
                    for strategy in nama_strategies:
                        try:
                            nama_elems = card.find_elements(By.XPATH, strategy)
                            for elem in nama_elems:
                                text = elem.text.strip()
                                if text and len(text) > 5 and not text.startswith('Rp'):
                                    nama = text
                                    break
                            if nama:
                                break
                        except:
                            continue
                    
                    if not nama:
                        try:
                            nama = link_elem.get_attribute("title")
                        except:
                            pass
                    
                    if not nama and link:
                        path_parts = link.split('/')
                        for part in reversed(path_parts):
                            if len(part) > 10 and not part.startswith('ps--'):
                                nama = part.replace('-', ' ').title()
                                break
                    
                    nama = nama[:150] if nama else "Unknown Product"
                    
                    price_text = ""
                    price_strategies = [
                        ".//div[contains(@class, 'els-product__price-top')]//span[@data-v-1c3396be]",
                        ".//div[contains(@class, 'els-product__fixed-price-wrapper')]//span[@data-v-1c3396be]",
                        ".//span[contains(text(), 'Rp') and string-length(text()) > 5]",
                        ".//div[contains(@class, 'price')]//span[string-length(text()) > 5]",
                        ".//*[contains(text(), 'Rp')]"
                    ]
                    
                    for strategy in price_strategies:
                        try:
                            price_elems = card.find_elements(By.XPATH, strategy)
                            for price_elem in price_elems:
                                text = price_elem.text.strip()
                                if text and len(text) > 2 and ('Rp' in text or text.replace('.', '').isdigit()):
                                    price_text = text
                                    break
                            if price_text:
                                break
                        except:
                            continue
                    
                    if not price_text:
                        all_text = card.text
                        price_match = re.search(r'Rp\s*([\d.]+)', all_text)
                        if price_match:
                            price_text = price_match.group(0)
                    
                    harga = bersihkan_harga(price_text)
                    
                    if harga > 5000:
                        product_data = {
                            'marketplace': 'Blibli',
                            'nama_produk': nama,
                            'harga': harga,
                            'link': link if link else ""
                        }
                        all_products.append(product_data)
                        success_count += 1
                        
                except Exception as e:
                    continue
            
            print(f"      ✓ {success_count} produk berhasil")
            
            if page < num_pages:
                time.sleep(5)
        
        driver.quit()
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:80]}")
        if driver:
            try:
                driver.quit()
            except:
                pass
    
    blibli_products = [p for p in all_products if p['marketplace'] == 'Blibli']
    print(f"   ✅ Total: {len(blibli_products)} produk")
    return blibli_products



def scrape_lazada(keyword, provinsi_id, num_pages=3):
    print(f"\n🟠 LAZADA - {keyword}")
    
    if provinsi_id:
        prov = PROVINSI_INDONESIA[provinsi_id]
        location = prov['lazada']
        print(f"   📍 Lokasi: {prov['nama']}")
    else:
        location = None
        print(f"   📍 Lokasi: Nasional")
    
    print(f"   📄 Target: {num_pages} halaman")
    
    all_products = []
    driver = None
    
    try:
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = uc.Chrome(options=options, use_subprocess=True)
        driver.set_page_load_timeout(60)
        
        keyword_encoded = quote_plus(keyword)
        
        for page in range(1, num_pages + 1):
            url = f"https://www.lazada.co.id/catalog/?q={keyword_encoded}"
            
            if location:
                url += f"&location={location}"
            
            if page > 1:
                url += f"&page={page}"
            
            print(f"   📄 Halaman {page}/{num_pages} - Loading...")
            driver.get(url)
            
            wait_time = 12 if page == 1 else 8
            time.sleep(wait_time)
            
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            products = soup.find_all('div', {'data-qa-locator': 'product-item'})
            
            if not products:
                products = soup.find_all('div', class_=re.compile(r'.*product.*item.*', re.I))
            
            success_count = 0
            for idx, product in enumerate(products, 1):
                try:
                    nama_elem = product.find('div', class_=re.compile(r'.*title.*|.*name.*', re.I))
                    if not nama_elem:
                        nama_elem = product.find('a', {'title': True})
                    nama = nama_elem.text.strip() if nama_elem else nama_elem.get('title', 'Unknown') if hasattr(nama_elem, 'get') else "Unknown"
                    
                    link_elem = product.find('a', href=True)
                    link = link_elem['href'] if link_elem else ""
                    if link and not link.startswith('http'):
                        link = "https:" + link if link.startswith('//') else "https://www.lazada.co.id" + link
                    
                    price_elem = product.find('span', class_=re.compile(r'.*price.*', re.I))
                    if not price_elem:
                        price_elem = product.find('span', string=re.compile(r'Rp'))
                    
                    price_text = price_elem.text if price_elem else ""
                    harga = bersihkan_harga(price_text)
                    
                    if harga > 5000:
                        product_data = {
                            'marketplace': 'Lazada',
                            'nama_produk': nama[:150],
                            'harga': harga,
                            'link': link
                        }
                        all_products.append(product_data)
                        success_count += 1
                        
                except Exception as e:
                    continue
            
            print(f"      ✓ {success_count} produk berhasil")
            
            if page < num_pages:
                time.sleep(4)
        
        driver.quit()
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:80]}")
        if driver:
            try:
                driver.quit()
            except:
                pass
    
    lazada_products = [p for p in all_products if p['marketplace'] == 'Lazada']
    print(f"   ✅ Total: {len(lazada_products)} produk")
    return lazada_products



def scrape_gabungan(keyword, provinsi_id, num_pages=3):
    print(f"\n{'='*80}")
    print(f"🔍 SCRAPING: {keyword}")
    print(f"{'='*80}")
    
    products_blibli = scrape_blibli(keyword, provinsi_id, num_pages)
    time.sleep(3)
    products_lazada = scrape_lazada(keyword, provinsi_id, num_pages)
    
    all_products = products_blibli + products_lazada
    
    print(f"\n📊 RINGKASAN:")
    print(f"   🔵 Blibli: {len(products_blibli)} produk")
    print(f"   🟠 Lazada: {len(products_lazada)} produk")
    print(f"   📦 Total: {len(all_products)} produk")
    
    return all_products



def filter_outliers_dan_hitung_rata_rata(products, item_key):
    if len(products) < 4:
        print(f"   ⚠️ Data kurang ({len(products)}), pakai estimasi")
        return HARGA_FALLBACK[item_key], products
    
    harga_list = [p['harga'] for p in products]
    
    print(f"\n🧹 FILTER OUTLIER (IQR):")
    print(f"   📊 Total RAW: {len(harga_list)} produk")
    
    cleaned_prices, outliers, stats = remove_outliers_iqr(harga_list, multiplier=1.5)
    
    print(f"   📈 Q1: Rp {stats['q1']:,} | Median: Rp {stats['q2']:,} | Q3: Rp {stats['q3']:,}")
    print(f"   🗑️ Outlier dihapus: {stats['outliers_removed']} ({stats['outliers_pct']:.1f}%)")
    print(f"   ✅ Data bersih: {stats['total_cleaned']} produk")
    
    cleaned_products = [p for p in products if p['harga'] in cleaned_prices]
    
    if cleaned_prices:
        median = statistics.median(cleaned_prices)
        mean = statistics.mean(cleaned_prices)
        
        print(f"\n💰 STATISTIK HARGA:")
        print(f"   📊 Median: Rp {median:,.0f}")
        print(f"   📊 Mean: Rp {mean:,.0f}")
        print(f"   📈 Range: Rp {min(cleaned_prices):,} - Rp {max(cleaned_prices):,}")
        
        return median, cleaned_products
    else:
        print(f"   ⚠️ Pakai estimasi")
        return HARGA_FALLBACK[item_key], products



def hitung_kebutuhan(jumlah_jiwa):
    kebutuhan = {}
    
    for key, data in STANDAR_BNPB.items():
        if key in ['minyak_goreng', 'gula_pasir']:
            jumlah_keluarga = max(1, (jumlah_jiwa + 3) // 4)
            total = jumlah_keluarga * data['kebutuhan_per_keluarga_3_hari']
        elif key == 'selimut':
            # KOREKSI: 2 selimut per keluarga (5 jiwa) = 0.4 per jiwa
            jumlah_keluarga = max(1, (jumlah_jiwa + 4) // 5)
            total = jumlah_keluarga * data['kebutuhan_per_keluarga']
        else:
            total = jumlah_jiwa * data['kebutuhan_per_jiwa_per_hari'] * 3
        
        kemasan = int(total / data['konversi']) + (1 if total % data['konversi'] > 0 else 0)
        
        kebutuhan[key] = {
            'nama': data['nama'],
            'kebutuhan_total': total,
            'satuan': data['satuan'],
            'jumlah_kemasan': kemasan,
            'keyword': data['keyword'],
            'prioritas': data['prioritas']
        }
    
    return kebutuhan



def print_header(lokasi_bencana, jumlah_jiwa, provinsi_id):
    print("\n" + "="*80)
    print("📊 ESTIMASI BIAYA BANTUAN DARURAT BENCANA")
    print("="*80)
    print(f"📍 Lokasi Bencana: {lokasi_bencana}")
    
    if provinsi_id:
        prov = PROVINSI_INDONESIA[provinsi_id]
        print(f"🗺️ Filter Harga: {prov['nama']}")
    else:
        print(f"🗺️ Filter Harga: Nasional")
    
    print(f"👥 Jumlah Korban: {jumlah_jiwa:,} jiwa")
    print(f"⏰ Periode: 3 hari masa darurat")
    print(f"📋 Standar: BNPB No. 7 Tahun 2008")
    print(f"🛒 Sumber Data: Blibli + Lazada")
    print(f"📅 Tanggal: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}")
    print("="*80)



def print_tabel_hasil(hasil, total):
    print("\n📋 RINCIAN KEBUTUHAN DAN BIAYA:")
    print("-" * 120)
    print(f"{'No':<3} {'Barang':<20} {'Kebutuhan':<15} {'Kemasan':<10} {'Harga/Unit':<18} {'Subtotal':<18} {'Data':<12}")
    print("-" * 120)
    
    for i, (key, data) in enumerate(hasil.items(), 1):
        print(f"{i:<3} {data['nama']:<20} {data['kebutuhan_total']:.1f} {data['satuan']:<12} "
              f"{data['jumlah_kemasan']:<10} Rp {data['harga_per_kemasan']:>13,} "
              f"Rp {data['subtotal']:>13,} {data['jumlah_data']:<12}")
    
    print("-" * 120)
    print(f"{'TOTAL ESTIMASI BIAYA':<75} Rp {total:>13,}")
    print("=" * 120)



def main():
    print("🚀 SISTEM ESTIMASI BIAYA BANTUAN DARURAT BENCANA")
    print("="*80)
    
    try:
        print("\n📝 INPUT DATA:")
        jumlah_jiwa = int(input("Jumlah korban jiwa: "))
        if jumlah_jiwa <= 0:
            print("❌ Harus > 0!")
            return
        
        lokasi_bencana = input("Lokasi bencana: ").strip()
        if not lokasi_bencana:
            print("❌ Lokasi tidak boleh kosong!")
            return
        
        provinsi_id = pilih_provinsi()
        
    except ValueError:
        print("❌ Input harus angka!")
        return
    except KeyboardInterrupt:
        print("\n⚠️ Dibatalkan")
        return
    
    print_header(lokasi_bencana, jumlah_jiwa, provinsi_id)
    
    print("\n📊 MENGHITUNG KEBUTUHAN BNPB...")
    kebutuhan = hitung_kebutuhan(jumlah_jiwa)
    
    print("✅ Kebutuhan:")
    for key, data in kebutuhan.items():
        print(f"  • {data['nama']}: {data['kebutuhan_total']:.1f} {data['satuan']} ({data['jumlah_kemasan']} kemasan)")
    
    print("\n" + "="*80)
    print("🛒 MULAI SCRAPING DARI 2 MARKETPLACE")
    print("="*80)
    
    all_scraped_data = []
    hasil_kalkulasi = {}
    
    for item_key, item_info in sorted(kebutuhan.items(), key=lambda x: x[1]['prioritas']):
        print(f"\n{'='*80}")
        print(f"📦 {item_info['nama']} ({item_info['jumlah_kemasan']} kemasan)")
        print(f"{'='*80}")
        
        try:
            products = scrape_gabungan(item_info['keyword'], provinsi_id, num_pages=3)
            
            if products:
                harga_median, cleaned_products = filter_outliers_dan_hitung_rata_rata(products, item_key)
                
                for prod in cleaned_products:
                    prod['kategori_barang'] = item_info['nama']
                
                all_scraped_data.extend(cleaned_products)
                
                subtotal = item_info['jumlah_kemasan'] * harga_median
                
                hasil_kalkulasi[item_key] = {
                    'nama': item_info['nama'],
                    'kebutuhan_total': item_info['kebutuhan_total'],
                    'satuan': item_info['satuan'],
                    'jumlah_kemasan': item_info['jumlah_kemasan'],
                    'harga_per_kemasan': harga_median,
                    'subtotal': subtotal,
                    'jumlah_data': len(cleaned_products)
                }
            else:
                print(f"   ⚠️ Tidak ada data, menggunakan estimasi")
                harga_est = HARGA_FALLBACK[item_key]
                subtotal = item_info['jumlah_kemasan'] * harga_est
                
                hasil_kalkulasi[item_key] = {
                    'nama': item_info['nama'],
                    'kebutuhan_total': item_info['kebutuhan_total'],
                    'satuan': item_info['satuan'],
                    'jumlah_kemasan': item_info['jumlah_kemasan'],
                    'harga_per_kemasan': harga_est,
                    'subtotal': subtotal,
                    'jumlah_data': 0
                }
            
            time.sleep(3)
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}")
            harga_est = HARGA_FALLBACK[item_key]
            subtotal = item_info['jumlah_kemasan'] * harga_est
            
            hasil_kalkulasi[item_key] = {
                'nama': item_info['nama'],
                'kebutuhan_total': item_info['kebutuhan_total'],
                'satuan': item_info['satuan'],
                'jumlah_kemasan': item_info['jumlah_kemasan'],
                'harga_per_kemasan': harga_est,
                'subtotal': subtotal,
                'jumlah_data': 0
            }
    
    total_biaya = sum(d['subtotal'] for d in hasil_kalkulasi.values())
    
    print("\n" + "="*80)
    print("💰 HASIL KALKULASI BIAYA")
    print("="*80)
    
    print_tabel_hasil(hasil_kalkulasi, total_biaya)
    
    print(f"\n📈 ANALISIS:")
    print(f"  💰 Biaya per jiwa (3 hari): Rp {total_biaya/jumlah_jiwa:,.0f}")
    print(f"  📊 Biaya per jiwa per hari: Rp {total_biaya/(jumlah_jiwa*3):,.0f}")
    
    prioritas_tinggi = sum(d['subtotal'] for d in hasil_kalkulasi.values() if kebutuhan[next(k for k in kebutuhan if kebutuhan[k]['nama'] == d['nama'])]['prioritas'] <= 3)
    print(f"  🥇 Prioritas tinggi (air, beras, mi): Rp {prioritas_tinggi:,.0f} ({prioritas_tinggi/total_biaya*100:.1f}%)")
    
    print(f"\n📊 STATISTIK SCRAPING:")
    blibli_count = len([p for p in all_scraped_data if p['marketplace'] == 'Blibli'])
    lazada_count = len([p for p in all_scraped_data if p['marketplace'] == 'Lazada'])
    print(f"  🔵 Blibli: {blibli_count} produk")
    print(f"  🟠 Lazada: {lazada_count} produk")
    print(f"  📦 Total: {len(all_scraped_data)} produk (setelah filter outlier)")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    lokasi_safe = re.sub(r'[^\w\s-]', '', lokasi_bencana).replace(' ', '_')
    
    if provinsi_id:
        prov_safe = re.sub(r'[^\w\s-]', '', PROVINSI_INDONESIA[provinsi_id]['nama']).replace(' ', '_')
    else:
        prov_safe = 'Nasional'
    
    try:
        df_detail = pd.DataFrame(all_scraped_data)
        filename_detail = f"detail_produk_{lokasi_safe}_{prov_safe}_{timestamp}.csv"
        df_detail.to_csv(filename_detail, index=False, encoding='utf-8-sig')
        print(f"\n💾 Detail produk tersimpan: {filename_detail}")
    except Exception as e:
        print(f"⚠️ Gagal simpan detail: {str(e)[:50]}")
    
    try:
        ringkasan_data = []
        for key, data in hasil_kalkulasi.items():
            ringkasan_data.append({
                'Kategori': data['nama'],
                'Kebutuhan': data['kebutuhan_total'],
                'Satuan': data['satuan'],
                'Jumlah_Kemasan': data['jumlah_kemasan'],
                'Harga_Per_Kemasan': data['harga_per_kemasan'],
                'Subtotal': data['subtotal'],
                'Jumlah_Data_Produk': data['jumlah_data']
            })
        
        ringkasan_data.append({
            'Kategori': 'TOTAL',
            'Kebutuhan': '',
            'Satuan': '',
            'Jumlah_Kemasan': '',
            'Harga_Per_Kemasan': '',
            'Subtotal': total_biaya,
            'Jumlah_Data_Produk': ''
        })
        
        df_ringkasan = pd.DataFrame(ringkasan_data)
        filename_ringkasan = f"ringkasan_biaya_{lokasi_safe}_{prov_safe}_{timestamp}.csv"
        df_ringkasan.to_csv(filename_ringkasan, index=False, encoding='utf-8-sig')
        print(f"💾 Ringkasan biaya tersimpan: {filename_ringkasan}")
    except Exception as e:
        print(f"⚠️ Gagal simpan ringkasan: {str(e)[:50]}")
    
    print(f"\n" + "="*80)
    print("✅ ANALISIS SELESAI!")
    print(f"📊 Total Biaya: Rp {total_biaya:,.0f}")
    print(f"👥 Untuk {jumlah_jiwa:,} jiwa di {lokasi_bencana}")
    print(f"🗺️ Filter: {PROVINSI_INDONESIA[provinsi_id]['nama'] if provinsi_id else 'Nasional'}")
    print(f"📦 Total Produk Dianalisis: {len(all_scraped_data)}")
    print("="*80)



if __name__ == "__main__":
    main()
