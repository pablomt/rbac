# RBAC Microservice

This project is a microservice developed in Python(FastAPI) with the objective of implementing a Role-Based Access Control system. The primary goal is to manage and enforce access permissions based on roles assigned to users. The service provides secure and flexible access control for resources, ensuring that users can only perform actions permitted by role


## Proyect structure

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

1. Clone the repositorie:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd rbac
   ```

2. Install of dependencies:
   ```
   pip install -r requirements.txt
   ```

## Use

1. Start application
   ```
   uvicorn src.main:app --reload
   ```

2. Access to the API in `http://localhost:8000` (or on the configured port).

## API Examples

- **Login**
  - **Endpoint:** `/login`
  - **Method:** POST
  - **Body:** `{ "username": "usuario", "password": "contraseña" }`

- **Check Permissions**
  - **Endpoint:** `/authorize`
  - **Método:** POST
  - **Body:** `{ "token": "123", "requiredAction": "read", "targerAction": "delta_table", "query":  "SELECT * FROM delta_table" }`

