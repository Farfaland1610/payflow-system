package com.payflow.dao;

import com.payflow.db.DatabaseConnection;
import com.payflow.model.Transaccion;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class TransaccionDAO {

    public boolean guardar(Transaccion tx) {
        String sql = "INSERT INTO transacciones (id_transaccion, id_orden_origen, monto, metodo_pago, estado) " +
                "VALUES (?, ?, ?, ?, ?);";

        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, tx.getIdTransaccion());
            stmt.setString(2, tx.getIdOrdenOrigen());
            stmt.setDouble(3, tx.getMonto());
            stmt.setString(4, tx.getMetodoPago());
            stmt.setString(5, tx.getEstado());

            return stmt.executeUpdate() > 0;

        } catch (SQLException e) {
            System.err.println("TransaccionDAO Error: " + e.getMessage());
            return false;
        }
    }
}