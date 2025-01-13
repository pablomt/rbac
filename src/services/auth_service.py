from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import boto3
import hashlib
import hmac
import base64
from src.config import settings
from botocore.exceptions import ClientError


class AuthService:
    def __init__(self, db):
        self.db = db
        self.region = settings.AWS_REGION
        self.client_id = settings.COGNITO_CLIENT_ID
        self.client_secret = settings.COGNITO_CLIENT_SECRET
        self.user_pool_id = settings.COGNITO_USER_POOL_ID
        self.cognito_client = boto3.client('cognito-idp', region_name=self.region)


    def get_secret_hash(self, username: str) -> str:
        """Calculate the secret hash for Cognito authentication"""
        message = username + self.client_id
        dig = hmac.new(
            key=self.client_secret.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    def update_pasword(self, username: str, session: str, new_password: str):
        try:
            response = self.cognito_client.respond_to_auth_challenge(
                ClientId=self.client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                Session=session,
                ChallengeResponses={
                    'USERNAME': username,
                    'NEW_PASSWORD': new_password,
                    'SECRET_HASH': self.get_secret_hash(username),
                    "userAttributes.nickname": "pablomt",
                    "userAttributes.name": "Pablo",
                    "userAttributes.given_name": "Moreno",
                    "userAttributes.family_name": "Tepichin",

                }
            )
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'CodeMismatchException':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid verification code"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )

    def login(self, username: str, password: str) -> dict:
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SECRET_HASH': self.get_secret_hash(username)
                }
            )
            return {
                'access_token': response['AuthenticationResult']['AccessToken'],
                'id_token': response['AuthenticationResult']['IdToken'],
                'refresh_token': response['AuthenticationResult']['RefreshToken']
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'NotAuthorizedException':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            elif e.response['Error']['Code'] == 'UserNotFoundException':
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )

    def get_cognito_jwk(self):
        response = self.client_cognito.get_jwk(self.user_pool_id)
        return response['keys']

    def verify_token(self, token: str):
        jwks = self.get_cognito_jwk()
        try:
            payload = jwt.decode(token, jwks, algorithms=['RS256'], audience=self.client_id)
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    # def assign_role(self, user_id, role):
    #     self.db.users.update_one({"user_id": user_id}, {"$set": {"role": role}})

    def check_permissions(self, user_id, required_action: str, target_action: str, query: str =None):
        user = self.db.users.find_one({"user_id": user_id})
        if user and user.get('role'):
            # Aquí puedes agregar la lógica para verificar los permisos específicos del rol
            # y la acción requerida, así como la consulta opcional.
            # Por ejemplo:
            role = user.get('role')
            permissions = self.db.permissions.find_one({"role": role, "action": required_action})
            if permissions:
                if query:
                    # Lógica adicional para validar la consulta
                    pass
                return True
        return False