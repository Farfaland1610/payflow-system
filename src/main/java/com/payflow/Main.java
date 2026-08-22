package com.payflow;

import com.payflow.network.TcpPaymentServer;

public class Main {
    public static void main(String[] args) {
        TcpPaymentServer server = new TcpPaymentServer(8080);
        server.iniciar();
    }
}