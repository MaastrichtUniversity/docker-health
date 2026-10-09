/* DABS dashboard demo — Bricks-schil + federatiedashboard */

// Elke node krijgt een eigen kleur én vorm, zodat meetpunten ook zonder kleur te
// onderscheiden zijn. Nodes die hier niet staan krijgen automatisch een vrije combinatie,
// zodat Envida en Vitala meteen werken zodra ze live meedraaien.
const BRON_STIJL = {
  mumc: { kleur: "#2b5fd9", vorm: "cirkel" },
  zio: { kleur: "#c2691a", vorm: "ruit" },
  envida: { kleur: "#0f8a6a", vorm: "vierkant" },
  vitala: { kleur: "#7d4bc2", vorm: "driehoek" },
};
const RESERVE = [
  { kleur: "#a8324a", vorm: "cirkel" }, { kleur: "#1f7a8c", vorm: "ruit" },
  { kleur: "#8a6d1f", vorm: "vierkant" }, { kleur: "#5b6273", vorm: "driehoek" },
];
const _toegewezen = {};

function bronStijl(bron) {
  if (BRON_STIJL[bron]) return BRON_STIJL[bron];
  if (!_toegewezen[bron]) {
    _toegewezen[bron] = RESERVE[Object.keys(_toegewezen).length % RESERVE.length];
  }
  return _toegewezen[bron];
}

// De verbindingslijn is bewust gedempt: de gekleurde meetpunten moeten opvallen.
const LIJN_NEUTRAAL = "#7c8396";
const BRON_NAAM = { mumc: "MUMC", zio: "ZIO", federatie: "Federation-API" };

const state = { bsn: null, btg: false, alleenBrondata: false, data: null, laden: false, config: {} };

const $ = (sel) => document.querySelector(sel);
const el = (tag, attrs = {}, kinderen = []) => {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") node.className = v;
    else if (k === "html") node.innerHTML = v;
    else if (k === "text") node.textContent = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const kind of [].concat(kinderen)) {
    if (kind) node.appendChild(typeof kind === "string" ? document.createTextNode(kind) : kind);
  }
  return node;
};

const bronNaam = (b) => BRON_NAAM[b] || (b || "onbekend").toUpperCase();
const bronKleur = (b) => bronStijl(b).kleur;
const bronVorm = (b) => bronStijl(b).vorm;

function fmtDatum(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  if (isNaN(d)) return iso;
  return d.toLocaleDateString("nl-NL", { day: "numeric", month: "short", year: "numeric" });
}

function fmtGetal(n, decimalen = 0) {
  if (n === null || n === undefined) return "—";
  return Number(n).toLocaleString("nl-NL", { minimumFractionDigits: decimalen, maximumFractionDigits: decimalen });
}

function bronBadge(bron) {
  return el("span", { class: "bron", style: `background:${bronKleur(bron)}`, text: bronNaam(bron) });
}

/* ══ Bricks-schil ═══════════════════════════════════════════════════ */

function toonZoek() {
  $("#view-zoek").classList.remove("verborgen");
  $("#view-dossier").classList.add("verborgen");
}

function openDossier(bsn) {
  state.bsn = bsn;
  state.data = null;
  $("#pk-naam").textContent = "Dhr/Mw test (46)";
  $("#pk-geboortedatum").textContent = "01-01-1980";
  $("#pk-bsn").textContent = bsn;
  $("#view-zoek").classList.add("verborgen");
  $("#view-dossier").classList.remove("verborgen");
  kiesTab("journaal");
}

function kiesTab(naam) {
  document.querySelectorAll("#tabs button").forEach((b) => b.classList.toggle("actief", b.dataset.tab === naam));
  const isDabs = naam === "dabs";
  $("#tab-leeg").classList.toggle("verborgen", isDabs);
  $("#tab-dabs").classList.toggle("verborgen", !isDabs);
  if (isDabs && !state.data && !state.laden) laadDabs();
}

function zoek(bsn) {
  const doel = $("#zoekresultaat");
  doel.innerHTML = "";
  if (!/^\d{8,9}$/.test(bsn)) {
    doel.appendChild(el("div", { class: "geen-treffer", text: "Voer een geldig BSN in (8 of 9 cijfers)." }));
    return;
  }
  doel.appendChild(
    el("button", { class: "treffer", onclick: () => openDossier(bsn) }, [
      el("div", {}, [
        el("div", { class: "treffer-naam", text: "Dhr/Mw test" }),
        el("div", { class: "treffer-meta", text: `BSN ${bsn} · geboren 01-01-1980 · Praktijk DABS` }),
      ]),
    ])
  );
}

/* ══ Data ophalen ═══════════════════════════════════════════════════ */

async function laadDabs() {
  state.laden = true;
  toonSkelet();
  try {
    // "Alleen brondata" haalt rechtstreeks bij de nodes op, zonder terugval op fixtures.
    const url = `/api/patient/${state.bsn}?requester=Rolf&btg=${state.btg}` +
                (state.alleenBrondata ? "&bron=nodes" : "");
    const resp = await fetch(url);
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || `HTTP ${resp.status}`);
    state.data = data;
    tekenDashboard(data);
  } catch (err) {
    $("#tab-dabs").innerHTML = "";
    $("#tab-dabs").appendChild(
      el("div", { class: "foutmelding", text: `Ophalen mislukt: ${err.message}` })
    );
  } finally {
    state.laden = false;
  }
}

function toonSkelet() {
  const doel = $("#tab-dabs");
  doel.innerHTML = "";
  doel.appendChild(el("div", { class: "skelet", style: "height:46px;margin-bottom:16px" }));
  const tegels = el("div", { class: "tegels" });
  for (let i = 0; i < 4; i++) tegels.appendChild(el("div", { class: "skelet skelet-tegel" }));
  doel.appendChild(tegels);
  doel.appendChild(el("div", { class: "skelet skelet-paneel" }));
  doel.appendChild(el("div", { class: "skelet skelet-paneel" }));
}

/* ══ Dashboard ══════════════════════════════════════════════════════ */

function tekenDashboard(data) {
  const doel = $("#tab-dabs");
  doel.innerHTML = "";

  doel.appendChild(federatiestrip(data));

  // De herkomst van wat er op het scherm staat, moet niet te missen zijn: fixture-data
  // mag er nooit uitzien alsof de nodes hem zojuist geleverd hebben.
  if (data.meta.mode === "fixture" || data.meta.mode === "fallback" || data.meta.mode === "gemengd") {
    const detail = {
      fixture: "De federation-endpoints zijn hiervoor niet bevraagd.",
      fallback: "De federation-endpoints zijn bevraagd maar leverden niets, dus is teruggevallen op vastgelegde responses.",
      gemengd: "Een deel komt live van de nodes, de rest uit vastgelegde responses.",
    }[data.meta.mode];
    doel.appendChild(
      el("div", { class: "banner banner-fixture", html:
        `<b>Geen live data.</b> ${detail} Zet <b>Alleen brondata</b> aan om uitsluitend te tonen ` +
        `wat de nodes op dit moment werkelijk leveren.` })
    );
  }

  if (data.meta.dataset === "rich") {
    doel.appendChild(
      el("div", { class: "banner banner-demo", html:
        "<b>Verrijkte demoset.</b> De meetreeksen in deze weergave zijn aangevuld om het verloop " +
        "in de grafieken zichtbaar te maken. Dit is geen brondata uit MUMC of ZIO." })
    );
  }
  if (data.meta.btg) {
    const extra = data.meta.btg_extra_records;
    let staart;
    if (extra > 0) {
      staart = `Dat levert <b>${extra} record${extra === 1 ? "" : "s"}</b> op die zonder ` +
               `toestemming voor gegevensuitwisseling verborgen bleven.`;
    } else if (extra === 0) {
      const eigen = data.meta.eigen_node ? bronNaam(data.meta.eigen_node) : "de eigen node";
      staart = `Voor deze patiënt levert dit geen extra records: ${eigen} is de eigen node en ` +
               `wordt sowieso niet gefilterd, en de overige nodes hadden al toestemming.`;
    } else {
      staart = "Records zonder toestemming voor gegevensuitwisseling worden nu getoond.";
    }
    doel.appendChild(
      el("div", { class: "banner banner-btg", html:
        "<b>Break-the-glass actief.</b> Het informed-consent-filter is uitgeschakeld en deze " +
        "inzage wordt gelogd. " + staart })
    );
  }
  if (state.alleenBrondata) {
    const heeftData = data.patient.length || data.bloeddruk.length || data.gewicht.length || data.lengte.length;
    doel.appendChild(
      el("div", { class: `banner ${heeftData ? "banner-bron" : "banner-btg"}`, html: heeftData
        ? "<b>Alleen brondata.</b> Rechtstreeks opgehaald bij de federation-endpoints, zonder fixtures " +
          "en zonder afgeleide waarden."
        : "<b>Alleen brondata — de nodes leveren op dit moment niets.</b> Er is rechtstreeks bij de " +
          "federation-endpoints opgehaald, zonder terugval op fixtures. Wat de nodes niet geven, " +
          "wordt hier ook niet getoond. De reden per node staat in de federatiestrip." })
    );
  }

  doel.appendChild(patientgegevens(data));
  doel.appendChild(kpiTegels(data));
  doel.appendChild(bloeddrukPaneel(data));
  doel.appendChild(gewichtPaneel(data));
  doel.appendChild(ruweData(data));
}

/* ── Federatiestrip ────────────────────────────────────────────────── */

function federatiestrip(data) {
  const strip = el("div", { class: "strip" }, [el("span", { class: "strip-label", text: "Federatie" })]);

  // Alleen echte live data verdient een groene chip. Komt het uit fixtures, dan wordt de
  // chip neutraal en draagt hij het label "fixture", zodat niemand hem voor live aanziet.
  const isLive = data.meta.mode === "live" || data.meta.mode === "nodes";

  for (const node of data.nodes) {
    const klasse = { ok: isLive ? "chip-ok" : "chip-fixture", consent_blocked: "chip-consent",
                     geen_data: "chip-leeg", offline: "chip-offline" }[node.status];
    const tekst = {
      ok: `${bronNaam(node.name)} · ${node.records} records${isLive ? "" : " · fixture"}`,
      consent_blocked: `${bronNaam(node.name)} · geen toestemming`,
      geen_data: `${bronNaam(node.name)} · geen gegevens`,
      offline: `${bronNaam(node.name)} · niet bereikbaar`,
    }[node.status];
    strip.appendChild(
      el("span", {
        class: `chip ${klasse}`,
        title: node.own
          ? "Eigen node — wordt zonder informed-consent-filter bevraagd"
          : (node.message || ""),
      }, [
        el("span", { class: "chip-punt" }),
        tekst,
        node.own ? el("span", { class: "chip-eigen", text: "eigen node" }) : null,
      ].filter(Boolean))
    );
  }

  const schakelaar = el("label", { class: "schakelaar", title: "Schakelt het informed-consent-filter uit" }, [
    el("input", {
      type: "checkbox", ...(state.btg ? { checked: "checked" } : {}),
      onchange: (e) => { state.btg = e.target.checked; laadDabs(); },
    }),
    el("span", { class: "schakelaar-spoor" }),
    "Break-the-glass",
  ]);

  const bronSchakelaar = el("label", {
    class: "schakelaar schakelaar-bron",
    title: "Toont uitsluitend wat via de endpoints uit de nodes is opgehaald",
  }, [
    el("input", {
      type: "checkbox", ...(state.alleenBrondata ? { checked: "checked" } : {}),
      onchange: (e) => { state.alleenBrondata = e.target.checked; laadDabs(); },
    }),
    el("span", { class: "schakelaar-spoor" }),
    "Alleen brondata",
  ]);

  const modus = {
    live: "live data",
    nodes: "live · alleen nodes",
    fixture: "fixtures",
    fallback: "fixtures (federatie onbereikbaar)",
    gemengd: "gemengd (live + fixtures)",
  }[data.meta.mode] || data.meta.mode;
  strip.appendChild(
    el("div", { class: "strip-rechts" }, [
      el("span", { class: "strip-meta", text: `${modus} · ${data.meta.duration_ms} ms · requester ${data.meta.requester}` }),
      bronSchakelaar,
      schakelaar,
    ])
  );
  return strip;
}

/* ── KPI-tegels ────────────────────────────────────────────────────── */

const laatste = (reeks) => (reeks && reeks.length ? reeks[reeks.length - 1] : null);

function tegel(kop, waardeNode, voetKinderen, leeg = false) {
  return el("div", { class: `tegel${leeg ? " tegel-leeg" : ""}` }, [
    el("div", { class: "tegel-kop", text: kop }),
    el("div", { class: "tegel-waarde" }, waardeNode),
    el("div", { class: "tegel-voet" }, voetKinderen),
  ]);
}

function kpiTegels(data) {
  const rij = el("div", { class: "tegels" });

  const bd = laatste(data.bloeddruk);
  rij.appendChild(
    bd
      ? tegel("Laatste bloeddruk",
          [`${bd.systolische_bloeddruk}/${bd.diastolische_bloeddruk}`, el("small", { text: "mmHg" })],
          [bronBadge(bd._source), fmtDatum(bd.bloeddruk_datum_tijd)])
      : tegel("Laatste bloeddruk", ["Geen meting"], [], true)
  );

  const gw = laatste(data.gewicht);
  rij.appendChild(
    gw
      ? tegel("Laatste gewicht",
          [fmtGetal(gw.gewichtwaarde_magnitude, 1), el("small", { text: gw.gewichtwaarde_units })],
          [bronBadge(gw._source), fmtDatum(gw.gewicht_datum_tijd)])
      : tegel("Laatste gewicht", ["Geen meting"], [], true)
  );

  const lg = laatste(data.lengte);
  rij.appendChild(
    lg
      ? tegel("Laatste lengte",
          [fmtGetal(lg.lengtewaarde_magnitude), el("small", { text: lg.lengtewaarde_units })],
          [bronBadge(lg._source), fmtDatum(lg.lengte_datum_tijd)])
      : tegel("Laatste lengte", ["Geen meting"], [], true)
  );

  // BMI combineert gewicht uit de ene bron met lengte uit de andere. Precies wat een
  // federatie oplevert en wat geen van de bronsystemen los kan berekenen — en daarmee
  // ook de enige waarde op dit scherm die niet uit een endpoint komt.
  if (state.alleenBrondata) {
    return rij;
  }
  if (gw && lg && lg.lengtewaarde_magnitude > 0) {
    const meter = lg.lengtewaarde_magnitude / 100;
    const bmi = gw.gewichtwaarde_magnitude / (meter * meter);
    const duiding = bmi < 18.5 ? "ondergewicht" : bmi < 25 ? "gezond gewicht" : bmi < 30 ? "overgewicht" : "obesitas";
    const voet = [];
    if (gw._source !== lg._source) {
      voet.push(bronBadge(gw._source), el("span", { text: "+" }), bronBadge(lg._source),
                el("span", { text: `${duiding} · gecombineerd uit twee bronnen` }));
    } else {
      voet.push(bronBadge(gw._source), el("span", { text: duiding }));
    }
    rij.appendChild(tegel("BMI (afgeleid)", [fmtGetal(bmi, 1)], voet));
  } else {
    rij.appendChild(tegel("BMI (afgeleid)", ["Onvoldoende data"], [], true));
  }

  return rij;
}

/* ── Grafiek ───────────────────────────────────────────────────────── */

const NS = "http://www.w3.org/2000/svg";
const svgEl = (tag, attrs = {}) => {
  const n = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v !== null && v !== undefined) n.setAttribute(k, v);
  return n;
};

/** Meetpuntmarker voor een bron: vorm én kleur dragen de herkomst. */
function tekenMarker(bron, cx, cy, r = 4.8) {
  const { kleur, vorm } = bronStijl(bron);
  let node;
  if (vorm === "ruit") {
    node = svgEl("rect", { x: cx - r * 0.96, y: cy - r * 0.96, width: r * 1.92, height: r * 1.92,
                           transform: `rotate(45 ${cx} ${cy})` });
  } else if (vorm === "vierkant") {
    node = svgEl("rect", { x: cx - r * 0.88, y: cy - r * 0.88, width: r * 1.76, height: r * 1.76 });
  } else if (vorm === "driehoek") {
    node = svgEl("polygon", {
      points: `${cx},${cy - r * 1.15} ${cx + r * 1.05},${cy + r * 0.78} ${cx - r * 1.05},${cy + r * 0.78}`,
    });
  } else {
    node = svgEl("circle", { cx, cy, r });
  }
  node.setAttribute("fill", "#fff");
  node.setAttribute("stroke", kleur);
  node.setAttribute("stroke-width", 2.4);
  return node;
}


function netteTicks(min, max, aantal = 5) {
  if (min === max) { min -= 1; max += 1; }
  const ruw = (max - min) / aantal;
  const macht = Math.pow(10, Math.floor(Math.log10(ruw)));
  const stap = [1, 2, 2.5, 5, 10].map((m) => m * macht).find((s) => s >= ruw) || macht * 10;
  const start = Math.floor(min / stap) * stap;
  const ticks = [];
  for (let v = start; v <= max + stap * 0.001; v += stap) ticks.push(Number(v.toFixed(10)));
  return ticks;
}

/**
 * Tijdreeksgrafiek als inline SVG.
 * series: [{naam, kleur, punten:[{t:Date, y:Number, bron, tip}], streep}]
 * banden: [{van, tot, kleur, label}] — horizontale referentievlakken
 */
function tekenGrafiek({ series, banden = [], yEenheid = "", hoogte = 300, domeinHint = null }) {
  const B = 900, H = hoogte;
  const M = { boven: 26, rechts: 16, onder: 36, links: 52 };
  const pb = B - M.links - M.rechts;
  const ph = H - M.boven - M.onder;

  const allePunten = series.flatMap((s) => s.punten);
  const svg = svgEl("svg", { class: "grafiek", viewBox: `0 0 ${B} ${H}`, role: "img" });
  if (!allePunten.length) return svg;

  const tMin = Math.min(...allePunten.map((p) => p.t.getTime()));
  const tMax = Math.max(...allePunten.map((p) => p.t.getTime()));
  const tPad = (tMax - tMin) * 0.06 || 86400000 * 30;
  const x0 = tMin - tPad, x1 = tMax + tPad;

  // Referentiebanden mogen het domein niet oprekken — een band tot 300 mmHg zou de
  // metingen tot een streep onderin persen. De data bepaalt de schaal, eventueel
  // verruimd met een klinisch zinvol minimumbereik, en de banden worden erop geknipt.
  let yMin = Math.min(...allePunten.map((p) => p.y));
  let yMax = Math.max(...allePunten.map((p) => p.y));
  if (domeinHint) {
    yMin = Math.min(yMin, domeinHint.min);
    yMax = Math.max(yMax, domeinHint.max);
  }
  const yPad = (yMax - yMin) * 0.14 || 5;
  yMin -= yPad; yMax += yPad;

  const X = (t) => M.links + ((t - x0) / (x1 - x0)) * pb;
  const Y = (v) => M.boven + ph - ((v - yMin) / (yMax - yMin)) * ph;

  // referentiebanden
  for (const band of banden) {
    if (band.tot <= yMin || band.van >= yMax) continue; // valt volledig buiten beeld
    const yv = Y(Math.min(band.tot, yMax)), yo = Y(Math.max(band.van, yMin));
    svg.appendChild(svgEl("rect", {
      x: M.links, y: yv, width: pb, height: Math.max(0, yo - yv), fill: band.kleur, opacity: 0.5,
    }));
    if (band.label) {
      // Links uitlijnen: de recentste meting staat rechts en valt juist vaak binnen een
      // normaalband, waar het label er dan bovenop zou liggen.
      const t = svgEl("text", { x: M.links + 6, y: yv + 12, "text-anchor": "start", class: "band-tekst" });
      t.textContent = band.label;
      svg.appendChild(t);
    }
  }

  // y-as
  for (const tick of netteTicks(yMin, yMax)) {
    if (tick < yMin || tick > yMax) continue;
    const y = Y(tick);
    svg.appendChild(svgEl("line", { x1: M.links, y1: y, x2: M.links + pb, y2: y, class: "raster" }));
    const label = svgEl("text", { x: M.links - 9, y: y + 4, "text-anchor": "end" });
    label.textContent = fmtGetal(tick, Number.isInteger(tick) ? 0 : 1);
    svg.appendChild(label);
  }

  // x-as
  const stappen = Math.min(6, Math.max(2, allePunten.length));
  for (let i = 0; i <= stappen; i++) {
    const t = x0 + ((x1 - x0) * i) / stappen;
    const x = X(t);
    svg.appendChild(svgEl("line", { x1: x, y1: M.boven, x2: x, y2: M.boven + ph, class: "raster" }));
    const label = svgEl("text", { x, y: H - 14, "text-anchor": "middle" });
    label.textContent = new Date(t).toLocaleDateString("nl-NL", { month: "short", year: "2-digit" });
    svg.appendChild(label);
  }

  svg.appendChild(svgEl("line", { x1: M.links, y1: M.boven + ph, x2: M.links + pb, y2: M.boven + ph, class: "as" }));
  svg.appendChild(svgEl("line", { x1: M.links, y1: M.boven, x2: M.links, y2: M.boven + ph, class: "as" }));

  if (yEenheid) {
    const e = svgEl("text", { x: M.links - 9, y: 13, "text-anchor": "end" });
    e.textContent = yEenheid;
    svg.appendChild(e);
  }

  // reeksen
  for (const reeks of series) {
    const punten = [...reeks.punten].sort((a, b) => a.t - b.t);
    if (punten.length > 1) {
      svg.appendChild(svgEl("path", {
        d: punten.map((p, i) => `${i ? "L" : "M"}${X(p.t.getTime())},${Y(p.y)}`).join(" "),
        fill: "none", stroke: reeks.kleur, "stroke-width": 2,
        "stroke-linejoin": "round", "stroke-dasharray": reeks.streep ? "5 4" : null,
      }));
    }
    for (const punt of punten) {
      // De lijn loopt door alle bronnen heen; het meetpunt zegt waar het vandaan komt.
      const vorm = tekenMarker(punt.bron, X(punt.t.getTime()), Y(punt.y));
      vorm.setAttribute("class", "punt");
      koppelTooltip(vorm, punt.tip);
      svg.appendChild(vorm);
    }
  }

  return svg;
}

function koppelTooltip(node, html) {
  const tip = $("#tooltip");
  node.addEventListener("mouseenter", (e) => {
    tip.innerHTML = html;
    tip.hidden = false;
    plaatsTooltip(e);
  });
  node.addEventListener("mousemove", plaatsTooltip);
  node.addEventListener("mouseleave", () => { tip.hidden = true; });
}

function plaatsTooltip(e) {
  const tip = $("#tooltip");
  const marge = 14;
  let x = e.clientX + marge, y = e.clientY + marge;
  const rect = tip.getBoundingClientRect();
  if (x + rect.width > window.innerWidth - 8) x = e.clientX - rect.width - marge;
  if (y + rect.height > window.innerHeight - 8) y = e.clientY - rect.height - marge;
  tip.style.left = `${x}px`;
  tip.style.top = `${y}px`;
}

function legenda(items) {
  return el("div", { class: "legenda" }, items.map((it) => {
    let teken;
    if (it.vorm === "lijn") {
      teken = el("i", { class: "lijn", style: `background:${it.kleur}` });
    } else if (it.vorm === "streeplijn") {
      teken = el("i", { class: "lijn", style:
        `background:repeating-linear-gradient(90deg,${it.kleur} 0 4px,transparent 4px 7px)` });
    } else {
      // Zelfde tekenfunctie als de grafiek, zodat legenda en meetpunten nooit uiteenlopen.
      teken = svgEl("svg", { width: 14, height: 14, viewBox: "0 0 14 14", class: "legenda-marker" });
      teken.appendChild(tekenMarker(it.bron, 7, 7, 4.4));
    }
    return el("span", {}, [teken, it.label]);
  }));
}

function paneel(titel, kopExtra, body) {
  return el("div", { class: "paneel" }, [
    el("div", { class: "paneel-kop" }, [el("h3", { text: titel }), kopExtra]),
    el("div", { class: "paneel-body" }, body),
  ]);
}

/* ── Bloeddruk ─────────────────────────────────────────────────────── */

function bloeddrukPaneel(data) {
  const rijen = data.bloeddruk;
  if (!rijen.length) {
    return paneel("Bloeddruk", null, el("div", { class: "leegmelding", text: "Geen bloeddrukmetingen beschikbaar." }));
  }

  const punt = (r, veld, label) => ({
    t: new Date(r.bloeddruk_datum_tijd),
    y: r[veld],
    bron: r._source,
    tip: `<b>${label} ${r[veld]} mmHg</b><br>${fmtDatum(r.bloeddruk_datum_tijd)}` +
         `<br>${r.systolische_bloeddruk}/${r.diastolische_bloeddruk} mmHg` +
         (r.houding ? `<br>${r.houding}` : "") +
         (r.anatomische_locatie?.locatie ? `<br>${r.anatomische_locatie.locatie}` : "") +
         `<br><span class="tt-bron">${bronNaam(r._source)} · ${r.system_id}</span>`,
  });

  // Eén lijn per meetwaarde, dwars door alle bronnen heen: dat is het verloop van de
  // patiënt. De lijn is gedempt en verbindt slechts; de markers dragen de herkomst.
  const perBron = {};
  for (const r of rijen) (perBron[r._source] ||= []).push(r);

  const series = [
    { naam: "Systolisch", kleur: LIJN_NEUTRAAL,
      punten: rijen.map((r) => punt(r, "systolische_bloeddruk", "Systolisch")) },
    { naam: "Diastolisch", kleur: LIJN_NEUTRAAL, streep: true,
      punten: rijen.map((r) => punt(r, "diastolische_bloeddruk", "Diastolisch")) },
  ];

  const svg = tekenGrafiek({
    series,
    banden: [
      { van: 60, tot: 80, kleur: "#e6f4ea", label: "diastolisch normaal" },
      { van: 90, tot: 120, kleur: "#e6f4ea", label: "systolisch normaal" },
      { van: 140, tot: 300, kleur: "#fbeaea", label: "hypertensie" },
    ],
    yEenheid: "mmHg",
    domeinHint: { min: 60, max: 150 }, // houdt de klinische referentie in beeld
  });

  const uitleg = rijen.length < 4
    ? el("p", { class: "conflict-uitleg", text:
        `Let op: ${rijen.length} meting${rijen.length === 1 ? "" : "en"} beschikbaar. De verbindingslijn suggereert een verloop dat op zo weinig punten niet te onderbouwen is — lees de losse meetpunten en de tabel.` })
    : null;

  const tabel = el("div", { class: "tabelwrap" }, [
    el("table", { class: "data" }, [
      el("thead", {}, el("tr", {}, ["Datum", "Systolisch", "Diastolisch", "Houding", "Locatie", "Bron", "Systeem"]
        .map((h) => el("th", { text: h })))),
      el("tbody", {}, [...rijen].reverse().map((r) =>
        el("tr", {}, [
          el("td", { text: fmtDatum(r.bloeddruk_datum_tijd) }),
          el("td", { text: `${r.systolische_bloeddruk} mmHg` }),
          el("td", { text: `${r.diastolische_bloeddruk} mmHg` }),
          el("td", { text: r.houding || "—" }),
          el("td", { text: r.anatomische_locatie?.locatie || "—" }),
          el("td", {}, [bronBadge(r._source)]),
          el("td", { text: r.system_id || "—" }),
        ])
      )),
    ]),
  ]);

  const legendaItems = Object.keys(perBron).sort().map((b) =>
    ({ vorm: "marker", bron: b, label: bronNaam(b) }));
  legendaItems.push({ vorm: "lijn", kleur: LIJN_NEUTRAAL, label: "Systolisch" });
  legendaItems.push({ vorm: "streeplijn", kleur: LIJN_NEUTRAAL, label: "Diastolisch" });

  return paneel("Bloeddruk", legenda(legendaItems), [uitleg, svg, tabel].filter(Boolean));
}

/* ── Gewicht ───────────────────────────────────────────────────────── */

function gewichtPaneel(data) {
  const rijen = data.gewicht;
  if (!rijen.length) {
    return paneel("Gewichtsverloop", null, el("div", { class: "leegmelding", text: "Geen gewichtsmetingen beschikbaar." }));
  }

  const bronnen = [...new Set(rijen.map((r) => r._source))].sort();

  // Eén doorlopende reeks over alle bronnen; de markers geven de herkomst aan.
  const series = [{
    naam: "Gewicht",
    kleur: LIJN_NEUTRAAL,
    punten: rijen.map((r) => ({
      t: new Date(r.gewicht_datum_tijd),
      y: r.gewichtwaarde_magnitude,
      bron: r._source,
      tip: `<b>${fmtGetal(r.gewichtwaarde_magnitude, 1)} ${r.gewichtwaarde_units}</b><br>` +
           `${fmtDatum(r.gewicht_datum_tijd)}<br>` +
           `<span class="tt-bron">${bronNaam(r._source)} · ${r.system_id}</span>`,
    })),
  }];

  const svg = tekenGrafiek({ series, yEenheid: "kg", hoogte: 260 });

  const tabel = el("div", { class: "tabelwrap" }, [
    el("table", { class: "data" }, [
      el("thead", {}, el("tr", {}, ["Datum", "Gewicht", "Bron", "Systeem"].map((h) => el("th", { text: h })))),
      el("tbody", {}, [...rijen].reverse().map((r) =>
        el("tr", {}, [
          el("td", { text: fmtDatum(r.gewicht_datum_tijd) }),
          el("td", { text: `${fmtGetal(r.gewichtwaarde_magnitude, 1)} ${r.gewichtwaarde_units}` }),
          el("td", {}, [bronBadge(r._source)]),
          el("td", { text: r.system_id || "—" }),
        ])
      )),
    ]),
  ]);

  return paneel("Gewichtsverloop",
    legenda(bronnen.map((b) => ({ vorm: "marker", bron: b, label: bronNaam(b) }))),
    [svg, tabel]);
}

/* ── Bronvergelijking ──────────────────────────────────────────────── */

const VELDEN = [
  { sleutel: "naam", label: "Naam",
    lees: (p) => [p.naamgegevens?.voornamen, p.naamgegevens?.voorvoegsels, p.naamgegevens?.achternaam].filter(Boolean).join(" ") || "—" },
  { sleutel: "geboortedatum", label: "Geboortedatum", lees: (p) => fmtDatum(p.geboortedatum) },
  { sleutel: "geslacht", label: "Geslacht", lees: (p) => p.geslacht || "—" },
  { sleutel: "identificatienummer", label: "Identificatienummers",
    lees: (p) => (p.identificatienummer || []).join(", ") || "—" },
  { sleutel: "adres", label: "Adres", lees: (p) => {
    const a = (p.adresgegevens || [])[0];
    if (!a) return "—";
    return [[a.straat, a.huisnummer, a.huisnummertoevoeging].filter(Boolean).join(" "),
            [a.postcode, a.woonplaats].filter(Boolean).join(" ")].filter(Boolean).join(", ");
  } },
  { sleutel: "telefoon", label: "Telefoon",
    lees: (p) => (p.contactgegevens?.telefoonnummers || []).map((t) => t.telefoonnummer).join(", ") || "—" },
  { sleutel: "email", label: "E-mail",
    lees: (p) => (p.contactgegevens?.email_adressen || []).map((e) => e.email_adres).join(", ") || "—" },
  { sleutel: "overleden", label: "Overleden",
    lees: (p) => (p.overlijdens_indicator ? `Ja${p.datum_overlijden ? ` (${fmtDatum(p.datum_overlijden)})` : ""}` : "Nee") },
];

/** Wanneer dit veld in dit bronsysteem voor het laatst is bijgewerkt. */
function veldDatum(record, sleutel) {
  return (record._veld_gewijzigd || {})[sleutel] || record.start_time || "";
}

/**
 * Patiëntgegevens als één set: per variabele de meest recente waarde.
 *
 * Recentheid komt uit start_time van de compositie. Een bron die voor een veld niets
 * heeft, wordt overgeslagen, zodat een ouder record een gat van een nieuwer kan vullen.
 * Wijkt een andere bron af, dan blijft dat zichtbaar naast de waarde.
 */
function patientgegevens(data) {
  const bronnen = data.patient;
  if (!bronnen.length) {
    return paneel("Patiëntgegevens", null,
      el("div", { class: "leegmelding", text: "Geen patiëntgegevens beschikbaar." }));
  }

  const rijen = [];
  let aantalAfwijkend = 0;

  for (const { sleutel, label, lees } of VELDEN) {
    // Per veld apart sorteren: het adres kan het laatst in ZIO zijn bijgewerkt terwijl
    // de naam uit MUMC komt. Zo ontstaat een samenstelling uit beide bronsystemen.
    const metWaarde = bronnen
      .filter((p) => { const v = lees(p); return v && v !== "—"; })
      .sort((a, b) => String(veldDatum(b, sleutel)).localeCompare(String(veldDatum(a, sleutel))));

    if (!metWaarde.length) {
      rijen.push({ label, waarde: "—", bron: null, datum: null, anderen: [] });
      continue;
    }
    const gekozen = metWaarde[0];
    const waarde = lees(gekozen);
    const anderen = metWaarde.slice(1)
      .filter((p) => lees(p) !== waarde)
      .map((p) => ({ bron: p._source, waarde: lees(p), datum: veldDatum(p, sleutel) }));
    if (anderen.length) aantalAfwijkend++;
    rijen.push({ label, waarde, bron: gekozen._source, datum: veldDatum(gekozen, sleutel), anderen });
  }

  const lijst = el("dl", { class: "gegevens" });
  for (const rij of rijen) {
    lijst.appendChild(el("dt", { class: rij.anderen.length ? "afwijkend" : null, text: rij.label }));
    const waardeNodes = [el("span", { class: "gegeven-waarde", text: rij.waarde })];
    if (rij.bron) {
      waardeNodes.push(bronBadge(rij.bron));
      if (rij.datum) waardeNodes.push(el("span", { class: "gegeven-datum", text: fmtDatum(rij.datum) }));
    }
    for (const ander of rij.anderen) {
      waardeNodes.push(el("span", { class: "afwijking" }, [
        "≠ ", ander.waarde, " ", bronBadge(ander.bron),
        ander.datum ? el("span", { class: "gegeven-datum", text: fmtDatum(ander.datum) }) : null,
      ].filter(Boolean)));
    }
    lijst.appendChild(el("dd", { class: rij.anderen.length ? "afwijkend" : null }, waardeNodes));
  }

  const gebruikteBronnen = [...new Set(rijen.map((r) => r.bron).filter(Boolean))];
  const heeftVeldDatums = bronnen.some((p) => p._veld_gewijzigd);

  let uitleg;
  if (bronnen.length < 2) {
    uitleg = `Eén bron beschikbaar (${gebruikteBronnen.map(bronNaam).join(", ")}). ` +
             `Zet break-the-glass aan om de overige nodes mee te nemen.`;
  } else {
    uitleg = `Per variabele de waarde die het laatst is bijgewerkt, samengesteld uit ` +
             `${gebruikteBronnen.map(bronNaam).join(" en ")}. ` +
             (aantalAfwijkend
               ? `Bij ${aantalAfwijkend} veld${aantalAfwijkend === 1 ? "" : "en"} heeft de andere bron een ` +
                 `afwijkende, oudere waarde; die staat erachter.`
               : `De bronnen zijn het eens over alle velden.`);
  }
  if (!heeftVeldDatums && bronnen.length > 1) {
    uitleg += " Let op: deze bron levert geen wijzigingsdatum per veld, dus is teruggevallen " +
              "op het tijdstempel van de hele compositie.";
  }

  return paneel("Patiëntgegevens", null, [el("p", { class: "conflict-uitleg", text: uitleg }), lijst]);
}

/* ── Ruwe data ─────────────────────────────────────────────────────── */

function ruweData(data) {
  return el("details", { class: "ruw" }, [
    el("summary", { text: "Ruwe response (genormaliseerd)" }),
    el("pre", { text: JSON.stringify(data, null, 2) }),
  ]);
}

/* ══ Start ══════════════════════════════════════════════════════════ */

$("#zoekform").addEventListener("submit", (e) => { e.preventDefault(); zoek($("#bsn-input").value.trim()); });
$("#bsn-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") { e.preventDefault(); zoek(e.target.value.trim()); }
});
$("#vul-demo").addEventListener("click", () => { $("#bsn-input").value = "999990603"; zoek("999990603"); });
$("#topbar-zoek").addEventListener("click", () => {
  const v = $("#topbar-bsn").value.trim();
  if (!v) return toonZoek();
  toonZoek(); $("#bsn-input").value = v; zoek(v);
});
$("#topbar-bsn").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#topbar-zoek").click(); });
$("#tabs").addEventListener("click", (e) => {
  const knop = e.target.closest("button[data-tab]");
  if (knop) kiesTab(knop.dataset.tab);
});

fetch("/api/config").then((r) => r.json()).then((c) => { state.config = c; }).catch(() => {});

// Diep linken vanuit de DABS-tab van Bricks: ?bsn=999990603 opent het dossier direct.
const params = new URLSearchParams(location.search);
if (params.get("bsn")) {
  openDossier(params.get("bsn"));
  if (params.get("tab") === "dabs") kiesTab("dabs");
} else {
  toonZoek();
}
