import os
import sys 
import time
import random
import math
import subprocess
import platform
from pynput import keyboard
import pygame

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)


keys = keyboard.Controller()
coffee_in_corso = False

# Functions
def write_basita():
    time.sleep(0.1)
    keys.type("Basita.")

def write_preoccupata():
    time.sleep(0.1)
    keys.type("Preoccupata.")

def write_fondo_e_nero():
    time.sleep(0.1)
    keys.type("Fondo e nero.")

# Timer Function
def esegui_coffee_break():
    global coffee_in_corso
    if coffee_in_corso: return 
    
    print("SEGNALE RICEVUTO! Avvio il processo grafico Coffee Break...")
    coffee_in_corso = True
    percorso_interfaccia = os.path.join(BASE_DIR, "interfaccia_caffe.py")
    
    try:
        if getattr(sys, 'frozen', False):
            subprocess.run(["python3", percorso_interfaccia])
        else:
            subprocess.run([sys.executable, percorso_interfaccia])
            
        print("Timer chiuso. Il programma principale e' ancora in ascolto!")
    except Exception as e:
        print(f"Errore durante il lancio della grafica: {e}")
        
    coffee_in_corso = False

# Luminosity
def esegui_luminosita():
    print("SEGNALE RICEVUTO! Preparo Apri Tutto (Luminosita')...")
    percorso_audio = os.path.join(BASE_DIR, "Apri_Tutto.mp3")
    if os.path.exists(percorso_audio):
        subprocess.Popen(["afplay", percorso_audio]) 
    
    try:
        script_mac = (
            'tell application "System Events"\n'
            '    repeat 50 times\n'
            '        key code 144\n'
            '        delay 0.01\n'
            '    end repeat\n'
            'end tell'
        )
        subprocess.run(["osascript", "-e", script_mac])
        print("Luminosita' al 100%!")
    except Exception as e:
        print(f"Errore luminosita': {e}")

def ferma_tutto():
    global coffee_in_corso
    if coffee_in_corso: return 
    print("STOP! Riprese finite, andiamo tutti a casa!")
    os._exit(0)

# Shortcuts
shortcuts = {
    '<f4>':     write_basita,        # fn + F4
    '<f5>':     write_preoccupata,   # fn + F5
    '<f7>':     write_fondo_e_nero,  # fn + F7
    '<ctrl>+b': esegui_coffee_break, 
    '<ctrl>+l': esegui_luminosita,
    '<esc>':    ferma_tutto,
}
ascoltatore = keyboard.GlobalHotKeys(shortcuts)
ascoltatore.start()

print("Il set de 'Gli Occhi del Cuore' e' APERTO!")
print("  fn+F4     → Basita.")
print("  fn+F5     → Preoccupata.")
print("  fn+F7     → Fondo a nero.")
print("  Ctrl+B      → Coffee Break! (Interfaccia e Statistiche)")
print("  Ctrl+L      → Luminosita' al 100% (Apri Tutto)")
print("  ESC         → Chiudi l'intero programma.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ferma_tutto()
