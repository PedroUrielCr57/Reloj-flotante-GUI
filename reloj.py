from tkinter import Tk, Label, Canvas
import time
import colorsys
import psutil
import GPUtil
from ventana import centrar_ventana

# Tamaño ventana
WIDTH = 300
HEIGHT = 180

# Colores
BACKGROUND = "gray"  # será transparente
TEXT_COLOR = "#ffffff"
FONT = ("Helvetica Neue", 40, "bold")
DATE_FONT = ("Helvetica Neue", 12)
TEMP_FONT = ("Helvetica Neue", 11)

# Inicializar ventana
ventana = Tk()
ventana.geometry(f"{WIDTH}x{HEIGHT}")
ventana.overrideredirect(True)
ventana.config(bg=BACKGROUND)
ventana.wm_attributes("-transparentcolor", BACKGROUND)
centrar_ventana(ventana, WIDTH, HEIGHT)
# ventana.wm_attributes("-topmost", True)  # lo quitamos para que no esté encima

# Hora
time_label = Label(ventana, font=FONT, fg=TEXT_COLOR, bg=BACKGROUND)
time_label.pack(pady=(10, 0))

# Fecha
date_label = Label(ventana, font=DATE_FONT, fg=TEXT_COLOR, bg=BACKGROUND)
date_label.pack()

# Temperatura CPU/GPU
temp_label = Label(ventana, font=TEMP_FONT, fg=TEXT_COLOR, bg=BACKGROUND)
temp_label.pack(pady=(5, 0))

# Barra RGB
canvas = Canvas(ventana, width=WIDTH - 40, height=8, bg=BACKGROUND, highlightthickness=0)
canvas.pack(pady=(10, 0))
bar = canvas.create_rectangle(0, 0, 0, 8, fill="red", width=0)

# Variables para color RGB
hue = 0

def get_temperatures():
    cpu_temp = "?"
    gpu_temp = "?"

    # CPU
    try:
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                if "cpu" in entry.label.lower() or "core" in entry.label.lower():
                    cpu_temp = f"{entry.current:.0f}°C"
                    break
    except:
        cpu_temp = "N/D"

    # GPU
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_temp = f"{gpus[0].temperature:.0f}°C"
    except:
        gpu_temp = "N/D"

    return cpu_temp, gpu_temp

def update_time():
    global hue
    now = time.localtime()
    hour = time.strftime("%I:%M %p", now)
    date = time.strftime("%d.%m.%Y", now)
    sec = now.tm_sec

    time_label.config(text=hour)
    date_label.config(text=date)

    # Temperaturas
    cpu, gpu = get_temperatures()
    temp_label.config(text=f"CPU: {cpu} | GPU: {gpu}")

    # RGB barra
    percent = sec / 60
    canvas.coords(bar, 0, 0, (WIDTH - 40) * percent, 8)
    r, g, b = [int(i * 255) for i in colorsys.hsv_to_rgb(hue, 1, 1)]
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.itemconfig(bar, fill=color)
    hue = (hue + 0.005) % 1

    ventana.after(1000, update_time)

# Movimiento ventana
def start_move(event):
    global x, y
    x = event.x
    y = event.y

def stop_move(event):
    global x, y
    x = None
    y = None

def do_move(event):
    deltax = event.x - x
    deltay = event.y - y
    ventana.geometry(f"+{ventana.winfo_x() + deltax}+{ventana.winfo_y() + deltay}")

ventana.bind("<ButtonPress-1>", start_move)
ventana.bind("<ButtonRelease-1>", stop_move)
ventana.bind("<B1-Motion>", do_move)
ventana.bind("<KeyPress-Escape>", lambda e: ventana.destroy())

# Iniciar
update_time()
ventana.mainloop()
