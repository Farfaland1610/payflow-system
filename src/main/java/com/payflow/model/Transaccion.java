package com.payflow.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Transaccion {
    private String idTransaccion;
    private String idOrdenOrigen;
    private double monto;
    private String metodoPago;
    private String estado;



}