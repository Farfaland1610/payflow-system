package com.payflow.network;

import com.payflow.service.PaymentProcessor;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class TcpPaymentServer {
    private final int puerto;
    private final PaymentProcessor paymentProcessor = new PaymentProcessor();

    public TcpPaymentServer(int puerto) {
        this.puerto = puerto;
    }

    public void iniciar() {
        try (ServerSocket serverSocket = new ServerSocket(puerto)) {
            System.out.println("PayFlow - JavaServidor de Pagos (TCP) listo en el puerto: " + puerto);

            while (true) {
                try (Socket clientSocket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {

                    String mensaje = in.readLine();
                    if (mensaje != null) {
                        System.out.println("Petición recibida: " + mensaje);
                        // Protocolo esperado: PAGO|ORD-101|50000|VISA
                        String[] partes = mensaje.split("\\|");

                        if ("PAGO".equals(partes[0]) && partes.length == 4) {
                            String respuesta = paymentProcessor.procesarPago(
                                    partes[1],
                                    Double.parseDouble(partes[2]),
                                    partes[3]
                            );
                            out.println(respuesta);
                            System.out.println("Respuesta enviada: " + respuesta);
                        } else {
                            out.println("RECHAZADO: FORMATO_INVALIDO");
                        }
                    }
                } catch (Exception e) {
                    System.err.println("Error con el cliente: " + e.getMessage());
                }
            }
        } catch (Exception e) {
            System.err.println("Error en Servidor TCP: " + e.getMessage());
        }
    }
}