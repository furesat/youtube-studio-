# 001 Kahve · Almanca kanal kurgusu v3 ("Bohne erzählt")

Türkçe versiyonun çevirisi değil. Aynı görsel havuzundan **ayrı bir kurgu**: farklı açılış, farklı sıra, farklı tempo, farklı ses ve görsel dokusu.

## 1. Kurgu ve tempo farkı
| | Türkçe (Fasulye) | Almanca (Bohne erzählt) |
|---|---|---|
| Açılış | Modern kafe + "fincanı sıkı tut" | **Soğuk açılış: Prusya 1781, Kaffeeriecher pencerede kokluyor** |
| Sıra | Kronolojik: Mekke → İstanbul → Londra → Prusya → İsveç → Viyana | Prusya önden ipucu, sonra kronoloji; **Prusya geri dönüş**, **Viyana final** |
| Çekim sayısı | 142 çekim, ort. ~2,8 sn | **60 çekim, ort. ~4.9 sn** |
| Geçiş | Sert kesme, her cümlede yeni kare | Bölüm içi 0,5 sn çapraz geçiş, bölümler arası 1 sn kâğıda karartma |
| Uzunluk | 6:43 | ~5:20–5:50 (sesle kesinleşir) |
| Atılan sahneler | – | S002, S004, S010, S019, S022, S023, S029, S033, S034, S040, S050 + birçok ara çekim |

## 2. Metin ve açılış farkı
- Ton: **sakin, kuru, ince ironi** (Almanca belgesel geleneği). Ünlem ve "rate mal" tarzı sorular yok, espri alt söylemde.
- Kültürel vurgular: Kaffeeriecher (açılış + geri dönüş), "Bier statt Kaffee" ve Biersuppe, Bach Kahve Kantatı (Leipzig), Viyana: Kolschitzky efsanesi, Diodato, kahvehane kültürü kültürel miras.
- Türk okuyucuya özgü adlar çıkarıldı (Peçevi, Hakem/Şems, Bostanzade, Kâtip Çelebi, Kansu Gavri).
- Kapanış girişe bağlanıyor: Friedrich bira istedi, bugün Almanya biradan çok kahve içiyor. "Hat also nicht ganz geklappt."

## 3. Ses ve görsel doku farkı
| | Türkçe | Almanca |
|---|---|---|
| Ses | Yaşlı Adam 3 (klon) | **David – Slow & Charming** (ana dili Almanca, deadpan, uzun duraklar) `LTo9oDjTW1FdEgMfiXWQ` |
| Müzik | 9 parça, her bölüme bir | **En fazla 3 sakin parça**, -34 LUFS; soğuk açılış ve espri anlarında sessizlik |
| Efekt | 19 efekt, damga sesleri | Sadece ortam: koklama, ateş çıtırtısı, sokak; bölüm geçişinde kâğıt hışırtısı. Damga sesi yok |
| Hareket | Dönüşümlü yakınlaşma | **Yatay kaydırma** ağırlıklı, nadiren yaklaşma; hafif çizgi titremesi (render_v3) |
| Kadraj | Tam kare | %6–8 daha sıkı kırpma, odak üçte bir çizgide → aynı görsel farklı kadraj |
| Renk | Sıcak sepya | **Daha serin parşömen**: doygunluk −%12, gölgede hafif mavi-yeşil, kâğıt dokusu + yumuşak vinyet |
| Ekran yazısı | Kırmızı yuvarlak etiket | **Mürekkep siyahı yazı, krem kâğıt şerit**; kırmızı sadece LEGENDE damgasında |

## Çekim listesi (EDL_de_v3.json)
Süreler hedef; ses gelince her çekim kendi cümlesine oturtulur.

| # | Bölüm | Çekim | Süre | Hareket | Metin |
|---|---|---|---|---|---|
| 1 | A Kaltstart | S047 | 6.5 | yatay kaydırma ← | Preußen, siebzehnhunderteinundachtzig. Ein alter Soldat bleibt vor einem offenen Fenster stehen. Und schnuppert. |
| 2 | A Kaltstart | S047d | 4.0 | yavaş yaklaşma | Er sucht keinen Dieb. Er sucht Kaffee. |
| 3 | A Kaltstart | S047b | 6.5 | yatay kaydırma → | Privat gerösteter Kaffee ist in Preußen nämlich verboten. Und der König hat rund vierhundert solcher Männer auf die Straße geschickt. |
| 4 | A Kaltstart | S047c | 3.5 | sabit + çizgi titremesi | Der Volksmund nennt sie: die Kaffeeriecher. |
| 5 | B Heute | S001 | 5.5 | yavaş yaklaşma | Heute ist Kaffee das Lieblingsgetränk der Deutschen. Noch vor Wasser. Und noch vor Bier. |
| 6 | B Heute | S003 | 7.0 | yatay kaydırma → | Preußen war damit übrigens nicht allein. Mekka, Istanbul, London, Schweden. Kaffee wurde immer wieder verboten. |
| 7 | B Heute | S005b | 6.5 | yatay kaydırma ← | Das Merkwürdige daran: Um den Kaffee selbst ging es dabei fast nie. Gehen wir der Sache nach. |
| 8 | C Mekka | S006 | 3.5 | sabit + çizgi titremesi | Mekka, fünfzehnhundertelf. |
| 9 | C Mekka | S007b | 5.5 | yatay kaydırma → | Sufis trinken das neue Getränk aus dem Jemen, um nachts beim Gebet wach zu bleiben. |
| 10 | C Mekka | S008 | 4.5 | yatay kaydırma ← | Bald entstehen Kaffeehäuser. Man sitzt zusammen. Man redet. |
| 11 | C Mekka | S009b | 4.5 | yavaş yaklaşma | Das missfällt Khair Beg, dem Aufseher über Sitte und Ordnung. |
| 12 | C Mekka | S011 | 5.5 | yatay kaydırma → | Er bestellt Gelehrte und Ärzte ein. Die Frage: Macht dieses Getränk betrunken? |
| 13 | C Mekka | S012 | 3.5 | sabit + çizgi titremesi | Das Ergebnis steht vorher fest. Verboten. |
| 14 | C Mekka | S013 | 4.0 | yavaş yaklaşma | Kaffeesäcke brennen auf offener Straße. |
| 15 | C Mekka | S014b | 6.0 | yatay kaydırma ← | Nur untersteht Mekka dem Sultan in Kairo. Und der trinkt, wie man hört, selbst gern Kaffee. |
| 16 | C Mekka | S015 | 4.0 | sabit + çizgi titremesi | Nach wenigen Wochen ist das Verbot vom Tisch. |
| 17 | C Mekka | S016 | 5.0 | yavaş yaklaşma | Merken wir uns: Das Problem war nie die Tasse. Es war der Tisch. |
| 18 | D Istanbul | S017 | 3.5 | sabit + çizgi titremesi | Istanbul, fünfzehnhundertvierundfünfzig. |
| 19 | D Istanbul | S018c | 4.5 | yatay kaydırma → | Zwei Händler aus Syrien eröffnen die ersten Kaffeehäuser der Stadt. |
| 20 | D Istanbul | S020 | 5.0 | yatay kaydırma ← | Man liest, spielt Backgammon, trägt Gedichte vor. |
| 21 | D Istanbul | S021 | 3.5 | yavaş yaklaşma | Und man redet über die Regierung. |
| 22 | D Istanbul | S024 | 4.5 | sabit + çizgi titremesi | Das gefällt nicht jedem Sultan. Murad dem Vierten schon gar nicht. |
| 23 | D Istanbul | S025b | 5.0 | yatay kaydırma → | Sein Bruder Osman war von meuternden Janitscharen ermordet worden. |
| 24 | D Istanbul | S026 | 4.5 | yatay kaydırma ← | Und die Janitscharen trafen sich am liebsten: im Kaffeehaus. |
| 25 | D Istanbul | S027 | 4.5 | yavaş yaklaşma | Sechzehnhundertdreiunddreißig brennt ein großer Teil der Stadt. |
| 26 | D Istanbul | S028 | 6.5 | yatay kaydırma → | Murad hat seinen Vorwand. Wegen Brandgefahr werden die Kaffeehäuser geschlossen, der Tabak gleich mit. Wer erwischt wird, riskiert den Tod. |
| 27 | D Istanbul | S030 | 5.5 | yatay kaydırma ← | Es heißt, er sei nachts verkleidet durch die Gassen gegangen, um Sünder selbst zu ertappen. |
| 28 | D Istanbul | S031 | 3.5 | sabit + çizgi titremesi | Belegt ist das nicht. Gewirkt hat es trotzdem. |
| 29 | D Istanbul | S032b | 5.5 | yatay kaydırma → | Auffällig: Zu Hause durfte man weiter Kaffee trinken. Verboten war nur der gemeinsame Tisch. |
| 30 | D Istanbul | S035b | 4.0 | yavaş yaklaşma | Nach Murads Tod öffnen die Kaffeehäuser wieder. |
| 31 | E London | S036 | 3.5 | sabit + çizgi titremesi | London, sechzehnhundertfünfundsiebzig. |
| 32 | E London | S037c | 6.5 | yatay kaydırma ← | Für einen Penny gibt es Kaffee und Diskussion, so lange man will. Man nennt die Kaffeehäuser Penny-Universitäten. |
| 33 | E London | S038 | 5.0 | yavaş yaklaşma | König Karl der Zweite nennt sie anders: Brutstätten von Lügen über die Regierung. |
| 34 | E London | S039 | 3.5 | sabit + çizgi titremesi | Kurz vor Neujahr verbietet er sie. |
| 35 | E London | S041b | 4.5 | yatay kaydırma → | London protestiert. Händler, Kaufleute, sogar Leute vom Hof. |
| 36 | E London | S042 | 5.0 | sabit + çizgi titremesi | Nach zehn Tagen nimmt der König das Verbot zurück. Noch bevor es überhaupt gilt. |
| 37 | F Preussen | S043 | 7.0 | yavaş yaklaşma | Und damit zurück nach Preußen. Kaffee ist hier längst Alltag. Im benachbarten Leipzig hat Bach sogar eine Kantate darüber geschrieben. |
| 38 | F Preussen | S044b | 5.0 | yatay kaydırma → | Friedrich der Große aber sieht vor allem eines: Geld, das ins Ausland fließt. |
| 39 | F Preussen | S044 | 4.5 | yavaş yaklaşma | Nach seiner Rechnung: Hunderttausende Taler im Jahr. |
| 40 | F Preussen | S045b | 6.5 | yatay kaydırma ← | Siebzehnhundertsiebenundsiebzig empfiehlt er seinen Untertanen: Trinkt Bier. Er selbst sei schließlich mit Biersuppe groß geworden. |
| 41 | F Preussen | S045 | 3.0 | sabit + çizgi titremesi | Die Untertanen sehen das anders. |
| 42 | F Preussen | S045d | 4.5 | yatay kaydırma → | Bier wird schließlich im eigenen Land gebraut. Und bringt Steuern. |
| 43 | F Preussen | S046 | 5.5 | yatay kaydırma → | Also wird das Rösten Staatssache. Wer privat röstet, macht sich strafbar. Und dann kommen die Kaffeeriecher. |
| 44 | F Preussen | S048b | 5.5 | yavaş yaklaşma | Siebzehnhundertsechsundachtzig stirbt Friedrich. Seine Kaffeeriecher überleben ihn nicht lange. |
| 45 | G Schweden | S049 | 5.0 | yatay kaydırma ← | Den Rekord hält Schweden. Fünf Verbote in knapp siebzig Jahren. |
| 46 | G Schweden | S051 | 4.5 | yavaş yaklaşma | Manche Schweden trugen ihre Kaffeekannen sogar zu Grabe. |
| 47 | G Schweden | S052d | 7.5 | yatay kaydırma → | Und dann ist da König Gustav der Dritte. Er soll zwei verurteilte Zwillinge verschont haben, unter einer Bedingung. Der eine trinkt täglich Kaffee, der andere Tee. |
| 48 | G Schweden | S053b | 5.0 | yatay kaydırma ← | Zuerst sterben die Ärzte. Dann der König. Die Zwillinge leben weiter. |
| 49 | G Schweden | S054 | 3.5 | sabit + çizgi titremesi | Ob es dieses Experiment je gab, ist sehr fraglich. |
| 50 | G Schweden | S055b | 4.5 | yavaş yaklaşma | Heute gehört Schweden zu den größten Kaffeetrinkern der Welt. |
| 51 | H Wien | S056 | 3.0 | sabit + çizgi titremesi | Und Wien? |
| 52 | H Wien | S056d | 7.5 | yatay kaydırma → | Die Geschichte kennt hier jeder. Die Osmanen ziehen ab, lassen Säcke voller Bohnen zurück, und der Kundschafter Kolschitzky eröffnet das erste Kaffeehaus. |
| 53 | H Wien | S057 | 4.0 | sabit + çizgi titremesi | Aufgeschrieben wurde das allerdings erst rund hundert Jahre später. |
| 54 | H Wien | S058 | 5.5 | yavaş yaklaşma | Die erste belegte Erlaubnis bekommt sechzehnhundertfünfundachtzig der armenische Händler Johannes Diodato. |
| 55 | H Wien | S058b | 5.5 | yatay kaydırma ← | Heute ist die Wiener Kaffeehauskultur immaterielles Kulturerbe. Ein Verbot hätte da wenig Chancen. |
| 56 | I Schluss | S059 | 6.0 | yatay kaydırma → | Mekka, Istanbul, London, Preußen. Es ging um Versammlungen, um Aufstände, um Gerede und um Geld. |
| 57 | I Schluss | S059f | 4.0 | yavaş yaklaşma | Um das Getränk ging es so gut wie nie. |
| 58 | I Schluss | S060 | 6.0 | yatay kaydırma ← | Kaffee hat Menschen an einen Tisch gebracht, sie reden lassen und wach gehalten. Das war sein eigentliches Vergehen. |
| 59 | I Schluss | S061 | 6.0 | yavaş yaklaşma | Friedrich wollte übrigens, dass seine Untertanen Bier trinken. Heute trinkt Deutschland mehr Kaffee als Bier. |
| 60 | I Schluss | S061d | 4.0 | sabit + çizgi titremesi | Hat also nicht ganz geklappt. |

## Başlık / kapak
- **Titel:** Der König, der Kaffee-Schnüffler auf die Straße schickte
- Alternatif: Warum wurde Kaffee immer wieder verboten?
- **Kapak:** Kaffeeriecher burun yakın planı (S047d) + "VERBOTEN?" – Türkçe kapaktan farklı görsel.
