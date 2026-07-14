🌐 Idioma: [English](README.md) | **Español**

# 📡 Network Traffic Monitor

> Herramienta ligera para monitorear tráfico de red desarrollada con Python, Scapy y Npcap.

Network Traffic Monitor es una aplicación de consola que captura paquetes de red en tiempo real para monitorear el consumo de ancho de banda y detectar las consultas DNS realizadas por el equipo.

Este proyecto nació como una prueba de concepto para aprender captura de paquetes, análisis de redes, programación concurrente y distribución de aplicaciones de escritorio utilizando Python.

---

# ✨ Características

- 📊 Monitoreo del tráfico de red en tiempo real.
- 🌐 Detección de consultas DNS.
- ⚡ Arquitectura multihilo para un procesamiento fluido.
- 💻 Interfaz ligera basada en terminal.
- 📦 Ejecutable para Windows (.exe).
- 🔓 Proyecto Open Source.

---

# 🏗 Arquitectura

```text
                    +----------------------+
                    |    Hilo Principal    |
                    | UI + Estadísticas    |
                    +----------+-----------+
                               |
                               |
                    +----------v-----------+
                    |   Hilo de Captura    |
                    |  Scapy + Npcap       |
                    +----------------------+
```

La captura de paquetes se ejecuta en un hilo independiente mientras el hilo principal actualiza continuamente la consola y muestra las estadísticas, evitando bloqueos incluso cuando existe un alto tráfico de red.

---

# 📸 Capturas

<img width="617" height="266" alt="image" src="https://github.com/user-attachments/assets/d812b9e2-b6e3-46df-b999-cd44c8cee7a2" />
<img width="831" height="371" alt="image" src="https://github.com/user-attachments/assets/a6b793b2-fbb6-48d8-8ac5-e8d050f0cd05" />
<img width="641" height="351" alt="image" src="https://github.com/user-attachments/assets/94d12526-8e4d-4c76-8a31-d2a424dff1aa" />


---

# 🚀 Instalación

Existen dos formas de utilizar la aplicación.

## Opción 1 — Descargar el Ejecutable

Recomendado para quienes solo desean utilizar la herramienta.

1. Descarga la última versión desde **Releases**.
2. Instala **Npcap**.
3. Ejecuta `main.exe` como Administrador.
4. Selecciona tu interfaz de red activa.
5. Comienza el monitoreo.

---

## Opción 2 — Ejecutar desde el Código Fuente

Clonar el repositorio

```bash
git clone https://github.com/maycol18ap/networkMonitoring.git

cd networkMonitoring
```

Crear el entorno virtual

```bash
python -m venv .venv
```

Activarlo

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Instalar las dependencias

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación

```bash
python main.py
```

---

# ⚠ Requisitos

La aplicación requiere:

- Windows
- Npcap instalado
- Ejecutarse con permisos de Administrador

Sin estos requisitos, Scapy no podrá capturar paquetes desde la interfaz de red.

---

# ▶ Uso

1. Ejecuta la aplicación.
2. Selecciona la interfaz de red activa.
3. La captura comenzará automáticamente.
4. Observa el consumo de red en tiempo real.
5. Finaliza la aplicación para visualizar el reporte de la sesión.

Ejemplo del reporte

```text
Consumo total: 245.8 MB

Dominios detectados

google.com
github.com
youtube.com
stackoverflow.com
```

---

# 🛠 Tecnologías

| Tecnología | Propósito |
|------------|-----------|
| Python 3.12 | Lenguaje principal |
| Scapy | Captura y análisis de paquetes |
| Npcap | Driver para captura de paquetes en Windows |
| Threading | Procesamiento concurrente |
| PyInstaller | Generación del ejecutable |
| uv | Gestión de dependencias |

---

# 📂 Estructura del Proyecto

```text
networkMonitoring/

├── main.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── README.es.md
├── main.spec
└── dist/
```

La versión actual está enfocada en validar la idea principal del proyecto. En futuras versiones la arquitectura será modularizada para mejorar el mantenimiento y la escalabilidad.

---

# 🗺 Roadmap

## Versión 1.0

- ✅ Captura de paquetes en tiempo real.
- ✅ Monitoreo del consumo de red.
- ✅ Detección de consultas DNS.
- ✅ Ejecutable para Windows.

## Próximas funcionalidades

- [ ] Historial de sesiones utilizando SQLite.
- [ ] Estadísticas por sesión.
- [ ] Exportación del historial a CSV.
- [ ] Interfaz interactiva con Rich.
- [ ] Filtros avanzados para dominios.
- [ ] Gráficas de consumo.
- [ ] Interfaz gráfica de escritorio.

---

# 🤝 Contribuciones

Las contribuciones, sugerencias y reportes de errores son bienvenidos.

Puedes abrir un **Issue** o enviar un **Pull Request**.

---

# 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.
