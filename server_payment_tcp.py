import random
import socket
import time
import psycopg2

HOST = "127.0.0.1"  # IP Local (localhost)
PORT = 8080  # Puerto donde escuchará PayFlow

# Configuración de conexión a PostgreSQL (bd_payflow)
DB_CONFIG = {
    "dbname": "bd_payflow",
    "user": "postgres",
    "password": "admin",  # ⚠️ Cambia por tu contraseña real de Postgres
    "host": "localhost",
    "port": "5432",
}


def registrar_transaccion_db(tx_id, order_id, monto, metodo, estado):
    """Guarda el log transaccional en la BD bd_payflow."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = """
            INSERT INTO transacciones (id_transaccion, id_orden_origen, monto, metodo_pago, estado)
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(query, (tx_id, order_id, monto, metodo, estado))
        conn.commit()
        cursor.close()
        conn.close()
        print(
            f"🗄️ [DB PayFlow] Transacción {tx_id} guardada con estado '{estado}'."
        )
    except Exception as e:
        print(f"⚠️ [DB Error PayFlow] No se pudo guardar en Postgres: {e}")


def procesar_pago(mensaje):
    """Simula la lógica de negocio y registra en BD."""
    try:
        # Formato esperado: "PAGO|order_id|monto|metodo"
        partes = mensaje.strip().split("|")

        if partes[0] == "PAGO" and len(partes) >= 3:
            order_id = partes[1]
            monto = float(partes[2])
            metodo = partes[3] if len(partes) > 3 else "TARJETA"

            # Simulación de tiempo bancario
            time.sleep(1)

            if monto > 0:
                tx_id = f"TX-{random.randint(10000, 99999)}"
                # Guardar en BD como APROBADO
                registrar_transaccion_db(
                    tx_id, order_id, monto, metodo, "APROBADO"
                )
                return f"APROBADO|{tx_id}|Cobro de GS. {monto:.0f} procesado exitosamente para la orden {order_id}"
            else:
                tx_id = f"TX-{random.randint(10000, 99999)}"
                # Guardar en BD como RECHAZADO
                registrar_transaccion_db(
                    tx_id, order_id, monto, metodo, "RECHAZADO"
                )
                return "RECHAZADO|TX-0000|El monto ingresado debe ser mayor a cero"
        else:
            return "ERROR|TX-0000|Formato de mensaje invalido"

    except Exception as e:
        return f"ERROR|TX-0000|Error procesando la transaccion: {str(e)}"


def iniciar_servidor_pagos():
    """Inicializa y mantiene corriendo el Servidor TCP."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("=" * 60)
    print(f"🟢 [PayFlow] Servidor de Pagos (TCP) Iniciado.")
    print(f"📡 Escuchando peticiones en {HOST}:{PORT}")
    print("=" * 60)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(
                f"\n📥 [NUEVA CONEXIÓN TCP] Petición recibida desde {client_address}"
            )

            datos_recibidos = client_socket.recv(1024).decode("utf-8")

            if datos_recibidos:
                print(f"📄 Datos recibidos: {datos_recibidos}")
                respuesta = procesar_pago(datos_recibidos)
                client_socket.sendall(respuesta.encode("utf-8"))
                print(f"📤 Respuesta enviada: {respuesta}")

            client_socket.close()
            print(
                "🔒 Conexión finalizada. Servidor listo para siguiente pago."
            )

    except KeyboardInterrupt:
        print("\n🔴 [PayFlow] Apagando el servidor de pagos...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    iniciar_servidor_pagos()