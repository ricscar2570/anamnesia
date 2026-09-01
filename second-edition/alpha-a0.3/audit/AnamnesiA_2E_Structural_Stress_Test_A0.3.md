# ANAMNESIA 2E — STRUCTURAL STRESS TEST & REMEDIATION A0.3

**Oggetto:** Core Alpha 0.2 + *L’Incidente* Alpha 0.2.  
**Tipo di verifica:** stress test matematico/procedurale + Monte Carlo + dry-run di compatibilità narrativa.  
**Esito:** **REMEDIATION APPLICATA / READY FOR HUMAN ALPHA 1 rev0.3**, non rules-locked.

---

# 1. COSA PUÒ E NON PUÒ DIMOSTRARE QUESTO TEST

Questo lavoro **non sostituisce un playtest umano**. Una simulazione non può validare:
- qualità delle interpretazioni;
- intensità emotiva;
- facilità reale della Regola d’Oro;
- valore percepito delle Carte;
- soddisfazione della Sintesi Finale;
- sicurezza al tavolo;
- sensazione che la verità sia realmente emergente.

Può invece trovare problemi strutturali prima di usare tempo umano:
- risk-cliff della matematica;
- risorse che si auto-annullano;
- soglie impossibili;
- capacità che scalano troppo;
- timing circolari;
- doppie applicazioni di Stress/Breakdown;
- differenze eccessive fra profili di spesa;
- edge case tra regole.

---

# 2. CAMPIONE SIMULATO

La build candidata A0.3 è stata sottoposta a:

- **137.500 sessioni simulate**;
- **350.000 player-session**;
- circa **2.603.550 tiri simulati**;
- gruppi da 2, 3 e 4 giocatori;
- tutte le combinazioni possibili dei quattro Archetipi core per ogni dimensione del gruppo;
- cinque profili di comportamento volutamente diversi.

I profili non rappresentano percentuali previste di giocatori reali. Sono sonde di stress:

- **Concentrato:** tende a un solo tiro ampio per Ciclo.
- **Bilanciato:** normalmente due tiri medi.
- **Esplorativo:** molti tentativi piccoli, entro il nuovo cap di due.
- **Profondo:** cerca spesso Approcci +1/+2.
- **Ottimizzatore gratuito:** cerca quasi sempre l’Approccio gratuito e concentra i dadi.

Assunzioni parametriche come frequenza della Vulnerabilità o probabilità che una Verità Dolorosa generi Stress sono state mantenute costanti tra configurazioni. I numeri sono quindi **comparativi**, non previsioni di frequenze umane.

---

# 3. P0 MATEMATICO TROVATO — RISK-CLIFF DEI TIRI SPEZZATI

Con la matematica di AnamnesiA, il numero totale di dadi non determina da solo il rischio: conta soprattutto **in quanti tiri vengono spezzati**.

Usando quattro dadi totali con Approccio gratuito:

| Ripartizione degli stessi 4 dadi | P(almeno un Collasso) | Collassi attesi | Echi attesi |
|---|---:|---:|---:|
| 4 | 19,8% | 0,198 | 1,333 |
| 2 + 2 | 69,1% | 0,889 | 1,333 |
| 3 + 1 | 76,5% | 0,963 | 1,333 |
| 2 + 1 + 1 | 93,8% | 1,778 | 1,333 |
| 1 + 1 + 1 + 1 | 98,8% | 2,667 | 1,333 |

Il numero medio di Echi resta identico perché vengono comunque tirati quattro dadi. Il rischio di Collasso, invece, passa da circa **19,8%** con un unico 4d6 a **98,8%** con quattro tiri da 1d6.

Ancora più importante: i Collassi attesi passano da **0,198 a 2,667**, cioè oltre **13 volte** tanto Stress da Collasso prima dei recuperi.

La Core A0.2 dichiarava correttamente che dividere la Riserva aumenta il rischio, ma consentiva catene di tiri finché esistevano Frammenti. Vulnerabilità, Senso di Colpa ed Effetto Domino potevano inoltre rimettere Frammenti in circolo nello stesso Ciclo.

## Test di conferma

Nel profilo esplorativo A0.2, capace di arrivare fino a quattro Focus con tiro:
- P(Breakdown Finale) simulata: circa **92,8–94,2%** a seconda della dimensione del gruppo.

Applicando **soltanto un tetto di due tiri di memoria per personaggio/Ciclo**:
- P(Breakdown Finale) scendeva a circa **24,9–27,6%** nello stesso stress profile, prima delle altre remediation A0.3.

## Decisione A0.3

Introdotto, come regola Alpha:

> **Massimo due normali tiri di memoria per personaggio per Ciclo.**

Focus narrativi, Carte senza tiro e interventi sui tiri altrui non contano. Ultimo Ricordo conta come tiro.

Questa modifica non è rules-locked: il playtest umano deve stabilire se il tetto protegge il ritmo oppure appare artificiale.

---

# 4. P0 PROCEDURALE — STRESS DELLO STESSO TIRO

A0.2 conteneva un edge case reale.

Forzare avveniva prima dell’interpretazione, ma lo Stress della Verità Dolorosa dipendeva da **ciò che sarebbe stato interpretato**. Se la Verità Dolorosa veniva Forzata in Successo Parziale, il testo non permetteva di stabilire in modo non circolare quale Stress “originale” conservare.

Inoltre una stessa azione poteva produrre:
- Stress da Collasso;
- Stress da Forzare;
- Stress da Ultimo Ricordo;

e attraversare 4 e 5 in momenti successivi, rischiando due Breakdown generati dallo stesso Ricordo.

## Decisione A0.3 — Pacchetto di Stress

Tutto lo Stress della stessa azione viene sommato e applicato **una volta, dopo l’interpretazione**.

Se il Pacchetto porta direttamente a 5:
- si gioca soltanto il Breakdown Finale.

### Verità Dolorosa Forzata

Se viene trasformata in Successo Parziale:
- non produce il suo Stress condizionale;
- paga +1 Stress di Forzare;
- eventuali altre fonti indipendenti restano.

Questo chiude il circolo procedurale senza alterare la probabilità dei dadi.

---

# 5. P1 — EFFETTO DOMINO DEL CATALIZZATORE

A0.2 non limitava il numero di attivazioni di Effetto Domino nello stesso Ciclo.

In un ambiente con più tiri piccoli questo produceva due effetti:
1. ripetuti recuperi di Frammenti agli altri;
2. ripetuti Echi automatici sul Catalizzatore.

Nello stress model esplorativo precedente il Catalizzatore arrivava a Identità Fratturata con una frequenza molto elevata.

## Decisione A0.3

**Effetto Domino: massimo 1/Ciclo.**

Inoltre:
- si attiva soltanto su un Collasso **non Forzato**;
- se il Collasso viene trasformato in Verità Dolorosa, Domino non si attiva.

La modifica conserva l’identità “le mie crisi propagano conseguenze” senza premiare/punire catene di Collassi nello stesso Ciclo.

---

# 6. RISULTATI MONTE CARLO DELLA BUILD CANDIDATA A0.3

Le seguenti medie aggregano tutte le combinazioni di Archetipi disponibili per la dimensione del gruppo.

|   Giocatori | Profilo                |   Tiri/PG |   Stress finale |   Echi finali | Breakdown finale   | Identità Fratturata   |   +2 bloccato/PG |
|------------:|:-----------------------|----------:|----------------:|--------------:|:-------------------|:----------------------|-----------------:|
|           2 | concentrato            |      5    |            0.65 |          5.63 | 0.5%               | 8.4%                  |             0.05 |
|           2 | bilanciato             |      8.98 |            2.56 |          6.18 | 20.6%              | 16.7%                 |             0.57 |
|           2 | esplorativo            |      9.63 |            2.7  |          5.24 | 20.9%              | 10.7%                 |             0.07 |
|           2 | profondo               |      8.67 |            3.09 |          5.36 | 31.4%              | 9.0%                  |             1.76 |
|           2 | ottimizzatore_gratuito |      5    |            0.4  |          6.08 | 0.1%               | 13.9%                 |             0    |
|           3 | concentrato            |      4.99 |            0.61 |          5.58 | 0.4%               | 8.9%                  |             0.07 |
|           3 | bilanciato             |      8.93 |            2.41 |          6.17 | 18.3%              | 17.1%                 |             0.58 |
|           3 | esplorativo            |      9.6  |            2.62 |          5.36 | 19.3%               | 10.7%                 |             0.08 |
|           3 | profondo               |      8.64 |            2.96 |          5.41 | 28.8%              | 9.3%                  |             1.77 |
|           3 | ottimizzatore_gratuito |      5    |            0.38 |          6.05 | 0.1%               | 15.2%                 |             0    |
|           4 | concentrato            |      4.99 |            0.58 |          5.49 | 0.3%               | 8.5%                  |             0.07 |
|           4 | bilanciato             |      8.87 |            2.31 |          6.09 | 15.6%              | 16.2%                 |             0.57 |
|           4 | esplorativo            |      9.6  |            2.5  |          5.32 | 16.4%              | 9.9%                  |             0.08 |
|           4 | profondo               |      8.57 |            2.85 |          5.32 | 26.0%              | 8.2%                  |             1.76 |
|           4 | ottimizzatore_gratuito |      5    |            0.36 |          5.91 | 0.0%               | 13.8%                 |             0    |

## Lettura

### Profilo bilanciato
La build candidata produce:
- circa **8,9 tiri per personaggio** sull’intera sessione;
- Stress finale medio circa **2,3–2,6**;
- Breakdown Finale individuale circa **15,6–20,6%**.

È una fascia plausibile per un horror breve: il Breakdown è possibile ma non automatico.

### Profilo esplorativo
Con il cap di due tiri:
- il Collasso resta frequente, come deve essere per tiri piccoli;
- il Breakdown Finale si mantiene circa **16,4–20,9%** invece di avvicinarsi alla certezza.

Il cap risolve il comportamento patologico senza rendere i piccoli tiri “sicuri”.

### Profilo profondo
È il più costoso:
- Breakdown Finale circa **26–31%**;
- l’Approccio +2 desiderato ma non acquistabile compare circa **1,76 volte per personaggio/sessione**.

Questo non viene corretto a tavolino. È una questione P1 da playtest umano: potrebbe rappresentare correttamente il deterioramento oppure impedire proprio nel finale l’Approccio più tematico.

### Profilo concentrato / ottimizzatore gratuito
Mostra l’altra estremità:
- pochissimo Stress finale;
- Breakdown Finale quasi assente;
- ma Echi comunque elevati, circa 5,5–6,1 in media, e Identità Fratturata non nulla.

Questo significa che la pressione non scompare: si sposta dallo Stress agli Echi.

Resta però una **red flag comportamentale**: se al tavolo i giocatori riescono a formulare quasi ogni azione con l’Approccio gratuito e un unico tiro ampio, la strategia può diventare troppo dominante. Per questo la frequenza dell’Approccio gratuito resta una metrica Alpha, non viene “bilanciata” artificialmente prima di osservare la fiction reale.

---

# 7. ACCESSIBILITÀ DEGLI APPROCCI +2

La matematica esatta mostra una differenza importante tra Base 4 e Base 5.

## Archetipi Base 4
Per poter pagare +2 e almeno 1 dado serve Riserva ≥3.

Quindi +2 diventa indisponibile quando, per esempio:
- Stress ≥2 anche senza penalità Echi;
- Stress 1 + fascia Echi 3–5;
- fascia Echi 6+ anche a Stress 0.

## Archetipi Base 5
+2 resta disponibile più a lungo:
- può ancora essere usato con 1 dado a Stress 2 senza penalità Echi;
- oppure con Stress 1 + penalità Echi −1;
- oppure con Stress 0 + penalità Echi −2.

## Decisione

**Nessuna modifica A0.3.**

Motivo: il dato è strutturalmente chiaro ma non dimostra da solo che l’esperienza sia sbagliata. Il playtest deve rispondere:

> quando il Protettore o il Catalizzatore non possono più permettersi il proprio +2, la perdita sembra una conseguenza drammatica interessante o una privazione del loro Approccio più caratterizzante?

Se prevale la seconda risposta, il costo degli Approcci andrà ridisegnato nella successiva remediation.

---

# 8. ECHI E IDENTITÀ FRATTURATA

Nella build candidata:
- Echi finali medi si collocano spesso tra **5 e 6+**;
- Sopravvissuto tende a rimanere molto più basso grazie ai ritiri;
- Protettore/Testimone/Catalizzatore possono caricarsi di Echi tramite le proprie capacità.

Il dato è coerente con l’idea che gli Echi siano più frequenti dello Stress.

Non viene modificata la soglia 9+.

## Red flag per Alpha 1

Se Identità Fratturata:
- compare troppo presto;
- genera troppe Contraddizioni;
- oppure sembra una punizione per usare la propria capacità;

la soluzione preferita non sarà alzare automaticamente la soglia. Prima andrà controllato **quanto Eco aggiuntivo producono le capacità**.

---

# 9. CONNESSIONE UMANA E SCALING DEL GRUPPO

Il trigger attuale è collettivo:

> Connessione Umana è disponibile se **nessun personaggio** ha subito Breakdown nel Ciclo.

Questo produce inevitabilmente una dipendenza dalla dimensione del gruppo: con più persone aumenta la probabilità che qualcuno blocchi la Connessione per tutti.

Le simulazioni non mostrano però, dopo la remediation dei tiri, un collasso evidente della scalabilità 2→4. Le capacità incrociate del gruppo compensano in parte il fenomeno.

## Decisione

**Mantenere il trigger collettivo in Alpha 1.**

Da misurare:
- se i gruppi da 4 lo percepiscono come punizione per il problema di un altro;
- oppure come coerente effetto di trauma condiviso.

Nessun cambio prima del test umano.

---

# 10. FORZARE NEL CICLO 5

Resta il caso più severo:

- Collasso C5 = +2 Stress;
- Forzare = +1;
- totale = +3 nel Pacchetto.

Inoltre *La Verità Emerge Sempre* garantisce già un elemento decisivo anche senza Forzare.

Quindi, da un punto di vista puramente utilitaristico, Forzare un Collasso in C5 può apparire dominato.

## Decisione

**Non addolcirlo ancora.**

È un test drammatico, non soltanto matematico. Il playtest deve misurare se i giocatori scelgono comunque di Forzare perché vogliono una memoria più definita anche sapendo che potrebbe spezzare il personaggio.

Red flag:
- 0 utilizzi su molte opportunità consapevoli;
- commento ricorrente “non avrebbe mai senso farlo”.

In quel caso A0.4 dovrà differenziare meglio il valore narrativo di Collasso C5 e Verità Dolorosa C5 oppure cambiare il costo.

---

# 11. DRY-RUN STRUTTURALE DI L’INCIDENTE

Sono state percorse configurazioni narrative molto differenti combinando:
- natura del trauma precedente;
- rapporto con il quinto partecipante;
- destino del quinto;
- ruolo di Fassini;
- grado di consenso alla procedura.

Il template Fatti Fissi + Domande Aperte ha retto senza richiedere una soluzione segreta.

Durante il controllo è emersa però un’incoerenza procedurale reale:

- la distribuzione diceva di rivelare **tutte e quattro** le Carte Rivelazione all’inizio del Ciclo 5;
- R4 — *La Scelta* diceva invece di entrare **dopo la Sintesi Finale**.

## Decisione A0.3

- inizio C5: rivelare **R1, R2, R3**;
- R4 resta coperta;
- R4 viene rivelata soltanto dopo la Sintesi Finale.

Inoltre viene chiarito che i Vincoli 1 e 2 sono **scadenze di emersione di Fatti Fissi già veri**, non nuovi fatti aggiunti allo scenario.

---

# 12. CONFIGURAZIONI NARRATIVE VERIFICATE

Il dry-run ha incluso almeno queste famiglie:

1. incidente stradale precedente; quinto = persona che guidava; Fassini negligente;
2. salvataggio fallito; quinto = persona salvata/abbandonata; Fassini protettore ambiguo;
3. incendio domestico; quinto = testimone; destino incerto;
4. copertura di un errore professionale; quinto = whistleblower; Fassini complice;
5. ricatto; quinto = persona che deteneva la prova; Fassini manipolato;
6. fallimento medico precedente alla clinica; quinto = paziente/familiare; consenso misto;
7. evento collettivo con omissione; quinto = unico che voleva denunciare;
8. fuga da una minaccia; quinto = persona da cui il gruppo dipendeva;
9. incidente durante un viaggio; quinto = guida/organizzatore;
10. patto di silenzio tra amici; quinto = persona esclusa dal patto;
11. relazione familiare nascosta; quinto = parente di uno o più personaggi;
12. evento precedente orchestrato dal quinto; quinto non necessariamente vittima.

Nessuna di queste configurazioni richiede di contraddire i cinque Fatti Fissi.

**Nota:** questo prova soltanto ampiezza strutturale. Non prova che tutte producano una buona sessione.

---

# 13. VERDETTO A0.3

## Difetti chiusi prima dell’Alpha umano
- risk-cliff da catene di tiri: **mitigato con cap 2**;
- doppio Breakdown dalla stessa azione: **chiuso con Pacchetto di Stress**;
- circolo Verità Dolorosa → Forzare → Stress: **chiuso**;
- Effetto Domino ripetibile nello stesso Ciclo: **chiuso**;
- timing R4: **chiuso**.

## P1 ancora aperti
- Approcci +2 e Base 4;
- possibile dominanza dell’Approccio gratuito;
- severità di Forzare in C5;
- frequenza reale di Identità Fratturata;
- effetto combinato Vulnerabilità + Connessione + Ancora;
- percezione del limite di due tiri;
- efficacia reale delle Ombre del Trauma;
- quantità di Contraddizioni;
- utilità delle Carte senza costo aggiuntivo.

# 14. GATE

**G0 — Design Constitution:** PASS  
**Core completezza procedurale:** PASS  
**Structural Stress Test:** PASS CON REMEDIATION  
**L’Incidente compatibilità strutturale:** PASS  
**Build candidata:** **A0.3**  
**Human Alpha 1:** **READY**  
**G2 Scenario:** PENDING HUMAN EVIDENCE  
**Il Tradimento 2E:** ancora BLOCCATO

La simulazione ha ormai esaurito ciò che può dimostrare con affidabilità. Il prossimo dato realmente informativo deve arrivare da sessioni umane.