# PayFlow - Pasarela y Procesador Transaccional de Pagos

Este repositorio contiene la implementación del sistema independiente **PayFlow**, encargado de la autorización, validación y liquidación monetaria para el miniproyecto de sistemas distribuidos.

## 🛠️ Tecnología y Arquitectura de Red
- **Lenguaje:** Python 3.8+
- **Protocolo de Transporte:** TCP (Transmission Control Protocol)
- **Rol en la Red:** Servidor TCP (Escucha pasiva 24/7)
- **Puerto por Defecto:** `8080`

## 📡 Protocolo de Aplicación (Mensajería)
El servidor acepta solicitudes en formato de texto plano con campos delimitados por barra vertical (`|`):

1. **Estructura de Petición (Cliente -> Servidor):**
   `PAGO|<id_orden>|<monto>|<metodo_pago>`
   *Ejemplo:* `PAGO|ORD-101|50000|TARJETA_VISA`

2. **Estructura de Respuesta (Servidor -> Cliente):**
   `APROBADO|<id_transaccion>|<mensaje>`
   *Ejemplo:* `APROBADO|TX-9982|Cobro procesado exitosamente`

## 🚀 Instrucciones de Ejecución

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Farfaland1610/payflow-system.git](https://github.com/Farfaland1610/payflow-system.git)
   cd payflow-system