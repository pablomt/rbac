# Mi Microservicio de Control de Acceso

This project is a microservice developed in Python with the objective of implementing a Role-Based Access Control system. The primary goal is to manage and enforce access permissions based on roles assigned to users. The service provides secure and flexible access control for resources, ensuring that users can only perform actions permitted by role


## Estructura del Proyecto

```
mi-microservicio
├── src
│   ├── main.py                # Punto de entrada de la aplicación
│   ├── models
│   │   └── user_model.py       # Modelo de usuario
│   ├── routes
│   │   └── auth_routes.py       # Configuración de rutas de autenticación
│   ├── services
│   │   └── auth_service.py      # Lógica de negocio de autenticación
│   └── utils
│       └── db.py                # Funciones para manejo de base de datos
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación del proyecto
```

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd mi-microservicio
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
  - **Método:** POST
  - **Cuerpo:** `{ "username": "usuario", "password": "contraseña" }`

- **Verificar Permisos**
  - **Endpoint:** `/check_permissions`
  - **Método:** GET
  - **Headers:** `Authorization: Bearer <token>`

