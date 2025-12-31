Okullarda, ofislerde veya kendi çalışma ortamımızda odaklanmayı artırmak için belirli web sitelerine erişimi kısıtlamak gerekebilir. Pardus üzerinde terminal komutlarıyla uğraşmadan, görsel bir arayüz üzerinden site engelleyip açabileceğimiz bir Python 3 ve arayüz kütüphanesi olarak PyQt6 kullanılan uygulama.

### Çalışma Mantığı: /etc/hosts Nedir?
Bu uygulama, Linux sistemlerin temel alan adı çözümleme dosyası olan hosts dosyasını kullanır.

Bir web sitesine (örn: facebook.com) girmek istediğinizde, bilgisayar önce bu dosyaya bakar.

Biz uygulamamızla bu adresi 127.0.0.1 (Localhost) ip adresine yönlendireceğiz.

Böylece tarayıcı siteyi internette aramak yerine kendi bilgisayarınıza yönlenecek ve site açılmayacaktır.

Önemli Not: Bu dosya sistem dosyası olduğu için, uygulamamızın Yönetici Yetkileriyle (Sudo) çalıştırılması gerekecektir.

### Gerekli Kurulumlar
Uygulamayı geliştirmek için Pardus terminalini açın ve aşağıdaki komutla PyQt6 kütüphanesini yükleyin:

Bash:
#### sudo apt update
#### sudo apt install python3-pip python3-pyqt6

### 4. Uygulamayı Çalıştırma
Bu uygulama sistem dosyalarına (/etc/hosts) müdahale ettiği için normal bir kullanıcı olarak çalıştırılamaz. Pardus terminalini açın ve kaydettiğiniz dizine giderek şu komutu girin:

Bash:
#### sudo python3 site_engelleyici.py
Şifrenizi girdikten sonra uygulama açılacaktır.
<img width="622" height="559" alt="image" src="https://github.com/user-attachments/assets/730a69a0-eecc-4897-bd31-96fb3d262b22" />
