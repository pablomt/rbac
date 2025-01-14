# RBAC Microservice

This project is a microservice developed in Python(FastAPI) with the objective of implementing a Role-Based Access Control system. The primary goal is to manage and enforce access permissions based on roles assigned to users. The service provides secure and flexible access control for resources, ensuring that users can only perform actions permitted by role


## Proyecto structure

```
mi-microservicio
├── src
│   ├── main.py                # Entry point of application
│   ├── config.py              # Settings file
│   ├── models
│   │   └── user.py            # User model
│   │   └── role.py            # Roles model
│   │   └── ...                # extra models
│   ├── routes
│   │   └── auth_routes.py      # routes configuration
│   ├── repositories
│   │   └── permissions.py      # Queries to database
│   ├── services
│   │   └── auth_service.py     # Business Auth logic
│   └── utils
│       └── db.py                # Handler dabatase connection
│       └── enums.py             # Enum classes
├── requirements.txt             # Proyect dependencies
└── README.md                    # Proyect documentation
```

## Intallation

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd rbac
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Inicia la aplicación:
   ```
   uvicorn src.main:app --reload
   ```

2. Accede a la API en `http://localhost:8000` (o el puerto que hayas configurado).

## Ejemplos de API

- **Login**
  - **Endpoint:** `/login`
  - **Method:** POST
  - **Body:** `{ "username": "usuario", "password": "contraseña" }`

- **Check Permissions**
  - **Endpoint:** `/authorize`
  - **Método:** POST
  - **Body:** `{ "token": "123", "requiredAction": "read", "targerAction": "delta_table", "query":  "SELECT * FROM delta_table" }`

