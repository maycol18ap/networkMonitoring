import sys
import threading
import time
from datetime import datetime
from scapy.all import sniff, DNS, DNSQR, conf
from src.database.db_manager import inicializar_db, guardar_sesion, guardar_dispositivos
from src.core.scanner import escanear_red

# 0. Inicializar la Base de Datos
inicializar_db()
fecha_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("=" * 60)
print("     VERSION 1.2: MONITOR PRO (CONTADOR + DOMINIOS)")
print("=" * 60)

# 1. Selección de interfaz
interfaces_lista = list(conf.ifaces.values())
for idx, face in enumerate(interfaces_lista):
    print(f"  [{idx}] -> {face.description}")

print("-" * 60)
try:
    opcion = int(input("[?] Elige el numero de tu tarjeta Wi-Fi activa (ref: 4 ): "))
    iface_seleccionada = interfaces_lista[opcion]
    print(f"\n[+] Conectado a: {iface_seleccionada.description}")
except (ValueError, IndexError):
    print("[-] Opcion invalida...")
    sys.exit()

# Variables globales compartidas entre hilos
total_bytes = 0
sitios_visitados = {}
ejecutando = True

def procesar_paquete(packet):
    global total_bytes, sitios_visitados
    
    # Sumar tamaño bruto
    total_bytes += len(packet)
    
    # Extraer dominios si es consulta DNS
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:
        dns_layer = packet.getlayer(DNSQR)
        if dns_layer:
            dominio = dns_layer.qname.decode('utf-8', errors='ignore').strip('.')
            if not any(x in dominio for x in ['microsoft', 'windows', 'local', 'arpa', 'cloudflare', 'internal']):
                sitios_visitados[dominio] = sitios_visitados.get(dominio, 0) + 1

def bucle_sniff():
    """Hilo secundario para captura de paquetes a bajo nivel"""
    global ejecutando
    sniff(iface=iface_seleccionada, prn=procesar_paquete, store=False, stop_filter=lambda p: not ejecutando)

# 2. Lanzamos la captura en segundo plano
hilo_red = threading.Thread(target=bucle_sniff, daemon=True)
hilo_red.start()

print("\n[🚀] Captura iniciada con éxito.")
print("[💡] Para detener el monitoreo y guardar datos, presiona Ctrl + C.\n")

# 3. Bucle principal de actualización visual
try:
    while ejecutando:
        total_mb = total_bytes / (1024 * 1024)
        print(f"\r[🔥] CONSUMO TOTAL: {total_mb:.4f} MB | Sitios web detectados: {len(sitios_visitados)}", end="")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n\nDeteniendo monitoreo...")

# --- PROCESO DE CIERRE Y GUARDADO DE SESIÓN ---
ejecutando = False
fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
total_mb = round(total_bytes / (1024 * 1024), 2)

print("\n" + "=" * 60)
print("                REPORTE DE SESIÓN FINAL")
print("=" * 60)
print(f"[📊] Consumo Neto Wi-Fi: {total_mb} MB")
print(f"[✨] Sitios web únicos registrados: {len(sitios_visitados)}")
print("\n[🌐] TOP 10 Dominios consultados:")

top_sitios = sorted(sitios_visitados.items(), key=lambda x: x[1], reverse=True)[:10]
if top_sitios:
    for sitio, visitas in top_sitios:
        print(f"   - {sitio} (Detectado {visitas} veces)")
else:
    print("   No se registraron sitios fuera del ecosistema base de Windows.")
print("=" * 60)

# 4. Guardar consumo en SQLite
if total_mb > 0 or sitios_visitados:
    guardar_sesion(fecha_inicio, fecha_fin, total_mb, sitios_visitados)

# --- 5. ESCANEO Y GUARDADO DE DISPOSITIVOS EN LA RED ---
dispositivos = escanear_red()
fecha_escaneo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("\n" + "=" * 50)
print("     DISPOSITIVOS DETECTADOS EN LA RED LOCAL")
print("=" * 50)
for d in dispositivos:
    print(f" 📱 IP: {d['ip']:<15} | MAC: {d['mac']}")
print("=" * 50)

# Guardar los dispositivos encontrados en SQLite
guardar_dispositivos(dispositivos, fecha_escaneo)

# 6. Pausa final para revisar la pantalla antes de salir
input("\n[📌] Presiona Enter para cerrar la aplicación...")