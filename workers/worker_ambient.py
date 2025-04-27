import asyncio
import json
from aiokafka import AIOKafkaConsumer
import asyncpg
from dateutil import parser

# Configuración
KAFKA_TOPIC = "sensor_metrics_ambient"
KAFKA_BOOTSTRAP_SERVERS = "10.10.76.231:7676" 
POSTGRES_DSN = "postgresql://admin:loYo1HT25@10.10.76.244:6565/greenlake_data" 

async def consume_and_insert_ambient():
    conn = await asyncpg.connect(dsn=POSTGRES_DSN)

    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="sensor_metrics_ambient-group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    await consumer.start()
    print(f"Escuchando el topic: {KAFKA_TOPIC}")

    try:
        async for msg in consumer:
            data = msg.value
            print(f"[{KAFKA_TOPIC}] Mensaje recibido: {data}")

            event_time = parser.parse(data["event_time"])

            try:
                await conn.execute(
                    """
                    INSERT INTO sensor_metrics_ambient (humidity, sensor_id, event_time, temperature, solar_radiation)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    data["humidity"],
                    data["sensor_id"],
                    event_time,  
                    data["temperature"],
                    data["solar_radiation"]
                )
                print(f"[{KAFKA_TOPIC}] Insertado correctamente")
            except Exception as db_error:
                print(f"[{KAFKA_TOPIC}] Error insertando en PostgreSQL: {db_error}")
    except Exception as kafka_error:
        print(f"[{KAFKA_TOPIC}] Error de consumo: {kafka_error}")
    finally:
        await consumer.stop()
        await conn.close()

if __name__ == "__main__":
    asyncio.run(consume_and_insert_ambient())


