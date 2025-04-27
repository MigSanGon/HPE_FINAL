import json
from aiokafka import AIOKafkaConsumer
import asyncio
import asyncpg
from dateutil import parser


# Configuración
KAFKA_TOPIC = "sensor_metrics_air"
KAFKA_BOOTSTRAP_SERVERS = "10.10.76.231:7676" 
POSTGRES_DSN = "postgresql://admin:loYo1HT25@10.10.76.244:6565/greenlake_data" 

async def consume_and_insert():
    # Conexión a PostgreSQL
    conn = await asyncpg.connect(dsn=POSTGRES_DSN)

    # Crear el consumer de Kafka
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="postgres-writer-group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    await consumer.start()
    print(f"Escuchando el topic {KAFKA_TOPIC}...")

    try:
        async for msg in consumer:
            data = msg.value
            print(f"Insertando mensaje: {data}")

            event_time = parser.parse(data["event_time"])
            
            try:
                await conn.execute(
                    """
                    INSERT INTO sensor_metrics_air (co, o3, co2, no2, so2, pm10, sensor_id, event_time)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    data["co"],
                    data["o3"],
                    data["co2"],
                    data["no2"],
                    data["so2"],
                    data["pm10"],
                    data["sensor_id"],
                    event_time
                )
            except Exception as e:
                print(f"Error insertando en PostgreSQL: {e}")
    except Exception as e:
        print(f"Error en el consumo: {e}")
    finally:
        await consumer.stop()
        await conn.close()

if __name__ == "__main__":
    asyncio.run(consume_and_insert())
