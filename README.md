# Library Project

Prueba tecnica para useit, sistema de gestión de biblioteca desarrollado con Django y PostgreSQL (Neon).

## Stack Tecnológico

- **Backend:** Django
- **Base de datos:** PostgreSQL (servicio Neon)
- **Despliegue** Render

## Configuración y ejecución local

### 1. Clona el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd library_project
```

### 2. Crea y activa un entorno virtual

En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
En Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno

Crea un archivo `.env` en la raíz del proyecto (`library_project/.env`) con el siguiente contenido:

```
PGDATABASE=Library
PGUSER=Library_owner
PGPASSWORD=npg_z4NEXlfeb2KC
PGHOST=ep-soft-sky-a59hp372-pooler.us-east-2.aws.neon.tech
PGPORT=5432
PGSSLMODE=require
```

### 5. Aplica las migraciones

```bash
py manage.py migrate
```

### 6. Carga los datos iniciales (seed)

```bash
py manage.py seed_data
```

### 7. Ejecuta el servidor de desarrollo

```bash
py manage.py runserver
```

La aplicación estará disponible en [http://localhost:8000](http://localhost:8000)

---

**Notas:**
- Asegurarse de tener acceso a la base de datos Neon y que las credenciales sean correctas.
