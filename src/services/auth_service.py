from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import boto3
import hashlib
import hmac
import base64
from src.repositories.permissions import get_permisions
from src.repositories.roles_permissions import get_roles_permisions
from src.repositories.users import get_user
from src.repositories.user_roles import get_user_roles
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

    async def update_pasword(self, username: str, session: str, new_password: str):
        try:
            response = await self.cognito_client.respond_to_auth_challenge(
                ClientId=self.client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                Session=session,
                ChallengeResponses={
                    'USERNAME': username,
                    'NEW_PASSWORD': new_password,
                    'SECRET_HASH': self.get_secret_hash(username),
                    # "userAttributes.nickname": "pablomt",
                    # "userAttributes.name": "Pablo",
                    # "userAttributes.given_name": "Moreno",
                    # "userAttributes.family_name": "Tepichin",

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


    def get_cognito_user(self, token: str):
        try:
            response = self.cognito_client.get_user(
                AccessToken=token
            )
            return {
                'username': response['Username'],
                'user_attributes': {
                    attr['Name']: attr['Value']
                    for attr in response['UserAttributes']
                }
            }
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


    # def assign_role(self, user_id, role):
    #     self.db.users.update_one({"user_id": user_id}, {"$set": {"role": role}})

    async def check_permissions(self, user: dict, required_action: str, target_action: str, query: str =None):
        email = user.get('user_attributes', {}).get('email')
        user = await get_user(self.db, email)
        user_roles = await get_user_roles(self.db, user_id=user.id)
        if user and user_roles:
            roles_ids = [role_id[0].role_id for role_id in user_roles]
            roles_permissions_ids = await get_roles_permisions(self.db, roles_ids)
            if roles_permissions_ids:
                permissions_ids = [roles_permission_id[0].permission_id for roles_permission_id in roles_permissions_ids]
                permissions = await get_permisions(self.db, permissions_ids)
                for permission in permissions:
                    if query:
                        # Lógica adicional para validar queries
                        pass
                    if permission[0].name == required_action and permission[0].resource == target_action:
                        return True
                    else:
                        return False
        return False