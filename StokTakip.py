import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import pandas as pd
import datetime

class StokTakibiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stok Takibi Sistemi")
        
        # Tam ekran açmak için bu satırı ekleyin
        self.root.attributes('-fullscreen', True)  # Pencereyi tam ekran yapar
        self.root.config(bg="#f2f2f2")

        # Ürünlerin ve miktarlarının tutulduğu sözlük
        self.stoklar = {}
        self.depolar_listesi = []

        # Yükleme zamanını gösterecek label
        self.yukleme_zamani_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#FFFF00", fg="black", relief="solid", bd=1, padx=10, pady=1)

        # Ana frame: Butonları ve yükleme zamanını yerleştireceğiz
        self.main_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.main_frame.pack(fill="both", expand=True)
        self.button_frame = tk.Frame(self.main_frame, bg="#f2f2f2")
        self.button_frame.pack(fill="x", pady=10)  # Butonların arasına biraz boşluk ekledik
        self.urun_ekle_button = tk.Button(self.button_frame, text="Ürün Ekle", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.urun_ekle_frame, relief="flat", width=15)# Butonlar
        self.urun_ekle_button.pack(side=tk.LEFT, padx=10)
        self.urun_cikart_button = tk.Button(self.button_frame, text="Ürün Çıkart", font=("Arial", 12), bg="#FF5722", fg="white", command=self.urun_cikart_frame, relief="flat", width=15)
        self.urun_cikart_button.pack(side=tk.LEFT, padx=10)
        self.stok_takibi_button = tk.Button(self.button_frame, text="Stok Takibi", font=("Arial", 12), bg="#2196F3", fg="white", command=self.stok_takibi_frame, relief="flat", width=15)
        self.stok_takibi_button.pack(side=tk.LEFT, padx=10)
        self.excel_yukle_button = tk.Button(self.button_frame, text="Excel'den Yükle", font=("Arial", 12), bg="#673AB7", fg="white", command=self.dosya_yukle, relief="flat", width=15)# Excel Yükle Butonu
        self.excel_yukle_button.pack(side=tk.LEFT, padx=10)
        self.dosya_kaydet_button = tk.Button(self.button_frame, text="Excel'e Kaydet", font=("Arial", 12), bg="#2196F3", fg="white", command=self.dosya_kaydet, relief="flat", width=15)# Excel'e Kaydet Butonu (Yeni Buton)
        self.dosya_kaydet_button.pack(side=tk.LEFT, padx=10)
        self.depodan_al_button = tk.Button(self.button_frame, text="Depodan Al", font=("Arial", 12), bg="#FF9800", fg="white", command=self.depodan_al_frame, relief="flat", width=15)# Depodan Al Butonu
        self.depodan_al_button.pack(side=tk.LEFT, padx=10)
        self.stok_kontrol_button = tk.Button(self.button_frame, text="Stok Kontrolü", font=("Arial", 12), bg="#FF0000", fg="white", command=self.kontrol_et_stok, relief="flat", width=15)
        self.stok_kontrol_button.pack(side=tk.LEFT, padx=10)
        self.header_frame = tk.Frame(self.main_frame, bg="#f2f2f2")# Yükleme zamanını gösterecek olan label'ı, sağ üst köşeye yerleştirecek özel bir frame
        self.header_frame.pack(fill="x", side="top")  # Butonların hemen üstüne yerleştiriyoruz        
        self.yukleme_zamani_label.pack(side="right", padx=10, pady=10)  # Sağda hizalı, biraz boşluk bırakıyoruz
        # Frame'ler
        self.frame_urun_ekle = None
        self.frame_urun_cikart = None
        self.frame_stok_takibi = None
        self.frame_depodan_al = None
        self.stok_takibi_frame()  # Varsayılan olarak stok takibi sayfasını göster
        def toggle_fullscreen(event=None):
            current_state = self.root.attributes('-fullscreen')
            self.root.attributes('-fullscreen', not current_state)

        self.root.bind("<Escape>", toggle_fullscreen)     

    def dosya_yukle(self):
        dosya_yolu = filedialog.askopenfilename(filetypes=[("Excel Dosyası", "*.xlsx;*.xls")])
        if dosya_yolu:
            try:
                df = pd.read_excel(dosya_yolu, engine='openpyxl')
                if 'Ürün Kodu' in df.columns and 'Ürün İsmi' in df.columns and 'Stok' in df.columns and 'Depolar' in df.columns and 'Birim' in df.columns:
                    # Stokları int türüne dönüştür
                    df['Stok'] = df['Stok'].astype(int)
                
                    # Depoları ve stokları ilgili sütundan al
                    self.stoklar = {row['Ürün Kodu']: {'Ürün İsmi': row['Ürün İsmi'], 'Stok': row['Stok'], 'Depolar': row['Depolar'], 'Birim': row['Birim']} for _, row in df.iterrows()}
                    
                    # Yükleme zamanını kaydet
                    self.yukleme_zamani = datetime.datetime.now().strftime("%H:%M:%S %m.%d.%Y")
                    self.yukleme_zamani_label.config(text=f"Güncelleme: {self.yukleme_zamani}")
                    
                    messagebox.showinfo("Başarılı", "Excel dosyası başarıyla yüklendi.")
                    self.stok_goruntule()
                else:
                    messagebox.showerror("Hata", "Dosyada gerekli sütunlar eksik.")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken hata oluştu: {str(e)}")               

    def stok_goruntule(self):
        if hasattr(self, 'tree'):  # Eğer self.tree mevcutsa, verileri güncelle
            # Treeview'deki mevcut veriyi temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
        else:
            # Eğer Treeview widget'ı yoksa, onu oluştur
            self.tree = ttk.Treeview(self.frame_stok_takibi, columns=("Ürün Kodu", "Ürün İsmi", "Birim", "Stok", "Depolar"), show="headings")
            self.tree.heading("Ürün Kodu", text="Ürün Kodu")
            self.tree.heading("Ürün İsmi", text="Ürün İsmi")
            self.tree.heading("Birim", text="Birim")
            self.tree.heading("Stok", text="Stok")
            self.tree.heading("Depolar", text="Depolar")
            
            self.tree.column("Ürün Kodu", anchor="center", width=120)
            self.tree.column("Ürün İsmi", anchor="center", width=200)
            self.tree.column("Birim", anchor="center", width=100)
            self.tree.column("Stok", anchor="center", width=100)
            self.tree.column("Depolar", anchor="center", width=250)
            
            self.tree.pack(fill="both", expand=True)            

        # Veriyi Treeview'e ekle
        for urun_kodu, urun in self.stoklar.items():
            self.tree.insert("", "end", values=(urun_kodu, urun["Ürün İsmi"], urun["Birim"], urun["Stok"], urun["Depolar"]))


    def urun_ara(self, event=None):  # 'event' parametresi Enter tuşu için gereklidir
        arama = self.aranan_urun_entry.get().lower()
        # Treeview'deki mevcut veriyi temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        if arama:
            bulunan_urunler = [
                (urun_kodu, urun['Ürün İsmi'], urun['Birim'], urun['Stok'], urun['Depolar'])
                for urun_kodu, urun in self.stoklar.items()
                if arama in urun_kodu.lower() or arama in urun['Ürün İsmi'].lower()
            ]
            if bulunan_urunler:
                for urun in bulunan_urunler:
                    self.tree.insert("", "end", values=urun)
            else:
                self.tree.insert("", "end", values=("Arama ile eşleşen ürün bulunamadı.", "", "", "", ""))
        else:
            self.stok_goruntule()

    def stok_takibi_frame(self):
        self.clear_frames()
        self.frame_stok_takibi = tk.Frame(self.main_frame, bg="#f2f2f2")
        self.frame_stok_takibi.pack(fill="both", expand=True)        

        # Ürün Ara Çubuğu
        self.aranan_urun_label = tk.Label(self.frame_stok_takibi, text="Ürün Ara:", font=("Arial", 12), bg="#f2f2f2", fg="#333")
        self.aranan_urun_label.pack(pady=5)
        self.aranan_urun_entry = tk.Entry(self.frame_stok_takibi, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.aranan_urun_entry.pack(pady=5)
        self.aranan_urun_entry.bind("<Return>", self.urun_ara)  # Enter tuşu ile arama yapılacak

        self.urun_ara_button = tk.Button(self.frame_stok_takibi, text="Ara", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.urun_ara, relief="flat", width=15)
        self.urun_ara_button.pack(pady=5)        
        # Treeview ile mevcut stokları görüntüleme
        self.tree = ttk.Treeview(self.frame_stok_takibi, columns=("Ürün Kodu", "Ürün İsmi", "Birim", "Stok", "Depolar"), show="headings")
        self.tree.heading("Ürün Kodu", text="Ürün Kodu")
        self.tree.heading("Ürün İsmi", text="Ürün İsmi")
        self.tree.heading("Birim", text="Birim")
        self.tree.heading("Stok", text="Stok")
        self.tree.heading("Depolar", text="Depolar")        
        self.tree.column("Ürün Kodu", anchor="center", width=120)
        self.tree.column("Ürün İsmi", anchor="center", width=200)
        self.tree.column("Birim", anchor="center", width=100)
        self.tree.column("Stok", anchor="center", width=100)
        self.tree.column("Depolar", anchor="center", width=250)
        self.tree.pack(fill="both", expand=True)
    def show_right_click_menu(self, event):
        """Sağ tıklama menüsünü gösterir."""
        selected_item = self.tree.selection()
        if selected_item:
            self.right_click_menu.post(event.x_root, event.y_root)     

    def clear_frames(self):
        """Mevcut frame'leri temizler."""
        if hasattr(self, "frame_urun_ekle") and self.frame_urun_ekle:
            self.frame_urun_ekle.destroy()
        if hasattr(self, "frame_urun_cikart") and self.frame_urun_cikart:
            self.frame_urun_cikart.destroy()
        if hasattr(self, "frame_depodan_al") and self.frame_depodan_al:
            self.frame_depodan_al.destroy()

        # frame_stok_takibi'ni temizlerken, self.tree widget'ını koruruz
        if hasattr(self, "frame_stok_takibi") and self.frame_stok_takibi:
            self.frame_stok_takibi.destroy()

    def urun_ekle_frame(self):
        self.clear_frames()
        self.frame_urun_ekle = tk.Frame(self.main_frame, bg="#f2f2f2")
        self.frame_urun_ekle.pack(fill="both", expand=True)

        # Ürün Kodu
        self.urun_kodu_label = tk.Label(self.frame_urun_ekle, text="Ürün Kodu:", font=("Arial", 12), bg="#f2f2f2")
        self.urun_kodu_label.pack(pady=5)
        self.urun_kodu_entry = tk.Entry(self.frame_urun_ekle, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.urun_kodu_entry.pack(pady=5)

        # Ürün İsmi
        self.urun_ismi_label = tk.Label(self.frame_urun_ekle, text="Ürün İsmi:", font=("Arial", 12), bg="#f2f2f2")
        self.urun_ismi_label.pack(pady=5)
        self.urun_ismi_entry = tk.Entry(self.frame_urun_ekle, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.urun_ismi_entry.pack(pady=5)

        # Stok Miktarı
        self.stok_label = tk.Label(self.frame_urun_ekle, text="Stok Miktarı:", font=("Arial", 12), bg="#f2f2f2")
        self.stok_label.pack(pady=5)
        self.stok_entry = tk.Entry(self.frame_urun_ekle, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.stok_entry.pack(pady=5)

        # Depolar
        self.depolar_label = tk.Label(self.frame_urun_ekle, text="Depolar:", font=("Arial", 12), bg="#f2f2f2")
        self.depolar_label.pack(pady=5)
        self.depolar_entry = tk.Entry(self.frame_urun_ekle, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.depolar_entry.pack(pady=5)

        # Birim
        self.birim_label = tk.Label(self.frame_urun_ekle, text="Birim:", font=("Arial", 12), bg="#f2f2f2")
        self.birim_label.pack(pady=5)
        self.birim_entry = tk.Entry(self.frame_urun_ekle, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.birim_entry.pack(pady=5)

        # Ekleme butonu
        self.urun_ekle_button = tk.Button(self.frame_urun_ekle, text="Ürün Ekle", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.urun_ekle, relief="flat", width=15)
        self.urun_ekle_button.pack(pady=10)
        pass
    def urun_ekle(self):
        urun_kodu = self.urun_kodu_entry.get()
        urun_ismi = self.urun_ismi_entry.get()
        stok = self.stok_entry.get()
        depolar = self.depolar_entry.get()
        birim = self.birim_entry.get()

        if not urun_kodu or not urun_ismi or not stok or not depolar or not birim:
            messagebox.showerror("Hata", "Tüm alanları doldurduğunuzdan emin olun.")
            return

        try:
            stok = int(stok)
            self.stoklar[urun_kodu] = {'Ürün İsmi': urun_ismi, 'Stok': stok, 'Depolar': depolar, 'Birim': birim}
            messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi.")
            self.stok_goruntule()
        except ValueError:
            messagebox.showerror("Hata", "Stok miktarı geçersiz. Lütfen geçerli bir sayı girin.") 
    def urun_cikart_frame(self):
        self.clear_frames()
        self.frame_urun_cikart = tk.Frame(self.main_frame, bg="#f2f2f2")
        self.frame_urun_cikart.pack(fill="both", expand=True)

         # Ürün Kodu
        self.urun_kodu_label = tk.Label(self.frame_urun_cikart, text="Ürün Kodu:", font=("Arial", 12), bg="#f2f2f2")
        self.urun_kodu_label.pack(pady=5)
        self.urun_kodu_entry = tk.Entry(self.frame_urun_cikart, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.urun_kodu_entry.pack(pady=5)

         # Çıkartılacak Miktar
        self.miktar_label = tk.Label(self.frame_urun_cikart, text="Çıkartılacak Miktar:", font=("Arial", 12), bg="#f2f2f2")
        self.miktar_label.pack(pady=5)
        self.miktar_entry = tk.Entry(self.frame_urun_cikart, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.miktar_entry.pack(pady=5)

         # Çıkartma butonu
        self.urun_cikart_button = tk.Button(self.frame_urun_cikart, text="Stoktan Çıkart", font=("Arial", 12), bg="#FF5722", fg="white", command=self.urun_cikart, relief="flat", width=15)
        self.urun_cikart_button.pack(pady=10)
    def urun_cikart(self):
        urun_kodu = self.urun_kodu_entry.get()
        miktar = self.miktar_entry.get()

        if urun_kodu not in self.stoklar:
            messagebox.showerror("Hata", "Bu ürün mevcut değil.")
            return
        
        if not miktar or not miktar.isdigit():
            messagebox.showerror("Hata", "Geçerli bir miktar girin.")
            return
         
        miktar = int(miktar)
        mevcut_stok = self.stoklar[urun_kodu]["Stok"]

        if miktar > mevcut_stok:
            messagebox.showerror("Hata", "Stok yetersiz.")
            return

        self.stoklar[urun_kodu]["Stok"] -= miktar
        messagebox.showinfo("Başarılı", f"{miktar} adet ürün başarıyla çıkartıldı.")
        self.stok_goruntule()     

    def depodan_al_frame(self):
        self.clear_frames()
        self.frame_depodan_al = tk.Frame(self.main_frame, bg="#f2f2f2")
        self.frame_depodan_al.pack(fill="both", expand=True)

        # Depo Seçme
        self.depo_secin_label = tk.Label(self.frame_depodan_al, text="Depo Seçin:", font=("Arial", 12), bg="#f2f2f2")
        self.depo_secin_label.pack(pady=5)

        # Combobox ile depoları seçme
        self.depo_combobox = ttk.Combobox(self.frame_depodan_al, values=self.depolar_listesi, font=("Arial", 12), state="readonly", width=30)
        self.depo_combobox.pack(pady=5)

        # Ürün Kodu
        self.urun_kodu_label = tk.Label(self.frame_depodan_al, text="Ürün Kodu:", font=("Arial", 12), bg="#f2f2f2")
        self.urun_kodu_label.pack(pady=5)
        self.urun_kodu_entry = tk.Entry(self.frame_depodan_al, font=("Arial", 12), width=30)
        self.urun_kodu_entry.pack(pady=5)

        # Miktar
        self.miktar_label = tk.Label(self.frame_depodan_al, text="Miktar:", font=("Arial", 12), bg="#f2f2f2")
        self.miktar_label.pack(pady=5)
        self.miktar_entry = tk.Entry(self.frame_depodan_al, font=("Arial", 12), width=30)
        self.miktar_entry.pack(pady=5)

        # Depodan Al Butonu
        self.depodan_al_btn = tk.Button(self.frame_depodan_al, text="Depodan Al", font=("Arial", 12), bg="#FF9800", fg="white", command=self.depodan_al, relief="flat", width=15)
        self.depodan_al_btn.pack(pady=10)

    def depodan_al(self):
        depo = self.depo_combobox.get()
        urun_kodu = self.urun_kodu_entry.get()
        miktar = self.miktar_entry.get()

        if not depo or not urun_kodu or not miktar:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        try:
            miktar = int(miktar)
            if urun_kodu in self.stoklar:
                urun = self.stoklar[urun_kodu]
                if depo == urun['Depolar']:  # Depo doğruysa ve stok yeterliyse
                    if urun['Stok'] >= miktar:
                        urun['Stok'] -= miktar
                        messagebox.showinfo("Başarılı", f"{miktar} adet {urun['Ürün İsmi']} ürünü depodan alındı.")
                        self.stok_goruntule()  # Güncel stokları göster
                    else:
                        messagebox.showerror("Hata", "Yeterli stok yok.")
                else:
                    messagebox.showerror("Hata", f"Bu ürün {urun['Depolar']} depo kodunda mevcut.")
            else:
                messagebox.showerror("Hata", "Ürün kodu bulunamadı.")
        except ValueError:
            messagebox.showerror("Hata", "Miktar geçersiz.")

    def depodan_al_frame(self):
        self.clear_frames()
        self.frame_depodan_al = tk.Frame(self.main_frame, bg="#f2f2f2")
        self.frame_depodan_al.pack(fill="both", expand=True)

        # Depo Seçme
        self.depo_secin_label = tk.Label(self.frame_depodan_al, text="Depo Seçin:", font=("Arial", 12), bg="#f2f2f2")
        self.depo_secin_label.pack(pady=5)
        # Combobox ile depoları seçme
        self.depo_combobox = ttk.Combobox(self.frame_depodan_al, values=self.depolar_listesi, font=("Arial", 12), state="readonly", width=30)
        self.depo_combobox.pack(pady=5)
        # Ürün Kodu
        self.urun_kodu_label = tk.Label(self.frame_depodan_al, text="Ürün Kodu:", font=("Arial", 12), bg="#f2f2f2")
        self.urun_kodu_label.pack(pady=5)
        self.urun_kodu_entry = tk.Entry(self.frame_depodan_al, font=("Arial", 12), width=30)
        self.urun_kodu_entry.pack(pady=5)
        # Miktar
        self.miktar_label = tk.Label(self.frame_depodan_al, text="Miktar:", font=("Arial", 12), bg="#f2f2f2")
        self.miktar_label.pack(pady=5)
        self.miktar_entry = tk.Entry(self.frame_depodan_al, font=("Arial", 12), width=30)
        self.miktar_entry.pack(pady=5)
        # Depodan Al Butonu
        self.depodan_al_btn = tk.Button(self.frame_depodan_al, text="Depodan Al", font=("Arial", 12), bg="#FF9800", fg="white", command=self.depodan_al, relief="flat", width=15)
        self.depodan_al_btn.pack(pady=10)
    
    def dosya_kaydet(self):
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Dosyası", "*.xlsx;*.xls")])
        if dosya_yolu:
            try:
                # "Ürün Kodu"nu da DataFrame'e ekle
                veriler = []

                # self.stoklar sözlüğünü gezerek verileri uygun şekilde al
                for urun_kodu, urun in self.stoklar.items():
                    veriler.append({
                        'Ürün Kodu': urun_kodu,
                        'Ürün İsmi': urun['Ürün İsmi'],
                        'Stok': urun['Stok'],
                        'Depolar': urun['Depolar'],
                        'Birim': urun['Birim']
                    })

                # Verileri DataFrame'e dönüştür
                df = pd.DataFrame(veriler)

                # Veriyi Excel dosyasına kaydet
                df.to_excel(dosya_yolu, index=False, engine='openpyxl')
                messagebox.showinfo("Başarılı", "Veriler başarıyla kaydedildi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Veriler kaydedilirken hata oluştu: {str(e)}")

    def dosya_yukle(self):
        dosya_yolu = filedialog.askopenfilename(filetypes=[("Excel Dosyası", "*.xlsx;*.xls")])
        if dosya_yolu:
            try:
                df = pd.read_excel(dosya_yolu, engine='openpyxl')
                if 'Ürün Kodu' in df.columns and 'Ürün İsmi' in df.columns and 'Stok' in df.columns and 'Depolar' in df.columns and 'Birim' in df.columns:
                    # Stokları int türüne dönüştür
                    df['Stok'] = df['Stok'].astype(int)
                
                    # Depoları ve stokları ilgili sütundan al
                    self.stoklar = {row['Ürün Kodu']: {'Ürün İsmi': row['Ürün İsmi'], 'Stok': row['Stok'], 'Depolar': row['Depolar'], 'Birim': row['Birim']} for _, row in df.iterrows()}
                    
                    # Depoları listele
                    self.depolar_listesi = list(set(df['Depolar'].dropna()))  # Depoları benzersiz olarak al
                    
                    # Yükleme zamanını kaydet
                    self.yukleme_zamani = datetime.datetime.now().strftime("%H:%M:%S %m.%d.%Y")
                    self.yukleme_zamani_label.config(text=f"Güncelleme: {self.yukleme_zamani}")
                    
                    messagebox.showinfo("Başarılı", "Excel dosyası başarıyla yüklendi.")
                    self.stok_goruntule()
                else:
                    messagebox.showerror("Hata", "Dosyada gerekli sütunlar eksik.")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken hata oluştu: {str(e)}")           
                
    def kontrol_et_stok(self):
        alarm_seviyesi = 10  # Örneğin 10'un altına düşen ürünler uyarı verir.
        alarm_urunler = []

        # Tüm ürünleri kontrol et
        for urun_kodu, urun in self.stoklar.items():
            if urun["Stok"] < alarm_seviyesi:
                alarm_urunler.append(urun)
        if alarm_urunler:
            uyarilar = "\n".join([f"{urun['Ürün İsmi']} ({urun['Stok']} adet)" for urun in alarm_urunler])
            messagebox.showwarning("Düşük Stok Uyarısı", f"Aşağıdaki ürünlerin stoğu düşük:\n\n{uyarilar}")
        else:
            messagebox.showinfo("Stok Durumu", "Tüm ürünlerin stoğu yeterli.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StokTakibiApp(root)
    root.mainloop()
