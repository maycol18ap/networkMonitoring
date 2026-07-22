import sqlite3

DB_NAME = "network_monitor.db"

def obtener_conexion():
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Tabla de sesiones de monitoreo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT,
            total_mb REAL NOT NULL
        )
    """)
    
    # Tabla para almacenar los dominios visitados en cada sesión
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dominios_visitados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sesion_id INTEGER,
            dominio TEXT NOT NULL,
            visitas INTEGER NOT NULL,
            FOREIGN KEY (sesion_id) REFERENCES sesiones (id)
        )
                   
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos_detectados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_deteccion TEXT NOT NULL,
        ip TEXT NOT NULL,
        mac TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def guardar_sesion(fecha_inicio, fecha_fin, total_mb, dict_dominios):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # 1. Insertar la sesión general
    cursor.execute("""
        INSERT INTO sesiones (fecha_inicio, fecha_fin, total_mb)
        VALUES (?, ?, ?)
    """, (fecha_inicio, fecha_fin, total_mb))
    
    sesion_id = cursor.lastrowid
    
    # 2. Insertar cada dominio real capturado
    for dominio, visitas in dict_dominios.items():
        cursor.execute("""
            INSERT INTO dominios_visitados (sesion_id, dominio, visitas)
            VALUES (?, ?, ?)
        """, (sesion_id, dominio, visitas))
        
    conn.commit()
    conn.close()
    print(f"\n[💾 BASE DE DATOS] ¡Sesión #{sesion_id} guardada con éxito en {DB_NAME}!")


def guardar_dispositivos(lista_dispositivos, fecha_actual):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    for dev in lista_dispositivos:
        cursor.execute("""
            INSERT INTO dispositivos_detectados (fecha_deteccion, ip, mac)
            VALUES (?, ?, ?)
        """, (fecha_actual, dev['ip'], dev['mac']))
            
    conn.commit()
    conn.close()
    print(f"[💾 BASE DE DATOS] Guardados {len(lista_dispositivos)} dispositivos detectados.")