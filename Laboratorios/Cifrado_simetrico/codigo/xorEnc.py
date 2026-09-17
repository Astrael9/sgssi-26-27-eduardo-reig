



def cifradoFlujoXOR(mensaje, clave):
    print("Cifrado de flujo XOR")
    print("Mensaje: ", mensaje)
    print("Clave: ", clave)
    while(len(clave) < len(mensaje)):
        clave += " "
    while(len(clave) > len(mensaje)):
            mensaje += " "
    bMensaje = mensaje.encode('utf-8')
    bClave = clave.encode('utf-8')
    mensaje_cifrado = bytes(
    byte_mensaje ^ byte_clave
    for byte_mensaje, byte_clave in zip(bMensaje, bClave)
)
    print("Mensaje cifrado: ", mensaje_cifrado)
    mensaje_descifrado = bytes(
    byte_mensaje ^ byte_clave
    for byte_mensaje, byte_clave in zip(mensaje_cifrado, bClave)
)
    print("Mensaje descifrado: ", mensaje_descifrado)


cifradoFlujoXOR("ATAQUE AL AMANECER", "CLAVE12345678901")