# Coffee-Break
A timer for your PC based on the famous Italian TV series "Boris"
# Coffee Break Timer & Soundboard

Un timer per le pause ispirato a *Boris*, che gira silenzioso in background e si attiva solo quando ti serve.

L'idea è semplice: il programma sta in RAM, ascolta la tastiera, e quando lo chiami apre una finestra con un countdown, un pesce rosso che nuota e le statistiche di quante pause caffè hai fatto. Poi torna a sparire.

---

## Cosa fa

**Background silenzioso.** Una volta avviato, non vedi niente. Niente icona, niente finestra fissa.

**Interfaccia grafica 8-bit.** Quando la chiami, appare una finestra a schermo intero costruita in Pygame: oceano animato, bollicine, un pesce rosso che scandisce il conto alla rovescia.

**Statistiche caffè.** Ogni pausa completata viene salvata in un file JSON locale. L'interfaccia mostra subito: caffè di oggi, della settimana, del mese.

**Automazione testi.** Tre tasti digitano istantaneamente le battute storiche in qualsiasi campo attivo — editor, chat, note...

**Luminosità al 100%.** `Ctrl+L` forza lo schermo al 100% di luminosità tramite AppleScript (Mac). 

---

## Hotkeys

| Tasto | Cosa fa |
|---|---|
| `Ctrl + B` | Apre l'interfaccia del timer |
| `Ctrl + L` | Luminosità al 100% + audio |
| `fn + F4` | Digita: *Basita.* |
| `fn + F5` | Digita: *Preoccupata.* |
| `fn + F7` | Digita: *Fondo e nero.* |
| `ESC` | Chiude la finestra grafica, o termina il programma se sei fuori dal timer |

---

## ⚠️ I file audio non sono inclusi

Per rispettare il copyright della serie, questo repository **non contiene nessun file `.mp3`**.

Il codice è già predisposto per riprodurli. Se vuoi l'audio, procurati i file, rinominali esattamente così e mettili nella cartella del progetto:

- `e-coffee-break-signori.mp3` — suona all'apertura del timer
- `DAI.mp3` — suona quando parte il countdown
- `Apri_Tutto.mp3` — suona con `Ctrl+L`

Senza file audio il programma funziona normalmente, salta semplicemente la riproduzione degli audio.

---

## Installazione

Python installato, repository clonata, poi:

```bash
pip install pygame pynput
```

```bash
python Coffee_break.py
```

**Mac:** al primo avvio il sistema chiede i permessi di Accessibilità per `pynput`. Vai in Impostazioni di Sistema → Privacy e sicurezza → Accessibilità e aggiungi il terminale (o l'app) che stai usando.

---

## Struttura dei file

```
progetto/
├── Coffee_break.py          # Script principale, hotkeys e background loop
├── interfaccia_caffe.py     # Finestra grafica Pygame, timer, statistiche
├── font8bit.ttf             # Font pixel (necessario per la grafica)
├── coffee_history.json      # Generato automaticamente al primo caffè completato
├── Bolla_di_sapone.png      # Sprite bollicine (opzionale, ha fallback)
└── Sprite_goldfish_*.png    # Sprite animazione pesce (opzionale, ha fallback)
```

---

## Note

Scritto per Mac, ma la parte grafica (Pygame) gira su qualsiasi sistema. La funzione luminosità usa `osascript`, quindi è Mac-only. La funzione `afplay` per l'audio è anch'essa Mac — su Linux/Windows va sostituita con `aplay` o simili.

*Dai, dai, dai.*

---

---

# ☕ Coffee Break Timer & Soundboard

A break timer inspired by the Italian cult series *Boris*, built to run silently in the background and only show up when it's needed.

The concept: the script sits in RAM, listens to your keyboard, and when you call it, opens a countdown window with a goldfish, animated bubbles, and your daily coffee stats. Then it disappears again.

---

## Features

**Silent background mode.** Once started, nothing is visible. No tray icon, no persistent window. Under 25MB in memory, just listening for hotkeys.

**8-bit graphical interface.** When triggered, it opens a fullscreen window built in Pygame: animated ocean, floating bubbles, a goldfish swimming out the countdown. The timer is big and hard to miss.

**Coffee tracking.** Every completed break is logged to a local JSON file. The interface shows your count for today, this week, and this month.

**Text automation.** Three hotkeys instantly type iconic catchphrases into any active text field — editor, chat, notes, anywhere.

**Full brightness.** `Ctrl+L` forces your screen to 100% brightness via AppleScript (Mac only). 

---

## Hotkeys

| Key | Action |
|---|---|
| `Ctrl + B` | Open the timer UI |
| `Ctrl + L` | Brightness to 100% + audio |
| `fn + F4` | Types: *Basita.* |
| `fn + F5` | Types: *Preoccupata.* |
| `fn + F7` | Types: *Fondo e nero.* |
| `ESC` | Closes the UI, or kills the background process if you're outside the timer |

---

## ⚠️ Audio files are not included

To respect the copyright of the original show, **this repository does not contain any `.mp3` files**.

The code is fully wired to play them. If you want audio, source the files yourself, rename them exactly as shown below, and place them in the project root before running:

- `e-coffee-break-signori.mp3` — plays when the timer opens
- `DAI.mp3` — plays when the countdown starts
- `Apri_Tutto.mp3` — plays via `Ctrl+L`

Without the audio files, everything else works fine. The script skips playback without crashing.

---

## Setup

Python installed, repo cloned, then:

```bash
pip install pygame pynput
```

```bash
python Coffee_break.py
```

**macOS:** On first launch the OS will ask for Accessibility permissions for `pynput`. Go to System Settings → Privacy & Security → Accessibility and add whichever terminal or app you're running it from.

---

## File structure

```
project/
├── Coffee_break.py          # Main script, hotkeys, background loop
├── interfaccia_caffe.py     # Pygame window, timer logic, stats display
├── font8bit.ttf             # Pixel font (required for the UI)
├── coffee_history.json      # Auto-generated on first completed break
├── Bolla_di_sapone.png      # Bubble sprite (optional, has fallback)
└── Sprite_goldfish_*.png    # Goldfish animation frames (optional, has fallback)
```

---

## Notes

Written on Mac, but the Pygame side runs on any OS. The brightness function uses `osascript` so it's Mac-only. `afplay` for audio is also Mac-only — on Linux/Windows substitute with `aplay` or equivalent.

*Dai, dai, dai.*
