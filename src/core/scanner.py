from scapy.all import ARP, Ether, srp
import socket

def obtener_ip_local():
    """Obtiene la IP local de tu PC para deducir el rango de la red (ej. 192.168.1.1/24)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita conexión real, solo deduce la interfaz activa
        s.connect(('10.255.255.255', 1))
        ip_local = s.getsockname()[0]
    except Exception:
        ip_local = '127.0.0.1'
    finally:
        s.close()
    return ip_local

def escanear_red(rango_ip=None):
    """
    Envía un paquete ARP a todo el rango de la red local
    y retorna una lista de diccionarios con IP y MAC de cada dispositivo activo.
    """
    if not rango_ip:
        ip_local = obtener_ip_local()
        # Asumimos una máscara /24 estándar de hogar (ej. 192.168.1.0/24)
        ip_partes = ip_local.split('.')
        rango_ip = f"{ip_partes[0]}.{ip_partes[1]}.{ip_partes[2]}.1/24"

    print(f"\n[🔍 ESCÁNER] Escaneando red local: {rango_ip} ...")

    # 1. Crear el paquete ARP broadcast
    solicitud_arp = ARP(pdst=rango_ip)
    broadcast_ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    paquete_completo = broadcast_ether / solicitud_arp

    # 2. Enviar y recibir paquetes (srp = send/receive at layer 2)
    # timeout=2 espera 2 segundos respuestas, verbose=False evita spam en consola
    respuestas, _ = srp(paquete_completo, timeout=2, verbose=False)

    dispositivos = []
    for enviado, recibido in respuestas:
        dispositivos.append({
            "ip": recibido.psrc,
            "mac": recibido.hwsrc
        })

    return dispositivos