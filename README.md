# Stok Takibi Sistemi

Bu proje, basit bir **stok takibi uygulaması** sunmak amacıyla geliştirilmiştir. Kullanıcılar ürünleri ekleyebilir, çıkartabilir ve stokları takip edebilirler. Ayrıca, ürünler hakkında detaylı bilgi görsel olarak sunulmaktadır.

## Özellikler

- **Ürün Ekleme**: Kullanıcılar yeni ürünler ekleyebilir.
- **Ürün Çıkartma**: Stoktan ürün çıkartılabilir.
- **Stok Takibi**: Ürünlerin mevcut stok durumu görüntülenebilir.
- **Excel Yükleme**: Excel dosyasından stok bilgileri yüklenebilir.
- **Excel'e Kaydetme**: Güncellenmiş stoklar Excel dosyasına kaydedilebilir.

## Kullanım

### Adımlar

1. **Projeyi Çalıştırma**:
   - Projeyi çalıştırmak için Python yüklü olmalıdır.
   - Gerekli kütüphaneleri yüklemek için şu komutu çalıştırın:
   
     ```bash
     pip install tkinter pandas openpyxl
     ```

2. **Uygulamayı Başlatma**:
   - Uygulamayı başlatmak için `app.py` dosyasını çalıştırın:
   
     ```bash
     python app.py
     ```

3. **Fonksiyonlar**:
   - **Ürün Ekleme**: Menüden "Ürün Ekle"yi seçerek yeni ürün ekleyebilirsiniz.
   - **Ürün Çıkartma**: Menüden "Ürün Çıkart" seçeneği ile stoktan ürün çıkarabilirsiniz.
   - **Stok Takibi**: "Stok Takibi" bölümüne geçerek mevcut stokları görüntüleyebilirsiniz.
   - **Excel Yükleme**: "Excel'den Yükle" seçeneği ile bir Excel dosyasından stok bilgisi yükleyebilirsiniz.
   - **Excel'e Kaydetme**: Mevcut stokları Excel dosyasına kaydetmek için "Excel'e Kaydet" seçeneğini kullanabilirsiniz.


## Kullanıcı Arayüzü

- **Ana Ekran**: Ürün ekleyebilir, çıkartabilir ve stokları takip edebilirsiniz.
- **Stok Görüntüleme**: Mevcut stokları görsel olarak takip edebilirsiniz.
- **Arama Özelliği**: Ürünleri arayarak hızlı bir şekilde bulabilirsiniz.

## Python Uygulamasını `.exe` Dosyasına Dönüştürme

Python projenizi Windows işletim sistemi için çalıştırılabilir bir `.exe` dosyasına dönüştürmek için **PyInstaller**'ı kullanabilirsiniz. Aşağıda bu işlemi nasıl yapacağınız adım adım açıklanmıştır.

### **1. PyInstaller Yükleme**

İlk olarak, PyInstaller'ı yüklemeniz gerekiyor. Terminal veya komut istemcisini açarak aşağıdaki komutu çalıştırın:

```bash
pip install pyinstaller
```

2. Python Dosyasını .exe Dosyasına Dönüştürme
Python dosyanızı .exe dosyasına dönüştürmek için terminali açın ve aşağıdaki komutu çalıştırın:
```
pyinstaller --onefile --noconsole app.py

```

Buradaki app.py dosyanızın adıdır. Bu komut, Python dosyasını tek bir .exe dosyasına dönüştürür.
--onefile seçeneği, tüm bağımlılıkları tek bir dosyada toplar. Eğer bu seçeneği kullanmazsanız, .exe dosyasının yanında birden fazla dosya (bağımlılıklar için) oluşacaktır.

## Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz, aşağıdaki adımları takip edebilirsiniz:

1. Projeyi fork edin.
2. Yeni bir branch oluşturun (`git checkout -b feature-branch`).
3. Yaptığınız değişiklikleri commit edin (`git commit -am 'Added new feature'`).
4. Değişikliklerinizi push edin (`git push origin feature-branch`).
5. Pull request oluşturun.



