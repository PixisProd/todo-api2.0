# 📌 To-Do API
![Python](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-⚡-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-🧪-blue)
![Alembic](https://img.shields.io/badge/Alembic-⚗-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-🐘-blue)


## 📖 Description
A fast and modern asynchronous To-Do API built with FastAPI and PostgreSQL.
Includes secure authentication with JWT, role-based access control (RBAC), and advanced admin tools for managing users and tasks efficiently.

### 🔥 Highlights
⚡ Fully asynchronous architecture for high performance  
🔐 JWT authentication and security layer  
🧩 Role-based access control (RBAC) — user and admin roles  
📝 CRUD operations for tasks  
🛠️ Admin tools to manage users and their tasks  
🧪 SQLAlchemy + Alembic for database management  
🐘 PostgreSQL support  
🔬 Integrational tests for more stability

---

## 🔧 Features
- Fully asynchronous
- Authentication and security system
- RBAC system (user, admin)
- Task operations:
  - View tasks
  - Edit tasks
  - Delete tasks
  - Create tasks
- Admin tools:
  - Deactivate users
  - Activate users
  - View all users
  - View tasks of all users

---

## 🛠 Technologies
- **Language**: Python 3.13 🐍
- **Framework**: FastAPI ⚡ 
- **Database**: PostgreSQL 🐘
- **ORM**: SQLAlchemy 🧪
- **Migrations**: Alembic ⚗
- **Tests**: Pytest 🔬

---

# ⚙ How to setup and run

## 📦 Preparation
1. **Clone the repository to your folder:**
```
git clone https://github.com/PixisProd/todo-api2.0.git
```

2. **Install poetry:**
```
pip install poetry
```

3. **Install the dependencies:**
```
poetry install --no-root
```

4. **Download and install PostgreSQL**:
   - Visit the [official PostgreSQL download page](https://www.postgresql.org/download/).
   - Ensure PostgreSQL is running and note the credentials for your database setup.

---

## 🚀 Launch
1. First, create a `.env` file by copying `.env.example` and filling in all the required fields.  
*You can also configure additional parameters, such as `JWT_SECRET_KEY`, etc.*

2. **Activate poetry virtual environment**:
```
poetry shell
```

3. **Run project**:
```
poetry run uvicorn src.main:app --reload
```

---

# 🌌 Conclusion
Thank you for your attention. If you like the structure and implementation of the project, feel free to give it a star.  

_✨ Crafted to build knowledge._
