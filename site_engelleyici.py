import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QListWidget, 
                             QLabel, QMessageBox)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

class SiteBlockerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Ayarlar ---
        self.hosts_path = "/etc/hosts"
        self.redirect_ip = "127.0.0.1"
        self.app_title = "Pardus Web Engelleyici"
        
        # Pencere Ayarları
        self.setWindowTitle(self.app_title)
        self.setGeometry(100, 100, 500, 400)
        self.init_ui()
        self.load_blocked_sites()

    def init_ui(self):
        # Ana Widget ve Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Başlık
        title_label = QLabel("Yasaklanacak Web Sitesi:")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        main_layout.addWidget(title_label)

        # Giriş Alanı ve Ekle Butonu (Yanyana)
        input_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Örn: www.facebook.com")
        self.url_input.setFixedHeight(35)
        input_layout.addWidget(self.url_input)

        add_btn = QPushButton("Engelle")
        add_btn.setFixedHeight(35)
        add_btn.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold;")
        add_btn.clicked.connect(self.add_site)
        input_layout.addWidget(add_btn)
        
        main_layout.addLayout(input_layout)

        # Liste Başlığı
        list_label = QLabel("Engellenen Siteler Listesi:")
        list_label.setFont(QFont("Arial", 10))
        main_layout.addWidget(list_label)

        # Liste Görünümü
        self.site_list = QListWidget()
        main_layout.addWidget(self.site_list)

        # Alt Butonlar (Sil ve Kaydet)
        bottom_layout = QHBoxLayout()

        remove_btn = QPushButton("Seçileni Kaldır")
        remove_btn.setStyleSheet("background-color: #f0ad4e; color: white;")
        remove_btn.clicked.connect(self.remove_site)
        bottom_layout.addWidget(remove_btn)

        save_btn = QPushButton("Ayarları Uygula (Kaydet)")
        save_btn.setStyleSheet("background-color: #5cb85c; color: white; font-weight: bold;")
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self.save_changes)
        bottom_layout.addWidget(save_btn)

        main_layout.addLayout(bottom_layout)

        # Bilgi Notu
        info_label = QLabel("Not: Değişikliklerin etkili olması için 'Ayarları Uygula' butonuna basmalısınız.")
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(info_label)

    def load_blocked_sites(self):
        """Mevcut hosts dosyasını okur ve listede gösterir."""
        try:
            with open(self.hosts_path, 'r') as file:
                content = file.read().splitlines()
                for line in content:
                    if self.redirect_ip in line:
                        # "127.0.0.1 facebook.com" formatını parçala
                        parts = line.split()
                        if len(parts) >= 2:
                            # Sadece domain kısmını al (örn: facebook.com)
                            site = parts[1]
                            # Localhost'un kendisini listeye ekleme
                            if site != "localhost":
                                self.site_list.addItem(site)
        except PermissionError:
            QMessageBox.critical(self, "Hata", "Dosya okuma izni yok! Uygulamayı 'sudo' ile çalıştırın.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Beklenmedik hata: {str(e)}")

    def add_site(self):
        """Listeye yeni site ekler (Henüz kaydetmez)."""
        site = self.url_input.text().strip()
        if site:
            # www. koyulmamışsa hem normal hem www halini ekleyelim garanti olsun
            if not site.startswith("www."):
                self.site_list.addItem(site)
                self.site_list.addItem("www." + site)
            else:
                self.site_list.addItem(site)
            
            self.url_input.clear()

    def remove_site(self):
        """Listeden seçili siteyi siler."""
        selected_items = self.site_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.site_list.takeItem(self.site_list.row(item))

    def save_changes(self):
        """Hosts dosyasını yeniden yazar."""
        try:
            # 1. Mevcut hosts dosyasını oku, bizim engellediklerimiz hariç her şeyi tut.
            with open(self.hosts_path, 'r') as file:
                lines = file.readlines()
            
            new_content = []
            for line in lines:
                # Eğer satırda redirect IP var ama localhost değilse (yani engellenmiş siteyse) alma
                if self.redirect_ip in line and "localhost" not in line:
                    continue
                new_content.append(line)

            # 2. Listeden engellenecekleri yeni içeriğe ekle
            items = []
            for index in range(self.site_list.count()):
                items.append(self.site_list.item(index).text())

            # Son satırda boşluk yoksa ekle
            if new_content and not new_content[-1].endswith('\n'):
                new_content[-1] += '\n'

            for site in items:
                new_content.append(f"{self.redirect_ip} {site}\n")

            # 3. Dosyayı yaz
            with open(self.hosts_path, 'w') as file:
                file.writelines(new_content)
            
            QMessageBox.information(self, "Başarılı", "Siteler başarıyla engellendi/kaldırıldı!")

        except PermissionError:
            QMessageBox.critical(self, "Hata", "Yazma izni reddedildi! Lütfen uygulamayı 'sudo' ile başlatın.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SiteBlockerApp()
    window.show()
    sys.exit(app.exec())