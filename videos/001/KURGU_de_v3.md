# 001 Kahve · Almanca kanal kurgusu v3 ("Bohne erzählt")

Türkçe versiyonun çevirisi değil: aynı görsel havuzundan + 14 yeni görselle **ayrı bir kurgu**. Farklı açılış, farklı sıra, farklı tempo, farklı ses ve görsel dokusu.

**Hedef uzunluk:** 7:30–8:30 · 940 kelime · 78 çekim

## 1. Kurgu ve tempo farkı
| | Türkçe (Fasulye) | Almanca (Bohne erzählt) |
|---|---|---|
| Açılış | Modern kafe + "fincanı sıkı tut" | **Soğuk açılış: Prusya 1781, Kaffeeriecher pencerede kokluyor** |
| Sıra | Mekke → İstanbul → Londra → Prusya → İsveç → Viyana | Prusya ipucu → kronoloji → **Prusya ana bölüm (Bach, baskın, Zichorie)** → İsveç → Viyana → **DDR 1977** → kapanış |
| Çekim | 142 çekim, ort. ~2,8 sn | **78 çekim, ort. ~5.1 sn** |
| Geçiş | Sert kesme | Bölüm içi 0,5 sn çapraz geçiş, bölümler arası 1 sn kâğıda kararma |
| Uzunluk | 6:43 | ~7:30–8:30 (sesle kesinleşir) |
| Atılan | – | S002, S004, S010, S019, S022, S023, S029, S033, S034, S040, S050 + ara çekimler |

**Bölüm süreleri (hedef, sessiz):** A Kaltstart 24 sn · B Heute 23 sn · C Mekka 46 sn · D Istanbul 60 sn · E London 28 sn · F Preussen 100 sn · G Schweden 30 sn · H Wien 26 sn · H2 DDR 34 sn · I Schluss 27 sn

## 2. Metin ve açılış farkı
- Ton: **sakin, kuru, ince ironi**. Ünlem ve "rate mal" tarzı sorular yok.
- Almanca izleyiciye özgü bölümler: Kaffeeriecher (açılış + baskın), Friedrich Wilhelm I. lüks malı, Yedi Yıl Savaşı sonrası boş hazine, "Trinkt Bier" ve Biersuppe, **Bach Kahve Kantatı: baba kızına kahveyi yasaklıyor ve kaybediyor**, Hessen-Kassel, **Zichorie / Preußenkaffee / Blümchenkaffee / Muckefuck**, Viyana (Kolschitzky efsanesi, Diodato, kültürel miras), **DDR 1977 Kaffee-Mix / "Erichs Krönung"**.
- Türk okuyucuya özgü adlar çıkarıldı (Peçevi, Hakem/Şems, Bostanzade, Kâtip Çelebi, Kansu Gavri).
- Kapanış girişe bağlanıyor: Friedrich bira istedi, bugün Almanya biradan çok kahve içiyor. "Hat also nicht ganz geklappt."

## 3. Ses ve görsel doku farkı
| | Türkçe | Almanca |
|---|---|---|
| Ses | Yaşlı Adam 3 | **Yaşlı Adam 1** ("Yasli adam", `x6MH8NM5Cgf2UNidRBXE`), daha yavaş okuma, espri sonrası 0,6 sn durak |
| Müzik | 9 parça | **Müzik yok** |
| Efekt | 19 efekt, damga sesleri | Sadece ortam: koklama, ateş çıtırtısı, sokak, kâğıt hışırtısı (bölüm geçişi). Damga sesi yok |
| Hareket | Dönüşümlü yakınlaşma | **Yatay kaydırma** ağırlıklı; hafif çizgi titremesi |
| Kadraj | Tam kare | %6–8 daha sıkı kırpma, odak üçte bir çizgide |
| Renk | Sıcak sepya | **Serin parşömen**: doygunluk −%12, kâğıt dokusu + yumuşak vinyet; DDR bölümü daha gri |
| Ekran yazısı | Kırmızı yuvarlak etiket | Krem kâğıt şerit üstünde mürekkep siyahı; kırmızı sadece LEGENDE damgasında |
| Görseller | 142 çekim | 49 mevcut + **14 yeni (D01–D14)**, aynı karede farklı kadraj |

## Çekim listesi (EDL_de_v3.json)
Süreler hedef; ses gelince her çekim kendi cümlesine oturtulur.

| # | Bölüm | Çekim | Süre | Hareket | Metin |
|---|---|---|---|---|---|
| 1 | A Kaltstart | D01 **(yeni)** | 4.0 | yatay kaydırma → | Preußen, siebzehnhunderteinundachtzig. |
| 2 | A Kaltstart | S047 | 6.5 | yatay kaydırma ← | Ein alter Soldat bleibt vor einem offenen Fenster stehen. Und schnuppert. |
| 3 | A Kaltstart | S047d | 4.0 | yavaş yaklaşma | Er sucht keinen Dieb. Er sucht Kaffee. |
| 4 | A Kaltstart | S047b | 6.5 | yatay kaydırma → | Privat gerösteter Kaffee ist in Preußen nämlich verboten. Und der König hat rund vierhundert solcher Männer auf die Straße geschickt. |
| 5 | A Kaltstart | S047c | 3.5 | sabit + çizgi titremesi | Der Volksmund nennt sie: die Kaffeeriecher. |
| 6 | B Heute | S001 | 5.5 | yavaş yaklaşma | Heute ist Kaffee das Lieblingsgetränk der Deutschen. |
| 7 | B Heute | D02 **(yeni)** | 4.0 | yavaş yaklaşma | Noch vor Wasser. Und noch vor Bier. |
| 8 | B Heute | S003 | 7.0 | yatay kaydırma → | Preußen war damit übrigens nicht allein. Mekka, Istanbul, London, Schweden. Kaffee wurde immer wieder verboten. |
| 9 | B Heute | S005b | 6.5 | yatay kaydırma ← | Das Merkwürdige daran: Um den Kaffee selbst ging es dabei fast nie. Gehen wir der Sache nach. |
| 10 | C Mekka | S006 | 3.5 | sabit + çizgi titremesi | Mekka, fünfzehnhundertelf. |
| 11 | C Mekka | S007b | 5.5 | yatay kaydırma → | Sufis trinken das neue Getränk aus dem Jemen, um nachts beim Gebet wach zu bleiben. |
| 12 | C Mekka | S008 | 4.5 | yatay kaydırma ← | Bald entstehen Kaffeehäuser. Man sitzt zusammen. Man redet. |
| 13 | C Mekka | S009b | 4.5 | yavaş yaklaşma | Das missfällt Khair Beg, dem Aufseher über Sitte und Ordnung. |
| 14 | C Mekka | S011 | 5.5 | yatay kaydırma → | Er bestellt Gelehrte und Ärzte ein. Die Frage: Macht dieses Getränk betrunken? |
| 15 | C Mekka | S012 | 3.5 | sabit + çizgi titremesi | Das Ergebnis steht vorher fest. Verboten. |
| 16 | C Mekka | S013 | 4.0 | yavaş yaklaşma | Kaffeesäcke brennen auf offener Straße. |
| 17 | C Mekka | S014b | 6.0 | yatay kaydırma ← | Nur untersteht Mekka dem Sultan in Kairo. Und der trinkt, wie man hört, selbst gern Kaffee. |
| 18 | C Mekka | S015 | 4.0 | sabit + çizgi titremesi | Nach wenigen Wochen ist das Verbot vom Tisch. |
| 19 | C Mekka | S016 | 5.0 | yavaş yaklaşma | Merken wir uns: Das Problem war nie die Tasse. Es war der Tisch. |
| 20 | D Istanbul | S017 | 3.5 | sabit + çizgi titremesi | Istanbul, fünfzehnhundertvierundfünfzig. |
| 21 | D Istanbul | S018c | 4.5 | yatay kaydırma → | Zwei Händler aus Syrien eröffnen die ersten Kaffeehäuser der Stadt. |
| 22 | D Istanbul | S020 | 5.0 | yatay kaydırma ← | Man liest, spielt Backgammon, trägt Gedichte vor. |
| 23 | D Istanbul | S021 | 3.5 | yavaş yaklaşma | Und man redet über die Regierung. |
| 24 | D Istanbul | S024 | 4.5 | sabit + çizgi titremesi | Das gefällt nicht jedem Sultan. Murad dem Vierten schon gar nicht. |
| 25 | D Istanbul | S025b | 5.0 | yatay kaydırma → | Sein Bruder Osman war von meuternden Janitscharen ermordet worden. |
| 26 | D Istanbul | S026 | 4.5 | yatay kaydırma ← | Und die Janitscharen trafen sich am liebsten: im Kaffeehaus. |
| 27 | D Istanbul | S027 | 4.5 | yavaş yaklaşma | Sechzehnhundertdreiunddreißig brennt ein großer Teil der Stadt. |
| 28 | D Istanbul | S028 | 6.5 | yatay kaydırma → | Murad hat seinen Vorwand. Wegen Brandgefahr werden die Kaffeehäuser geschlossen, der Tabak gleich mit. Wer erwischt wird, riskiert den Tod. |
| 29 | D Istanbul | S030 | 5.5 | yatay kaydırma ← | Es heißt, er sei nachts verkleidet durch die Gassen gegangen, um Sünder selbst zu ertappen. |
| 30 | D Istanbul | S031 | 3.5 | sabit + çizgi titremesi | Belegt ist das nicht. Gewirkt hat es trotzdem. |
| 31 | D Istanbul | S032b | 5.5 | yatay kaydırma → | Auffällig: Zu Hause durfte man weiter Kaffee trinken. Verboten war nur der gemeinsame Tisch. |
| 32 | D Istanbul | S035b | 4.0 | yavaş yaklaşma | Nach Murads Tod öffnen die Kaffeehäuser wieder. |
| 33 | E London | S036 | 3.5 | sabit + çizgi titremesi | London, sechzehnhundertfünfundsiebzig. |
| 34 | E London | S037c | 6.5 | yatay kaydırma ← | Für einen Penny gibt es Kaffee und Diskussion, so lange man will. Man nennt die Kaffeehäuser Penny-Universitäten. |
| 35 | E London | S038 | 5.0 | yavaş yaklaşma | König Karl der Zweite nennt sie anders: Brutstätten von Lügen über die Regierung. |
| 36 | E London | S039 | 3.5 | sabit + çizgi titremesi | Kurz vor Neujahr verbietet er sie. |
| 37 | E London | S041b | 4.5 | yatay kaydırma → | London protestiert. Händler, Kaufleute, sogar Leute vom Hof. |
| 38 | E London | S042 | 5.0 | sabit + çizgi titremesi | Nach zehn Tagen nimmt der König das Verbot zurück. Noch bevor es überhaupt gilt. |
| 39 | F Preussen | S043 | 7.5 | yavaş yaklaşma | Und damit zurück nach Preußen. Kaffee ist hier längst Alltag. Schon Friedrichs Vater hatte ihn zum Luxusgut erklärt, was ihn natürlich nur noch begehrter machte. |
| 40 | F Preussen | D03 **(yeni)** | 5.0 | yatay kaydırma ← | Im benachbarten Leipzig führt Bach um siebzehnhundertvierunddreißig im Kaffeehaus eine Kantate auf. Ihr Thema: ein Kaffeeverbot. |
| 41 | F Preussen | D07 **(yeni)** | 6.5 | yavaş yaklaşma | Ein Vater namens Schlendrian will seiner Tochter Lieschen den Kaffee verbieten. Er droht mit allem: keine neuen Kleider, keine Spaziergänge, kein Fenster zur Straße. |
| 42 | F Preussen | D07 **(yeni)** | 5.5 | sabit + çizgi titremesi | Lieschen bleibt gelassen. Ohne ihre drei Schalen Kaffee am Tag, singt sie, würde sie vertrocknen wie ein Ziegenbraten. |
| 43 | F Preussen | D08 **(yeni)** | 6.5 | yatay kaydırma → | Erst als der Vater ihr einen Ehemann verspricht, gibt sie nach. Heimlich aber lässt sie ausrichten: Heiraten wird sie nur einen Mann, der ihr den Kaffee erlaubt. |
| 44 | F Preussen | D08 **(yeni)** | 4.0 | yavaş yaklaşma | Ein Kaffeeverbot, das schon im Lied scheitert. |
| 45 | F Preussen | S044b | 6.5 | yatay kaydırma → | Nach dem Siebenjährigen Krieg ist die Staatskasse leer. Und Friedrich der Große sieht vor allem eines: Geld, das ins Ausland fließt. |
| 46 | F Preussen | S044 | 4.5 | yavaş yaklaşma | Nach seiner Rechnung: Hunderttausende Taler im Jahr. |
| 47 | F Preussen | S045b | 6.5 | yatay kaydırma ← | Siebzehnhundertsiebenundsiebzig empfiehlt er seinen Untertanen: Trinkt Bier. Er selbst sei schließlich mit Biersuppe groß geworden. |
| 48 | F Preussen | S045 | 3.0 | sabit + çizgi titremesi | Die Untertanen sehen das anders. |
| 49 | F Preussen | S045d | 4.5 | yatay kaydırma → | Bier wird schließlich im eigenen Land gebraut. Und bringt Steuern. |
| 50 | F Preussen | S046 | 6.0 | yatay kaydırma → | Siebzehnhunderteinundachtzig wird das Rösten Staatssache. Gebrannt werden darf nur noch in königlichen Röstereien. Wer privat röstet, macht sich strafbar. |
| 51 | F Preussen | D06 **(yeni)** | 7.0 | yatay kaydırma ← | Jetzt schlägt die Stunde der Kaffeeriecher. Ausgediente Soldaten ziehen durch die Gassen. Wer beim heimlichen Kaffeeklatsch erwischt wird, zahlt eine saftige Strafe. |
| 52 | F Preussen | D06 **(yeni)** | 4.5 | yavaş yaklaşma | Die Kanne verschwindet dann eben unter dem Tisch. |
| 53 | F Preussen | S003 | 5.0 | sabit + çizgi titremesi | Preußen war damit nicht einmal allein. Auch in Hessen-Kassel gingen Kaffeeriecher auf Streife. |
| 54 | F Preussen | D09 **(yeni)** | 6.5 | yatay kaydırma → | Und viele steigen um: auf geröstete Zichorienwurzel. Man nennt das Getränk Preußenkaffee. Oder, wegen der blauen Blüten der Wegwarte, Blümchenkaffee. |
| 55 | F Preussen | D10 **(yeni)** | 6.0 | yatay kaydırma ← | In Braunschweig entsteht schon siebzehnhundertsiebzig eine der ersten Zichorienfabriken. Bald folgen viele weitere. Später findet der Volksmund ein eigenes Wort dafür: Muckefuck. |
| 56 | F Preussen | S048b | 5.5 | yavaş yaklaşma | Siebzehnhundertsechsundachtzig stirbt Friedrich. Seine Kaffeeriecher überleben ihn nicht lange. |
| 57 | G Schweden | S049 | 5.0 | yatay kaydırma ← | Den Rekord hält Schweden. Fünf Verbote in knapp siebzig Jahren. |
| 58 | G Schweden | S051 | 4.5 | yavaş yaklaşma | Manche Schweden trugen ihre Kaffeekannen sogar zu Grabe. |
| 59 | G Schweden | S052d | 7.5 | yatay kaydırma → | Und dann ist da König Gustav der Dritte. Er soll zwei verurteilte Zwillinge verschont haben, unter einer Bedingung. Der eine trinkt täglich Kaffee, der andere Tee. |
| 60 | G Schweden | S053b | 5.0 | yatay kaydırma ← | Zuerst sterben die Ärzte. Dann der König. Die Zwillinge leben weiter. |
| 61 | G Schweden | S054 | 3.5 | sabit + çizgi titremesi | Ob es dieses Experiment je gab, ist sehr fraglich. |
| 62 | G Schweden | S055b | 4.5 | yavaş yaklaşma | Heute gehört Schweden zu den größten Kaffeetrinkern der Welt. |
| 63 | H Wien | S056 | 3.0 | sabit + çizgi titremesi | Und Wien? |
| 64 | H Wien | S056d | 7.5 | yatay kaydırma → | Die Geschichte kennt hier jeder. Die Osmanen ziehen ab, lassen Säcke voller Bohnen zurück, und der Kundschafter Kolschitzky eröffnet das erste Kaffeehaus. |
| 65 | H Wien | S057 | 4.0 | sabit + çizgi titremesi | Aufgeschrieben wurde das allerdings erst rund hundert Jahre später. |
| 66 | H Wien | S058 | 5.5 | yavaş yaklaşma | Die erste belegte Erlaubnis bekommt sechzehnhundertfünfundachtzig der armenische Händler Johannes Diodato. |
| 67 | H Wien | D04 **(yeni)** | 5.5 | yatay kaydırma ← | Heute ist die Wiener Kaffeehauskultur immaterielles Kulturerbe. Ein Verbot hätte da wenig Chancen. |
| 68 | H2 DDR | D11 **(yeni)** | 6.5 | yatay kaydırma → | Und wer glaubt, das alles sei lange her: Neunzehnhundertsiebenundsiebzig, DDR. Der Weltmarktpreis für Kaffee explodiert, und dem Staat fehlen die Devisen. |
| 69 | H2 DDR | D12 **(yeni)** | 7.0 | yavaş yaklaşma | Die Lösung des Politbüros heißt Kaffee-Mix. Nur einundfünfzig Prozent Kaffee. Der Rest: geröstete Erbsen, Roggen, Gerste, Zichorie und Zuckerrübe. |
| 70 | H2 DDR | D11 **(yeni)** | 4.0 | sabit + çizgi titremesi | Der Volksmund tauft ihn: Erichs Krönung. |
| 71 | H2 DDR | D13 **(yeni)** | 6.0 | yatay kaydırma ← | Tausende Beschwerdebriefe gehen ein. Und vor allem: Die Leute kaufen das Zeug einfach nicht. |
| 72 | H2 DDR | D14 **(yeni)** | 5.5 | yatay kaydırma → | Die Regierung hatte ohnehin gehofft, dass viele ihren Kaffee aus dem Westpaket bekommen. |
| 73 | H2 DDR | D13 **(yeni)** | 5.5 | yavaş yaklaşma | Anfang neunzehnhundertachtundsiebzig wird die Produktion eingestellt. Wieder hat der Tisch gewonnen. |
| 74 | I Schluss | S059 | 7.0 | yatay kaydırma → | Mekka, Istanbul, London, Preußen, die DDR. Es ging um Versammlungen, um Aufstände, um Gerede, um Geld. Und um Devisen. |
| 75 | I Schluss | S059f | 4.0 | yavaş yaklaşma | Um das Getränk ging es so gut wie nie. |
| 76 | I Schluss | S060 | 6.0 | yatay kaydırma ← | Kaffee hat Menschen an einen Tisch gebracht, sie reden lassen und wach gehalten. Das war sein eigentliches Vergehen. |
| 77 | I Schluss | S061 | 6.0 | yavaş yaklaşma | Friedrich wollte übrigens, dass seine Untertanen Bier trinken. Heute trinkt Deutschland mehr Kaffee als Bier. |
| 78 | I Schluss | S061d | 4.0 | sabit + çizgi titremesi | Hat also nicht ganz geklappt. |

## Başlık / kapak
- **Titel:** Der König, der Kaffee-Schnüffler auf die Straße schickte
- Alternatif: Warum wurde Kaffee immer wieder verboten?
- **Kapak:** D05 (Kaffeeriecher burnu) + "VERBOTEN?"

## Yeni görseller
`IMAGE_PROMPTS_de_v3.md`: D01 Preußen sabah sokağı · D02 Kaffee/Bier terazisi · D03 Leipzig kahvehane konseri · D04 Viyana kahvehanesi bugün · D05 kapak · D06 Kaffeeklatsch baskını · D07 Schlendrian & Lieschen · D08 Lieschen'in gizli şartı · D09 Zichorie tarlası · D10 Braunschweig Zichorie fabrikası · D11 DDR dükkânı 1977 · D12 Kaffee-Mix içindekiler · D13 şikâyet mektupları · D14 Westpaket

## Kaynaklar (yeni bilgiler)
- Kaffeeverbrauch: Deutscher Kaffeeverband (tageskarte.io)
- Kaffeeriecher, Hessen-Kassel, Luxusgut, Steuer: en.wikipedia "Coffee sniffers"; germanhistorydocs.org
- Bach BWV 211 Handlung: Wikipedia BWV 211, bachtrack.com
- Zichorie/Preußenkaffee/Blümchenkaffee: Uni Potsdam Botanischer Garten; Braunschweig 1770: museum.de
- DDR Kaffeekrise: Bundesarchiv; DDR Museum; Wikipedia "East German coffee crisis"
- Wiener Kaffeehauskultur: unesco.at, wien.info
