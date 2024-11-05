import spidev
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Nastavení SPI pro MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0 (CS pin 8)
spi.max_speed_hz = 50000

# Funkce pro čtení hodnoty z MCP3008 (kanál 0 až 7)
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_value = ((r[1] & 3) << 8) + r[2]
    return adc_value

# Nastavení pro vizualizaci
fig, ax = plt.subplots()
x_data, y_data_pot, y_data_ldr = [], [], []

# Funkce pro aktualizaci grafu
def update_plot(frame):
    # Čti hodnotu z potenciometru (kanál 0)
    potentiometer_value = read_adc(0)
    # Čti hodnotu z fotorezistoru (kanál 1)
    ldr_value = read_adc(1)
    
    # Přidání dat pro vizualizaci
    x_data.append(time.time())
    y_data_pot.append(potentiometer_value)
    y_data_ldr.append(ldr_value)
    
    # Vizualizace grafu
    ax.clear()
    
    # Graf pro potenciometr
    ax.plot(x_data, y_data_pot, label="Potenciometr", color='b')
    
    # Graf pro fotorezistor
    ax.plot(x_data, y_data_ldr, label="Fotorezistor", color='g')
    
    ax.set_xlabel('Čas (s)')
    ax.set_ylabel('Hodnota')
    ax.set_title('Vizualizace potenciometru a fotorezistoru')
    ax.legend()
    ax.grid(True)

# Animace grafu
ani = FuncAnimation(fig, update_plot, interval=100)

# Hlavní smyčka
try:
    plt.show()  # Spustí vizualizaci
except KeyboardInterrupt:
    spi.close()  # Zavření SPI spojení
    print("\nProgram ukončen.")
