#!/usr/bin/env python3
"""
Generator voor de Smylee-locatiepagina's ("tanden bleken <stad>").
Draai:  python3 generate_locations.py
Genereert per stad een losse, on-brand landingspagina en schrijft
daarnaast sitemap.xml + llms.txt bij. Niet bedoeld voor de Pages-deploy
(staat in .assetsignore).
"""
import json, os, html
from datetime import date

BASE = "https://www.smyleetandenbleker.nl"
BOOK = "https://smylee.rocketplanner.nl/boeken/services?vestiging=1cfe002f-52ed-4d8a-9459-fada85aa1c4d"
WA = "https://wa.me/31616863387"
TEL = "+31616863387"
TEL_LINK = "tel:+31616863387"
MAIL = "smyleetandenbleker@gmail.com"
ADDR = "Dorpsstraat 57, 6661 EG Elst (Gld)"
ADDR_STREET = "Dorpsstraat 57"
ADDR_ZIP = "6661 EG"
ADDR_CITY = "Elst"
ADDR_REGION = "Gelderland"
GEO = "51.9196, 5.8486"
MAPS_QUERY = "Dorpsstraat+57+6661+EG+Elst"
TODAY = date.today().isoformat()

PRICES = [
    ("Fresh Smile", "3 × 20 min · 1 afspraak", "€64,95", "", "Bij lichte verkleuring", "Ideaal om mee te starten"),
    ("Bright Smile", "5 × 20 min · 1 afspraak", "€84,95", "€149,95", "Bij gemiddelde verkleuring", "Professionele whitening-formule"),
    ("Diamond Smile", "7 × 20 min · 2 afspraken (4 + 3)", "€99,95", "€199,90", "Bij duidelijke of hardnekkige verkleuring", "Helder en egaal wit"),
    ("Hollywood Smile", "10 × 20 min · 2 afspraken (5 + 5)", "€149,95", "€299,90", "Bij sterke verkleuring", "Perfect voor bruiloft, event of fotoshoot"),
]

# Echte reistijden (OSRM, centrum -> Dorpsstraat 57 Elst), geverifieerd 2026-10-22.
CITIES = [
    {
        "slug": "tanden-bleken-arnhem",
        "city": "Arnhem",
        "min": 20, "km": 13,
        "meta": "Tanden bleken in Arnhem? Bij Smylee in Elst, ±20 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Arnhem doe je bij Smylee Whitening Studio in Elst, op ongeveer 20 minuten rijden van het centrum van Arnhem. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit het centrum van Arnhem rijd je via de A325 richting Nijmegen en neem je de afslag Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, precies tussen Arnhem en Nijmegen. Ook vanuit Arnhem-Zuid, Schuytgraaf en Oosterbeek ben je er in ongeveer een kwartier.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Arnhem?", "Vlakbij Arnhem, bij Smylee Whitening Studio in Elst. Vanaf het centrum van Arnhem ben je er in ongeveer 20 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Arnhem naar Smylee?", "Vanuit het centrum van Arnhem is het ongeveer 20 minuten rijden (zo'n 13 kilometer) via de A325 richting Nijmegen. Ook met de trein stap je uit op station Elst, op loopafstand van de studio."),
            ("Wat kost tanden bleken voor klanten uit Arnhem?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
    {
        "slug": "tanden-bleken-nijmegen",
        "city": "Nijmegen",
        "min": 15, "km": 10,
        "meta": "Tanden bleken in Nijmegen? Bij Smylee in Elst, ±15 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Nijmegen doe je bij Smylee Whitening Studio in Elst, op ongeveer 15 minuten rijden van het centrum van Nijmegen. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Nijmegen rijd je via de A325 richting Arnhem en neem je de afslag Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, precies tussen Nijmegen en Arnhem. Ook vanuit Lent, Nijmegen-Noord en Oosterhout ben je er in een kwartiertje.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Vanaf Nijmegen is het een korte rit over de A325.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Nijmegen?", "Vlakbij Nijmegen, bij Smylee Whitening Studio in Elst. Vanaf het centrum van Nijmegen ben je er in ongeveer 15 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Nijmegen naar Smylee?", "Vanuit het centrum van Nijmegen is het ongeveer 15 minuten rijden (zo'n 10 kilometer) via de A325 richting Arnhem. Ook met de trein stap je uit op station Elst, op loopafstand van de studio."),
            ("Wat kost tanden bleken voor klanten uit Nijmegen?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
    {
        "slug": "tanden-bleken-bemmel",
        "city": "Bemmel",
        "min": 11, "km": 8,
        "meta": "Tanden bleken in Bemmel? Bij Smylee in Elst, ±11 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Bemmel doe je bij Smylee Whitening Studio in Elst, op ongeveer 11 minuten rijden van Bemmel. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Bemmel rijd je via de N839 richting Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, vlakbij Bemmel in de Betuwe. Vanuit Bemmel en de rest van Lingewaard ben je er in een klein kwartier.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Bemmel?", "Vlakbij Bemmel, bij Smylee Whitening Studio in Elst. Vanaf Bemmel ben je er in ongeveer 11 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Bemmel naar Smylee?", "Vanuit Bemmel is het ongeveer 11 minuten rijden (zo'n 8 kilometer). Je rijdt via de N839 richting Elst."),
            ("Wat kost tanden bleken voor klanten uit Bemmel?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
    {
        "slug": "tanden-bleken-huissen",
        "city": "Huissen",
        "min": 14, "km": 12,
        "meta": "Tanden bleken in Huissen? Bij Smylee in Elst, ±14 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Huissen doe je bij Smylee Whitening Studio in Elst, op ongeveer 14 minuten rijden van Huissen. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Huissen rijd je richting Bemmel en vervolgens via de N839 naar Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57.",
        "why": [
            "Smylee ligt in Elst, vlakbij Huissen in de Betuwe. Vanuit Huissen en de rest van Lingewaard ben je er in een klein kwartier.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Huissen?", "Vlakbij Huissen, bij Smylee Whitening Studio in Elst. Vanaf Huissen ben je er in ongeveer 14 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Huissen naar Smylee?", "Vanuit Huissen is het ongeveer 14 minuten rijden (zo'n 12 kilometer). Je rijdt richting Bemmel en daarna via de N839 naar Elst."),
            ("Wat kost tanden bleken voor klanten uit Huissen?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
    {
        "slug": "tanden-bleken-driel",
        "city": "Driel",
        "min": 8, "km": 6,
        "meta": "Tanden bleken in Driel? Bij Smylee in Elst, ±8 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Driel doe je bij Smylee Whitening Studio in Elst, op ongeveer 8 minuten rijden van Driel. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Driel rijd je in zuidelijke richting naar Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, op een paar minuten rijden van Driel. Vanuit Driel, Heteren en Randwijk ben je er het snelst van de hele regio.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Driel?", "Vlakbij Driel, bij Smylee Whitening Studio in Elst. Vanaf Driel ben je er in ongeveer 8 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Driel naar Smylee?", "Vanuit Driel is het ongeveer 8 minuten rijden (zo'n 6 kilometer) in zuidelijke richting naar Elst."),
            ("Wat kost tanden bleken voor klanten uit Driel?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
    {
        "slug": "tanden-bleken-zetten",
        "city": "Zetten",
        "min": 14, "km": 14,
        "meta": "Tanden bleken in Zetten? Bij Smylee in Elst, ±14 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Zetten doe je bij Smylee Whitening Studio in Elst, op ongeveer 14 minuten rijden van Zetten. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Zetten rijd je via de N836 richting Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, op een klein kwartier rijden van Zetten. Vanuit Zetten, Andelst en Herveld ben je er zo.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Zetten?", "Vlakbij Zetten, bij Smylee Whitening Studio in Elst. Vanaf Zetten ben je er in ongeveer 14 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Zetten naar Smylee?", "Vanuit Zetten is het ongeveer 14 minuten rijden (zo'n 14 kilometer). Je rijdt via de N836 richting Elst."),
            ("Wat kost tanden bleken voor klanten uit Zetten?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },

    {
        "slug": "tanden-bleken-wageningen",
        "city": "Wageningen",
        "min": 20, "km": 19,
        "meta": "Tanden bleken in Wageningen? Bij Smylee in Elst, ±20 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Wageningen doe je bij Smylee Whitening Studio in Elst, op ongeveer 20 minuten rijden van Wageningen. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Wageningen rijd je via de N837 en de A15 richting Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, op een klein halfuur rijden van Wageningen. Ook vanuit Renkum, Heelsum en Bennekom ben je er snel.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Wageningen?", "Vlakbij Wageningen, bij Smylee Whitening Studio in Elst. Vanaf Wageningen ben je er in ongeveer 20 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Wageningen naar Smylee?", "Vanuit Wageningen is het ongeveer 20 minuten rijden (zo'n 19 kilometer). Je rijdt via de N837 en de A15 richting Elst."),
            ("Wat kost tanden bleken voor klanten uit Wageningen?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
    {
        "slug": "tanden-bleken-lent",
        "city": "Lent",
        "min": 11, "km": 8,
        "meta": "Tanden bleken in Lent? Bij Smylee in Elst, ±11 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Lent doe je bij Smylee Whitening Studio in Elst, op ongeveer 11 minuten rijden van Lent. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Lent rijd je via de A325 richting Arnhem en neem je de afslag Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, vlakbij Lent en Nijmegen-Noord. Vanuit Lent ben je er in een klein kwartier.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Lent?", "Vlakbij Lent, bij Smylee Whitening Studio in Elst. Vanaf Lent ben je er in ongeveer 11 minuten met de auto. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Lent naar Smylee?", "Vanuit Lent is het ongeveer 11 minuten rijden (zo'n 8 kilometer). Je rijdt via de A325 richting Arnhem en neemt de afslag Elst."),
            ("Wat kost tanden bleken voor klanten uit Lent?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },

    {
        "slug": "tanden-bleken-veenendaal",
        "city": "Veenendaal",
        "min": 35, "km": 36,
        "meta": "Tanden bleken in Veenendaal? Bij Smylee in Elst, ±35 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Veenendaal doe je bij Smylee Whitening Studio in Elst, op ongeveer 35 minuten rijden van Veenendaal. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Veenendaal rijd je via de A12 richting Arnhem en daarna via de A15 richting Nijmegen. Neem de afslag Elst; in het dorpscentrum vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, tussen Arnhem en Nijmegen. Vanuit Veenendaal combineer je het makkelijk met een bezoek aan Arnhem of Nijmegen.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Veenendaal?", "Bij Smylee Whitening Studio in Elst, op ongeveer 35 minuten rijden van Veenendaal. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Veenendaal naar Smylee?", "Vanuit Veenendaal is het ongeveer 35 minuten rijden (zo'n 36 kilometer). Je rijdt via de A12 richting Arnhem en daarna via de A15 richting Nijmegen."),
            ("Wat kost tanden bleken voor klanten uit Veenendaal?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
    {
        "slug": "tanden-bleken-tiel",
        "city": "Tiel",
        "min": 31, "km": 35,
        "meta": "Tanden bleken in Tiel? Bij Smylee in Elst, ±31 min rijden. Non-peroxide gel en LED-licht, vanaf €64,95. Betaal pas na de behandeling.",
        "intro": "Tanden bleken in Tiel doe je bij Smylee Whitening Studio in Elst, op ongeveer 31 minuten rijden van Tiel. Je bleekt met een milde non-peroxide formule en LED-licht, in sessies van 20 minuten, en je betaalt pas na de behandeling.",
        "route": "Vanuit Tiel rijd je via de A15 richting Arnhem en neem je de afslag Elst. In het dorpscentrum van Elst vind je Smylee aan de Dorpsstraat 57, met parkeergelegenheid in de buurt.",
        "why": [
            "Smylee ligt in Elst, tussen Arnhem en Nijmegen. Vanuit Tiel ben je er in een halfuur, langs de A15.",
            "Je boekt eenvoudig online en betaalt pas na de behandeling. Rondom de studio kun je gemakkelijk parkeren.",
        ],
        "faq": [
            ("Waar kan ik mijn tanden laten bleken in Tiel?", "Bij Smylee Whitening Studio in Elst, op ongeveer 31 minuten rijden van Tiel. We bleken met een non-peroxide formule en LED-licht, in sessies van 20 minuten."),
            ("Hoe lang ben ik onderweg van Tiel naar Smylee?", "Vanuit Tiel is het ongeveer 31 minuten rijden (zo'n 35 kilometer). Je rijdt via de A15 richting Arnhem en neemt de afslag Elst."),
            ("Wat kost tanden bleken voor klanten uit Tiel?", "Dezelfde prijzen als voor al onze klanten: Fresh Smile €64,95, Bright Smile €84,95, Diamond Smile €99,95 en Hollywood Smile €149,95. Je betaalt pas na de behandeling, met pin."),
        ],
    },
]

CSS = """
:root{--bg:#FBF8F3;--ink:#1F1C19;--muted:#6B635A;--line:#E9E0D2;--gold:#8C6A3C;--gold-deep:#B08D57;--gold-light:#C9A46C;--surface:#FFFFFF;--soft:#F4EEE4}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.7 "Montserrat",system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
@font-face{font-family:"Playfair Display";src:url(/assets/playfair.woff) format("woff");font-weight:400 600;font-style:normal;font-display:swap}
@font-face{font-family:"Montserrat";src:url(/assets/montserrat.woff) format("woff");font-weight:400 700;font-style:normal;font-display:swap}
a{color:inherit}
img{max-width:100%;display:block}
h1,h2,h3{font-family:"Playfair Display",Georgia,serif;font-weight:400;line-height:1.12;margin:0 0 .5em}
h1{font-size:clamp(34px,5vw,52px)}
h2{font-size:clamp(26px,3.6vw,38px)}
h3{font-size:20px;font-weight:500}
p{margin:0 0 1em}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
section{padding:64px 0}
.eyebrow{font:600 12px/1 "Montserrat",sans-serif;letter-spacing:.3em;text-transform:uppercase;color:var(--gold)}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 26px;border-radius:999px;font:600 13px "Montserrat",sans-serif;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;border:1.5px solid transparent;cursor:pointer}
.btn-gold{background:var(--gold);color:#fff}
.btn-ghost{border-color:var(--gold);color:var(--ink);background:transparent}
.btn:hover{transform:translateY(-1px);filter:brightness(1.04)}
header.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;height:72px}
.brand img{height:46px;width:auto}
.breadcrumb{font:500 13px "Montserrat",sans-serif;color:var(--muted);margin:0 0 6px}
.breadcrumb a{color:var(--gold);text-decoration:none}
.hero{background:linear-gradient(160deg,var(--soft),var(--bg));border-bottom:1px solid var(--line);padding:56px 0 48px}
.hero .eyebrow{display:block;margin-bottom:14px}
.lede{color:var(--muted);font-size:18px;max-width:62ch}
.hero-cta{display:flex;gap:14px;flex-wrap:wrap;margin-top:22px}
.usps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:28px}
.usp{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px}
.usp b{display:block;font:600 14px "Montserrat",sans-serif;margin-bottom:4px}
.usp span{color:var(--muted);font-size:14px}
.route{display:grid;grid-template-columns:1.2fr .8fr;gap:32px;align-items:start}
.route .card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:26px}
.route .card b{font:600 15px "Montserrat",sans-serif}
.route .facts{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.route .fact{background:var(--soft);border-radius:12px;padding:14px;text-align:center}
.route .fact b{display:block;font:600 24px "Playfair Display",serif;color:var(--gold)}
.route .fact span{font-size:13px;color:var(--muted)}
.packs{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}
.pack{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:24px;display:flex;flex-direction:column;gap:8px}
.pack h3{margin:0}
.pack .meta{font-size:13px;color:var(--muted)}
.pack ul{list-style:none;padding:0;margin:0 0 6px;font-size:14px;color:var(--muted)}
.pack ul li{padding-left:18px;position:relative}
.pack ul li::before{content:"\u2726";position:absolute;left:0;color:var(--gold)}
.pack .price{font:400 30px "Playfair Display",serif;margin:0}
.pack .deal{font-size:13px;color:var(--muted)}
.pack .deal s{color:#b9a88e}
.pack .deal b{color:var(--gold)}
.pack.fav{border:2px solid var(--gold)}
.pill{display:inline-block;background:var(--gold);color:#fff;font:600 11px "Montserrat",sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:4px 12px;border-radius:999px;align-self:flex-start}
.note{font-size:13px;color:var(--muted)}
.faq details{border-bottom:1px solid var(--line);padding:14px 0}
.faq summary{cursor:pointer;font:600 16px "Montserrat",sans-serif;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--gold);font-size:22px;line-height:1}
.faq details[open] summary::after{content:"\u2212"}
.faq details p{color:var(--muted);margin:12px 0 0}
.contact{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:24px}
.contact .card{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:24px}
.contact .card h3{margin-bottom:8px}
.contact .card p{color:var(--muted);font-size:15px}
.contact a.link{color:var(--gold);text-decoration:none;font-weight:600}
.other-locations{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.other-locations a{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:8px 16px;font:500 13px "Montserrat",sans-serif;text-decoration:none;color:var(--ink)}
.other-locations a:hover{border-color:var(--gold);color:var(--gold)}
footer{background:var(--ink);color:#F6F1E9;padding:48px 0;margin-top:32px}
footer a{color:#F6F1E9;text-decoration:none;display:inline-block;margin:3px 0;font-size:14px}
footer a:hover{color:var(--gold-light)}
footer .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:28px}
footer h3{font:600 12px "Montserrat",sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-light);margin-bottom:12px}
footer .fine{color:rgba(246,241,233,.6);font-size:12px;margin-top:28px}
@media(max-width:760px){.route{grid-template-columns:1fr}.route .facts{grid-template-columns:1fr 1fr}.hero-cta{flex-direction:column}}
"""

HEAD_TMPL = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Smylee Whitening Studio">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/og-image.jpg">
<link rel="alternate" hreflang="nl-NL" href="{url}">
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<script type="application/ld+json">{jsonld}</script>
<style>{css}</style>
</head>
<body>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{BASE}/" aria-label="Smylee Whitening Studio, naar home"><img src="/assets/logo_light.png" alt="Smylee Whitening Studio"></a>
    <a class="btn btn-gold" href="{BOOK}" target="_blank" rel="noopener">Afspraak maken</a>
  </div>
</header>
<main>
"""

FOOT_TMPL = """
</main>
<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <h3>Smylee Whitening Studio</h3>
        <p style="margin:0;font-size:14px">{addr}</p>
        <p style="margin:0;font-size:14px"><a href="{TEL_LINK}">06 16 86 33 87</a></p>
        <p style="margin:0;font-size:14px"><a href="mailto:{MAIL}">smyleetandenbleker@gmail.com</a></p>
      </div>
      <div>
        <h3>Tanden bleken in de regio</h3>
        {location_links}
      </div>
      <div>
        <h3>Studio</h3>
        <a href="{BASE}/#prijzen">Prijzen</a><br>
        <a href="{BASE}/#resultaten">Resultaten</a><br>
        <a href="{BASE}/#faq">Veelgestelde vragen</a><br>
        <a href="https://www.instagram.com/smyleetandenbleker/" target="_blank" rel="noopener">Instagram</a>
      </div>
      <div>
        <h3>Informatie</h3>
        <a href="{BASE}/algemene-voorwaarden/">Algemene voorwaarden</a><br>
        <a href="{BASE}/privacybeleid/">Privacybeleid</a><br>
        <a href="{BASE}/cookiebeleid/">Cookiebeleid</a>
      </div>
    </div>
    <p class="fine">© 2026 Smylee Whitening Studio · Dorpsstraat 57, Elst (Gld) · Laatst bijgewerkt: {today}</p>
  </div>
</footer>
</body>
</html>
"""


def json_ld(city):
    slug = city["slug"]
    url = f"{BASE}/{slug}/"
    graph = [
        {
            "@type": "Organization",
            "@id": f"{BASE}/#org",
            "name": "Smylee Whitening Studio",
            "alternateName": "Smylee",
            "url": f"{BASE}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/logo_light.png"},
            "address": {
                "@type": "PostalAddress",
                "streetAddress": ADDR_STREET,
                "postalCode": ADDR_ZIP,
                "addressLocality": ADDR_CITY,
                "addressRegion": ADDR_REGION,
                "addressCountry": "NL",
            },
            "telephone": TEL,
            "email": MAIL,
            "sameAs": [
                "https://www.instagram.com/smyleetandenbleker/",
                "https://www.facebook.com/Smylee.nl/",
            ],
        },
        {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": f"Tanden bleken in {city['city']}",
            "serviceType": "Tanden bleken",
            "provider": {"@id": f"{BASE}/#org"},
            "areaServed": {"@type": "City", "name": city["city"]},
            "description": city["meta"],
            "offers": {
                "@type": "Offer",
                "priceCurrency": "EUR",
                "lowPrice": "64.95",
                "highPrice": "149.95",
                "url": f"{BASE}/#prijzen",
            },
        },
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": city["title"],
            "description": city["meta"],
            "inLanguage": "nl-NL",
            "isPartOf": {"@id": f"{BASE}/#website"},
            "about": {"@id": f"{url}#service"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": f"Tanden bleken in {city['city']}", "item": url},
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def faq_html(city):
    out = []
    for q, a in city["faq"]:
        out.append(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>')
    return "\n".join(out)


def location_links(current_slug):
    items = []
    for c in CITIES:
        if c["slug"] == current_slug:
            items.append(f'<a href="{BASE}/{c["slug"]}/" style="color:var(--gold-light);font-weight:600">{c["city"]}</a>')
        else:
            items.append(f'<a href="{BASE}/{c["slug"]}/">{c["city"]}</a>')
    return "<br>".join(items)


def price_cards():
    out = []
    for i, (name, meta, price, was, *bullets) in enumerate(PRICES):
        fav = name == "Diamond Smile"
        pill = '<span class="pill">Meest gekozen</span>' if fav else ""
        deal = ""
        if was:
            pct = {"Bright Smile": "43", "Diamond Smile": "50", "Hollywood Smile": "50"}.get(name, "50")
            deal = f'<p class="deal"><s>{was}</s> <b>−{pct}%</b></p>'
        lis = "".join(f"<li>{html.escape(b)}</li>" for b in bullets)
        cls = "pack fav" if fav else "pack"
        out.append(
            f'<article class="{cls}">{pill}<h3>{name}</h3><p class="meta">{meta}</p><ul>{lis}</ul>'
            f'<p class="price">{price}</p>{deal}'
            f'<a class="btn btn-ghost" href="{BOOK}" target="_blank" rel="noopener">Boek {name}</a></article>'
        )
    return "\n".join(out)


def render(city):
    city = dict(city)
    city.setdefault("title", f"Tanden bleken in {city['city']} | Smylee Whitening Studio")
    city.setdefault("h1", f"Tanden bleken in {city['city']}")
    url = f"{BASE}/{city['slug']}/"
    body = []
    body.append(f'<section class="hero"><div class="wrap">')
    body.append('<nav class="breadcrumb" aria-label="Kruimelpad"><a href="' + BASE + '/">Home</a> › Tanden bleken in ' + city["city"] + "</nav>")
    body.append(f'<span class="eyebrow">Smylee Whitening Studio · Elst</span>')
    body.append(f"<h1>{city['h1']}</h1>")
    body.append(f'<p class="lede">{html.escape(city["intro"])}</p>')
    body.append(f'<div class="hero-cta"><a class="btn btn-gold" href="{BOOK}" target="_blank" rel="noopener">Maak een afspraak</a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp ons</a></div>')
    body.append('<div class="usps">')
    body.append('<div class="usp"><b>Non-peroxide formule</b><span>Mild voor glazuur en tandvlees</span></div>')
    body.append('<div class="usp"><b>LED-licht</b><span>Sessies van 20 minuten</span></div>')
    body.append(f'<div class="usp"><b>Vanaf €64,95</b><span>Je betaalt pas na de behandeling</span></div>')
    body.append(f'<div class="usp"><b>± {city["min"]} min rijden</b><span>Vanuit {city["city"]} naar Elst</span></div>')
    body.append("</div></div></section>")

    # Route
    body.append('<section id="route"><div class="wrap"><h2>Zo rijd je vanuit ' + city["city"] + "</h2>")
    body.append('<div class="route"><div class="card">')
    body.append(f"<p>{html.escape(city['route'])}</p>")
    body.append(f'<p><a class="link" href="https://www.google.com/maps/dir/?api=1&origin={city["city"]}+Gelderland&destination={MAPS_QUERY}" target="_blank" rel="noopener">Open de route in Google Maps →</a></p>')
    body.append("</div>")
    body.append('<div class="facts">')
    body.append(f'<div class="fact"><b>± {city["min"]} min</b><span>met de auto</span></div>')
    body.append(f'<div class="fact"><b>± {city["km"]} km</b><span>naar de studio</span></div>')
    body.append('<div class="fact"><b>€64,95</b><span>vanaf-prijs</span></div>')
    body.append('<div class="fact"><b>Achteraf</b><span>betalen met pin</span></div>')
    body.append("</div></div></div></section>")

    # Prijzen
    body.append('<section id="prijzen" style="background:var(--soft)"><div class="wrap">')
    body.append('<span class="eyebrow">Prijzen</span>')
    body.append("<h2>Wat kost tanden bleken?</h2>")
    body.append('<p class="lede" style="margin-bottom:26px">Dezelfde pakketten en prijzen voor klanten uit ' + city["city"] + " en de hele regio. Geen verborgen kosten, je betaalt pas na de behandeling.</p>")
    body.append('<div class="packs">' + price_cards() + "</div>")
    body.append('<p class="note" style="margin-top:18px">Prijzen inclusief btw. Doorgestreepte prijzen zijn de normale prijzen. Resultaten verschillen per persoon. Terugkerende klant? <a class="link" href="' + BASE + '/#smyle-refresh">Smyle Refresh</a> is €50.</p>')
    body.append("</div></section>")

    # Why
    body.append('<section id="waarom"><div class="wrap">')
    body.append(f"<h2>Waarom vanuit {city['city']} naar Smylee?</h2>")
    body.append('<div class="route" style="margin-top:20px"><div class="card"><ul style="margin:0;padding-left:0;list-style:none;display:grid;gap:14px">')
    for w in city["why"]:
        body.append(f'<li style="padding-left:22px;position:relative;color:var(--muted)"><span style="position:absolute;left:0;color:var(--gold)">✦</span>{html.escape(w)}</li>')
    body.append("</ul></div>")
    body.append('<div class="card"><b>Onze studio</b><p style="margin-top:10px">' + ADDR + '<br>Ma 12:00–19:00 · di t/m za 10:00–19:00 · zo gesloten<br>Telefoon/WhatsApp: <a class="link" href="' + TEL_LINK + '">06 16 86 33 87</a></p></div>')
    body.append("</div></div></section>")

    # FAQ
    body.append('<section id="faq"><div class="wrap">')
    body.append('<span class="eyebrow">Veelgestelde vragen</span>')
    body.append(f"<h2>Tanden bleken in {city['city']}: veelgestelde vragen</h2>")
    body.append('<div class="faq" style="margin-top:20px">' + faq_html(city) + "</div>")
    body.append("</div></section>")

    # Contact CTA
    body.append('<section id="contact" style="background:var(--ink);color:#F6F1E9;text-align:center"><div class="wrap">')
    body.append(f"<h2 style='color:#F6F1E9'>Klaar voor een stralende glimlach vanuit {city['city']}?</h2>")
    body.append('<p class="lede" style="color:rgba(246,241,233,.72);margin:0 auto 24px;max-width:52ch">Boek online in 30 seconden. Je betaalt pas na de behandeling, met pin.</p>')
    body.append(f'<a class="btn btn-gold" href="{BOOK}" target="_blank" rel="noopener">Maak een afspraak</a>')
    body.append("</div></section>")

    main = "\n".join(body)
    ll = location_links(city["slug"])
    head = HEAD_TMPL.format(
        title=city["title"], meta=html.escape(city["meta"]), url=url, BASE=BASE,
        jsonld=json_ld(city), css=CSS, BOOK=BOOK,
    )
    foot = FOOT_TMPL.format(addr=ADDR, TEL_LINK=TEL_LINK, MAIL=MAIL, location_links=ll, BASE=BASE, today=TODAY)
    return head + main + foot


def write_sitemap():
    urls = [f"{BASE}/"] + [f"{BASE}/{c['slug']}/" for c in CITIES] + [
        f"{BASE}/blog/hoe-werkt-tanden-bleken/",
        f"{BASE}/algemene-voorwaarden/",
        f"{BASE}/privacybeleid/",
        f"{BASE}/cookiebeleid/",
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def write_llms():
    lines = ["# Smylee Whitening Studio", ""]
    lines.append("> Tandenbleekstudio in Elst (Gelderland), tussen Arnhem en Nijmegen. Tanden bleken met non-peroxide gel en LED-licht, in sessies van 20 minuten, vanaf €64,95. Je betaalt pas na de behandeling, met pin.")
    lines.append("")
    lines.append(f"Laatst bijgewerkt: {TODAY}. Website: {BASE}/")
    lines.append("")
    lines.append("## Locatiepagina's")
    for c in CITIES:
        lines.append(f"- [Tanden bleken in {c['city']}]({BASE}/{c['slug']}/)")
    lines.append("")
    lines.append("## Blog")
    lines.append(f"- [Hoe werkt tanden bleken? Eerlijk uitgelegd]({BASE}/blog/hoe-werkt-tanden-bleken/)")
    lines.append("")
    lines.append("## Kerngegevens")
    lines.append("- Naam: Smylee Whitening Studio (Smylee)")
    lines.append(f"- Adres: {ADDR}, Nederland. Eén locatie.")
    lines.append("- Regio: Elst, Arnhem, Nijmegen, Bemmel, Huissen, Driel, Zetten, Overbetuwe, Lingewaard en de rest van Gelderland")
    lines.append("- Telefoon en WhatsApp: 06 16 86 33 87 (+31 6 16 86 33 87)")
    lines.append(f"- E-mail: {MAIL}")
    lines.append(f"- Online boeken: {BOOK}")
    lines.append("")
    lines.append("## Prijzen")
    lines.append("- Fresh Smile: €64,95 (3 sessies van 20 minuten, 1 afspraak)")
    lines.append("- Bright Smile: €84,95 (5 sessies van 20 minuten, 1 afspraak)")
    lines.append("- Diamond Smile: €99,95 (7 sessies van 20 minuten, 2 afspraken)")
    lines.append("- Hollywood Smile: €149,95 (10 sessies van 20 minuten, 2 afspraken)")
    lines.append("- Smyle Refresh: €50,00 (polijsten en 2 sessies)")
    lines.append("- 1 tooth gem: €24,95 · 2 tooth gems: €39,95")
    lines.append("")
    lines.append("## Veelgestelde vragen")
    lines.append("### Wat kost tanden bleken in Elst?")
    lines.append("Tanden bleken bij Smylee in Elst kost €64,95 tot €149,95. Je betaalt pas na de behandeling, met pin.")
    lines.append("")
    lines.append("### Kan ik bij Smylee terecht als ik in Arnhem of Nijmegen woon?")
    lines.append("Ja. De studio zit aan de Dorpsstraat 57 in Elst, tussen Arnhem en Nijmegen. Ook vanuit Bemmel, Huissen, Driel en Zetten ben je er snel.")
    lines.append("")
    lines.append("## Goed om te weten")
    lines.append("- Smylee is een cosmetische tandenbleekstudio, geen tandartspraktijk.")
    return "\n".join(lines) + "\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    for c in CITIES:
        d = os.path.join(here, c["slug"])
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "index.html")
        with open(p, "w", encoding="utf-8") as f:
            f.write(render(c))
        print(f"✓ {c['slug']}/index.html  ({len(render(c))//1024} KB)")
    with open(os.path.join(here, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(write_sitemap())
    print("✓ sitemap.xml")
    with open(os.path.join(here, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(write_llms())
    print("✓ llms.txt")


if __name__ == "__main__":
    main()
