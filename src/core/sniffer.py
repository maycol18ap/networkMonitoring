import threading
from scapy.all import sniff, IP, DNS, DNSRR

total_bytes = 0
sitios_visitados = {}
ejecutando = True

def procesar_paquete(pkt):
    global total_bytes, sitios_visitados
    
    if pkt.haslayer(IP):
        total_bytes += len(pkt)
        
    if pkt.haslayer(DNS) and pkt.haslayer(DNSRR):
        try:
            qname = pkt[DNS].qd.qname.decode('utf-8').rstrip('.')
            if qname:
                sitios_visitados[qname] = sitios_visitados.get(qname, 0) + 1
        except Exception:
            pass

def iniciar_captura():
    sniff(filter="ip", prn=procesar_paquete, store=0, stop_filter=lambda x: not ejecutando)

def arrancar_hilo_sniffer():
    hilo = threading.Thread(target=iniciar_captura, daemon=True)
    hilo.start()
    return hilo