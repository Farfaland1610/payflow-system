import random
import socket
import time

HOST = "127.0.0.1"  # IP Local (localhost)
PORT = 8080  # Puerto donde escuchará PayFlow


def procesar_pago(mensaje):
    """Simula la lógica de negocio de la pasarela de pagos."""
    try:
        # Formato esperado: "PAGO|order_id|monto|metodo"
        partes = mensaje.strip().split("|")

        if partes[0] == "PAGO" and len(partes) >= 3:
            order_id = partes[1]
            monto = float(partes[2])

            # Simulación de tiempo de procesamiento bancario (1 segundo)
            time.sleep(1)

            # Regla de simulación: si el monto es positivo, se aprueba
            if monto > 0:
                tx_id = f"TX-{random.randint(10000, 99999)}"
                return f"APROBADO|{tx_id}|Cobro de GS. {monto:.0f} procesado exitosamente para la orden {order_id}"
            else:
                return "RECHAZADO|TX-0000|El monto ingresado debe ser mayor a cero"
        else:
            return "ERROR|TX-0000|Formato de mensaje invalido"

    except Exception as e:
        return f"ERROR|TX-0000|Error procesando la transaccion: {str(e)}"


def iniciar_servidor_pagos():
    """Inicializa y mantiene corriendo el Servidor TCP."""
    # 1. Crear el socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permitir reutilizar el puerto inmediatamente al reiniciar
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Enlazar la IP y el Puerto
    server_socket.bind((HOST, PORT))

    # 3. Poner en modo escucha pasiva
    server_socket.listen()

    print("=" * 60)
    print(f"🟢 [PayFlow] Servidor de Pagos (TCP) Iniciado.")
    print(f"📡 Escuchando peticiones en http://{HOST}:{PORT}")
    print("=" * 60)

    try:
        while True:
            # Bloquea y espera a que un cliente (OrderManager) se conecte
            client_socket, client_address = server_socket.accept()
            print(
                f"\n📥 [NUEVA CONEXIÓN TCP] Petición recibida desde {client_address}"
            )

            # Recibir datos del cliente (hasta 1024 bytes)
            datos_recibidos = client_socket.recv(1024).decode("utf-8")

            if datos_recibidos:
                print(f"📄 Datos recibidos: {datos_recibidos}")

                # Procesar la transacción
                respuesta = procesar_pago(datos_recibidos)

                # Enviar respuesta al cliente
                client_socket.sendall(respuesta.encode("utf-8"))
                print(f"📤 Respuesta enviada: {respuesta}")

            # Cerrar socket individual de la transacción
            client_socket.close()
            print("🔒 Conexión finalizada. Servidor listo para siguiente pago.")

    except KeyboardInterrupt:
        print("\n🔴 [PayFlow] Apagando el servidor de pagos...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    iniciar_servidor_pagos()