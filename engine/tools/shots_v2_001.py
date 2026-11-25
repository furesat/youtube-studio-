"""Video 001 · v2 ara çekimler (görüntü ~2-3 sn'de bir değişsin).
Çıktı: videos/001/SHOTS_v2.json + videos/001/IMAGE_PROMPTS_v2.md (ilk promptlarla aynı biçim; sahne içerikleri elle yazıldı)
Mevcut sahne görselleri (S001..S061) aynen kullanılır; burada yalnızca ek çekimler tanımlanır.
Kullanım: python3 engine/tools/shots_v2_001.py"""
import os, sys, json, copy
sys.path.insert(0, os.path.dirname(__file__))
from prompts import build_prompt

V = "videos/001"
EXTRA_CAST = {
    "pecevi": "PEÇEVİ (Ottoman historian): elderly bean man, short grey beard drawn as an ink mass, large round white turban, plain dark-teal robe, small reading spectacles.",
    "osman2": "YOUNG OSMAN II: a young bean man with a thin black moustache, very tall white ceremonial turban with a small plume, red kaftan with gold trim.",
    "young_frederick": "YOUNG FREDERICK: a small bean boy in a tiny powdered wig with a ribbon, blue coat, rosy cheeks.",
}

# (yeni_id, anlatımdaki başlangıç ifadesi, alanlar) — sahne içi SIRA = liste sırası; "A" mevcut görsel.
# Alanlar: action, expr, comp, cam (+ isteğe bağlı cast, costume, bg)
SHOTS = {
 "S002": [("A", ""), ("b", "krallar fermanlar yazdı", dict(
    action="An ink vignette rising out of cup steam at the bottom edge: a king's small round hand with a lace cuff presses a big red wax seal onto a long blank decree; beside it a coffee sack burns in small flames and a wooden shop shutter is slammed shut.",
    expr="", comp="seal and decree at the optical centre, flame left, shutter right, steam curls tie them to the cup at the bottom", cam="close-up, straight-on", cast=[]))],
 "S003": [("A", ""), ("b", "Londra, Prusya", dict(
    action="Closer view of the SAME unlabelled antique map, now showing only northern Europe: Britain, the North Sea, the Baltic coast and Scandinavia; ink coastlines, tiny waves, one small ship.",
    expr="", comp="Britain left third, Baltic coast lower centre, Scandinavia upper right", cam="top-down flat map, zoomed in")),
    ("c", "Kahve en az beş", dict(
    action="The SAME unlabelled antique map (as in S003) seen whole; five tiny hand-drawn coffee cups stand on it at Mecca, Istanbul, London, Berlin and Stockholm, each struck through with a short red ink cross stroke.",
    expr="", comp="same framing as S003", cam="top-down flat map"))],
 "S005": [("A", ""), ("b", "Bu yasakların neredeyse", dict(
    action="Extreme close-up through the magnifying glass: the coffee bean appears huge on the saucer, and one of Fasulye's big round eyes is seen enlarged and distorted at the edge of the lens.",
    expr="one giant curious eye, eyebrow raised", comp="round lens fills most of the frame, bean in the lens centre", cam="extreme close-up")),
    ("c", "kahveyle ilgili değildi", dict(
    action="Fasulye has lowered the magnifying glass and gives a small shrug; the single bean lies innocently on the saucer in front of him.",
    expr="dry, unimpressed half-lidded look, small shrug", comp="Fasulye centre, bean small in the lower foreground", cam="medium close-up, eye level")),
    ("d", "Peki neyle ilgiliydi?", dict(
    action="Fasulye turns to the viewer with his chin resting on one hand, thinking; three small empty ink thought-bubbles float above his curly tuft.",
    expr="thoughtful, eyes looking up and sideways", comp="Fasulye centre-left, bubbles upper right", cam="medium shot, eye level"))],
 "S007": [("A", ""), ("b", "Sufiler gece boyunca", dict(
    action="Close-up of a robed man's hands pouring dark coffee from a clay pot into a tiny handle-less cup by lamplight; behind, several pairs of wide-awake eyes glint; a crescent moon low in the night sky above the wall.",
    expr="calm, wide-awake eyes", comp="pot and cup at the optical centre, eyes in soft background", cam="close-up, slightly high angle"))],
 "S008": [("A", ""), ("b", "İnsanlar toplanıyor", dict(
    action="Close on the lute player singing with his eyes closed while two men clap along; Fasulye sways happily with his tiny cup; simple wavy ink lines float in the air for the music (no musical notation).",
    expr="joyful, relaxed", comp="lute player centre, clapping men left, Fasulye right", cam="medium close-up"))],
 "S009": [("A", ""), ("b", "Şehrin asayişinden", dict(
    action="Close portrait of Hayır Bey holding his short staff upright, chest out, looking down sternly with one eyebrow lowered.",
    expr="stern, suspicious, authoritative", comp="Hayır Bey centre, staff diagonal", cam="close-up, low angle"))],
 "S010": [("A", ""), ("b", "Ve şüpheleniyor", dict(
    action="Extreme close-up of Hayır Bey's narrowed eyes peeking around the edge of a wall; warm lantern light falls on half of his face, the rest is in blue shadow.",
    expr="eyes narrowed to slits, suspicious", comp="wall edge vertical at left third, eyes on the right of it", cam="extreme close-up", cast=["hayir_bey"]))],
 "S011": [("A", ""), ("b", "Bu içecek insanı", dict(
    action="Close-up on the physician holding the small coffee cup up to the window light, squinting at it; two scholars lean in, one sniffs it with his eyes closed.",
    expr="concentrated, sceptical", comp="cup at the optical centre, faces around it", cam="close-up", cast=["scholars"]))],
 "S014": [("b", "", dict(
    action="Hayır Bey stands small in the Mecca council room while a huge dark ink shadow of a seated ruler with a tall cap looms over him on the wall behind.",
    expr="Hayır Bey swallows nervously, eyes darting up", comp="Hayır Bey lower right, giant shadow fills the left and top", cam="medium shot, slight low angle",
    cast=["hayir_bey"], bg="the council room from S011, dim")),
    ("c", "Mekke o dönem", dict(
    action="Symbolic desert view: a lone messenger on a camel rides along a dotted ink path from a small cluster of Hijaz houses (left) across dunes and the Red Sea coast to a distant striped-arch palace on the Nile (right).",
    expr="", comp="path curves from lower left to upper right", cam="wide, high angle", cast=[], bg="pale sand dunes, a strip of teal sea, golden sky")),
    ("d", "Ve söylenene göre", dict(
    action="Inside the Cairo palace: we see Sultan Kansu Gavri only from behind, a large silhouette on cushions, slowly raising a small cup; a thin curl of steam rises above his turban.",
    expr="", comp="sultan's back centre, arches framing him", cam="medium shot from behind")),
    ("A", "Sultan Kansu Gavri de")],
 "S015": [("A", ""), ("b", "ama insanların kahvesine", dict(
    action="Close-up of Hayır Bey reading the sealed scroll, his whole face sagging, moustache drooping, a big sweat drop on his temple.",
    expr="deflated, defeated, mouth wobbling", comp="face centre, top edge of scroll in the lower frame", cam="close-up", cast=["hayir_bey"])),
    ("c", "Yasak birkaç hafta", dict(
    action="The Mecca lane from S013 a few weeks later: shutters are open again, a server pours coffee, people sit back down on benches; a faint black scorch mark on the ground where the bonfire was.",
    expr="", comp="open shop right, scorch mark lower left", cam="wide, eye level", cast=["bean_people"], bg="Mecca market lane, daylight"))],
 "S016": [("A", ""), ("b", "Sorun masaydı", dict(
    action="Top-down view of the long empty wooden table with stools around it in a warm pool of lamp light; the small coffee cup at the near end looks tiny.",
    expr="", comp="table runs diagonally across the frame, cup lower left", cam="top-down", cast=[]))],
 "S018": [("b", "", dict(
    action="The historian Peçevi writes at a low desk in a big book with a reed pen; the pages show only illegible wavy ink lines.",
    expr="focused, scholarly", comp="Peçevi centre-left, book centre", cam="medium shot", cast=["pecevi"], bg="calm study with a window and stacked books")),
    ("c", "Halep'ten Hakem", dict(
    action="Two travellers arrive at a city gate leading mules loaded with coffee sacks: Hakem (left) and Şems (right) greet each other with a wave.",
    expr="cheerful, hopeful", comp="Hakem left, Şems right, gate arch behind", cam="wide, eye level", cast=["hakem_sems"], bg="stone city gate, morning light")),
    ("A", "Tahtakale'de")],
 "S019": [("b", "", dict(
    action="Hakem pours coffee into a small cup while Şems invites a passer-by to sit on a cushioned bench in front of their shop.",
    expr="welcoming smiles", comp="Hakem left pouring, Şems right gesturing to the bench", cam="medium shot", cast=["hakem_sems", "osmanli_crowd"])),
    ("A", "Sonuç:")],
 "S020": [("A", ""), ("b", "tavla oynayan", dict(
    action="Close on a backgammon board between two players mid-move with dice; next to them a poet scribbles with a reed pen on paper covered only in wavy ink lines.",
    expr="playful concentration", comp="board centre, poet right", cam="close-up, slightly high angle", cast=["osmanli_crowd"]))],
 "S022": [("A", ""), ("b", "İnsanlar ibadeti", dict(
    action="A few bean people hurry past the elderly scholar toward the busy coffeehouse, one skipping with his slippers in his hand; the scholar shakes his head.",
    expr="scholar disapproving, hurrying men eager", comp="scholar left, runners moving right toward the coffeehouse", cam="wide, eye level", cast=["scholars", "osmanli_crowd"]))],
 "S023": [("b", "", dict(
    action="Inside the coffeehouse three well-dressed dignitaries (a pasha in a fur-trimmed kaftan, a rich merchant, a poet) raise their cups together like a friendly team.",
    expr="confident, warm", comp="three figures centre in a row", cam="medium shot", cast=["osmanli_crowd"], bg="coffeehouse interior from S020")),
    ("A", "Şeyhülislam"),
    ("c", "kahveye yeşil ışık", dict(
    action="Close-up: Bostanzade presses a seal stamp onto a blank scroll; a soft symbolic green glow spreads from the stamp; Fasulye gives a small thumbs-up in the background.",
    expr="Bostanzade calm and kind, Fasulye relieved", comp="stamp at the optical centre, Fasulye upper right", cam="close-up"))],
 "S025": [("b", "", dict(
    action="Murad IV stands alone at a palace window at night, brooding, looking down at the city where small coffeehouse windows glow.",
    expr="dark, distrustful, jaw tight", comp="Murad left silhouette, city lights right", cam="medium shot from behind his shoulder", cast=["murad4"], bg="night palace interior, blue moonlight")),
    ("c", "Ağabeyi Genç Osman", dict(
    action="A memory portrait of young Osman II in an oval wooden frame on a wall; the glass has a thin crack; sepia, muted colours.",
    expr="young, serious", comp="oval frame centred", cam="straight-on", cast=["osman2"], bg="dim palace wall")),
    ("A", "isyan eden")],
 "S026": [("A", ""), ("b", "Tahmin et", dict(
    action="Fasulye, holding the coffee tray, turns to the viewer with raised eyebrows; the loud janissaries are a soft blur behind him.",
    expr="knowing, dry 'you guessed it' look", comp="Fasulye centre, blurred group behind", cam="medium close-up"))],
 "S027": [("A", ""), ("b", "Şehrin beşte biri", dict(
    action="The next morning: a wide view of a burnt district, charred beams and ash, thin smoke wisps; surviving houses at the edges; a few small figures stand looking at the ruins.",
    expr="", comp="burnt area centre, survivors lower right", cam="wide, high angle", cast=["bean_people"], bg="grey morning sky with smoke"))],
 "S028": [("A", ""), ("b", "Tütünü de", dict(
    action="Close-up: a guard snaps a long tobacco pipe in two over a basket full of confiscated pipes; an old man watches sadly.",
    expr="guard stern, old man sad", comp="breaking pipe centre, basket below, old man right", cam="close-up", cast=["bean_people"]))],
 "S029": [("b", "", dict(
    action="A blank decree with a big red wax seal is nailed to a wooden wall; the long shadow of a guard's staff falls across it.",
    expr="", comp="decree centre, diagonal shadow", cam="close-up, straight-on", cast=[])),
    ("A", "Yasağı çiğneyen")],
 "S030": [("A", ""), ("b", "suçluları bizzat", dict(
    action="The cloaked figure throws open the door: inside, three men freeze mid-sip with cups in the air and huge round eyes, lit by the lantern.",
    expr="men frozen in shock", comp="cloaked figure in the doorway left, men right", cam="medium shot", cast=["murad4", "bean_people"]))],
 "S032": [("b", "", dict(
    action="Murad IV walks past a house window where a cup steams on the sill and ignores it, pointing sternly at the boarded coffeehouse across the street.",
    expr="stern, focused on the coffeehouse", comp="window and cup left, Murad centre, coffeehouse right", cam="wide, eye level", cast=["murad4"], bg="Istanbul street from S028")),
    ("A", "Evde içmek")],
 "S034": [("b", "", dict(
    action="A deserted street of shuttered coffeehouses: dust blows, dry leaves roll, cobwebs on the doors, a single cat sits on a step.",
    expr="", comp="street vanishing to the centre", cam="wide, eye level", cast=[], bg="grey quiet Istanbul street")),
    ("c", "Murad öldükten", dict(
    action="Close portrait of Kâtip Çelebi dipping a reed pen into an inkwell, thoughtful.",
    expr="thoughtful, slightly melancholic", comp="face centre-left, inkwell lower right", cam="close-up")),
    ("A", "kahvehanelerin cahilin")],
 "S035": [("b", "", dict(
    action="An official tears an old blank decree off a wall while a man nearby happily lights a long tobacco pipe.",
    expr="cheerful relief", comp="torn decree left, pipe smoker right", cam="medium shot", cast=["osmanli_crowd"])),
    ("A", "ve kahvehaneler"),
    ("c", "Masa geri geldi", dict(
    action="The long wooden table is back inside the coffeehouse under a warm lamp; people sit down again, steam rises from cups; Fasulye sits at the far end, satisfied.",
    expr="content, small smile", comp="table along the lower third, Fasulye right end", cam="medium wide", bg="coffeehouse interior from S020"))],
 "S036": [("b", "", dict(
    action="A merchant sailing ship moored at a London quay on the Thames; porters unload coffee sacks into timber warehouses.",
    expr="", comp="ship left, quay and sacks right", cam="wide, eye level", bg="grey sky, river")),
    ("A", "Londra'da")],
 "S037": [("b", "", dict(
    action="Close-up of a small round hand dropping one plain copper penny (no markings) onto a wooden counter next to a steaming cup.",
    expr="", comp="coin mid-air at the centre, cup right", cam="extreme close-up", cast=[])),
    ("A", "istediğin kadar"),
    ("c", "Bu yüzden onlara", dict(
    action="Fasulye in a periwig stands at the coffeehouse table like a professor, pointing at a blank newspaper, while the others listen like students with their cups.",
    expr="Fasulye professorial, listeners attentive", comp="Fasulye standing right, listeners seated left", cam="medium shot"))],
 "S039": [("b", "", dict(
    action="Charles II at his desk presses his seal onto a large blank proclamation with a smug expression; a quill in an inkwell.",
    expr="smug, satisfied", comp="king centre, proclamation lower centre", cam="medium close-up", cast=["charles2"], bg="palace room from S038")),
    ("A", "Kahvehaneler on Ocak")],
 "S040": [("b", "", dict(
    action="Inside a thought-cloud vignette with a wavy ink border: lazy coffeehouse men slouch, one yawns with his feet on the table, one grumbles with crossed arms; a small Charles II at the lower corner imagines it.",
    expr="lazy, grumpy (as the king imagines)", comp="vignette fills upper two thirds, king lower left", cam="medium shot", cast=["london_crowd", "charles2"])),
    ("A", "hükümet hakkında")],
 "S041": [("A", ""), ("b", "hatta kralın kendi adamları", dict(
    action="Inside the palace, courtiers in fine wigs approach Charles II nervously, holding coffee cups and a long blank petition; one whispers in his ear.",
    expr="courtiers nervous, king irritated", comp="courtiers left, king right", cam="medium shot", cast=["charles2", "london_crowd"], bg="palace room from S038"))],
 "S042": [("A", ""), ("b", "sekiz Ocak", dict(
    action="Inside the London coffeehouse men cheer and clink cups; one throws his periwig in the air.",
    expr="jubilant", comp="group centre", cam="medium wide", cast=["london_crowd"], bg="coffeehouse interior from S037")),
    ("c", "Ferman ile geri adım", dict(
    action="Ten small blank paper sheets peel off a wall pad one by one and flutter away, symbolising ten days.",
    expr="", comp="pad left, sheets flying right", cam="medium shot", cast=[], bg="plain warm paper wall"))],
 "S043": [("b", "", dict(
    action="Establishing view of a rococo summer palace on a terraced hillside of vineyards, pale yellow walls, a single dome, sunny sky.",
    expr="", comp="palace upper centre, terraces below", cam="wide, low angle", cast=[], bg="blue-white sky")),
    ("A", "Büyük Friedrich")],
 "S044": [("b", "", dict(
    action="Carts loaded with coffee sacks roll across a border bridge into Prussia, driven by foreign merchants.",
    expr="", comp="carts moving left to right", cam="wide", cast=["bean_people"])),
    ("c", "ve kralın hesabına", dict(
    action="Frederick at his desk scribbles sums in a ledger (only wavy ink lines, no digits); a stack of coins beside him shrinks; he looks horrified.",
    expr="horrified, eyes wide", comp="Frederick centre, coin stack right", cam="medium close-up", bg="rococo study from S043")),
    ("A", "her yıl yüz binlerce")],
 "S045": [("b", "", dict(
    action="Frederick at a window looks down at townsfolk in the square, each holding a coffee cup; he sighs with a fist on his hip.",
    expr="exasperated", comp="Frederick left at window, crowd below right", cam="medium shot, high angle")),
    ("A", "Çözümü de hazır"),
    ("c", "Bir mektubunda", dict(
    action="Frederick writes a letter with a quill; a beer mug stands next to the inkwell; he smiles nostalgically.",
    expr="nostalgic smile", comp="Frederick centre, mug right", cam="medium close-up", cast=["frederick"], bg="rococo study from S043")),
    ("d", "Kral bira çorbasıyla", dict(
    action="A soft memory vignette with a cloudy ink border: young Frederick eats beer soup from a huge bowl with a big spoon, rosy cheeks.",
    expr="happy child", comp="boy and bowl centre", cam="medium shot", cast=["young_frederick"], bg="simple palace nursery"))],
 "S047": [("b", "", dict(
    action="A line of veterans in old blue uniforms marches out of a town gate into the street.",
    expr="proud, serious", comp="column marching toward the viewer", cam="wide, eye level", cast=["sniffer", "prussian_crowd"])),
    ("c", "Yaklaşık dört yüz", dict(
    action="A lineup of war veterans saluting: one with an eyepatch, one with a peg leg, one on a crutch, big moustaches, varied heights.",
    expr="stiff, proud", comp="row across the frame", cam="medium shot, straight-on", cast=["sniffer", "prussian_crowd"])),
    ("A", "Görevleri"),
    ("d", "Halk onlara", dict(
    action="Extreme close-up of a sniffer's huge nose following a curling ink smell trail that comes from a chimney; his eyes are closed in concentration; townsfolk peek and giggle behind.",
    expr="intense concentration, townsfolk amused", comp="nose centre, trail from upper right", cam="extreme close-up", cast=["sniffer", "prussian_crowd"]))],
 "S048": [("b", "", dict(
    action="Frederick's empty armchair with his tricorn hat on the seat and his cane leaning on it; the greyhound lies sadly beside it; a candle has just gone out with a thin smoke line.",
    expr="", comp="chair centre, dog lower right", cam="medium shot", cast=[], bg="rococo study from S043, dim")),
    ("c", "Kahve kuralları da", dict(
    action="Two clerks comically bury a big blank rulebook in a small garden hole with a shovel.",
    expr="clerks bored", comp="hole centre, clerks either side", cam="medium shot", cast=["prussian_crowd"], bg="small garden, daylight")),
    ("A", "onunla birlikte")],
 "S049": [("b", "", dict(
    action="Establishing view of snowy 18th-century Stockholm old town by the water: red and ochre houses, ships frozen at the quay.",
    expr="", comp="houses across the middle, frozen water below", cam="wide", cast=[], bg="grey winter sky, snow")),
    ("A", "Önce vergi"),
    ("c", "İsveç kahveyi tam beş", dict(
    action="Five blank decrees with red seals pinned over one another on a wooden wall; snow drifts; a Swedish man in a fur hat rolls his eyes.",
    expr="exasperated", comp="decrees left, man right", cam="medium shot", cast=["swedish_folk"]))],
 "S050": [("A", ""), ("b", "gizlice içmeye", dict(
    action="View from under the table: faces lit by a candle, cups clinking; Fasulye holds a finger to his lips.",
    expr="secretive, giggling", comp="faces in a semicircle, candle centre", cam="close-up, low angle"))],
 "S051": [("b", "", dict(
    action="A few Swedes read a blank decree pinned to a door and frown; one woman hugs a copper coffee pot protectively.",
    expr="annoyed, protective", comp="door left, people right", cam="medium shot", cast=["swedish_folk"], bg="snowy street")),
    ("A", "bazı İsveçliler")],
 "S052": [("b", "", dict(
    action="Fasulye opens a large old book; an ink drawing of a small crown and two cups rises from the pages like steam.",
    expr="storyteller's playful look", comp="book centre, Fasulye behind it", cam="medium close-up", cast=["fasulye"], costume="modern", bg="plain warm paper background")),
    ("c", "Kral Üçüncü Gustav", dict(
    action="Theatrical portrait of King Gustav III in a blue coat and powdered wig, one hand raised dramatically.",
    expr="theatrical, self-confident", comp="king centre", cam="medium shot, low angle", cast=["gustav3"], bg="palace curtain")),
    ("d", "idam mahkûmu", dict(
    action="The identical twins in plain grey prison clothes stand side by side and look at each other, puzzled.",
    expr="puzzled", comp="twins centre", cam="medium shot", cast=["twins"])),
    ("A", "Biri her gün")],
 "S053": [("b", "", dict(
    action="Two empty chairs with notebooks and spectacles left on them, a burnt-out candle (no bodies); the older twins are in the background with their cups.",
    expr="", comp="chairs foreground, twins background", cam="medium shot")),
    ("c", "sonra kral öldü", dict(
    action="Gustav III's crown resting on an empty velvet cushion tied with a black ribbon.",
    expr="", comp="crown centre", cam="close-up", cast=[], bg="dark curtain")),
    ("A", "İkizler hâlâ")],
 "S055": [("b", "", dict(
    action="1823, snowy Stockholm square: people cheer, someone pours coffee in the street, a torn blank decree lies on the snow.",
    expr="celebrating", comp="crowd centre, torn decree lower left", cam="wide", cast=["swedish_folk"], costume=None, bg="snowy square from S049")),
    ("A", "Bugün İsveç"),
    ("c", "en çok kahve içen", dict(
    action="Close-up of the fika table: many cups and cinnamon buns; a hand reaches for a refill; Fasulye looks content.",
    expr="content", comp="table top centre, Fasulye right", cam="close-up, high angle"))],
 "S056": [("b", "", dict(
    action="Classic Viennese coffeehouse interior: marble tables, bentwood chairs, chandeliers, blank newspapers on wooden holders; Fasulye sits with a cup.",
    expr="curious", comp="Fasulye centre-right, room depth left", cam="medium wide", cast=["fasulye", "modern_crowd"], costume="modern", bg="elegant warm interior")),
    ("c", "Anlatılan hikâyeye göre", dict(
    action="An old-engraving-style framed vignette: the walls of Vienna with tents outside, drawn like a fairy-tale picture-book page.",
    expr="", comp="city walls centre, tents around", cam="wide", cast=[], bg="ink border frame, parchment")),
    ("d", "Osmanlı ordusu", dict(
    action="Dawn: an army camp being abandoned, tents folding, carts and soldiers marching away in the distance (no weapons in use, no battle).",
    expr="", comp="column moving away to the horizon", cam="wide, high angle", cast=["janissary"])),
    ("e", "çuval çuval kahve", dict(
    action="Piles of abandoned coffee sacks under a tent, beans spilling; a curious Viennese soldier pokes one with a finger.",
    expr="puzzled curiosity", comp="sacks centre, soldier right", cam="medium close-up", cast=["vienna_crowd"])),
    ("A", "Kahraman casus")],
 "S058": [("b", "", dict(
    action="A stack of old official ledgers and one document with a large wax seal; the handwriting is only illegible wavy ink lines.",
    expr="", comp="sealed document centre", cam="close-up, high angle", cast=[], bg="wooden archive table")),
("A", "Ermeni tüccar")],
 "S059": [("A", ""), ("b", "Mekke'de toplantılar", dict(
    action="Hayır Bey seated at the long table glares sideways at a small group of men talking over cups in a little vignette beside him.",
    expr="suspicious glare", comp="Hayır Bey left, vignette right", cam="medium close-up", cast=["hayir_bey", "bean_people"])),
    ("c", "İstanbul'da isyan", dict(
    action="Murad IV seated at the long table, eyes darting nervously toward faint silhouettes of tall janissary caps on the wall.",
    expr="nervous, distrustful", comp="Murad left, silhouettes right", cam="medium close-up", cast=["murad4"])),
    ("d", "Londra'da dedikodu", dict(
    action="Charles II seated at the long table with swirling rumour ink lines circling his head.",
    expr="annoyed, overwhelmed", comp="king centre", cam="medium close-up", cast=["charles2"])),
    ("e", "Prusya'da para", dict(
    action="Frederick seated at the long table clutching his coin purse tightly to his chest.",
    expr="stingy, worried", comp="Frederick centre", cam="medium close-up", cast=["frederick"])),
    ("f", "Hiçbiri gerçekten", dict(
    action="Top-down extreme close-up of a cup of black coffee on the wooden table; its still surface reflects the hanging lamp; one small ripple.",
    expr="", comp="cup centred", cam="top-down extreme close-up", cast=[]))],
 "S060": [("A", ""), ("c", "konuşturması", dict(
    action="Late night at the long table: the candle is low, a moon in a window, everyone still wide awake with big round eyes; Fasulye pours another cup.",
    expr="wide-awake", comp="table across the frame, moon upper right", cam="medium wide")),
    ("d", "Ve bunu yasaklamaya", dict(
    action="Under the table: five small crumpled blank decrees lie on the floor in the lamp light while the feet of happy people tap around them.",
    expr="", comp="decrees centre on the floor", cam="low angle, close", cast=[]))],
 "S061": [("b", "", dict(
    action="Fasulye sits in the modern café sipping peacefully with his eyes closed.",
    expr="peaceful", comp="Fasulye centre-left, cup at the optical centre", cam="medium shot", cast=["fasulye"])),
    ("c", "biri sana ters ters", dict(
    action="Close-up of the bean person at the next table glaring with one eyebrow down and arms crossed.",
    expr="disapproving glare", comp="face right of centre", cam="close-up", cast=["modern_crowd"])),
    ("d", "sadece şunu söyle", dict(
    action="Fasulye leans slightly toward the viewer and raises one finger; in the steam above his cup faint ink silhouettes of a small turban and a crown appear (callback to S002).",
    expr="calm, dry smirk", comp="Fasulye centre, steam shapes upper right", cam="medium close-up", cast=["fasulye"])),
    ("A", "Krallar denedi.")],
}

def main():
    data = json.load(open(f"{V}/SCENES.json"))
    data["cast"].update(EXTRA_CAST)
    nar = {l.split("|")[0]: l.split("|", 1)[1].strip() for l in open(f"{V}/NARRATION.txt", encoding="utf-8") if l.startswith("L")}
    fr = json.load(open(f"{V}/kdenlive_frames_tr.json"))["tr"] if os.path.exists(f"{V}/kdenlive_frames_tr.json") else None
    timeline, prompts = [], []
    t_scene = 0.0
    for i, s in enumerate(data["scenes"]):
        dur = (fr[i][1] - fr[i][0]) / 30 if fr else s["est_dur"]
        text = " ".join(nar[l] for l in s["lines"])
        plan = SHOTS.get(s["id"], [("A", "")])
        # anlatımdaki karakter oranına göre başlangıç
        starts = []
        for k, (sid, cue, *_ ) in enumerate(plan):
            if k == 0: starts.append(0.0); continue
            pos = text.find(cue)
            assert pos > 0, (s["id"], sid, cue)
            starts.append(pos / len(text))
        assert starts == sorted(starts), s["id"]
        for k, (sid, cue, *rest) in enumerate(plan):
            a = t_scene + starts[k] * dur
            b = t_scene + (starts[k + 1] * dur if k + 1 < len(plan) else dur)
            shot_id = s["id"] if sid == "A" else s["id"] + sid
            frag = text[int(starts[k] * len(text)):int((starts[k + 1] if k + 1 < len(plan) else 1) * len(text))].strip()
            timeline.append({"shot": shot_id, "scene": s["id"], "new": sid != "A", "start": round(a, 2), "dur": round(b - a, 2),
                             "image": f"images/001_{shot_id}_vK.png" if sid != "A" else f"images/001_{s['id']}_vK.png (mevcut)",
                             "narration": frag})
            if sid != "A":
                f = rest[0]; sub = copy.deepcopy(s)
                sub.update(id=shot_id, action=f["action"], expression=f.get("expr", ""), composition=f["comp"], camera=f["cam"],
                           function=f"Extra shot inside {s['id']} so the picture changes every 2-3 s; illustrates: \"{frag}\"",
                           continuity=f"Same location, light, characters and costumes as {s['id']} — attach images/001_{s['id']}_vK.png as style/continuity reference. Must look clearly different in framing from {s['id']}.")
                if "cast" in f: sub["cast"] = f["cast"]
                if "costume" in f: sub["fasulye_costume"] = f["costume"]
                if "bg" in f: sub["background"] = f["bg"]
                if "fasulye" in sub["cast"] and not sub.get("fasulye_costume"):
                    sub["fasulye_costume"] = "modern"
                prompts.append((sub, frag, round(b - a, 1)))
        t_scene += dur
    json.dump({"video": "001", "lang": "tr", "note": "v2 çekim listesi: mevcut 61 sahne + ara çekimler. start/dur TR anlatıma göre yaklaşık (karakter oranı).",
               "shots": timeline}, open(f"{V}/SHOTS_v2.json", "w"), ensure_ascii=False, indent=1)
    L = ["# 001 · IMAGE_PROMPTS v2 · Ara çekimler (görüntü 2–3 sn'de bir değişsin)", "",
         "Neden: referans kanalda görüntü ortalama ~2 sn'de bir değişiyor; bizde sahne başına ~6,6 sn idi. "
         f"Bu dosya **{len(prompts)} yeni görsel** ekler; mevcut 61 sahne görseli aynen kalır. Toplam {len(timeline)} çekim, ortalama ≈ {t_scene/len(timeline):.1f} sn.", "",
         "ChatGPT için: önce `IMAGE_GENERATION_GUIDE.md` oku. Her bloğun **tamamını** kopyala (ilk 56 promptla aynı biçim). "
         "Her ara çekimde **ana sahnenin görselini** (`images/001_Sxxx_vK.png`) de referans olarak ekle: aynı yer, ışık ve kostüm; ama kadraj belirgin farklı olsun.",
         "Dosya adı: `001_{Sxxx}{harf}_v{K}.png` → `videos/001/images/`. Kurgu sırası ve süreler: `SHOTS_v2.json`. "
         "Daha kısa, elle yazılmış alternatif: `IMAGE_PROMPTS_v2_kisa.md`.", ""]
    for sub, frag, d in prompts:
        L += [f"## {sub['id']} — ara çekim · {sub['title']}", f"- **Dosya:** `001_{sub['id']}_v1.png`",
              f"- **Anlatım parçası:** {frag}", f"- **Süre:** ≈ {d} sn",
              "- **Referanslar:** " + ", ".join(f"`{r}`" for r in sub["references"] + [f"images/001_{sub['id'][:4]}_vK.png (ana sahne)"]),
              "", "```", build_prompt(sub, data, None), "```", ""]
    open(f"{V}/IMAGE_PROMPTS_v2.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(len(prompts), "yeni prompt;", len(timeline), "çekim; ort", round(t_scene / len(timeline), 2), "sn; toplam", round(t_scene, 2))

if __name__ == "__main__":
    main()
