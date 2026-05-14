# Otel QR Sifariş Sistemi — Texniki Plan

**Layihə sahibi:** Grand Hotel Baku Central Park 4*
**Tarix:** 2026-05-13
**Status:** Developer-ə sifariş üçün hazır

---

## 1. Layihənin Məqsədi

Hər otaqda QR kod olsun. Qonaq skan etsin → veb səhifə açilsin → orada otel xidmətləri, məlumat, sifariş imkanı görsun. Sifariş verəndə dərhal resepsion/housekeeping/restoran-a Telegram-da bildiriş getsin. Qonaq heç bir app yükləmir, qeydiyyat etmir.

**Biznes məqsədləri:**
- In-stay xərcləməni 30-40% artırmaq (spa, restoran, tur upsell)
- Resepsiona telefon zənglərini azaltmaq
- Qonaq narazılıqlarını real-time həll etmək (Booking-də pis rey əvəzinə)
- Qonaq mə'lumat bazasını formalaşdırmaq (CRM)

---

## 2. Sistem Necə İşləyir

```
[Qonaq otaqda] ──skan──> [Veb səhifə açılır]
                                │
                                ↓
                          [Sifariş verir]
                                │
                                ↓
                       [Backend — Supabase]
                                │
        ┌───────────────────────┼────────────────────────┐
        ↓                       ↓                        ↓
[Telegram bot]          [Resepsion tablet]        [PMS — Opera/Protel]
   │  │  │                 (dashboard)              (qonaq hesabına yaz)
   ↓  ↓  ↓
🍽 F&B    🛏 Housekeeping    💆 Spa    🛎 Resepsion
qrupu     qrupu               qrupu     qrupu
```

---

## 3. Funksional Tələblər

### 3.1 Qonaq Tərəfi (Veb Tətbiq — PWA)

**Vacib şərt:** App yükləmə YOX. Browser-də açılır. Mobile-first dizayn.

**Dil dəstəyi:**
- Azərbaycan (default)
- İngilis
- Rus
- Ərəb (Körfəz turistləri ücün vacib)
- Telefonun dilinə görə avtomatik seçim

**Ekranlar:**

1. **Ana ekran** (QR oxudandan sonra ilk gördüyü):
   - Otelin logosu və adı
   - Otaq nömrəsi avtomatik göstərilir (URL-dən gəlir)
   - WiFi parol (one-tap copy)
   - Səhər yeməyi vaxtı, hovuz/spa/gym saatları
   - 4 əsas kateqoriya düyməsi

2. **Otaq Xidməti (F&B):**
   - Səhər yeməyi / Şam yeməyi / Şirniyat / İçkilər kateqoriyaları
   - Hər məhsulun şəkli, adı, qiyməti
   - Cart sistemi (add/remove/quantity)
   - Sifariş təsdiqi → bildiriş gedir

3. **Housekeeping:**
   - "Tez sifariş" şablonları: əlavə dəsmal, slipper, su, şampun, çarpayı dəyişdirilməsi, otaq təmizliyi
   - "Səs etməyin" rejimi düyməsi
   - Çatdırılma vaxtı seçimi (indi / 1 saat sonra / sabah səhər)

4. **Spa & Wellness:**
   - Xidmət siyahısı (klassik masaj, aroma, hammam, üz baxımı)
   - Real-time mövcud saatlar
   - Rezerv → Spa qrupuna bildiriş

5. **Resepsion:**
   - Geç check-out / erkən check-in tələbi
   - Taksi / transfer sifarişi
   - Tur paketləri (Qobustan, Şahdağ, Qəbələ)
   - Sərbəst mesaj (chat formatı)

6. **Sifariş statusu:**
   - Real-time yenilənir
   - 4 mərhələ: Qebul edildi → Hazırlanır → Çatdırılır → Tamam
   - İstəyə bağlı SMS bildiriş (qonaq telefon yazsa)

7. **Şəhər bələdçisi (bonus):**
   - Otelin tövsiyəsiylə restoranlar, görməli yerlər
   - Xəritə inteqrasiyası
   - Anti-scam taksi qiyməti

### 3.2 Staff Tərəfi (Telegram + Dashboard)

**Telegram qrupları:**
- 🍽 Restoran/F&B
- 🛏 Housekeeping
- 💆 Spa
- 🛎 Resepsion (general + suallar)
- 🚨 Eskalasiya (menecer üçün)

**Bildirim formatı:**
```
🔔 Yeni sifariş — Otaq 304
🛏 2x əlavə dəsmal + 1x slipper
🕐 17:34
[✅ Qəbul etdim] [✓ Tamamladım] [❌ İmtina]
```

**Eskalasiya qaydası:**
- 2 dəq cavab yox → Telegram qrupa təkrar
- 5 dəq cavab yox → menecere şəxsi mesaj + zəng (Twilio)
- 10 dəq cavab yox → sahibkar SMS

**Web Dashboard** (resepsion tablet üçün):
- Bütün aktiv sifarişlər canlı görünür
- Status sürətli dəyişdirilir
- Gün/həftə/ay üzrə statistika
- Otaq bazında satış hesabatı

### 3.3 Admin Tərəfi (Sahibkar üçün)

- Menu redaktoru (məhsul əlavə/sil/qiymət dəyiş)
- Qiymət/aksiya idarəsi
- Hesabat: ən çox sifariş edilən, ən yüksək gəlirli xidmət
- Staff performance: kim neçə dəqiqədə cavablayır
- Eksport: Excel/CSV mühasibata ötürmək üçün

---

## 4. Texniki Stack

| Layer | Texnologiya | Səbəb |
|---|---|---|
| **Frontend** | Next.js 14 + TypeScript + Tailwind CSS | Modern, sürətli, PWA dəstəyi |
| **Mobile UX** | PWA (Progressive Web App) | App yükləmə yox, "Add to Home Screen" var |
| **i18n** | next-intl | 4 dil dəstəyi |
| **Backend / DB** | Supabase (Postgres + Realtime + Auth + Storage) | Hazır həll, real-time daxildir |
| **Bildirim** | Telegram Bot API | Pulsuz, etibarlı |
| **SMS (eskalasiya)** | Twilio | Azərbaycanda işləyir |
| **Hosting** | Vercel (frontend) + Supabase (backend) | Sıfır DevOps yükü |
| **QR generasiya** | qrcode.js | Hər otaq üçün unikal token-li URL |
| **PMS inteqrasiyası** | REST API (PMS-dən asılı) | Faza 2-də |

**Aylıq xərc (100 otaq miqyasında):**
- Vercel: pulsuz (Hobby tier kifayət)
- Supabase Pro: $25
- Telegram: pulsuz
- Twilio (eskalasiya SMS): ~$10-20
- Domain: $15/il
- **Cəmi: ~$40-50/ay**

---

## 5. Mərhələlər (Sprints)

### Sprint 1 — MVP (3 hefte) ✦ ESAS
**Məqsəd:** İşləyən, qonaqlara verilə bilən minimal versiya.

- [ ] Supabase qurulması, sxem dizaynı
- [ ] Veb tətbiq — ana ekran + 2 dil (Az + En)
- [ ] Housekeeping və Resepsion sifariş axını
- [ ] Telegram bot + 2 qrup (test üçün)
- [ ] QR generator + 10 otaq üçün laminat kartlar
- [ ] Sadə dashboard

**Çıxış meyari:** 10 otaqda 1 hafte real istifadə, ən azı 20 sifariş.

### Sprint 2 — Genişlənmə (3 hefte)
- [ ] F&B menyu + cart sistemi
- [ ] Spa rezerv sistemi
- [ ] Rus + Ərəb dilləri
- [ ] Tam dashboard + hesabatlar
- [ ] Eskalasiya sistemi (Twilio)
- [ ] Bütün otaqlara genişlənmə

### Sprint 3 — İnteqrasiya (2 hefte)
- [ ] PMS API inteqrasiyası (Opera/Protel — sənin sistemə bağli)
- [ ] Avtomatik faktura/hesab
- [ ] Admin menu redaktoru
- [ ] Tur paketləri modulu
- [ ] Email/SMS marketing (CRM)

### Sprint 4 — Optimallaşdırma (1 hefte)
- [ ] Performans testi
- [ ] A/B test sistemi (hansı UI daha çox sifariş gətirir)
- [ ] Analytics (Mixpanel ya PostHog)
- [ ] Sənədləşmə + staff təlimi

**Cəmi: 9 hefte (~2 ay yarım)**

---

## 6. Qebul Meyarları

Layihə "hazırdı" sayılır əgər:

✅ Qonaq QR oxudandan **3 saniyəyə** səhifə açılır
✅ Sifariş **2 saniyə icinde** Telegram-a düşür
✅ Staff sifarişi **30 saniyəyə** qəbul edib status dəyişir
✅ 4 dil tam işləyir, dil dəyişdirildə hamısı tərcümə olunur
✅ 100 eyni anda istifadəçi sistemə düşməyə zorlasin
✅ Eskalasiya işləyir (test: 5 dəqiqə cavab verməyəndə zəng gəlir)
✅ Dashboard-da bütün sifarişlər real-time görünür
✅ Mobil cihazda (iOS Safari + Android Chrome) tam işləyir
✅ Offline rejim (zəif internet) zamanı UI çökmür

---

## 7. Vaxt + Büdcə Təxmini

| Mərhələ | Vaxt | Developer xərci (təxmini) |
|---|---|---|
| Sprint 1 (MVP) | 3 hefte | $2,500-3,500 |
| Sprint 2 | 3 hefte | $2,500-3,500 |
| Sprint 3 (PMS inteqr.) | 2 hefte | $1,500-2,500 |
| Sprint 4 | 1 hefte | $800-1,200 |
| **Cəmi** | **9 hefte** | **$7,300-10,700** |

**Əlavə xərclər:**
- Dizayn (əgər dedicated designer lazımdırsa): $1,000-2,000
- QR kartların printi (laminat, hər otağa): ~$2/otaq
- Dizayn testləri / fokus qrupları: opsional
- Aylıq dəstək/yenilik: $300-500/ay (developer ile retainer)

**Əgər təcrübəli single developer tutsan (Bakı bazarı):**
- Saatlıq: $15-25
- Cəmi ~250 saat → **~$4,000-6,000**
- Daha ucuz, amma sürət və keyfiyyət develop-dan asılı

---

## 8. Developerə Verilən Suallar

İlk görüşdə bu sualları soruş:

1. **Təcrübə:** Daha əvvəl PWA layihəsi yazmısan? Real-time sistemlə (WebSocket/Supabase Realtime) işləyirsən?
2. **Tech stack:** Next.js + Supabase ilə razısan, yoxsa başqa təklifin var?
3. **Telegram Bot API:** Daha əvvəl bot inteqrasiyası etmisən?
4. **PMS:** Opera/Protel REST API ilə təcrübən var? (Yox cavabı normaldı, Faza 2-də öyrənmək olar.)
5. **Çox dillilik:** Ərəbcə RTL (sağdan-sola) dəstəyi necə edəcəksən?
6. **Vaxt:** 9 həftədə qurtarmaq mümkündür? Hansi hissələrdə risk görürsən?
7. **Maintenance:** Layihə qurtardıqdan sonra dəstək necə olur — saatlıq ya retainer?
8. **Sənədləşmə:** Kod təhvil verəndə README + admin təlimatı yazırsan?
9. **Hosting:** Account-lar (Vercel, Supabase) kimin adına olacaq — sənin, mənim, ya şirkətin?
10. **Müəlliflik:** Kod sahibi kim olur (vacib məsələ)?

---

## 9. Risk Reyestri

| Risk | Ehtimal | Təsir | Yumşaltma |
|---|---|---|---|
| Qonaqlar QR-i skan etmir | Orta | Yüksek | İlk 2 hafte real test, kart dizaynında "WiFi şifrəsi üçün skan edin" kimi cəlbedici mətn |
| Staff Telegram bildiriməsini görmür | Aşağı | Yüksek | Eskalasiya sistemi (5 dəq sonra zəng) |
| PMS inteqrasiyası işləmir | Orta | Orta | Faza 2-də manual rejim ilə başla |
| Ərəbcə tərcümə zəifdir | Orta | Yüksek | Doğma ərəb dili daşıyıcısı ilə yoxlama |
| Yüksek tələbatda backend yavaşıyır | Aşağı | Orta | Supabase Pro tier, monitoring qur |

---

## 10. Layihənin Uzunmuddətli Vizyonu

Bu sistem sirf bir otel üçün deyil. **3 mərhələli inkişaf:**

1. **Birinci il:** Grand Hotel Baku Central Park-da tam istifadə, ROI sübutu
2. **İkinci il:** Beynəlxalq dil dəstəyi (xüsusilə ərəbcə) ilə **Marhaba Baku** turist app-ı ilə birləşmə
3. **Üçüncü il:** SaaS modelə çevrilir — başqa Azərbaycan oteləri istifadə edir (Qəbələ, Şahdağ, Quba) — aylıq $500-1000 abunəlik

---

## Əlavə: İlk Test Üçün Sadə MVP

Bu planı tam realizə etmədən, **bu hefte test ola bilər:**

1. **Tally.so**-da sadə form yarat (sirf housekeeping + resepsion)
2. **Make.com** ilə Tally → Telegram bot bağla
3. QR yarat, 5 otaqa qoy
4. 1 hafte sına: neçə qonaq skan edir, ne sifariş verir
5. Cavab pozitivdirse → bu plana keç

**Test xərci: $50 + 1 saat vaxtın. Risk: sıfır.**

---

**Plan müəllifi:** Claude (sənin texniki məsləhətçin)
**Növbəti addım:** Bu planı 2-3 developerə göndər, qiymət təklifi al, ən yaxşısını seç.
