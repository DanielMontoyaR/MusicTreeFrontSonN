# Diccionario de prueba (usuario: contraseña)
usuarios_prueba = {
    "admin": "1234",
    "usuario1": "abcd"
}

def verificar_credenciales(usuario, contraseña):
    print('usuario: ' + usuario + 'password' + contraseña)
    return usuarios_prueba.get(usuario) == contraseña
