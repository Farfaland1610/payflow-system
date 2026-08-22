package com.payflow.service;

import com.payflow.dao.TransaccionDAO;
import com.payflow.model.Transaccion;

import java.util.Random;

public class PaymentProcessor {
    private final TransaccionDAO transaccionDAO = new TransaccionDAO();

    public String procesarPago(String idOrden, double monto, String metodoPago) {
        String idTx = "TX-" + java.util.UUID.randomUUID().toString();

        // Si el monto es <= 0, es un rechazo de negocio explícito
        if (monto <= 0) {
            Transaccion tx = new Transaccion(idTx, idOrden, monto, metodoPago, "RECHAZADO");
            transaccionDAO.guardar(tx);
            return "RECHAZADO|TX-0000|El monto ingresado debe ser mayor a cero";
        }

        // Si el monto es válido, se procesa como APROBADO
        Transaccion tx = new Transaccion(idTx, idOrden, monto, metodoPago, "APROBADO");
        boolean guardado = transaccionDAO.guardar(tx);

        if (guardado) {
            return String.format("APROBADO|%s|Cobro procesado exitosamente para la orden %s", idTx, idOrden);
        } else {
            return "ERROR|TX-0000|Error al guardar la transacción en la base de datos";
        }
    }
}