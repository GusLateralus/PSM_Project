import bcrypt  # En este script se hace el tratamiento de hashing y salting 

# Necesitamos 2 funciones, una para hashear la contraseña y otra para verificarla

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificar_password(password_intento, hashed_password):
    return bcrypt.checkpw(password_intento.encode('utf-8'), hashed_password)



