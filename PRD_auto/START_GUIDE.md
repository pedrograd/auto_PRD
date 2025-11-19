# PRD Full Automation System - Quick Start Guide

Bu sistem, PRD.md dosyanızı otomatik olarak oluşturur, okur, analiz eder ve geliştirir. Cursor AI ile entegre çalışır ve GitHub ile senkronize olur.

## 🚀 Hızlı Başlangıç (Tek Komut)

```bash
# Tek komutla her şeyi yap: PRD oluştur/geliştir, prd_enhanced.md üret
python3 tools/automation/prd_auto.py full_auto --wait 60
```

Bu komut şunları yapar:
1. ✅ PRD.md yoksa oluşturur (template'den)
2. ✅ Sistemi otomatik initialize eder
3. ✅ PRD'yi chunk'lara böler
4. ✅ Her chunk için Cursor'da yeni chat tab açar (tek window, çoklu chat)
5. ✅ Chunk'ları AI ile geliştirir
6. ✅ Tek bir `prd_enhanced.md` dosyası oluşturur (ara dosyalar yok)
7. ✅ Tüm işlemleri detaylı loglar

### Tam Pipeline (Cleanup + Git ile)

```bash
# PRD geliştir + temizle + GitHub'a yükle
python3 tools/automation/prd_auto.py start --wait 60
```

### Sadece PRD Geliştirme (Git yok)

```bash
# Sadece PRD'yi geliştir, Git işlemleri yapma
python3 tools/automation/prd_auto.py full_auto --wait 60
```

### Test Modu (Dry-Run)

```bash
# Gerçek işlem yapmadan test et
python3 tools/automation/prd_auto.py full_auto --dry-run --limit 1
```

## Komutlar

### `full_auto` - Ana Komut (Önerilen)

```bash
python3 tools/automation/prd_auto.py full_auto [OPTIONS]
```

**Seçenekler:**
- `--wait SECONDS` - Cursor'dan yanıt beklemek için süre (varsayılan: 60)
- `--limit N` - Sadece N chunk işle (test için)
- `--dry-run` - Test modu (gerçek işlem yapmaz)

**Örnekler:**
```bash
# Tam otomasyon
python3 tools/automation/prd_auto.py full_auto --wait 90

# Test için sadece 1 chunk
python3 tools/automation/prd_auto.py full_auto --wait 60 --limit 1

# Test modu
python3 tools/automation/prd_auto.py full_auto --dry-run --limit 1
```

### `start` - Tam Pipeline (Cleanup + Git ile)

```bash
python3 tools/automation/prd_auto.py start [OPTIONS]
```

**Seçenekler:**
- `--wait SECONDS` - Bekleme süresi
- `--no-git` - Git işlemlerini atla
- `--no-cleanup` - Temizlik işlemlerini atla
- `--dry-run` - Test modu
- `--commit-message MESSAGE` - Git commit mesajı

**Örnekler:**
```bash
# Tam pipeline
python3 tools/automation/prd_auto.py start --wait 90

# Sadece PRD geliştirme, Git yok
python3 tools/automation/prd_auto.py start --no-git --wait 60
```

### `git-sync` - GitHub Senkronizasyonu

```bash
python3 tools/automation/prd_auto.py git-sync [OPTIONS]
```

**Seçenekler:**
- `--message MESSAGE` - Commit mesajı
- `--no-push` - Push yapma, sadece commit
- `--dry-run` - Test modu

**Örnek:**
```bash
python3 tools/automation/prd_auto.py git-sync --message "Update PRD"
```

### `cleanup` - Dosya Temizliği

```bash
python3 tools/automation/prd_auto.py cleanup [OPTIONS]
```

Gereksiz dosyaları temizler:
- `__pycache__/` klasörleri
- `*.pyc`, `*.pyo` dosyaları
- `.DS_Store` dosyaları

**Seçenekler:**
- `--dry-run` - Test modu

## Nasıl Çalışır?

### 1. PRD Oluşturma
- PRD.md yoksa, `prd_template.md`'den otomatik oluşturulur
- Template doldurulmuş bir PRD yapısı içerir

### 2. PRD Analizi
- PRD.md okunur ve bölümlere ayrılır (## ve ### başlıklarına göre)
- Her bölüm ayrı ayrı işlenir

### 3. AI Geliştirme
- Her bölüm için Cursor'da **yeni bir chat** açılır
- Bölüm AI'ya gönderilir ve geliştirilmesi istenir
- Geliştirilmiş bölüm geri alınır

### 4. PRD Güncelleme
- Geliştirilmiş bölümler PRD.md'ye yazılır
- Orijinal içerik korunur, sadece geliştirilmiş versiyonlar eklenir

### 5. GitHub Senkronizasyonu
- `git fetch` - Uzak değişiklikleri al
- `git pull` - Uzak değişiklikleri birleştir
- `git add .` - Tüm değişiklikleri ekle
- `git commit` - Değişiklikleri commit et
- `git push` - GitHub'a yükle

## Gereksinimler

1. **Python 3.7+**
2. **macOS** (AppleScript için)
3. **Cursor** yüklü ve çalışıyor olmalı
4. **macOS Automation İzinleri:**
   - System Settings → Privacy & Security → Accessibility
   - Cursor veya Terminal'i ekleyin

## Sorun Giderme

### Cursor Driver Hatası
```bash
# Test et
python3 tools/automation/prd_auto.py auto-improve --dry-run

# İzinleri kontrol et
# System Settings → Privacy & Security → Accessibility
```

### Git Hatası
```bash
# Git yapılandırmasını kontrol et
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Remote'u kontrol et
git remote -v
```

### PRD Bölümleri Bulunamıyor
- PRD.md'de ## veya ### ile başlayan başlıklar olduğundan emin olun
- Bölüm başlıkları düzgün formatlanmış olmalı

## Log Dosyaları

Tüm işlemler detaylı olarak loglanır:
```bash
# Log dosyasını görüntüle
tail -f tools/automation/prd_auto.log

# Son 50 satırı görüntüle
tail -n 50 tools/automation/prd_auto.log
```

## Örnek Kullanım Senaryoları

### Senaryo 1: Yeni Proje
```bash
# 1. Projeyi klonla veya oluştur
git clone your-repo
cd your-repo

# 2. PRD automation'ı kur (eğer yoksa)
# tools/automation/ klasörünü kopyala

# 3. İlk PRD'yi oluştur ve geliştir
python3 tools/automation/prd_auto.py start --wait 60
```

### Senaryo 2: Mevcut PRD'yi Geliştir
```bash
# Tüm PRD'yi geliştir
python3 tools/automation/prd_auto.py start --wait 90

# Veya sadece belirli bölümleri
python3 tools/automation/prd_auto.py auto-improve --section "Features" --wait 60
```

### Senaryo 3: Test ve İnceleme
```bash
# Önce test et
python3 tools/automation/prd_auto.py start --dry-run

# Sonra gerçek çalıştır
python3 tools/automation/prd_auto.py start --wait 60 --no-git

# PRD'yi incele, sonra manuel commit yap
git add prd.md
git commit -m "Improved PRD"
git push
```

## İpuçları

1. **İlk çalıştırmada `--dry-run` kullanın** - Sistemin nasıl çalıştığını görün
2. **`--wait` süresini artırın** - Büyük bölümler için daha fazla bekleme süresi gerekebilir
3. **Bölüm bazlı işlem yapın** - Tüm PRD yerine belirli bölümleri geliştirin
4. **Log dosyalarını takip edin** - Sorunları hızlıca tespit edin
5. **Git işlemlerini ayrı yapın** - Önce PRD'yi geliştirin, sonra manuel commit yapın

## Destek

Sorun yaşarsanız:
1. Log dosyasını kontrol edin: `tools/automation/prd_auto.log`
2. Dry-run modunda test edin
3. GitHub Issues'da sorun bildirin

