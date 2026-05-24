import os
import sys
import random
import math
import json
import pygame
from datetime import datetime


if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)

DB_FILE = os.path.join(BASE_DIR, "coffee_history.json")

COLORE_OCEANO  = (0, 105, 148)
COLORE_BIANCO  = (255, 255, 255)
COLORE_VERDE   = (76, 175, 80)      
COLORE_VERDE_S = (46, 125, 50)      
COLORE_ROSSO   = (220, 50, 50)      
COLORE_ROSSO_S = (150, 30, 30)      
COLORE_NERO    = (0, 0, 0)

# History
def carica_storico():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except: return []
    return []

def aggiungi_caffe_completato():
    storico = carica_storico()
    storico.append(datetime.now().isoformat())
    try:
        with open(DB_FILE, "w") as f:
            json.dump(storico, f)
    except: pass

def calcola_statistiche():
    storico = carica_storico()
    oggi, settimana, mese = 0, 0, 0
    now = datetime.now()
    
    for record in storico:
        try:
            dt = datetime.fromisoformat(record)
            if dt.date() == now.date(): oggi += 1
            if dt.isocalendar()[:2] == now.isocalendar()[:2]: settimana += 1
            if dt.year == now.year and dt.month == now.month: mese += 1
        except: pass
    return oggi, settimana, mese

# 8-bit graphic
def draw_8bit_box(screen, rect, bg_color, shadow_color=None, border_color=COLORE_NERO, bw=6):
    pygame.draw.rect(screen, border_color, (rect.x + bw, rect.y, rect.width - bw*2, bw))
    pygame.draw.rect(screen, border_color, (rect.x + bw, rect.bottom - bw, rect.width - bw*2, bw))
    pygame.draw.rect(screen, border_color, (rect.x, rect.y + bw, bw, rect.height - bw*2))
    pygame.draw.rect(screen, border_color, (rect.right - bw, rect.y + bw, bw, rect.height - bw*2))
    pygame.draw.rect(screen, bg_color, (rect.x + bw, rect.y + bw, rect.width - bw*2, rect.height - bw*2))
    if shadow_color:
        pygame.draw.rect(screen, shadow_color, (rect.x + bw, rect.bottom - bw*2, rect.width - bw*2, bw))
        pygame.draw.rect(screen, shadow_color, (rect.right - bw*2, rect.y + bw, bw, rect.height - bw*3))

def disegna_freccia_pixel(screen, colore, cx, cy, tipo, scala=8):
    if tipo == "SX":
        pygame.draw.rect(screen, colore, (cx - scala*1.5, cy - scala*0.5, scala, scala))
        pygame.draw.rect(screen, colore, (cx - scala*0.5, cy - scala*1.5, scala, scala*3))
        pygame.draw.rect(screen, colore, (cx + scala*0.5, cy - scala*2.5, scala, scala*5))
    elif tipo == "DX":
        pygame.draw.rect(screen, colore, (cx - scala*1.5, cy - scala*2.5, scala, scala*5))
        pygame.draw.rect(screen, colore, (cx - scala*0.5, cy - scala*1.5, scala, scala*3))
        pygame.draw.rect(screen, colore, (cx + scala*0.5, cy - scala*0.5, scala, scala))
    elif tipo == "PLAY":
        for i, h in enumerate([9, 7, 5, 3, 1]):
            pygame.draw.rect(screen, colore, (cx - scala*2.5 + i*scala, cy - scala*(h/2.0), scala, h*scala))

# Visual effects
def _crea_bollicine(larghezza, altezza, n=25):
    return [
        [random.randint(0, larghezza), random.randint(0, altezza),
         random.uniform(0.6, 2.0), random.randint(30, 60)]
        for _ in range(n)
    ]

def _aggiorna_bollicine(bollicine, larghezza, altezza):
    for b in bollicine:
        b[1] -= b[2] 
        if b[1] + b[3] < 0:
            b[0] = random.randint(0, larghezza)
            b[1] = altezza + random.randint(5, 50)

def _disegna_bollicine(screen, bollicine, sprite_bolla):
    for b in bollicine:
        if sprite_bolla:
            bolla_scalata = pygame.transform.scale(sprite_bolla, (b[3], b[3]))
            screen.blit(bolla_scalata, (int(b[0]), int(b[1])))
        else:
            # Fallback
            pygame.draw.circle(screen, (173, 216, 230), (int(b[0]), int(b[1])), b[3] // 2, 2)

def _font(percorso, size):
    try: return pygame.font.Font(percorso, size)
    except: return pygame.font.SysFont("courier", size, bold=True)

# Main window
def main():
    pygame.init()
    pygame.mixer.init()

    info = pygame.display.Info()
    larghezza, altezza = info.current_w, info.current_h
    screen = pygame.display.set_mode((larghezza, altezza), pygame.NOFRAME)
    
    percorso_font = os.path.join(BASE_DIR, "font8bit.ttf")
    f_titolo = _font(percorso_font, 55)
    f_grande = _font(percorso_font, 70)
    f_pic    = _font(percorso_font, 34)
    f_timer  = _font(percorso_font, 160)
    f_stats  = _font(percorso_font, 24) 

    sprite_bolla = None
    for estensione in [".jpg", ".png", ".JPEG", ".PNG"]:
        path_bolla = os.path.join(BASE_DIR, f"Bolla_di_sapone{estensione}")
        if os.path.exists(path_bolla):
            try:
                img_bolla = pygame.image.load(path_bolla).convert_alpha()
                colore_angolo = img_bolla.get_at((0, 0))
                img_bolla.set_colorkey(colore_angolo)
                sprite_bolla = img_bolla
                break
            except: pass

    bollicine = _crea_bollicine(larghezza, altezza)
    clock = pygame.time.Clock()
    cx, cy = larghezza // 2, altezza // 2

    box_w, box_h = 320, 160
    btn_w, btn_h = 120, 160
    spazio = 20
    box_x, box_y = cx - box_w // 2, cy - 100
    btn_sx_x, btn_dx_x = box_x - btn_w - spazio, box_x + box_w + spazio
    play_w, play_h = (btn_dx_x + btn_w) - btn_sx_x, 140
    play_x, play_y = btn_sx_x, box_y + box_h + spazio

    rect_btn_sx = pygame.Rect(btn_sx_x, box_y, btn_w, btn_h)
    rect_btn_dx = pygame.Rect(btn_dx_x, box_y, btn_w, btn_h)
    rect_box    = pygame.Rect(box_x, box_y, box_w, box_h)
    rect_play   = pygame.Rect(play_x, play_y, play_w, play_h)

    c_oggi, c_settimana, c_mese = calcola_statistiche()

    pygame.mouse.set_visible(True)
    input_testo = "05"
    running = True
    while running:
        try: ultimi_minuti = int(input_testo)
        except: ultimi_minuti = 5
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                elif event.key == pygame.K_RETURN and 1 <= ultimi_minuti <= 60: running = False
                elif event.key == pygame.K_BACKSPACE: input_testo = input_testo[:-1]
                elif event.unicode.isdigit() and len(input_testo) < 2: input_testo += event.unicode
                elif event.key in [pygame.K_LEFT, pygame.K_DOWN]: input_testo = f"{max(1, ultimi_minuti - 1):02d}"
                elif event.key in [pygame.K_RIGHT, pygame.K_UP]: input_testo = f"{min(60, ultimi_minuti + 1):02d}"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if rect_btn_sx.collidepoint(mx, my): input_testo = f"{max(1, ultimi_minuti - 1):02d}"
                elif rect_btn_dx.collidepoint(mx, my): input_testo = f"{min(60, ultimi_minuti + 1):02d}"
                elif rect_play.collidepoint(mx, my) and 1 <= ultimi_minuti <= 60: running = False

        _aggiorna_bollicine(bollicine, larghezza, altezza)
        screen.fill(COLORE_OCEANO)
        _disegna_bollicine(screen, bollicine, sprite_bolla)
        
        screen.blit(f_titolo.render("SCEGLI DURATA", True, COLORE_BIANCO), f_titolo.render("SCEGLI DURATA", True, COLORE_BIANCO).get_rect(center=(cx, box_y - 80)))
        
        stat_testo = f"COFFEE BREAK: OGGI [{c_oggi}] | SETTIMANA [{c_settimana}] | MESE [{c_mese}]"
        t_stat = f_stats.render(stat_testo, True, COLORE_BIANCO)
        screen.blit(t_stat, t_stat.get_rect(center=(cx, play_y + play_h + 60)))

        draw_8bit_box(screen, rect_btn_sx, COLORE_VERDE, COLORE_VERDE_S)
        draw_8bit_box(screen, rect_btn_dx, COLORE_VERDE, COLORE_VERDE_S)
        draw_8bit_box(screen, rect_box, COLORE_BIANCO)
        draw_8bit_box(screen, rect_play, COLORE_ROSSO, COLORE_ROSSO_S)

        txt_display = f_grande.render(input_testo if input_testo != "" else "0", True, COLORE_NERO)
        screen.blit(txt_display, txt_display.get_rect(center=rect_box.center))
        
        disegna_freccia_pixel(screen, COLORE_NERO, rect_btn_sx.centerx, rect_btn_sx.centery, "SX")
        disegna_freccia_pixel(screen, COLORE_NERO, rect_btn_dx.centerx, rect_btn_dx.centery, "DX")
        disegna_freccia_pixel(screen, COLORE_NERO, rect_play.centerx, rect_play.centery, "PLAY")
        
        pygame.display.flip()
        clock.tick(60)

    # Audio Intro
    pygame.mouse.set_visible(False)
    try:
        suono_inizio = pygame.mixer.Sound(os.path.join(BASE_DIR, "e-coffee-break-signori.mp3"))
        suono_inizio.set_volume(0.7)
        suono_inizio.play()
        while pygame.mixer.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.mixer.stop(); return
            _aggiorna_bollicine(bollicine, larghezza, altezza)
            screen.fill(COLORE_OCEANO)
            _disegna_bollicine(screen, bollicine, sprite_bolla)
            txt = f_pic.render("...è coffee break, signori...", True, COLORE_BIANCO)
            screen.blit(txt, txt.get_rect(center=(cx, altezza // 2)))
            pygame.display.flip()
            clock.tick(60)
    except: pass

    # Timer 
    suono_fine = None
    try: suono_fine = pygame.mixer.Sound(os.path.join(BASE_DIR, "DAI.mp3"))
    except: pass

    frame_pesce = []
    for i in range(1, 10):
        path_min = os.path.join(BASE_DIR, f"Sprite_goldfish_{i}.png")
        path_mai = os.path.join(BASE_DIR, f"Sprite_Goldfish_{i}.png")
        percorso_sprite = path_min if os.path.exists(path_min) else path_mai
        
        if os.path.exists(percorso_sprite):
            img = pygame.image.load(percorso_sprite).convert_alpha()
            colore_angolo = img.get_at((0, 0))
            if colore_angolo[3] == 255:
                img.set_colorkey(colore_angolo) 
            frame_pesce.append(pygame.transform.scale(img, (200, 150)))
        else:
            break
            
    if not frame_pesce:
        surf = pygame.Surface((200, 150), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (255, 165, 0), (0, 40, 140, 70))
        frame_pesce.append(surf)

    vel_nuoto, direzione, x_pesce, y_base = 4, 1, larghezza // 2, altezza // 2 + 80
    durata_ms = ultimi_minuti * 60 * 1000
    inizio_ms = pygame.time.get_ticks()
    frame_count = 0
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return

        rimasto = max(0, durata_ms - (pygame.time.get_ticks() - inizio_ms))
        
        if rimasto == 0:
            aggiungi_caffe_completato() 
            screen.fill(COLORE_OCEANO)
            tz = f_timer.render("00:00", True, COLORE_BIANCO)
            screen.blit(tz, tz.get_rect(center=(cx, altezza // 3)))
            pygame.display.flip()
            
            if suono_fine:
                suono_fine.play()
                fine_t = pygame.time.get_ticks() + min(10000, int(suono_fine.get_length() * 1000))
                while pygame.time.get_ticks() < fine_t and pygame.mixer.get_busy():
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.mixer.stop(); return
                    pygame.display.update()
                    clock.tick(60)
            else:
                pygame.time.delay(2000)
            break

        frame_count += 1
        y_att = int(y_base + 30 * math.sin(frame_count * 0.05))
        x_pesce += int(vel_nuoto * direzione)
        if x_pesce + 100 >= larghezza or x_pesce - 100 <= 0: direzione *= -1

        _aggiorna_bollicine(bollicine, larghezza, altezza)
        screen.fill(COLORE_OCEANO)
        
        tr = f_timer.render(f"{(rimasto // 1000) // 60:02d}:{(rimasto // 1000) % 60:02d}", True, COLORE_BIANCO)
        screen.blit(tr, tr.get_rect(center=(cx, altezza // 3)))
        sotto = f_pic.render("-- COFFEE BREAK --", True, COLORE_BIANCO)
        screen.blit(sotto, sotto.get_rect(center=(cx, altezza // 3 + 110)))
        
        indice_sprite = (frame_count // 10) % len(frame_pesce)
        sprite_attuale = frame_pesce[indice_sprite]
        
        if direzione == 1: 
            sprite_attuale = pygame.transform.flip(sprite_attuale, True, False)
            
        screen.blit(sprite_attuale, sprite_attuale.get_rect(center=(x_pesce, y_att)))
        _disegna_bollicine(screen, bollicine, sprite_bolla)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()