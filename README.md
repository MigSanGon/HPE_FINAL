# HPE_FINAL

# Despliegue del Proyecto

Este repositorio contiene:

- **Backend**: API REST desarrollada en **FastAPI**, corriendo en el puerto `5454`.
- **Frontend**: Aplicación en **Streamlit**, corriendo en el puerto `8501`.
- **Workers**: 5 procesos que escuchan eventos desde Kafka y escriben en PostgreSQL.

## Requisitos

- Python 3.8 o superior
- `pip` actualizado
- Acceso SSH a la máquina virtual
- Permisos para abrir puertos `5454` y `8501`

## Instalación

1. Clona el repositorio en la VM:
   ```bash
   git clone https://github.com/usuario/tu-repo.git
   cd tu-repo
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.api.txt
   pip install -r requirements.streamlit.txt
   ```

## Levantar el Backend (FastAPI)

Ejecuta el siguiente comando para levantar la API REST en el puerto `5454`:
```bash
uvicorn api.api:app --host 0.0.0.0 --port 5454
```

## Levantar el Frontend (Streamlit)

Ejecuta el siguiente comando para levantar la aplicación Streamlit en el puerto `8501`:
```bash
streamlit run streamlit/home.py --server.address=0.0.0.0 --server.port=8501
```

## Configuración de Puertos

Asegúrate de abrir los puertos necesarios en el firewall de la VM:

```bash
sudo ufw allow 5454
sudo ufw allow 8501
```

## Despliegue de Workers (procesadores de Kafka)

Este proyecto incluye **5 workers** encargados de:

- Escuchar eventos de Kafka en `10.10.76.231:7676`.
- Procesar los mensajes recibidos.
- Insertarlos en la base de datos PostgreSQL (`10.10.76.244:6565` - base de datos `greenlake_data`).

### Variables de conexión utilizadas

- **Kafka Broker**:  
  `KAFKA_BOOTSTRAP_SERVERS = "10.10.76.231:7676"`

- **Base de Datos PostgreSQL**:  
  `POSTGRES_DSN = "postgresql://admin:loYo1HT25@10.10.76.244:6565/greenlake_data"`

### Levantar los Workers
Workers disponibles en workers/:

- worker_air.py
- worker_ambient.py
- worker_traffic.py
- worker_water_quality.py
- worker_water_usage.py

Cada worker se ejecuta independientemente. Para levantar un worker:

```bash
python workers/worker_name.py
```

## Automatización recomendada

Se recomienda usar **tmux**, **screen** o configurar **systemd services** para:

- Mantener los 5 workers corriendo en segundo plano.
- Evitar caídas en caso de cierre de sesión SSH o reinicio de la VM.

Ejemplo básico con `tmux`:

```bash
# Crear nueva sesión tmux para un worker
 tmux new -s worker1
python workers/worker1.py
# Luego presiona Ctrl+b y d para desconectar la sesión.
```

Repetir para cada worker.

## Acceso

- **Frontend (Streamlit)**:  
  `http://IP_DE_TU_VM:8501`

- **Backend API REST documentación**: 
  `http://IP_DE_TU_VM:5454/docs`

## Notas Adicionales

- El frontend Streamlit se comunica internamente con el backend FastAPI usando `http://localhost:5454`.
- El Frontend depende de los nombres de las variables en la base de datos. Si se modifican estos nombres, los cambios no se actualizan automáticamente en el Frontend, lo que puede provocar fallos.
  
