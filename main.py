import sys
import threading
import time
from scapy.all import sniff, DNS, DNSQR, conf

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
    
    # Operación ultra rápida: Sumar tamaño bruto de todo el tráfico
    total_bytes += len(packet)
    
    # Operación secundaria: Si es DNS, extraemos el dominio
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:
        dns_layer = packet.getlayer(DNSQR)
        if dns_layer:
            dominio = dns_layer.qname.decode('utf-8', errors='ignore').strip('.')
            if not any(x in dominio for x in ['microsoft', 'windows', 'local', 'arpa', 'cloudflare', 'internal']):
                sitios_visitados[dominio] = sitios_visitados.get(dominio, 0) + 1

def bucle_sniff():
    """Este hilo se encarga únicamente de capturar red a baja escala"""
    global ejecutando
    # Sniffer ligero. Detiene su captura si ejecutando pasa a False
    sniff(iface=iface_seleccionada, prn=procesar_paquete, store=False, stop_filter=lambda p: not ejecutando)

# 2. Lanzamos la captura en un hilo secundario (en segundo plano)
hilo_red = threading.Thread(target=bucle_sniff, daemon=True)
hilo_red.start()

print("\n[🚀] Captura iniciada con éxito.")
print("[💡] Para ver el reporte final sin romper el programa, escribe la palabra 'reporte' o 'salir' y dale Enter.\n")

# 3. El hilo principal se queda esperando una entrada de texto normal y actualizando la interfaz
try:
    while ejecutando:
        total_mb = total_bytes / (1024 * 1024)
        print(f"\r[🔥] CONSUMO TOTAL: {total_mb:.4f} MB | Sitios web detectados: {len(sitios_visitados)}", end="")
        
        # Un pequeño truco no bloqueante para chequear la consola
        time.sleep(0.5) 
except KeyboardInterrupt:
    # Por si acaso aún intentas usar Ctrl+C
    pass

# Al romper el bucle (escribiendo texto), procesamos el cierre
print("\n\n" + "=" * 60)
print("                REPORTE DE SESIÓN FINAL")
print("=" * 60)
print(f"[📊] Consumo Neto Wi-Fi: {total_bytes / (1024 * 1024):.2f} MB")
print(f"[✨] Sitios web únicos registrados: {len(sitios_visitados)}")
print("\n[🌐] TOP 10 Dominios consultados:")

top_sitios = sorted(sitios_visitados.items(), key=lambda x: x[1], reverse=True)[:10]
if top_sitios:
    for sitio, visitas in top_sitios:
        print(f"   - {sitio} (Detectado {visitas} veces)")
else:
    print("   No se registraron sitios fuera del ecosistema base de Windows.")
print("=" * 60)

# Apagamos el hilo de red limpiamente
ejecutando = False