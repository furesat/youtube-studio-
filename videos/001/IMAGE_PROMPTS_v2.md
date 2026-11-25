# 001 · IMAGE_PROMPTS v2 · Ara çekimler (görüntü 2–3 sn'de bir değişsin)

Neden: referans kanalda görüntü ortalama ~2 sn'de bir değişiyor; bizde sahne başına ~6,6 sn idi. Bu dosya **81 yeni görsel** ekler; mevcut 61 sahne görseli aynen kalır. Toplam 142 çekim, ortalama ≈ 2.8 sn.

ChatGPT için: önce `IMAGE_GENERATION_GUIDE.md` oku. Her bloğun **tamamını** kopyala (ilk 56 promptla aynı biçim). Her ara çekimde **ana sahnenin görselini** (`images/001_Sxxx_vK.png`) de referans olarak ekle: aynı yer, ışık ve kostüm; ama kadraj belirgin farklı olsun.
Dosya adı: `001_{Sxxx}{harf}_v{K}.png` → `videos/001/images/`. Kurgu sırası ve süreler: `SHOTS_v2.json`. Daha kısa, elle yazılmış alternatif: `IMAGE_PROMPTS_v2_kisa.md`.

## S002b — ara çekim · Buharda tarih: taç, ferman, alev
- **Dosya:** `001_S002b_v1.png`
- **Anlatım parçası:** krallar fermanlar yazdı.
- **Süre:** ≈ 1.7 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S002_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: An ink vignette rising out of cup steam at the bottom edge: a king's small round hand with a lace cuff presses a big red wax seal onto a long blank decree; beside it a coffee sack burns in small flames and a wooden shop shutter is slammed shut.

COMPOSITION: seal and decree at the optical centre, flame left, shutter right, steam curls tie them to the cup at the bottom
CAMERA: close-up, straight-on
BACKGROUND: same café wall as S001, slightly darker vignette
COLOURS: Steam drawn in thin grey ink lines; crown and seal tinted soft gold and red #B83A2B.
STORY FUNCTION: Extra shot inside S002 so the picture changes every 2-3 s; illustrates: "krallar fermanlar yazdı."
CONTINUITY: Same location, light, characters and costumes as S002 — attach images/001_S002_vK.png as style/continuity reference. Must look clearly different in framing from S002.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S003b — ara çekim · Harita: beş yasak noktası
- **Dosya:** `001_S003b_v1.png`
- **Anlatım parçası:** Londra, Prusya, İsveç…
- **Süre:** ≈ 2.0 sn
- **Referanslar:** `character-references/boards/03_paletler.png`, `images/001_S003_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Closer view of the SAME unlabelled antique map, now showing only northern Europe: Britain, the North Sea, the Baltic coast and Scandinavia; ink coastlines, tiny waves, one small ship.

COMPOSITION: Britain left third, Baltic coast lower centre, Scandinavia upper right
CAMERA: top-down flat map, zoomed in
BACKGROUND: parchment paper texture
COLOURS: Muted map palette: sand land, pale teal sea, ink coastlines.
STORY FUNCTION: Extra shot inside S003 so the picture changes every 2-3 s; illustrates: "Londra, Prusya, İsveç…"
CONTINUITY: Same location, light, characters and costumes as S003 — attach images/001_S003_vK.png as style/continuity reference. Must look clearly different in framing from S003.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S003c — ara çekim · Harita: beş yasak noktası
- **Dosya:** `001_S003c_v1.png`
- **Anlatım parçası:** Kahve en az beş farklı yerde yasaklandı.
- **Süre:** ≈ 3.5 sn
- **Referanslar:** `character-references/boards/03_paletler.png`, `images/001_S003_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: The SAME unlabelled antique map (as in S003) seen whole; five tiny hand-drawn coffee cups stand on it at Mecca, Istanbul, London, Berlin and Stockholm, each struck through with a short red ink cross stroke.

COMPOSITION: same framing as S003
CAMERA: top-down flat map
BACKGROUND: parchment paper texture
COLOURS: Muted map palette: sand land, pale teal sea, ink coastlines.
STORY FUNCTION: Extra shot inside S003 so the picture changes every 2-3 s; illustrates: "Kahve en az beş farklı yerde yasaklandı."
CONTINUITY: Same location, light, characters and costumes as S003 — attach images/001_S003_vK.png as style/continuity reference. Must look clearly different in framing from S003.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S005b — ara çekim · Dedektif Fasulye
- **Dosya:** `001_S005b_v1.png`
- **Anlatım parçası:** Bu yasakların neredeyse hiçbiri aslında
- **Süre:** ≈ 3.6 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S005_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).

SCENE: Extreme close-up through the magnifying glass: the coffee bean appears huge on the saucer, and one of Fasulye's big round eyes is seen enlarged and distorted at the edge of the lens.
POSE / EXPRESSION: one giant curious eye, eyebrow raised
COMPOSITION: round lens fills most of the frame, bean in the lens centre
CAMERA: extreme close-up
BACKGROUND: same café as S001, softly defocused
COLOURS: Base palette.
STORY FUNCTION: Extra shot inside S005 so the picture changes every 2-3 s; illustrates: "Bu yasakların neredeyse hiçbiri aslında"
CONTINUITY: Same location, light, characters and costumes as S005 — attach images/001_S005_vK.png as style/continuity reference. Must look clearly different in framing from S005.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S005c — ara çekim · Dedektif Fasulye
- **Dosya:** `001_S005c_v1.png`
- **Anlatım parçası:** kahveyle ilgili değildi.
- **Süre:** ≈ 2.3 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S005_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).

SCENE: Fasulye has lowered the magnifying glass and gives a small shrug; the single bean lies innocently on the saucer in front of him.
POSE / EXPRESSION: dry, unimpressed half-lidded look, small shrug
COMPOSITION: Fasulye centre, bean small in the lower foreground
CAMERA: medium close-up, eye level
BACKGROUND: same café as S001, softly defocused
COLOURS: Base palette.
STORY FUNCTION: Extra shot inside S005 so the picture changes every 2-3 s; illustrates: "kahveyle ilgili değildi."
CONTINUITY: Same location, light, characters and costumes as S005 — attach images/001_S005_vK.png as style/continuity reference. Must look clearly different in framing from S005.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S005d — ara çekim · Dedektif Fasulye
- **Dosya:** `001_S005d_v1.png`
- **Anlatım parçası:** Peki neyle ilgiliydi?
- **Süre:** ≈ 1.9 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S005_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).

SCENE: Fasulye turns to the viewer with his chin resting on one hand, thinking; three small empty ink thought-bubbles float above his curly tuft.
POSE / EXPRESSION: thoughtful, eyes looking up and sideways
COMPOSITION: Fasulye centre-left, bubbles upper right
CAMERA: medium shot, eye level
BACKGROUND: same café as S001, softly defocused
COLOURS: Base palette.
STORY FUNCTION: Extra shot inside S005 so the picture changes every 2-3 s; illustrates: "Peki neyle ilgiliydi?"
CONTINUITY: Same location, light, characters and costumes as S005 — attach images/001_S005_vK.png as style/continuity reference. Must look clearly different in framing from S005.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S007b — ara çekim · Gece uyanık kalan sufiler
- **Dosya:** `001_S007b_v1.png`
- **Anlatım parçası:** Sufiler gece boyunca uyanık kalmak için içiyor.
- **Süre:** ≈ 3.6 sn
- **Referanslar:** `images/001_S007_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.

SCENE: Close-up of a robed man's hands pouring dark coffee from a clay pot into a tiny handle-less cup by lamplight; behind, several pairs of wide-awake eyes glint; a crescent moon low in the night sky above the wall.
POSE / EXPRESSION: calm, wide-awake eyes
COMPOSITION: pot and cup at the optical centre, eyes in soft background
CAMERA: close-up, slightly high angle
BACKGROUND: dark blue night #17233A, warm lamp glow, a simple courtyard wall; no religious symbols
COLOURS: Night palette with warm lamp light #FFD166.
STORY FUNCTION: Extra shot inside S007 so the picture changes every 2-3 s; illustrates: "Sufiler gece boyunca uyanık kalmak için içiyor."
CONTINUITY: Same location, light, characters and costumes as S007 — attach images/001_S007_vK.png as style/continuity reference. Must look clearly different in framing from S007.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S008b — ara çekim · Mekke'de kahve dükkânı
- **Dosya:** `001_S008b_v1.png`
- **Anlatım parçası:** İnsanlar toplanıyor, sohbet ediyor, şarkı söylüyor.
- **Süre:** ≈ 2.8 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `images/001_S008_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye keeps his scarf and wears a small white turban and a cream robe (16th-century Hijaz look).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.

SCENE: Close on the lute player singing with his eyes closed while two men clap along; Fasulye sways happily with his tiny cup; simple wavy ink lines float in the air for the music (no musical notation).
POSE / EXPRESSION: joyful, relaxed
COMPOSITION: lute player centre, clapping men left, Fasulye right
CAMERA: medium close-up
BACKGROUND: Mecca market lane from S006, lanterns, sacks of beans
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S008 so the picture changes every 2-3 s; illustrates: "İnsanlar toplanıyor, sohbet ediyor, şarkı söylüyor."
CONTINUITY: Same location, light, characters and costumes as S008 — attach images/001_S008_vK.png as style/continuity reference. Must look clearly different in framing from S008.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S009b — ara çekim · Hayır Bey tanıtım
- **Dosya:** `001_S009b_v1.png`
- **Anlatım parçası:** Şehrin asayişinden sorumlu Hayır Bey.
- **Süre:** ≈ 2.5 sn
- **Referanslar:** `images/001_S009_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- HAYIR BEY (Mecca market/order inspector, 1511): bean person, stern; thick black moustache and short black beard, heavy frowning eyebrows; white turban wrapped around a dark red cap, long dark indigo robe #2C3B57 with an ochre sash, a short official staff.

SCENE: Close portrait of Hayır Bey holding his short staff upright, chest out, looking down sternly with one eyebrow lowered.
POSE / EXPRESSION: stern, suspicious, authoritative
COMPOSITION: Hayır Bey centre, staff diagonal
CAMERA: close-up, low angle
BACKGROUND: plain sun-baked wall and a corner of the market lane, low detail
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S009 so the picture changes every 2-3 s; illustrates: "Şehrin asayişinden sorumlu Hayır Bey."
CONTINUITY: Same location, light, characters and costumes as S009 — attach images/001_S009_vK.png as style/continuity reference. Must look clearly different in framing from S009.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S010b — ara çekim · Hayır Bey gözetliyor
- **Dosya:** `001_S010b_v1.png`
- **Anlatım parçası:** Ve şüpheleniyor.
- **Süre:** ≈ 1.0 sn
- **Referanslar:** `images/001_S010_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- HAYIR BEY (Mecca market/order inspector, 1511): bean person, stern; thick black moustache and short black beard, heavy frowning eyebrows; white turban wrapped around a dark red cap, long dark indigo robe #2C3B57 with an ochre sash, a short official staff.

SCENE: Extreme close-up of Hayır Bey's narrowed eyes peeking around the edge of a wall; warm lantern light falls on half of his face, the rest is in blue shadow.
POSE / EXPRESSION: eyes narrowed to slits, suspicious
COMPOSITION: wall edge vertical at left third, eyes on the right of it
CAMERA: extreme close-up
BACKGROUND: dusk blue sky, lantern glow
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S010 so the picture changes every 2-3 s; illustrates: "Ve şüpheleniyor."
CONTINUITY: Same location, light, characters and costumes as S010 — attach images/001_S010_vK.png as style/continuity reference. Must look clearly different in framing from S010.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S011b — ara çekim · Âlimler ve hekimler meclisi
- **Dosya:** `001_S011b_v1.png`
- **Anlatım parçası:** Bu içecek insanı sarhoş eder mi?
- **Süre:** ≈ 2.1 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S011_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SCHOLARS & PHYSICIAN: elderly bean people with long white or grey beards, large white turbans, cream and olive robes; the physician wears a dark teal robe #2A7F7A and carries a small brass mortar.

SCENE: Close-up on the physician holding the small coffee cup up to the window light, squinting at it; two scholars lean in, one sniffs it with his eyes closed.
POSE / EXPRESSION: concentrated, sceptical
COMPOSITION: cup at the optical centre, faces around it
CAMERA: close-up
BACKGROUND: simple room with arched window, books and scrolls (blank), carpet
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S011 so the picture changes every 2-3 s; illustrates: "Bu içecek insanı sarhoş eder mi?"
CONTINUITY: Same location, light, characters and costumes as S011 — attach images/001_S011_vK.png as style/continuity reference. Must look clearly different in framing from S011.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S014b — ara çekim · Kahire: Sultan Kansu Gavri
- **Dosya:** `001_S014b_v1.png`
- **Anlatım parçası:** Hayır Bey'in tek bir sorunu var: Onun da bir patronu var.
- **Süre:** ≈ 4.2 sn
- **Referanslar:** `images/001_S014_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- HAYIR BEY (Mecca market/order inspector, 1511): bean person, stern; thick black moustache and short black beard, heavy frowning eyebrows; white turban wrapped around a dark red cap, long dark indigo robe #2C3B57 with an ochre sash, a short official staff.

SCENE: Hayır Bey stands small in the Mecca council room while a huge dark ink shadow of a seated ruler with a tall cap looms over him on the wall behind.
POSE / EXPRESSION: Hayır Bey swallows nervously, eyes darting up
COMPOSITION: Hayır Bey lower right, giant shadow fills the left and top
CAMERA: medium shot, slight low angle
BACKGROUND: the council room from S011, dim
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Richer greens and golds for the palace.
STORY FUNCTION: Extra shot inside S014 so the picture changes every 2-3 s; illustrates: "Hayır Bey'in tek bir sorunu var: Onun da bir patronu var."
CONTINUITY: Same location, light, characters and costumes as S014 — attach images/001_S014_vK.png as style/continuity reference. Must look clearly different in framing from S014.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S014c — ara çekim · Kahire: Sultan Kansu Gavri
- **Dosya:** `001_S014c_v1.png`
- **Anlatım parçası:** Mekke o dönem Kahire'deki Memlük sultanına bağlı.
- **Süre:** ≈ 3.7 sn
- **Referanslar:** `images/001_S014_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Symbolic desert view: a lone messenger on a camel rides along a dotted ink path from a small cluster of Hijaz houses (left) across dunes and the Red Sea coast to a distant striped-arch palace on the Nile (right).

COMPOSITION: path curves from lower left to upper right
CAMERA: wide, high angle
BACKGROUND: pale sand dunes, a strip of teal sea, golden sky
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Richer greens and golds for the palace.
STORY FUNCTION: Extra shot inside S014 so the picture changes every 2-3 s; illustrates: "Mekke o dönem Kahire'deki Memlük sultanına bağlı."
CONTINUITY: Same location, light, characters and costumes as S014 — attach images/001_S014_vK.png as style/continuity reference. Must look clearly different in framing from S014.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S014d — ara çekim · Kahire: Sultan Kansu Gavri
- **Dosya:** `001_S014d_v1.png`
- **Anlatım parçası:** Ve söylenene göre
- **Süre:** ≈ 1.3 sn
- **Referanslar:** `images/001_S014_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SULTAN QANSUH AL-GHAWRI (Mamluk sultan in Cairo): bean person with a full grey beard, very tall white Mamluk turban with a rounded crown shape, rich green and gold robe, relaxed and amused.

SCENE: Inside the Cairo palace: we see Sultan Kansu Gavri only from behind, a large silhouette on cushions, slowly raising a small cup; a thin curl of steam rises above his turban.

COMPOSITION: sultan's back centre, arches framing him
CAMERA: medium shot from behind
BACKGROUND: Mamluk palace: striped stone arches (ablaq), lattice window, green-gold textiles
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Richer greens and golds for the palace.
STORY FUNCTION: Extra shot inside S014 so the picture changes every 2-3 s; illustrates: "Ve söylenene göre"
CONTINUITY: Same location, light, characters and costumes as S014 — attach images/001_S014_vK.png as style/continuity reference. Must look clearly different in framing from S014.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S015b — ara çekim · Hayır Bey'in yüzü düşüyor
- **Dosya:** `001_S015b_v1.png`
- **Anlatım parçası:** ama insanların kahvesine dokunma.
- **Süre:** ≈ 2.1 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S015_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- HAYIR BEY (Mecca market/order inspector, 1511): bean person, stern; thick black moustache and short black beard, heavy frowning eyebrows; white turban wrapped around a dark red cap, long dark indigo robe #2C3B57 with an ochre sash, a short official staff.

SCENE: Close-up of Hayır Bey reading the sealed scroll, his whole face sagging, moustache drooping, a big sweat drop on his temple.
POSE / EXPRESSION: deflated, defeated, mouth wobbling
COMPOSITION: face centre, top edge of scroll in the lower frame
CAMERA: close-up
BACKGROUND: same council room as S011, empty cushions
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S015 so the picture changes every 2-3 s; illustrates: "ama insanların kahvesine dokunma."
CONTINUITY: Same location, light, characters and costumes as S015 — attach images/001_S015_vK.png as style/continuity reference. Must look clearly different in framing from S015.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S015c — ara çekim · Hayır Bey'in yüzü düşüyor
- **Dosya:** `001_S015c_v1.png`
- **Anlatım parçası:** Yasak birkaç hafta içinde çöküyor.
- **Süre:** ≈ 2.1 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S015_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.

SCENE: The Mecca lane from S013 a few weeks later: shutters are open again, a server pours coffee, people sit back down on benches; a faint black scorch mark on the ground where the bonfire was.

COMPOSITION: open shop right, scorch mark lower left
CAMERA: wide, eye level
BACKGROUND: Mecca market lane, daylight
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S015 so the picture changes every 2-3 s; illustrates: "Yasak birkaç hafta içinde çöküyor."
CONTINUITY: Same location, light, characters and costumes as S015 — attach images/001_S015_vK.png as style/continuity reference. Must look clearly different in framing from S015.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S016b — ara çekim · Motif: sorun masaydı
- **Dosya:** `001_S016b_v1.png`
- **Anlatım parçası:** Sorun masaydı.
- **Süre:** ≈ 1.3 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S016_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Top-down view of the long empty wooden table with stools around it in a warm pool of lamp light; the small coffee cup at the near end looks tiny.

COMPOSITION: table runs diagonally across the frame, cup lower left
CAMERA: top-down
BACKGROUND: plain warm paper background, a pool of lamp light
COLOURS: Base palette, warm lamp light.
STORY FUNCTION: Extra shot inside S016 so the picture changes every 2-3 s; illustrates: "Sorun masaydı."
CONTINUITY: Same location, light, characters and costumes as S016 — attach images/001_S016_vK.png as style/continuity reference. Must look clearly different in framing from S016.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S018b — ara çekim · Hakem ve Şems dükkân açıyor
- **Dosya:** `001_S018b_v1.png`
- **Anlatım parçası:** Tarihçi Peçevi'ye göre
- **Süre:** ≈ 1.7 sn
- **Referanslar:** `images/001_S018_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- PEÇEVİ (Ottoman historian): elderly bean man, short grey beard drawn as an ink mass, large round white turban, plain dark-teal robe, small reading spectacles.

SCENE: The historian Peçevi writes at a low desk in a big book with a reed pen; the pages show only illegible wavy ink lines.
POSE / EXPRESSION: focused, scholarly
COMPOSITION: Peçevi centre-left, book centre
CAMERA: medium shot
BACKGROUND: calm study with a window and stacked books
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S018 so the picture changes every 2-3 s; illustrates: "Tarihçi Peçevi'ye göre"
CONTINUITY: Same location, light, characters and costumes as S018 — attach images/001_S018_vK.png as style/continuity reference. Must look clearly different in framing from S018.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S018c — ara çekim · Hakem ve Şems dükkân açıyor
- **Dosya:** `001_S018c_v1.png`
- **Anlatım parçası:** Halep'ten Hakem, Şam'dan Şems adında iki adam
- **Süre:** ≈ 3.3 sn
- **Referanslar:** `images/001_S018_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- HAKEM of Aleppo: practical merchant, short black beard, green-and-cream striped robe, small white turban, rolled sleeves. ŞEMS of Damascus: elegant, slim curled moustache, saffron kaftan #E9A33B with a fine sash, neat small turban.

SCENE: Two travellers arrive at a city gate leading mules loaded with coffee sacks: Hakem (left) and Şems (right) greet each other with a wave.
POSE / EXPRESSION: cheerful, hopeful
COMPOSITION: Hakem left, Şems right, gate arch behind
CAMERA: wide, eye level
BACKGROUND: stone city gate, morning light
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S018 so the picture changes every 2-3 s; illustrates: "Halep'ten Hakem, Şam'dan Şems adında iki adam"
CONTINUITY: Same location, light, characters and costumes as S018 — attach images/001_S018_vK.png as style/continuity reference. Must look clearly different in framing from S018.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S019b — ara çekim · Kuyruk ve kalabalık
- **Dosya:** `001_S019b_v1.png`
- **Anlatım parçası:** Fikir basit: Kahve sat, insanları oturt.
- **Süre:** ≈ 3.4 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `images/001_S019_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- HAKEM of Aleppo: practical merchant, short black beard, green-and-cream striped robe, small white turban, rolled sleeves. ŞEMS of Damascus: elegant, slim curled moustache, saffron kaftan #E9A33B with a fine sash, neat small turban.
- OTTOMAN COFFEEHOUSE CROWD: bean people in fezzes or small turbans, cream entari robes, saffron or indigo sashes, waistcoats; various beards and moustaches.

SCENE: Hakem pours coffee into a small cup while Şems invites a passer-by to sit on a cushioned bench in front of their shop.
POSE / EXPRESSION: welcoming smiles
COMPOSITION: Hakem left pouring, Şems right gesturing to the bench
CAMERA: medium shot
BACKGROUND: same street as S018
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S019 so the picture changes every 2-3 s; illustrates: "Fikir basit: Kahve sat, insanları oturt."
CONTINUITY: Same location, light, characters and costumes as S019 — attach images/001_S019_vK.png as style/continuity reference. Must look clearly different in framing from S019.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S020b — ara çekim · Kahvehane içi: kitap, tavla, şiir
- **Dosya:** `001_S020b_v1.png`
- **Anlatım parçası:** tavla oynayan, şiir yazan…
- **Süre:** ≈ 1.8 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `images/001_S020_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- OTTOMAN COFFEEHOUSE CROWD: bean people in fezzes or small turbans, cream entari robes, saffron or indigo sashes, waistcoats; various beards and moustaches.

SCENE: Close on a backgammon board between two players mid-move with dice; next to them a poet scribbles with a reed pen on paper covered only in wavy ink lines.
POSE / EXPRESSION: playful concentration
COMPOSITION: board centre, poet right
CAMERA: close-up, slightly high angle
BACKGROUND: warm wooden interior, small fountain in the centre, copper pots on shelves, window light
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S020 so the picture changes every 2-3 s; illustrates: "tavla oynayan, şiir yazan…"
CONTINUITY: Same location, light, characters and costumes as S020 — attach images/001_S020_vK.png as style/continuity reference. Must look clearly different in framing from S020.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S022b — ara çekim · İtiraz eden âlim
- **Dosya:** `001_S022b_v1.png`
- **Anlatım parçası:** İnsanlar ibadeti bırakıp kahvehaneye koşuyor.
- **Süre:** ≈ 2.9 sn
- **Referanslar:** `images/001_S022_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SCHOLARS & PHYSICIAN: elderly bean people with long white or grey beards, large white turbans, cream and olive robes; the physician wears a dark teal robe #2A7F7A and carries a small brass mortar.
- OTTOMAN COFFEEHOUSE CROWD: bean people in fezzes or small turbans, cream entari robes, saffron or indigo sashes, waistcoats; various beards and moustaches.

SCENE: A few bean people hurry past the elderly scholar toward the busy coffeehouse, one skipping with his slippers in his hand; the scholar shakes his head.
POSE / EXPRESSION: scholar disapproving, hurrying men eager
COMPOSITION: scholar left, runners moving right toward the coffeehouse
CAMERA: wide, eye level
BACKGROUND: street with plane tree, the coffeehouse from S018
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S022 so the picture changes every 2-3 s; illustrates: "İnsanlar ibadeti bırakıp kahvehaneye koşuyor."
CONTINUITY: Same location, light, characters and costumes as S022 — attach images/001_S022_vK.png as style/continuity reference. Must look clearly different in framing from S022.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S023b — ara çekim · Bostanzade yeşil ışık
- **Dosya:** `001_S023b_v1.png`
- **Anlatım parçası:** Ama kahvenin de güçlü dostları var.
- **Süre:** ≈ 2.8 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S023_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- OTTOMAN COFFEEHOUSE CROWD: bean people in fezzes or small turbans, cream entari robes, saffron or indigo sashes, waistcoats; various beards and moustaches.

SCENE: Inside the coffeehouse three well-dressed dignitaries (a pasha in a fur-trimmed kaftan, a rich merchant, a poet) raise their cups together like a friendly team.
POSE / EXPRESSION: confident, warm
COMPOSITION: three figures centre in a row
CAMERA: medium shot
BACKGROUND: coffeehouse interior from S020
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Soft green accent in the robe.
STORY FUNCTION: Extra shot inside S023 so the picture changes every 2-3 s; illustrates: "Ama kahvenin de güçlü dostları var."
CONTINUITY: Same location, light, characters and costumes as S023 — attach images/001_S023_vK.png as style/continuity reference. Must look clearly different in framing from S023.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S023c — ara çekim · Bostanzade yeşil ışık
- **Dosya:** `001_S023c_v1.png`
- **Anlatım parçası:** kahveye yeşil ışık yakıyor.
- **Süre:** ≈ 2.1 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S023_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye keeps his scarf and wears a red fez and a cream entari with a saffron sash (Ottoman townsman).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- BOSTANZADE MEHMED EFENDİ (Ottoman Şeyhülislam, 1590s): dignified elderly bean person, long white beard, very large rounded white turban, white robe with dark green over-robe, kind half-smile.

SCENE: Close-up: Bostanzade presses a seal stamp onto a blank scroll; a soft symbolic green glow spreads from the stamp; Fasulye gives a small thumbs-up in the background.
POSE / EXPRESSION: Bostanzade calm and kind, Fasulye relieved
COMPOSITION: stamp at the optical centre, Fasulye upper right
CAMERA: close-up
BACKGROUND: calm study with books and a window
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Soft green accent in the robe.
STORY FUNCTION: Extra shot inside S023 so the picture changes every 2-3 s; illustrates: "kahveye yeşil ışık yakıyor."
CONTINUITY: Same location, light, characters and costumes as S023 — attach images/001_S023_vK.png as style/continuity reference. Must look clearly different in framing from S023.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S025b — ara çekim · Boş taht: Genç Osman'ın anısı
- **Dosya:** `001_S025b_v1.png`
- **Anlatım parçası:** Murad'ın kahvehanelere güvenmemek için ciddi bir nedeni var.
- **Süre:** ≈ 3.5 sn
- **Referanslar:** `images/001_S025_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SULTAN MURAD IV (Ottoman, 1630s): young, strong bean person with a full short black beard and thick eyebrows; very large white Ottoman ceremonial turban (kavuk) with a jewelled aigrette and feather plume; crimson-and-gold kaftan #B83A2B with gold buttons; stern, intense gaze. DISGUISED VERSION: long dark brown hooded cloak covering the turban, only the eyes and beard visible.

SCENE: Murad IV stands alone at a palace window at night, brooding, looking down at the city where small coffeehouse windows glow.
POSE / EXPRESSION: dark, distrustful, jaw tight
COMPOSITION: Murad left silhouette, city lights right
CAMERA: medium shot from behind his shoulder
BACKGROUND: night palace interior, blue moonlight
COLOURS: Desaturated flashback: sepia ink #8E8478 with one muted red accent on the fallen turban.
STORY FUNCTION: Extra shot inside S025 so the picture changes every 2-3 s; illustrates: "Murad'ın kahvehanelere güvenmemek için ciddi bir nedeni var."
CONTINUITY: Same location, light, characters and costumes as S025 — attach images/001_S025_vK.png as style/continuity reference. Must look clearly different in framing from S025.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S025c — ara çekim · Boş taht: Genç Osman'ın anısı
- **Dosya:** `001_S025c_v1.png`
- **Anlatım parçası:** Ağabeyi Genç Osman, bin altı yüz yirmi ikide
- **Süre:** ≈ 2.6 sn
- **Referanslar:** `images/001_S025_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- YOUNG OSMAN II: a young bean man with a thin black moustache, very tall white ceremonial turban with a small plume, red kaftan with gold trim.

SCENE: A memory portrait of young Osman II in an oval wooden frame on a wall; the glass has a thin crack; sepia, muted colours.
POSE / EXPRESSION: young, serious
COMPOSITION: oval frame centred
CAMERA: straight-on
BACKGROUND: dim palace wall
COLOURS: Desaturated flashback: sepia ink #8E8478 with one muted red accent on the fallen turban.
STORY FUNCTION: Extra shot inside S025 so the picture changes every 2-3 s; illustrates: "Ağabeyi Genç Osman, bin altı yüz yirmi ikide"
CONTINUITY: Same location, light, characters and costumes as S025 — attach images/001_S025_vK.png as style/continuity reference. Must look clearly different in framing from S025.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S026b — ara çekim · Yeniçeriler kahvehanede
- **Dosya:** `001_S026b_v1.png`
- **Anlatım parçası:** Tahmin et.
- **Süre:** ≈ 1.0 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S026_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye keeps his scarf and wears a white turban, a striped apron and carries a brass tray with small cups (Ottoman coffee server).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- JANISSARIES: bean people with bushy moustaches, tall white felt börk caps that fold down at the back (with a small spoon-holder at the front), blue-grey long coats, red sashes; rowdy and cheerful when off-duty. Weapons are never drawn.

SCENE: Fasulye, holding the coffee tray, turns to the viewer with raised eyebrows; the loud janissaries are a soft blur behind him.
POSE / EXPRESSION: knowing, dry 'you guessed it' look
COMPOSITION: Fasulye centre, blurred group behind
CAMERA: medium close-up
BACKGROUND: same coffeehouse interior as S020
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S026 so the picture changes every 2-3 s; illustrates: "Tahmin et."
CONTINUITY: Same location, light, characters and costumes as S026 — attach images/001_S026_vK.png as style/continuity reference. Must look clearly different in framing from S026.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S027b — ara çekim · 1633 büyük yangın
- **Dosya:** `001_S027b_v1.png`
- **Anlatım parçası:** Şehrin beşte biri kül oluyor.
- **Süre:** ≈ 1.7 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S027_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.

SCENE: The next morning: a wide view of a burnt district, charred beams and ash, thin smoke wisps; surviving houses at the edges; a few small figures stand looking at the ruins.

COMPOSITION: burnt area centre, survivors lower right
CAMERA: wide, high angle
BACKGROUND: grey morning sky with smoke
COLOURS: Night palette with fire #F28C28 / #FFD166.
STORY FUNCTION: Extra shot inside S027 so the picture changes every 2-3 s; illustrates: "Şehrin beşte biri kül oluyor."
CONTINUITY: Same location, light, characters and costumes as S027 — attach images/001_S027_vK.png as style/continuity reference. Must look clearly different in framing from S027.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S028b — ara çekim · Kahvehane kapatılıyor
- **Dosya:** `001_S028b_v1.png`
- **Anlatım parçası:** Tütünü de yasaklıyor.
- **Süre:** ≈ 1.2 sn
- **Referanslar:** `images/001_S028_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.

SCENE: Close-up: a guard snaps a long tobacco pipe in two over a basket full of confiscated pipes; an old man watches sadly.
POSE / EXPRESSION: guard stern, old man sad
COMPOSITION: breaking pipe centre, basket below, old man right
CAMERA: close-up
BACKGROUND: same coffeehouse façade as S018, soot marks from the fire
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S028 so the picture changes every 2-3 s; illustrates: "Tütünü de yasaklıyor."
CONTINUITY: Same location, light, characters and costumes as S028 — attach images/001_S028_vK.png as style/continuity reference. Must look clearly different in framing from S028.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S029b — ara çekim · Gerilim: boş sokak
- **Dosya:** `001_S029b_v1.png`
- **Anlatım parçası:** Cezalar ağır.
- **Süre:** ≈ 1.0 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S029_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: A blank decree with a big red wax seal is nailed to a wooden wall; the long shadow of a guard's staff falls across it.

COMPOSITION: decree centre, diagonal shadow
CAMERA: close-up, straight-on
BACKGROUND: same street as S028, quiet and grey
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. More muted, colder.
STORY FUNCTION: Extra shot inside S029 so the picture changes every 2-3 s; illustrates: "Cezalar ağır."
CONTINUITY: Same location, light, characters and costumes as S029 — attach images/001_S029_vK.png as style/continuity reference. Must look clearly different in framing from S029.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S030b — ara çekim · Kılık değiştirmiş Murad
- **Dosya:** `001_S030b_v1.png`
- **Anlatım parçası:** suçluları bizzat yakalıyordu.
- **Süre:** ≈ 1.9 sn
- **Referanslar:** `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S030_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SULTAN MURAD IV (Ottoman, 1630s): young, strong bean person with a full short black beard and thick eyebrows; very large white Ottoman ceremonial turban (kavuk) with a jewelled aigrette and feather plume; crimson-and-gold kaftan #B83A2B with gold buttons; stern, intense gaze. DISGUISED VERSION: long dark brown hooded cloak covering the turban, only the eyes and beard visible.

SCENE: The cloaked figure throws open the door: inside, three men freeze mid-sip with cups in the air and huge round eyes, lit by the lantern.
POSE / EXPRESSION: men frozen in shock
COMPOSITION: cloaked figure in the doorway left, men right
CAMERA: medium shot
BACKGROUND: narrow alley, wooden overhangs, moonlight
COLOURS: Night palette #17233A / #2C3B57, warm lantern light.
STORY FUNCTION: Extra shot inside S030 so the picture changes every 2-3 s; illustrates: "suçluları bizzat yakalıyordu."
CONTINUITY: Same location, light, characters and costumes as S030 — attach images/001_S030_vK.png as style/continuity reference. Must look clearly different in framing from S030.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S032b — ara çekim · Ev serbest, kahvehane yasak
- **Dosya:** `001_S032b_v1.png`
- **Anlatım parçası:** İşin ilginç yanı: Murad kahveyi değil, kahvehaneyi hedef alıyor.
- **Süre:** ≈ 4.6 sn
- **Referanslar:** `images/001_S032_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SULTAN MURAD IV (Ottoman, 1630s): young, strong bean person with a full short black beard and thick eyebrows; very large white Ottoman ceremonial turban (kavuk) with a jewelled aigrette and feather plume; crimson-and-gold kaftan #B83A2B with gold buttons; stern, intense gaze. DISGUISED VERSION: long dark brown hooded cloak covering the turban, only the eyes and beard visible.

SCENE: Murad IV walks past a house window where a cup steams on the sill and ignores it, pointing sternly at the boarded coffeehouse across the street.
POSE / EXPRESSION: stern, focused on the coffeehouse
COMPOSITION: window and cup left, Murad centre, coffeehouse right
CAMERA: wide, eye level
BACKGROUND: Istanbul street from S028
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood.
STORY FUNCTION: Extra shot inside S032 so the picture changes every 2-3 s; illustrates: "İşin ilginç yanı: Murad kahveyi değil, kahvehaneyi hedef alıyor."
CONTINUITY: Same location, light, characters and costumes as S032 — attach images/001_S032_vK.png as style/continuity reference. Must look clearly different in framing from S032.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S034b — ara çekim · Kâtip Çelebi ve ıssız kahvehaneler
- **Dosya:** `001_S034b_v1.png`
- **Anlatım parçası:** Yasak tutmuş gibi görünüyor.
- **Süre:** ≈ 2.0 sn
- **Referanslar:** `images/001_S034_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: A deserted street of shuttered coffeehouses: dust blows, dry leaves roll, cobwebs on the doors, a single cat sits on a step.

COMPOSITION: street vanishing to the centre
CAMERA: wide, eye level
BACKGROUND: grey quiet Istanbul street
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Dusty, faded tones in the street view.
STORY FUNCTION: Extra shot inside S034 so the picture changes every 2-3 s; illustrates: "Yasak tutmuş gibi görünüyor."
CONTINUITY: Same location, light, characters and costumes as S034 — attach images/001_S034_vK.png as style/continuity reference. Must look clearly different in framing from S034.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S034c — ara çekim · Kâtip Çelebi ve ıssız kahvehaneler
- **Dosya:** `001_S034c_v1.png`
- **Anlatım parçası:** Murad öldükten on yıl sonra bile Kâtip Çelebi,
- **Süre:** ≈ 3.2 sn
- **Referanslar:** `images/001_S034_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- KÂTİP ÇELEBİ (Ottoman scholar, 1650s): bean person with a neat brown beard, medium white turban, olive robe, reed pen in hand, books stacked around.

SCENE: Close portrait of Kâtip Çelebi dipping a reed pen into an inkwell, thoughtful.
POSE / EXPRESSION: thoughtful, slightly melancholic
COMPOSITION: face centre-left, inkwell lower right
CAMERA: close-up
BACKGROUND: study interior + empty street view
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Dusty, faded tones in the street view.
STORY FUNCTION: Extra shot inside S034 so the picture changes every 2-3 s; illustrates: "Murad öldükten on yıl sonra bile Kâtip Çelebi,"
CONTINUITY: Same location, light, characters and costumes as S034 — attach images/001_S034_vK.png as style/continuity reference. Must look clearly different in framing from S034.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S035b — ara çekim · Kahvehaneler yeniden açılıyor
- **Dosya:** `001_S035b_v1.png`
- **Anlatım parçası:** Ama bin altı yüz kırk dokuzda tütün yasağı kalkıyor
- **Süre:** ≈ 3.5 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S035_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- OTTOMAN COFFEEHOUSE CROWD: bean people in fezzes or small turbans, cream entari robes, saffron or indigo sashes, waistcoats; various beards and moustaches.

SCENE: An official tears an old blank decree off a wall while a man nearby happily lights a long tobacco pipe.
POSE / EXPRESSION: cheerful relief
COMPOSITION: torn decree left, pipe smoker right
CAMERA: medium shot
BACKGROUND: same street as S028 in fresh morning light, steam from inside
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Fresh morning light.
STORY FUNCTION: Extra shot inside S035 so the picture changes every 2-3 s; illustrates: "Ama bin altı yüz kırk dokuzda tütün yasağı kalkıyor"
CONTINUITY: Same location, light, characters and costumes as S035 — attach images/001_S035_vK.png as style/continuity reference. Must look clearly different in framing from S035.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S035c — ara çekim · Kahvehaneler yeniden açılıyor
- **Dosya:** `001_S035c_v1.png`
- **Anlatım parçası:** Masa geri geldi.
- **Süre:** ≈ 1.1 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S035_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye keeps his scarf and wears a red fez and a cream entari with a saffron sash (Ottoman townsman).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- OTTOMAN COFFEEHOUSE CROWD: bean people in fezzes or small turbans, cream entari robes, saffron or indigo sashes, waistcoats; various beards and moustaches.

SCENE: The long wooden table is back inside the coffeehouse under a warm lamp; people sit down again, steam rises from cups; Fasulye sits at the far end, satisfied.
POSE / EXPRESSION: content, small smile
COMPOSITION: table along the lower third, Fasulye right end
CAMERA: medium wide
BACKGROUND: coffeehouse interior from S020
COLOURS: Ottoman/Middle-East period palette: terracotta, saffron #E9A33B, indigo #2C3B57, copper, cream, warm wood. Fresh morning light.
STORY FUNCTION: Extra shot inside S035 so the picture changes every 2-3 s; illustrates: "Masa geri geldi."
CONTINUITY: Same location, light, characters and costumes as S035 — attach images/001_S035_vK.png as style/continuity reference. Must look clearly different in framing from S035.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S036b — ara çekim · Londra 1675 kuruluş
- **Dosya:** `001_S036b_v1.png`
- **Anlatım parçası:** Bu arada kahve Avrupa'ya ulaşmış.
- **Süre:** ≈ 2.6 sn
- **Referanslar:** `images/001_S036_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- LONDON 1670s CROWD: bean people in long brown or grey periwigs and wide-brim hats, plain dark coats, white collars; merchants, tradesmen with aprons.

SCENE: A merchant sailing ship moored at a London quay on the Thames; porters unload coffee sacks into timber warehouses.

COMPOSITION: ship left, quay and sacks right
CAMERA: wide, eye level
BACKGROUND: grey sky, river
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S036 so the picture changes every 2-3 s; illustrates: "Bu arada kahve Avrupa'ya ulaşmış."
CONTINUITY: Same location, light, characters and costumes as S036 — attach images/001_S036_vK.png as style/continuity reference. Must look clearly different in framing from S036.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S037b — ara çekim · Peni üniversitesi
- **Dosya:** `001_S037b_v1.png`
- **Anlatım parçası:** Bir peni ver, kahveni al,
- **Süre:** ≈ 1.7 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `images/001_S037_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Close-up of a small round hand dropping one plain copper penny (no markings) onto a wooden counter next to a steaming cup.

COMPOSITION: coin mid-air at the centre, cup right
CAMERA: extreme close-up
BACKGROUND: dark wood panels, candle light, smoky air
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S037 so the picture changes every 2-3 s; illustrates: "Bir peni ver, kahveni al,"
CONTINUITY: Same location, light, characters and costumes as S037 — attach images/001_S037_vK.png as style/continuity reference. Must look clearly different in framing from S037.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S037c — ara çekim · Peni üniversitesi
- **Dosya:** `001_S037c_v1.png`
- **Anlatım parçası:** Bu yüzden onlara peni üniversiteleri deniyor.
- **Süre:** ≈ 3.0 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `images/001_S037_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye keeps his scarf and wears a long brown curly periwig and a dark coat (London 1670s).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- LONDON 1670s CROWD: bean people in long brown or grey periwigs and wide-brim hats, plain dark coats, white collars; merchants, tradesmen with aprons.

SCENE: Fasulye in a periwig stands at the coffeehouse table like a professor, pointing at a blank newspaper, while the others listen like students with their cups.
POSE / EXPRESSION: Fasulye professorial, listeners attentive
COMPOSITION: Fasulye standing right, listeners seated left
CAMERA: medium shot
BACKGROUND: dark wood panels, candle light, smoky air
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S037 so the picture changes every 2-3 s; illustrates: "Bu yüzden onlara peni üniversiteleri deniyor."
CONTINUITY: Same location, light, characters and costumes as S037 — attach images/001_S037_vK.png as style/continuity reference. Must look clearly different in framing from S037.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S039b — ara çekim · Tellal fermanı okuyor
- **Dosya:** `001_S039b_v1.png`
- **Anlatım parçası:** yirmi dokuz Aralık bin altı yüz yetmiş beşte bir ferman yayımlıyor:
- **Süre:** ≈ 3.7 sn
- **Referanslar:** `images/001_S039_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- KING CHARLES II (England, 1670s): bean person with a long, very curly black wig falling to the shoulders, thin black moustache, small gold crown, lace cravat, dark red velvet coat; vain, sulky expression.

SCENE: Charles II at his desk presses his seal onto a large blank proclamation with a smug expression; a quill in an inkwell.
POSE / EXPRESSION: smug, satisfied
COMPOSITION: king centre, proclamation lower centre
CAMERA: medium close-up
BACKGROUND: palace room from S038
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S039 so the picture changes every 2-3 s; illustrates: "yirmi dokuz Aralık bin altı yüz yetmiş beşte bir ferman yayımlıyor:"
CONTINUITY: Same location, light, characters and costumes as S039 — attach images/001_S039_vK.png as style/continuity reference. Must look clearly different in framing from S039.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S040b — ara çekim · Dedikodu saraya uçuyor
- **Dosya:** `001_S040b_v1.png`
- **Anlatım parçası:** Gerekçe: Buralar tembel ve hoşnutsuz insanların toplandığı,
- **Süre:** ≈ 3.8 sn
- **Referanslar:** `images/001_S040_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- LONDON 1670s CROWD: bean people in long brown or grey periwigs and wide-brim hats, plain dark coats, white collars; merchants, tradesmen with aprons.
- KING CHARLES II (England, 1670s): bean person with a long, very curly black wig falling to the shoulders, thin black moustache, small gold crown, lace cravat, dark red velvet coat; vain, sulky expression.

SCENE: Inside a thought-cloud vignette with a wavy ink border: lazy coffeehouse men slouch, one yawns with his feet on the table, one grumbles with crossed arms; a small Charles II at the lower corner imagines it.
POSE / EXPRESSION: lazy, grumpy (as the king imagines)
COMPOSITION: vignette fills upper two thirds, king lower left
CAMERA: medium shot
BACKGROUND: same interior as S037
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S040 so the picture changes every 2-3 s; illustrates: "Gerekçe: Buralar tembel ve hoşnutsuz insanların toplandığı,"
CONTINUITY: Same location, light, characters and costumes as S040 — attach images/001_S040_vK.png as style/continuity reference. Must look clearly different in framing from S040.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S041b — ara çekim · Londra ayakta
- **Dosya:** `001_S041b_v1.png`
- **Anlatım parçası:** hatta kralın kendi adamları bile itiraz ediyor.
- **Süre:** ≈ 3.1 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S041_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- KING CHARLES II (England, 1670s): bean person with a long, very curly black wig falling to the shoulders, thin black moustache, small gold crown, lace cravat, dark red velvet coat; vain, sulky expression.
- LONDON 1670s CROWD: bean people in long brown or grey periwigs and wide-brim hats, plain dark coats, white collars; merchants, tradesmen with aprons.

SCENE: Inside the palace, courtiers in fine wigs approach Charles II nervously, holding coffee cups and a long blank petition; one whispers in his ear.
POSE / EXPRESSION: courtiers nervous, king irritated
COMPOSITION: courtiers left, king right
CAMERA: medium shot
BACKGROUND: palace room from S038
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S041 so the picture changes every 2-3 s; illustrates: "hatta kralın kendi adamları bile itiraz ediyor."
CONTINUITY: Same location, light, characters and costumes as S041 — attach images/001_S041_vK.png as style/continuity reference. Must look clearly different in framing from S041.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S042b — ara çekim · Charles fermanı yırtıyor
- **Dosya:** `001_S042b_v1.png`
- **Anlatım parçası:** sekiz Ocak'ta geri çekiliyor.
- **Süre:** ≈ 2.3 sn
- **Referanslar:** `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S042_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- LONDON 1670s CROWD: bean people in long brown or grey periwigs and wide-brim hats, plain dark coats, white collars; merchants, tradesmen with aprons.

SCENE: Inside the London coffeehouse men cheer and clink cups; one throws his periwig in the air.
POSE / EXPRESSION: jubilant
COMPOSITION: group centre
CAMERA: medium wide
BACKGROUND: coffeehouse interior from S037
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S042 so the picture changes every 2-3 s; illustrates: "sekiz Ocak'ta geri çekiliyor."
CONTINUITY: Same location, light, characters and costumes as S042 — attach images/001_S042_vK.png as style/continuity reference. Must look clearly different in framing from S042.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S042c — ara çekim · Charles fermanı yırtıyor
- **Dosya:** `001_S042c_v1.png`
- **Anlatım parçası:** Ferman ile geri adım arasında sadece on gün var.
- **Süre:** ≈ 3.7 sn
- **Referanslar:** `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S042_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Ten small blank paper sheets peel off a wall pad one by one and flutter away, symbolising ten days.

COMPOSITION: pad left, sheets flying right
CAMERA: medium shot
BACKGROUND: plain warm paper wall
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S042 so the picture changes every 2-3 s; illustrates: "Ferman ile geri adım arasında sadece on gün var."
CONTINUITY: Same location, light, characters and costumes as S042 — attach images/001_S042_vK.png as style/continuity reference. Must look clearly different in framing from S042.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S043b — ara çekim · Friedrich para sayıyor
- **Dosya:** `001_S043b_v1.png`
- **Anlatım parçası:** Yüz yıl sonra Prusya'da
- **Süre:** ≈ 1.7 sn
- **Referanslar:** `images/001_S043_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Establishing view of a rococo summer palace on a terraced hillside of vineyards, pale yellow walls, a single dome, sunny sky.

COMPOSITION: palace upper centre, terraces below
CAMERA: wide, low angle
BACKGROUND: blue-white sky
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds. Prussian blue and silver.
STORY FUNCTION: Extra shot inside S043 so the picture changes every 2-3 s; illustrates: "Yüz yıl sonra Prusya'da"
CONTINUITY: Same location, light, characters and costumes as S043 — attach images/001_S043_vK.png as style/continuity reference. Must look clearly different in framing from S043.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S044b — ara çekim · Paralar uçup gidiyor
- **Dosya:** `001_S044b_v1.png`
- **Anlatım parçası:** Kahve yurt dışından geliyor
- **Süre:** ≈ 2.1 sn
- **Referanslar:** `images/001_S044_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.

SCENE: Carts loaded with coffee sacks roll across a border bridge into Prussia, driven by foreign merchants.

COMPOSITION: carts moving left to right
CAMERA: wide
BACKGROUND: simple countryside border with a striped barrier pole
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S044 so the picture changes every 2-3 s; illustrates: "Kahve yurt dışından geliyor"
CONTINUITY: Same location, light, characters and costumes as S044 — attach images/001_S044_vK.png as style/continuity reference. Must look clearly different in framing from S044.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S044c — ara çekim · Paralar uçup gidiyor
- **Dosya:** `001_S044c_v1.png`
- **Anlatım parçası:** ve kralın hesabına göre
- **Süre:** ≈ 1.8 sn
- **Referanslar:** `images/001_S044_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- FREDERICK THE GREAT (Prussia, 1770s): older bean person with grey powdered hair tied in a queue, black tricorn hat, worn Prussian-blue uniform coat with red cuffs, walking cane; sharp, thrifty, calculating eyes.

SCENE: Frederick at his desk scribbles sums in a ledger (only wavy ink lines, no digits); a stack of coins beside him shrinks; he looks horrified.
POSE / EXPRESSION: horrified, eyes wide
COMPOSITION: Frederick centre, coin stack right
CAMERA: medium close-up
BACKGROUND: rococo study from S043
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S044 so the picture changes every 2-3 s; illustrates: "ve kralın hesabına göre"
CONTINUITY: Same location, light, characters and costumes as S044 — attach images/001_S044_vK.png as style/continuity reference. Must look clearly different in framing from S044.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S045b — ara çekim · Bira çorbası önerisi
- **Dosya:** `001_S045b_v1.png`
- **Anlatım parçası:** bin yedi yüz yetmiş yedide halkının kahve tutkusundan şikâyet ediyor.
- **Süre:** ≈ 4.5 sn
- **Referanslar:** `images/001_S045_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- FREDERICK THE GREAT (Prussia, 1770s): older bean person with grey powdered hair tied in a queue, black tricorn hat, worn Prussian-blue uniform coat with red cuffs, walking cane; sharp, thrifty, calculating eyes.
- PRUSSIAN TOWNSFOLK: bean people in simple 18th-century working clothes, bonnets and aprons for women, brown waistcoats for men.

SCENE: Frederick at a window looks down at townsfolk in the square, each holding a coffee cup; he sighs with a fist on his hip.
POSE / EXPRESSION: exasperated
COMPOSITION: Frederick left at window, crowd below right
CAMERA: medium shot, high angle
BACKGROUND: Prussian town square with gabled houses
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S045 so the picture changes every 2-3 s; illustrates: "bin yedi yüz yetmiş yedide halkının kahve tutkusundan şikâyet ediyor."
CONTINUITY: Same location, light, characters and costumes as S045 — attach images/001_S045_vK.png as style/continuity reference. Must look clearly different in framing from S045.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S045c — ara çekim · Bira çorbası önerisi
- **Dosya:** `001_S045c_v1.png`
- **Anlatım parçası:** Bir mektubunda şöyle diyor:
- **Süre:** ≈ 1.8 sn
- **Referanslar:** `images/001_S045_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- FREDERICK THE GREAT (Prussia, 1770s): older bean person with grey powdered hair tied in a queue, black tricorn hat, worn Prussian-blue uniform coat with red cuffs, walking cane; sharp, thrifty, calculating eyes.

SCENE: Frederick writes a letter with a quill; a beer mug stands next to the inkwell; he smiles nostalgically.
POSE / EXPRESSION: nostalgic smile
COMPOSITION: Frederick centre, mug right
CAMERA: medium close-up
BACKGROUND: rococo study from S043
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S045 so the picture changes every 2-3 s; illustrates: "Bir mektubunda şöyle diyor:"
CONTINUITY: Same location, light, characters and costumes as S045 — attach images/001_S045_vK.png as style/continuity reference. Must look clearly different in framing from S045.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S045d — ara çekim · Bira çorbası önerisi
- **Dosya:** `001_S045d_v1.png`
- **Anlatım parçası:** Kral bira çorbasıyla büyüdü, halk da büyüyebilir.
- **Süre:** ≈ 3.2 sn
- **Referanslar:** `images/001_S045_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- YOUNG FREDERICK: a small bean boy in a tiny powdered wig with a ribbon, blue coat, rosy cheeks.

SCENE: A soft memory vignette with a cloudy ink border: young Frederick eats beer soup from a huge bowl with a big spoon, rosy cheeks.
POSE / EXPRESSION: happy child
COMPOSITION: boy and bowl centre
CAMERA: medium shot
BACKGROUND: simple palace nursery
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S045 so the picture changes every 2-3 s; illustrates: "Kral bira çorbasıyla büyüdü, halk da büyüyebilir."
CONTINUITY: Same location, light, characters and costumes as S045 — attach images/001_S045_vK.png as style/continuity reference. Must look clearly different in framing from S045.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S047b — ara çekim · Kahve koklayıcı
- **Dosya:** `001_S047b_v1.png`
- **Anlatım parçası:** Ve sokaklara özel bir birlik çıkarıyor:
- **Süre:** ≈ 2.9 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S047_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- COFFEE SNIFFER: war-veteran bean person in a faded blue uniform coat, one wooden peg leg and a crutch, very large comical sniffing nose added for the gag (the only bean person with a nose), bushy grey moustache.
- PRUSSIAN TOWNSFOLK: bean people in simple 18th-century working clothes, bonnets and aprons for women, brown waistcoats for men.

SCENE: A line of veterans in old blue uniforms marches out of a town gate into the street.
POSE / EXPRESSION: proud, serious
COMPOSITION: column marching toward the viewer
CAMERA: wide, eye level
BACKGROUND: cosy cottage interior, street outside
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S047 so the picture changes every 2-3 s; illustrates: "Ve sokaklara özel bir birlik çıkarıyor:"
CONTINUITY: Same location, light, characters and costumes as S047 — attach images/001_S047_vK.png as style/continuity reference. Must look clearly different in framing from S047.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S047c — ara çekim · Kahve koklayıcı
- **Dosya:** `001_S047c_v1.png`
- **Anlatım parçası:** Yaklaşık dört yüz savaş gazisi.
- **Süre:** ≈ 2.3 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S047_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- COFFEE SNIFFER: war-veteran bean person in a faded blue uniform coat, one wooden peg leg and a crutch, very large comical sniffing nose added for the gag (the only bean person with a nose), bushy grey moustache.
- PRUSSIAN TOWNSFOLK: bean people in simple 18th-century working clothes, bonnets and aprons for women, brown waistcoats for men.

SCENE: A lineup of war veterans saluting: one with an eyepatch, one with a peg leg, one on a crutch, big moustaches, varied heights.
POSE / EXPRESSION: stiff, proud
COMPOSITION: row across the frame
CAMERA: medium shot, straight-on
BACKGROUND: cosy cottage interior, street outside
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S047 so the picture changes every 2-3 s; illustrates: "Yaklaşık dört yüz savaş gazisi."
CONTINUITY: Same location, light, characters and costumes as S047 — attach images/001_S047_vK.png as style/continuity reference. Must look clearly different in framing from S047.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S047d — ara çekim · Kahve koklayıcı
- **Dosya:** `001_S047d_v1.png`
- **Anlatım parçası:** Halk onlara kahve koklayıcılar diyor.
- **Süre:** ≈ 2.7 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S047_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- COFFEE SNIFFER: war-veteran bean person in a faded blue uniform coat, one wooden peg leg and a crutch, very large comical sniffing nose added for the gag (the only bean person with a nose), bushy grey moustache.
- PRUSSIAN TOWNSFOLK: bean people in simple 18th-century working clothes, bonnets and aprons for women, brown waistcoats for men.

SCENE: Extreme close-up of a sniffer's huge nose following a curling ink smell trail that comes from a chimney; his eyes are closed in concentration; townsfolk peek and giggle behind.
POSE / EXPRESSION: intense concentration, townsfolk amused
COMPOSITION: nose centre, trail from upper right
CAMERA: extreme close-up
BACKGROUND: cosy cottage interior, street outside
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S047 so the picture changes every 2-3 s; illustrates: "Halk onlara kahve koklayıcılar diyor."
CONTINUITY: Same location, light, characters and costumes as S047 — attach images/001_S047_vK.png as style/continuity reference. Must look clearly different in framing from S047.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S048b — ara çekim · Kurallar gömülüyor
- **Dosya:** `001_S048b_v1.png`
- **Anlatım parçası:** Friedrich bin yedi yüz seksen altıda ölüyor.
- **Süre:** ≈ 3.3 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S048_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Frederick's empty armchair with his tricorn hat on the seat and his cane leaning on it; the greyhound lies sadly beside it; a candle has just gone out with a thin smoke line.

COMPOSITION: chair centre, dog lower right
CAMERA: medium shot
BACKGROUND: rococo study from S043, dim
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds. Bright daylight.
STORY FUNCTION: Extra shot inside S048 so the picture changes every 2-3 s; illustrates: "Friedrich bin yedi yüz seksen altıda ölüyor."
CONTINUITY: Same location, light, characters and costumes as S048 — attach images/001_S048_vK.png as style/continuity reference. Must look clearly different in framing from S048.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S048c — ara çekim · Kurallar gömülüyor
- **Dosya:** `001_S048c_v1.png`
- **Anlatım parçası:** Kahve kuralları da çok geçmeden
- **Süre:** ≈ 2.4 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/03_pozlar.png`, `images/001_S048_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- PRUSSIAN TOWNSFOLK: bean people in simple 18th-century working clothes, bonnets and aprons for women, brown waistcoats for men.

SCENE: Two clerks comically bury a big blank rulebook in a small garden hole with a shovel.
POSE / EXPRESSION: clerks bored
COMPOSITION: hole centre, clerks either side
CAMERA: medium shot
BACKGROUND: small garden, daylight
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds. Bright daylight.
STORY FUNCTION: Extra shot inside S048 so the picture changes every 2-3 s; illustrates: "Kahve kuralları da çok geçmeden"
CONTINUITY: Same location, light, characters and costumes as S048 — attach images/001_S048_vK.png as style/continuity reference. Must look clearly different in framing from S048.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S049b — ara çekim · İsveç: Kral Gustav ve beş yasak
- **Dosya:** `001_S049b_v1.png`
- **Anlatım parçası:** Ama inatta birincilik İsveç'in.
- **Süre:** ≈ 2.3 sn
- **Referanslar:** `images/001_S049_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Establishing view of snowy 18th-century Stockholm old town by the water: red and ochre houses, ships frozen at the quay.

COMPOSITION: houses across the middle, frozen water below
CAMERA: wide
BACKGROUND: grey winter sky, snow
COLOURS: Nordic winter palette: snow white, ochre #D9B27C, falu red #8E3B2E, cold blue sky.
STORY FUNCTION: Extra shot inside S049 so the picture changes every 2-3 s; illustrates: "Ama inatta birincilik İsveç'in."
CONTINUITY: Same location, light, characters and costumes as S049 — attach images/001_S049_vK.png as style/continuity reference. Must look clearly different in framing from S049.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S049c — ara çekim · İsveç: Kral Gustav ve beş yasak
- **Dosya:** `001_S049c_v1.png`
- **Anlatım parçası:** İsveç kahveyi tam beş kez yasaklıyor.
- **Süre:** ≈ 2.6 sn
- **Referanslar:** `images/001_S049_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SWEDISH TOWNSFOLK: bean people in thick wool coats, knitted caps and shawls, rosy cheeks; women in long skirts and white caps.

SCENE: Five blank decrees with red seals pinned over one another on a wooden wall; snow drifts; a Swedish man in a fur hat rolls his eyes.
POSE / EXPRESSION: exasperated
COMPOSITION: decrees left, man right
CAMERA: medium shot
BACKGROUND: snow, grey sky
COLOURS: Nordic winter palette: snow white, ochre #D9B27C, falu red #8E3B2E, cold blue sky.
STORY FUNCTION: Extra shot inside S049 so the picture changes every 2-3 s; illustrates: "İsveç kahveyi tam beş kez yasaklıyor."
CONTINUITY: Same location, light, characters and costumes as S049 — attach images/001_S049_vK.png as style/continuity reference. Must look clearly different in framing from S049.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S050b — ara çekim · Masanın altında gizli kahve
- **Dosya:** `001_S050b_v1.png`
- **Anlatım parçası:** gizlice içmeye devam ediyor.
- **Süre:** ≈ 2.7 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `images/001_S050_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye keeps his scarf and wears a knitted grey wool cap and a thick wool coat (Sweden).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SWEDISH TOWNSFOLK: bean people in thick wool coats, knitted caps and shawls, rosy cheeks; women in long skirts and white caps.

SCENE: View from under the table: faces lit by a candle, cups clinking; Fasulye holds a finger to his lips.
POSE / EXPRESSION: secretive, giggling
COMPOSITION: faces in a semicircle, candle centre
CAMERA: close-up, low angle
BACKGROUND: wooden kitchen, tiled stove, candle
COLOURS: Nordic winter palette, warm interior.
STORY FUNCTION: Extra shot inside S050 so the picture changes every 2-3 s; illustrates: "gizlice içmeye devam ediyor."
CONTINUITY: Same location, light, characters and costumes as S050 — attach images/001_S050_vK.png as style/continuity reference. Must look clearly different in framing from S050.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S051b — ara çekim · Demlik cenazesi
- **Dosya:** `001_S051b_v1.png`
- **Anlatım parçası:** bin yedi yüz doksan dörtteki yasağa tepki olarak
- **Süre:** ≈ 2.3 sn
- **Referanslar:** `character-references/fasulye/05_komik_tepkiler.png`, `images/001_S051_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SWEDISH TOWNSFOLK: bean people in thick wool coats, knitted caps and shawls, rosy cheeks; women in long skirts and white caps.

SCENE: A few Swedes read a blank decree pinned to a door and frown; one woman hugs a copper coffee pot protectively.
POSE / EXPRESSION: annoyed, protective
COMPOSITION: door left, people right
CAMERA: medium shot
BACKGROUND: snowy street
COLOURS: Nordic winter palette with black mourning clothes.
STORY FUNCTION: Extra shot inside S051 so the picture changes every 2-3 s; illustrates: "bin yedi yüz doksan dörtteki yasağa tepki olarak"
CONTINUITY: Same location, light, characters and costumes as S051 — attach images/001_S051_vK.png as style/continuity reference. Must look clearly different in framing from S051.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S052b — ara çekim · İkiz deneyi
- **Dosya:** `001_S052b_v1.png`
- **Anlatım parçası:** Bir de meşhur hikâye var:
- **Süre:** ≈ 1.8 sn
- **Referanslar:** `images/001_S052_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).

SCENE: Fasulye opens a large old book; an ink drawing of a small crown and two cups rises from the pages like steam.
POSE / EXPRESSION: storyteller's playful look
COMPOSITION: book centre, Fasulye behind it
CAMERA: medium close-up
BACKGROUND: plain warm paper background
COLOURS: Muted greys with the two cups as accents (dark brown coffee, amber tea).
STORY FUNCTION: Extra shot inside S052 so the picture changes every 2-3 s; illustrates: "Bir de meşhur hikâye var:"
CONTINUITY: Same location, light, characters and costumes as S052 — attach images/001_S052_vK.png as style/continuity reference. Must look clearly different in framing from S052.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S052c — ara çekim · İkiz deneyi
- **Dosya:** `001_S052c_v1.png`
- **Anlatım parçası:** Kral Üçüncü Gustav,
- **Süre:** ≈ 1.4 sn
- **Referanslar:** `images/001_S052_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- KING GUSTAV III (Sweden, 1770s): bean person with white powdered wig with side rolls, light blue silk coat, ermine-trimmed cloak, theatrical gesture.

SCENE: Theatrical portrait of King Gustav III in a blue coat and powdered wig, one hand raised dramatically.
POSE / EXPRESSION: theatrical, self-confident
COMPOSITION: king centre
CAMERA: medium shot, low angle
BACKGROUND: palace curtain
COLOURS: Muted greys with the two cups as accents (dark brown coffee, amber tea).
STORY FUNCTION: Extra shot inside S052 so the picture changes every 2-3 s; illustrates: "Kral Üçüncü Gustav,"
CONTINUITY: Same location, light, characters and costumes as S052 — attach images/001_S052_vK.png as style/continuity reference. Must look clearly different in framing from S052.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S052d — ara çekim · İkiz deneyi
- **Dosya:** `001_S052d_v1.png`
- **Anlatım parçası:** idam mahkûmu ikiz kardeşlerle bir deney yaptırmış.
- **Süre:** ≈ 3.5 sn
- **Referanslar:** `images/001_S052_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- THE TWINS: two identical bean people with identical short sandy hair and stubble, plain grey prison smocks; one always holds a coffee cup, the other a tea cup.

SCENE: The identical twins in plain grey prison clothes stand side by side and look at each other, puzzled.
POSE / EXPRESSION: puzzled
COMPOSITION: twins centre
CAMERA: medium shot
BACKGROUND: simple stone walls, barred window with light
COLOURS: Muted greys with the two cups as accents (dark brown coffee, amber tea).
STORY FUNCTION: Extra shot inside S052 so the picture changes every 2-3 s; illustrates: "idam mahkûmu ikiz kardeşlerle bir deney yaptırmış."
CONTINUITY: Same location, light, characters and costumes as S052 — attach images/001_S052_vK.png as style/continuity reference. Must look clearly different in framing from S052.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S053b — ara çekim · İkizler yaşlanıyor
- **Dosya:** `001_S053b_v1.png`
- **Anlatım parçası:** Hikâyeye göre önce deneyi izleyen doktorlar öldü,
- **Süre:** ≈ 4.2 sn
- **Referanslar:** `images/001_S053_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- THE TWINS: two identical bean people with identical short sandy hair and stubble, plain grey prison smocks; one always holds a coffee cup, the other a tea cup.

SCENE: Two empty chairs with notebooks and spectacles left on them, a burnt-out candle (no bodies); the older twins are in the background with their cups.

COMPOSITION: chairs foreground, twins background
CAMERA: medium shot
BACKGROUND: same room, cobwebs, dust
COLOURS: Same muted palette, slightly faded.
STORY FUNCTION: Extra shot inside S053 so the picture changes every 2-3 s; illustrates: "Hikâyeye göre önce deneyi izleyen doktorlar öldü,"
CONTINUITY: Same location, light, characters and costumes as S053 — attach images/001_S053_vK.png as style/continuity reference. Must look clearly different in framing from S053.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S053c — ara çekim · İkizler yaşlanıyor
- **Dosya:** `001_S053c_v1.png`
- **Anlatım parçası:** sonra kral öldü.
- **Süre:** ≈ 1.4 sn
- **Referanslar:** `images/001_S053_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Gustav III's crown resting on an empty velvet cushion tied with a black ribbon.

COMPOSITION: crown centre
CAMERA: close-up
BACKGROUND: dark curtain
COLOURS: Same muted palette, slightly faded.
STORY FUNCTION: Extra shot inside S053 so the picture changes every 2-3 s; illustrates: "sonra kral öldü."
CONTINUITY: Same location, light, characters and costumes as S053 — attach images/001_S053_vK.png as style/continuity reference. Must look clearly different in framing from S053.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S055b — ara çekim · Modern fika
- **Dosya:** `001_S055b_v1.png`
- **Anlatım parçası:** Kesin olan şu: bin sekiz yüz yirmi üçte son yasak kalkıyor.
- **Süre:** ≈ 4.6 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S055_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SWEDISH TOWNSFOLK: bean people in thick wool coats, knitted caps and shawls, rosy cheeks; women in long skirts and white caps.

SCENE: 1823, snowy Stockholm square: people cheer, someone pours coffee in the street, a torn blank decree lies on the snow.
POSE / EXPRESSION: celebrating
COMPOSITION: crowd centre, torn decree lower left
CAMERA: wide
BACKGROUND: snowy square from S049
COLOURS: Warm interior + cold blue window.
STORY FUNCTION: Extra shot inside S055 so the picture changes every 2-3 s; illustrates: "Kesin olan şu: bin sekiz yüz yirmi üçte son yasak kalkıyor."
CONTINUITY: Same location, light, characters and costumes as S055 — attach images/001_S055_vK.png as style/continuity reference. Must look clearly different in framing from S055.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S055c — ara çekim · Modern fika
- **Dosya:** `001_S055c_v1.png`
- **Anlatım parçası:** en çok kahve içen ülkelerden biri.
- **Süre:** ≈ 2.6 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S055_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- MODERN PEOPLE: bean people in casual contemporary clothes (hoodies, cardigans), various hair styles.

SCENE: Close-up of the fika table: many cups and cinnamon buns; a hand reaches for a refill; Fasulye looks content.
POSE / EXPRESSION: content
COMPOSITION: table top centre, Fasulye right
CAMERA: close-up, high angle
BACKGROUND: Scandinavian wooden interior, warm light
COLOURS: Warm interior + cold blue window.
STORY FUNCTION: Extra shot inside S055 so the picture changes every 2-3 s; illustrates: "en çok kahve içen ülkelerden biri."
CONTINUITY: Same location, light, characters and costumes as S055 — attach images/001_S055_vK.png as style/continuity reference. Must look clearly different in framing from S055.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S056b — ara çekim · Kolschitzky efsanesi
- **Dosya:** `001_S056b_v1.png`
- **Anlatım parçası:** Peki kahvehaneleriyle meşhur Viyana?
- **Süre:** ≈ 2.5 sn
- **Referanslar:** `images/001_S056_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- MODERN PEOPLE: bean people in casual contemporary clothes (hoodies, cardigans), various hair styles.

SCENE: Classic Viennese coffeehouse interior: marble tables, bentwood chairs, chandeliers, blank newspapers on wooden holders; Fasulye sits with a cup.
POSE / EXPRESSION: curious
COMPOSITION: Fasulye centre-right, room depth left
CAMERA: medium wide
BACKGROUND: elegant warm interior
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds. Golden sunrise.
STORY FUNCTION: Extra shot inside S056 so the picture changes every 2-3 s; illustrates: "Peki kahvehaneleriyle meşhur Viyana?"
CONTINUITY: Same location, light, characters and costumes as S056 — attach images/001_S056_vK.png as style/continuity reference. Must look clearly different in framing from S056.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S056c — ara çekim · Kolschitzky efsanesi
- **Dosya:** `001_S056c_v1.png`
- **Anlatım parçası:** Anlatılan hikâyeye göre
- **Süre:** ≈ 1.6 sn
- **Referanslar:** `images/001_S056_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: An old-engraving-style framed vignette: the walls of Vienna with tents outside, drawn like a fairy-tale picture-book page.

COMPOSITION: city walls centre, tents around
CAMERA: wide
BACKGROUND: ink border frame, parchment
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds. Golden sunrise.
STORY FUNCTION: Extra shot inside S056 so the picture changes every 2-3 s; illustrates: "Anlatılan hikâyeye göre"
CONTINUITY: Same location, light, characters and costumes as S056 — attach images/001_S056_vK.png as style/continuity reference. Must look clearly different in framing from S056.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S056d — ara çekim · Kolschitzky efsanesi
- **Dosya:** `001_S056d_v1.png`
- **Anlatım parçası:** Osmanlı ordusu bin altı yüz seksen üçte çekilirken
- **Süre:** ≈ 3.5 sn
- **Referanslar:** `images/001_S056_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- JANISSARIES: bean people with bushy moustaches, tall white felt börk caps that fold down at the back (with a small spoon-holder at the front), blue-grey long coats, red sashes; rowdy and cheerful when off-duty. Weapons are never drawn.

SCENE: Dawn: an army camp being abandoned, tents folding, carts and soldiers marching away in the distance (no weapons in use, no battle).

COMPOSITION: column moving away to the horizon
CAMERA: wide, high angle
BACKGROUND: pink-gold sunrise, hills
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds. Golden sunrise.
STORY FUNCTION: Extra shot inside S056 so the picture changes every 2-3 s; illustrates: "Osmanlı ordusu bin altı yüz seksen üçte çekilirken"
CONTINUITY: Same location, light, characters and costumes as S056 — attach images/001_S056_vK.png as style/continuity reference. Must look clearly different in framing from S056.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S056e — ara çekim · Kolschitzky efsanesi
- **Dosya:** `001_S056e_v1.png`
- **Anlatım parçası:** çuval çuval kahve bırakıyor.
- **Süre:** ≈ 2.0 sn
- **Referanslar:** `images/001_S056_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- VIENNA 1680s CROWD: bean people in wigs, tricorn-less broad hats, coats and bonnets.

SCENE: Piles of abandoned coffee sacks under a tent, beans spilling; a curious Viennese soldier pokes one with a finger.
POSE / EXPRESSION: puzzled curiosity
COMPOSITION: sacks centre, soldier right
CAMERA: medium close-up
BACKGROUND: pink-gold sunrise, hills
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds. Golden sunrise.
STORY FUNCTION: Extra shot inside S056 so the picture changes every 2-3 s; illustrates: "çuval çuval kahve bırakıyor."
CONTINUITY: Same location, light, characters and costumes as S056 — attach images/001_S056_vK.png as style/continuity reference. Must look clearly different in framing from S056.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S058b — ara çekim · Diodato'nun dükkânı
- **Dosya:** `001_S058b_v1.png`
- **Anlatım parçası:** Kayıtlara göre Viyana'nın ilk kahve izni bin altı yüz seksen beşte
- **Süre:** ≈ 5.5 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `character-references/fasulye/04_kostum_efekt.png`, `images/001_S058_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: A stack of old official ledgers and one document with a large wax seal; the handwriting is only illegible wavy ink lines.

COMPOSITION: sealed document centre
CAMERA: close-up, high angle
BACKGROUND: wooden archive table
COLOURS: European 17th–18th c. palette: brown wood, grey-blue, dark green, candle-warm light, muted reds.
STORY FUNCTION: Extra shot inside S058 so the picture changes every 2-3 s; illustrates: "Kayıtlara göre Viyana'nın ilk kahve izni bin altı yüz seksen beşte"
CONTINUITY: Same location, light, characters and costumes as S058 — attach images/001_S058_vK.png as style/continuity reference. Must look clearly different in framing from S058.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S059b — ara çekim · Hükümdarlar aynı masada
- **Dosya:** `001_S059b_v1.png`
- **Anlatım parçası:** Mekke'de toplantılar.
- **Süre:** ≈ 1.8 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S059_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- HAYIR BEY (Mecca market/order inspector, 1511): bean person, stern; thick black moustache and short black beard, heavy frowning eyebrows; white turban wrapped around a dark red cap, long dark indigo robe #2C3B57 with an ochre sash, a short official staff.

SCENE: Hayır Bey seated at the long table glares sideways at a small group of men talking over cups in a little vignette beside him.
POSE / EXPRESSION: suspicious glare
COMPOSITION: Hayır Bey left, vignette right
CAMERA: medium close-up
BACKGROUND: warm paper background and lamp light (same as S016)
COLOURS: Base palette; rulers in their signature colours.
STORY FUNCTION: Extra shot inside S059 so the picture changes every 2-3 s; illustrates: "Mekke'de toplantılar."
CONTINUITY: Same location, light, characters and costumes as S059 — attach images/001_S059_vK.png as style/continuity reference. Must look clearly different in framing from S059.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S059c — ara çekim · Hükümdarlar aynı masada
- **Dosya:** `001_S059c_v1.png`
- **Anlatım parçası:** İstanbul'da isyan korkusu.
- **Süre:** ≈ 2.2 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S059_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- SULTAN MURAD IV (Ottoman, 1630s): young, strong bean person with a full short black beard and thick eyebrows; very large white Ottoman ceremonial turban (kavuk) with a jewelled aigrette and feather plume; crimson-and-gold kaftan #B83A2B with gold buttons; stern, intense gaze. DISGUISED VERSION: long dark brown hooded cloak covering the turban, only the eyes and beard visible.

SCENE: Murad IV seated at the long table, eyes darting nervously toward faint silhouettes of tall janissary caps on the wall.
POSE / EXPRESSION: nervous, distrustful
COMPOSITION: Murad left, silhouettes right
CAMERA: medium close-up
BACKGROUND: warm paper background and lamp light (same as S016)
COLOURS: Base palette; rulers in their signature colours.
STORY FUNCTION: Extra shot inside S059 so the picture changes every 2-3 s; illustrates: "İstanbul'da isyan korkusu."
CONTINUITY: Same location, light, characters and costumes as S059 — attach images/001_S059_vK.png as style/continuity reference. Must look clearly different in framing from S059.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S059d — ara çekim · Hükümdarlar aynı masada
- **Dosya:** `001_S059d_v1.png`
- **Anlatım parçası:** Londra'da dedikodu.
- **Süre:** ≈ 1.6 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S059_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- KING CHARLES II (England, 1670s): bean person with a long, very curly black wig falling to the shoulders, thin black moustache, small gold crown, lace cravat, dark red velvet coat; vain, sulky expression.

SCENE: Charles II seated at the long table with swirling rumour ink lines circling his head.
POSE / EXPRESSION: annoyed, overwhelmed
COMPOSITION: king centre
CAMERA: medium close-up
BACKGROUND: warm paper background and lamp light (same as S016)
COLOURS: Base palette; rulers in their signature colours.
STORY FUNCTION: Extra shot inside S059 so the picture changes every 2-3 s; illustrates: "Londra'da dedikodu."
CONTINUITY: Same location, light, characters and costumes as S059 — attach images/001_S059_vK.png as style/continuity reference. Must look clearly different in framing from S059.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S059e — ara çekim · Hükümdarlar aynı masada
- **Dosya:** `001_S059e_v1.png`
- **Anlatım parçası:** Prusya'da para.
- **Süre:** ≈ 1.3 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S059_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- FREDERICK THE GREAT (Prussia, 1770s): older bean person with grey powdered hair tied in a queue, black tricorn hat, worn Prussian-blue uniform coat with red cuffs, walking cane; sharp, thrifty, calculating eyes.

SCENE: Frederick seated at the long table clutching his coin purse tightly to his chest.
POSE / EXPRESSION: stingy, worried
COMPOSITION: Frederick centre
CAMERA: medium close-up
BACKGROUND: warm paper background and lamp light (same as S016)
COLOURS: Base palette; rulers in their signature colours.
STORY FUNCTION: Extra shot inside S059 so the picture changes every 2-3 s; illustrates: "Prusya'da para."
CONTINUITY: Same location, light, characters and costumes as S059 — attach images/001_S059_vK.png as style/continuity reference. Must look clearly different in framing from S059.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S059f — ara çekim · Hükümdarlar aynı masada
- **Dosya:** `001_S059f_v1.png`
- **Anlatım parçası:** Hiçbiri gerçekten fincandaki o siyah sıvıyla ilgili değildi.
- **Süre:** ≈ 4.9 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S059_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Top-down extreme close-up of a cup of black coffee on the wooden table; its still surface reflects the hanging lamp; one small ripple.

COMPOSITION: cup centred
CAMERA: top-down extreme close-up
BACKGROUND: warm paper background and lamp light (same as S016)
COLOURS: Base palette; rulers in their signature colours.
STORY FUNCTION: Extra shot inside S059 so the picture changes every 2-3 s; illustrates: "Hiçbiri gerçekten fincandaki o siyah sıvıyla ilgili değildi."
CONTINUITY: Same location, light, characters and costumes as S059 — attach images/001_S059_vK.png as style/continuity reference. Must look clearly different in framing from S059.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S060c — ara çekim · Masa: her çağdan insanlar
- **Dosya:** `001_S060c_v1.png`
- **Anlatım parçası:** konuşturması ve uyanık tutmasıydı.
- **Süre:** ≈ 2.5 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S060_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- JANISSARIES: bean people with bushy moustaches, tall white felt börk caps that fold down at the back (with a small spoon-holder at the front), blue-grey long coats, red sashes; rowdy and cheerful when off-duty. Weapons are never drawn.
- LONDON 1670s CROWD: bean people in long brown or grey periwigs and wide-brim hats, plain dark coats, white collars; merchants, tradesmen with aprons.
- SWEDISH TOWNSFOLK: bean people in thick wool coats, knitted caps and shawls, rosy cheeks; women in long skirts and white caps.

SCENE: Late night at the long table: the candle is low, a moon in a window, everyone still wide awake with big round eyes; Fasulye pours another cup.
POSE / EXPRESSION: wide-awake
COMPOSITION: table across the frame, moon upper right
CAMERA: medium wide
BACKGROUND: warm lamp glow, steam rising
COLOURS: Warmest palette of the video.
STORY FUNCTION: Extra shot inside S060 so the picture changes every 2-3 s; illustrates: "konuşturması ve uyanık tutmasıydı."
CONTINUITY: Same location, light, characters and costumes as S060 — attach images/001_S060_vK.png as style/continuity reference. Must look clearly different in framing from S060.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S060d — ara çekim · Masa: her çağdan insanlar
- **Dosya:** `001_S060d_v1.png`
- **Anlatım parçası:** Ve bunu yasaklamaya çalışan herkes kaybetti.
- **Süre:** ≈ 3.2 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S060_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

SCENE: Under the table: five small crumpled blank decrees lie on the floor in the lamp light while the feet of happy people tap around them.

COMPOSITION: decrees centre on the floor
CAMERA: low angle, close
BACKGROUND: warm lamp glow, steam rising
COLOURS: Warmest palette of the video.
STORY FUNCTION: Extra shot inside S060 so the picture changes every 2-3 s; illustrates: "Ve bunu yasaklamaya çalışan herkes kaybetti."
CONTINUITY: Same location, light, characters and costumes as S060 — attach images/001_S060_vK.png as style/continuity reference. Must look clearly different in framing from S060.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S061b — ara çekim · Fasulye kadeh kaldırır
- **Dosya:** `001_S061b_v1.png`
- **Anlatım parçası:** Yani bir dahaki sefere kahveni içerken
- **Süre:** ≈ 3.0 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S061_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).

SCENE: Fasulye sits in the modern café sipping peacefully with his eyes closed.
POSE / EXPRESSION: peaceful
COMPOSITION: Fasulye centre-left, cup at the optical centre
CAMERA: medium shot
BACKGROUND: same café as S001
COLOURS: Base palette, warm daylight.
STORY FUNCTION: Extra shot inside S061 so the picture changes every 2-3 s; illustrates: "Yani bir dahaki sefere kahveni içerken"
CONTINUITY: Same location, light, characters and costumes as S061 — attach images/001_S061_vK.png as style/continuity reference. Must look clearly different in framing from S061.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S061c — ara çekim · Fasulye kadeh kaldırır
- **Dosya:** `001_S061c_v1.png`
- **Anlatım parçası:** biri sana ters ters bakarsa,
- **Süre:** ≈ 2.2 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S061_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- All other humans share Fasulye's exact bean anatomy (one egg-shaped head-body, big round eyes, no nose, thin ink limbs, small round hands, small oval shoes). Identity comes ONLY from hair, facial hair (drawn as an ink mass on the lower face), headwear, clothing and colour. No realistic faces, no portrait likeness.
- MODERN PEOPLE: bean people in casual contemporary clothes (hoodies, cardigans), various hair styles.

SCENE: Close-up of the bean person at the next table glaring with one eyebrow down and arms crossed.
POSE / EXPRESSION: disapproving glare
COMPOSITION: face right of centre
CAMERA: close-up
BACKGROUND: same café as S001
COLOURS: Base palette, warm daylight.
STORY FUNCTION: Extra shot inside S061 so the picture changes every 2-3 s; illustrates: "biri sana ters ters bakarsa,"
CONTINUITY: Same location, light, characters and costumes as S061 — attach images/001_S061_vK.png as style/continuity reference. Must look clearly different in framing from S061.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

## S061d — ara çekim · Fasulye kadeh kaldırır
- **Dosya:** `001_S061d_v1.png`
- **Anlatım parçası:** sadece şunu söyle: Sultanlar denedi.
- **Süre:** ≈ 2.8 sn
- **Referanslar:** `character-references/fasulye/01_donus_sayfasi.png`, `character-references/fasulye/02_ifadeler.png`, `images/001_S061_vK.png (ana sahne)`

```
STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight (thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, no anime, no chibi, no photorealism.
FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of important details (text is added later on a separate layer).

CHARACTERS (keep exactly this identity and anatomy):
- FASULYE (the narrator mascot): a single smooth egg/bean-shaped body that is head and torso in one, slightly narrower at the top, off-white paper colour #FFFAF0 with a pale beige shadow #E7DFD0 and fine ink hatching on the right side; NO neck, NO nose. Face in the upper third: two large round white eyes with thin ink outline, small black pupils and a tiny white highlight, short thin eyebrows, a single-line mouth, barely visible peach cheeks. Signature: ONE curly hair tuft on top shaped like a small question-mark curl, and a knotted terracotta scarf #E4572E around the 'neck' area with one end hanging to his right. Thin ink-line arms with elbows, small round light-coloured hands (not gloves, not black), thin legs (about 0.27 of body height), small black oval shoes. Calm, curious, dry-humoured; reactions are small and understated.
  COSTUME: Fasulye wears only his signature terracotta scarf (modern look).

SCENE: Fasulye leans slightly toward the viewer and raises one finger; in the steam above his cup faint ink silhouettes of a small turban and a crown appear (callback to S002).
POSE / EXPRESSION: calm, dry smirk
COMPOSITION: Fasulye centre, steam shapes upper right
CAMERA: medium close-up
BACKGROUND: same café as S001
COLOURS: Base palette, warm daylight.
STORY FUNCTION: Extra shot inside S061 so the picture changes every 2-3 s; illustrates: "sadece şunu söyle: Sultanlar denedi."
CONTINUITY: Same location, light, characters and costumes as S061 — attach images/001_S061_vK.png as style/continuity reference. Must look clearly different in framing from S061.

DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, no noses on bean people (except where explicitly asked), do not change Fasulye's design.
```

