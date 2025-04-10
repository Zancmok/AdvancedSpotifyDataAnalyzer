# POSLOVNI DEL

## Problem
- Zaradi varnosti podatkov ne obastaja natančna in napredna  analiza podatkov spotify zgodovine
- Ni skupinske analize spotify podatkov, analize podatkov večih ljudi na enkrat

## Rešitev
- Rešitev je v tem, da vsak uporabnik dobi možnost, da samostojno odloči, kateri podatki so dostopni drugim uporabnikom. Poleg tega lahko uporabnik omogoči, da so vsi njegovi podatki vidni vsem, če to želi.

## Cilnja skupina
- Uporabniki aplikacije Spotify

## Zakaj je drugačna
- Ni konkurence ki bi omogočala tako napredno analizo podatkov in skupinsko analizo podatkov

# Analiza trga

## Velikost trga
- Na celem svetu je približno 675 milijonov uporabnikov spotifya

- Predvidevava, da bi 20%  od 675 milijonov uporabnikov (135 milijonov), lahko bilo zainteresiranih za te podatke.

## Konkurenčna analiza

|       Ime           |                 Prednosti                            |               Slabosti                 |                   Naša raazlika               |
|---------------------|------------------------------------------------------|----------------------------------------|-----------------------------------------------|
| statsforspotify.com | za uporabo dovolj zgolj prijava s Spotify računom    | Nenatančni,nepopolni,omejeni podatki   | Vse kar manjka ostalim +večuporabniška analiza|
| volt.fm             | za uporabo dovolj zgolj prijava s Spotify računom    | Nenatančni,nepopolni,omejeni podatki   | Vse kar manjka ostalim +večuporabniška analiza|
| Trackify.am         | za uporabo dovolj zgolj prijava s Spotify računom    | Nenatančni,nepopolni,omejeni podatki   | Vse kar manjka ostalim +večuporabniška analiza|

# SWOT analiza

| Prednosti |   
|-----------|
| Večja fleksibilnost: Ker ne uporabljamo uradnega API-ja, imamo večjo svobodo pri prilagajanju analize, brez omejitev, ki jih postavlja Spotify.    | 
| Neodvisnost od sprememb API-ja: Ker ne uporabljaš uradnega API-ja, ni tveganja, da bi spremembe v Spotify API-ju vplivale na tvoje delovanje.    |
| Potencial za inovacije: Zbiranje podatkov iz različnih virov omogoča ustvarjanje novih in edinstvenih analiz, ki jih uradni API morda ne omogoča.    |

| Slabosti |
|-----------|
| Omejen dostop do podatkov: Brez uradnega API-ja lahko naletiš na težave pri pridobivanju podatkov, saj je lahko zbiranje podatkov iz drugih virov (npr. spletno strganje) težavno ali omejeno.    | 
| Težave pri zagotavljanju natančnosti podatkov: Zbiranje podatkov iz neformalnih virov lahko pomeni manjšo zanesljivost in natančnost podatkov v primerjavi z uradnim API-jem.   |
| Večja kompleksnost pri pridobivanju podatkov: Postopek za zbiranje podatkov lahko zahteva napredno tehnično znanje, kot so metode spletnega strganja (web scraping), API-ji drugih tretjih oseb itd    |

| Priložnosti |
|-----------|
| Razširjena uporaba podatkov iz drugih virov: Lahko integriraš podatke iz drugih virov (npr. YouTube, Apple Music), da ponudiš širše in bolj celovite analize glasbenih trendov.    | 
|Večja prilagodljivost za uporabnike: Možnost prilagoditve funkcionalnosti glede na specifične potrebe uporabnikov, brez omejitev, ki jih nalaga uradni API.    |
|  Možnost partnerstev z drugimi platformami: Povezovanje z drugimi storitvami za analizo glasbe, trženje ali umetnike, ki iščejo bolj prilagojene analize.   |

| Grožnje   |
|-----------|
|  Pravne težave: Zbiranje podatkov brez uradnega dovoljenja (npr. spletno strganje) lahko pripelje do pravnih težav ali blokad dostopa do podatkovnih virov.    | 
| Težave pri obvladovanju velikih količin podatkov: Zbiranje in obdelava podatkov iz več virov lahko postane težavno, če se količina podatkov povečuje, kar zahteva naprednejše tehnike za obvladovanje podatkov.    |
| Zmanjšanje dostopa do podatkov: Povečana regulacija spletnih podatkov ali spremembe na spletnih platformah (npr. blokiranje spletnega strganja) lahko vplivajo na zmožnost pridobivanja podatkov.    |

### Strategije na podlagi SWOT:
- S-O strategija:
    - Fleksibilnost in inovativni pristop za integracijo dodatnih virov, kot sta YouTube in Apple Music, je odlična priložnost za širitev funkcionalnosti in dosego širše ciljne skupine. To bi omogočilo edinstvene možnosti, ki jih konkurenca morda nima.

    - Neodvisnost od API-ja daje veliko prednost, saj omogoča hitrejšo prilagodljivost. V primeru hitrih sprememb v potrebah uporabnikov je to lahko odločilna prednost.
- W-O strategija:
    - Sistem za validacijo in preverjanje točnosti podatkov je ključnega pomena za izboljšanje zanesljivosti. To bo zmanjšalo tveganje napačnih informacij in izboljšalo uporabniško izkušnjo.

    - Partnerstva z drugimi platformami za dostop do boljših podatkov je zelo dobra priložnost za izboljšanje kakovosti virov in zmanjšanje odvisnosti od lastnih metod zbiranja.

- S-T strategija:
    - Inovativni pristopi in tehnična prilagodljivost so odlični za razvoj mehanizmov, ki se bodo lahko hitro prilagajali spremembam v spletnih platformah (npr. spremembam v anti-scraping politikah).

    - Svoboda za hitro razvijanje alternativnih metod zbiranja podatkov v primeru blokad je zelo pomembna, saj lahko to zmanjša vpliv morebitnih težav z dostopnostjo podatkov.
- W-T strategija:
    - Investiranje v pravno podporo in transparentno politiko uporabe podatkov je nujno, saj lahko pomaga pri preprečevanju pravnih težav, če se pojavijo spremembe v regulativah ali pritožbe uporabnikov.

    - Modularna struktura sistema omogoča hitro prilagajanje, kar je koristno v primeru, da pride do sprememb na posameznih virih. To omogoča fleksibilnost, da hitro reagiraš na grožnje.

# Poslovni model in osnovni finančni plan

## Viri prihodkov
- Osnovna aplikacija je brezplačna  
    - Omogoča osnovno individualno analizo poslušanja prek enostavne prijave s Spotify računom.

- Reklame na spletni strani

## Struktura stroškov:

- Začetni razvoj: 200€  
  - Minimalna izvedljiva verzija (MVP), večina dela opravljena s strani ustanoviteljev (razvoj, UI/UX, povezava z API-ji). 

- Mesečno vzdrževanje: 80€  
  - Gostovanje, baze podatkov, posodobitve, osnovna tehnična podpora.

## Strategija pridobivanja uporabnikov:

- Influencerji na področju glasbe in statistike  
  - YouTuberji in TikTokerji, ki delajo vsebine o Spotify Wrapped, glasbenih okusih itd.

- Kampanja “povabi prijatelja”  
  - Uporabnik in prijatelj dobita 1 mesec Premium članstva, če se prijatelj registrira in poveže Spotify račun.