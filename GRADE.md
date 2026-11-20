# GRADE — news-image-20261119 (entri v1, build 2026-11-20 pagi WIB)

## Cek teknis (grade lokal dari design spec)

| Cek | Hasil |
|---|---|
| main.py 2x run, sha256 | **IDENTIK** — `8441524365ff4da09cec06ff3c501a86a5065344cabb8c27db640137bb6bb4dc` (out1 == out2) |
| PNG valid 1024x1024 | YA — format PNG, mode P (palet 256 warna), 1024x1024 |
| Ukuran file | **136.316 byte** — di bawah target ≤160 KB (tie-break bagus vs papan atas 222–832 KB) |
| Fallback tanpa Pillow | YA — dengan PIL diblokir, main.py menyalin entry.png byte-for-byte (sha256 sama) |
| Tanggal di gambar | THURSDAY 19 NOVEMBER 2026 — chip besar di masthead + strap "36 STORIES • 6 CONTINENTS • ONE FRONT PAGE" |
| Teks garbled / artefak | TIDAK ADA — gambar diperiksa langsung; semua 36 headline terbaca, panorama terbaca |
| Putaran review | 1 putaran: (a) render pertama 459 KB RGB → palet 256 warna tanpa dither (136 KB); (b) adegan LEONIDA diperbaiki (matahari jadi cakram padat, palem dipertebal + fronds krem agar terbaca); (c) DEEP SPACE diperbaiki (piringan miring + feed arm, bukan kubah). Render ulang + verifikasi ulang. |

## 36 headline + sumber (semua pertama dilaporkan 19 Nov 2026)

### ASIA
1. Trump, Xi and Putin hold first trilateral summit in Shenzhen — USA Today / BBC / NYT
2. ICJ: Myanmar committed genocide against the Rohingya — Le Monde / NPR / Amnesty
3. Iran drones hit US bases in Kuwait and Bahrain — Reuters (via The Leaders Online) / The Curtain
4. Houthi missile damages Riyadh's PIF Tower — NYT (reporter di Riyadh) / NewsSumm
5. Israel launches ground operation in central Gaza — The Guardian
6. Cyclone Akvan nears India's east coast, landfall Friday — IMD via The Week / IANS
7. Bangladesh unrest: four killed, Yunus home torched — eGazette Daily Brief
8. North Korea expanding uranium enrichment, IAEA warns — IAEA / Just Security
9. South Korea court orders retrial for ex-PM Han — NewsSumm / The Guardian

### EUROPE
10. Ukraine allies meet in Berlin to back Kyiv — The Guardian / Europa Express
11. Russian strikes kill five in Ukraine; Kyiv hits Kerch Bridge — eGazette / Just Security
12. Russian drones damage Dutch, Austrian embassies in Kyiv — NewsSumm
13. Denmark approves US-Greenland Arctic security deal — Just Security / NewsSumm
14. AI cyberattack disrupts European Commission systems — NewsSumm (28 outlet)
15. UK Covid inquiry: late border controls left UK exposed — France 24
16. COP31 deadlocked on fossil fuels and finance — The Hindu BusinessLine

### AFRICA
17. Migrant boat sinks off Senegal; dozens missing — BBC / eGazette
18. Somalia expels UAE ambassador over sovereignty row — Al Jazeera
19. Nigeria's APGA endorses Tinubu for 2027 — NewsSumm
20. Ghana minister gives CPR to woman at COP31 — GyeNyame News
21. Dakar Youth Games put Africa on Olympic map — FrancsJeux

### NORTH AMERICA
22. Anthropic IPO raises record $107.3bn on Nasdaq debut — Bloomberg / CoinDesk
23. GTA VI launches: 99 Metascore, $1.84bn day one — USA Today (SensorTower)
24. Jeffries nominated Speaker 251-11, a first — TheWrap / The Guardian
25. Musk: "I'm not MAGA", regrets $500m spending — NYT DealBook via TheWrap
26. Trump asks top court to block Venezuelan TPS shield — AP via Bangladesh Chronicle
27. Begich keeps Alaska seat; last 2026 race called — AP (ditelepon Rabu malam AS = 19 Nov di Asia; dilaporkan di briefing pagi 19 Nov)
28. Voyager 1 confirmed one light-day from Earth — NASA / Reuters

### SOUTH AMERICA
29. Hegseth visits Colombia, delivers C-130 Hercules — Latin America Reports
30. Hegseth signs military deal in Venezuela — The Guardian / Daily The Destination
31. Colombia arrests 26 Clan del Golfo members — Breitbart
32. Flamengo loses Betano shirt deal in betting ban — SportBusiness

### OCEANIA
33. Australia jobless rate hits 4.9%, five-year high — One Turn / ABC
34. Bancroft: whole team knew of ball-tampering plot — ABC / BBC via One Turn
35. Nicholls ton lifts New Zealand to 243/5 vs India — EIN / NZ Herald
36. Cyclone Xavier threatens Northern Cook Islands — Orbis Weather

Catatan atribusi: klaim sensitif memakai atribusi di sumbernya (mis. "per ICJ estimate"
untuk 10.000 korban Rohingya; "SensorTower" untuk $1.84bn GTA VI). Dua cerita
(Begich, Musk) diumumkan Rabu malam waktu AS tapi pertama kali dilaporkan secara
luas di briefing 19 Nov dan jatuh pada 19 Nov di zona waktu Asia — sesuai aturan
"in any time zone".

## Penilaian jujur vs bar zona hadiah 98.8549% (Top 50), target #10 99.0595%

**Kekuatan:** tanggal mustahil terlewat (chip besar + strap); 36 cerita terverifikasi
lintas 6 benua dengan semua lead besar hari itu (Shenzhen, ICJ, GTA VI, IPO
Anthropic, Voyager); sudut "ONE DAY, ONE SKYLINE" original dan beda dari
front-page grid papan atas maupun v2 sibling 20261118; terbaca bersih pada
ukuran kecil; file 136 KB memberi keunggulan tie-break nyata melawan entri
222–832 KB di papan atas.

**Kelemahan yang tersisa:** (1) panorama digambar sebagai piktogram sederhana,
bukan adegan foto/realistis — kriteria craft (C5) bisa kalah dari entri dengan
render lebih kaya; (2) 36 cerita vs 40–43 di beberapa entri top; (3) tiap
segmen panorama hanya ~124 px lebar, labelnya mungil saat gambar dilihat
pada 300 px; (4) skor terkompresi (field 10.978 entri, #1–#50 selisih ~0,38
poin) dan judge head-to-head itu noisy — hasil akhir sangat tergantung
pairing Swiss/playoff.

**Verdict:** peluang masuk zona hadiah (Top 50, $3) **masuk akal tapi tidak
terjamin** — entri ini kuat di C1–C4 (tanggal, seleksi, keterbacaan,
keakuratan) dan kompetitif di tie-break ukuran, tapi Top 10 (99.0595%)
kemungkinan besar di luar jangkauan karena craft panorama yang sederhana.
Layak submit sebagai v1; kalau mau dorong lebih jauh, challenger berikutnya
harus menaikkan kekayaan visual panorama (bukan menambah cerita).
