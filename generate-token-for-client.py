import jwt
import time

# Configuration du token
SECRET_KEY = "1214814c7f707a30b5b597bff5fe949d72bfbae9e3452fdf3d728a45d69bb752"
ALGORITHM = "HS256"
ISSUER = "BreizhSport"
SUBJECT = "1"
EMAIL = "pabios@pabiosoft.com"
ROLES = ["ROLE_ARCHITECTE"]
TOKEN_VALIDITY_DAYS = 5

# Générer le payload
issued_at = int(time.time())
expiration = issued_at + (TOKEN_VALIDITY_DAYS * 24 * 60 * 60)

payload = {
    "iss": ISSUER,
    "sub": SUBJECT,
    "email": EMAIL,
    "roles": ROLES,
    "iat": issued_at,
    "exp": expiration
}

# Générer le token JWT
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Décoder le token pour vérifier son contenu
decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# Afficher le token et son contenu décodé
print("Token JWT : " + token)
print("Contenu décodé : " + str(decoded_token))
