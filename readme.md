# Blog API

Professional Blog API built with Django REST Framework featuring JWT authentication, user profiles, blog posts, categories, and nested comments.

## 🚀 Features

### Authentication & Users
- ✅ JWT Token Authentication
- ✅ User Registration & Login
- ✅ Custom User Model (Email-based login)
- ✅ User Profiles with Avatar Upload
- ✅ Password Hashing & Security

### Blog Management
- ✅ Create, Read, Update, Delete Posts
- ✅ Post Categories
- ✅ Post Status (Draft/Published)
- ✅ Auto-generated Slugs
- ✅ View Counter
- ✅ Search & Filter Posts
- ✅ Rich Text Content

### Comments System
- ✅ Nested Comments (Reply functionality)
- ✅ Comment Moderation
- ✅ CRUD Operations for Comments
- ✅ Author-only Edit/Delete

### Additional Features
- ✅ Swagger API Documentation
- ✅ CORS Support
- ✅ Media File Uploads
- ✅ Customized Admin Panel
- ✅ Permission-based Access Control

---

## 🛠️ Tech Stack

- **Backend Framework:** Django 6.0.1
- **API Framework:** Django REST Framework 3.16.1
- **Authentication:** djangorestframework-simplejwt 5.5.1
- **API Documentation:** drf-yasg 1.21.11
- **Image Processing:** Pillow 12.1.0
- **CORS:** django-cors-headers 4.9.0
- **Database:** SQLite (Development)

---

## 📋 Prerequisites

- Python 3.12+
- pip (Python package manager)
- Virtual environment (recommended)

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd blogAPI
```

### 2. Create virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment
**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser
```bash
python manage.py createsuperuser
```

### 7. Run development server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## 📚 API Documentation

### Swagger UI
Access interactive API documentation at:
```
http://127.0.0.1:8000/swagger/
```

### ReDoc
Alternative documentation view:
```
http://127.0.0.1:8000/redoc/
```

---

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | ❌ |
| POST | `/api/auth/login/` | Login user | ❌ |
| POST | `/api/auth/logout/` | Logout user | ✅ |
| POST | `/api/auth/token/refresh/` | Refresh access token | ❌ |
| GET | `/api/auth/profile/` | Get user profile | ✅ |
| PUT/PATCH | `/api/auth/profile/` | Update profile | ✅ |
| GET | `/api/auth/users/{id}/` | Get user details | ❌ |

### Categories
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/categories/` | List all categories | ❌ |
| POST | `/api/categories/` | Create category | ✅ |
| GET | `/api/categories/{id}/` | Get category details | ❌ |
| PUT/PATCH | `/api/categories/{id}/` | Update category | ✅ |
| DELETE | `/api/categories/{id}/` | Delete category | ✅ |

### Posts
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/posts/` | List published posts | ❌ |
| GET | `/api/posts/my/` | List user's posts | ✅ |
| POST | `/api/posts/create/` | Create new post | ✅ |
| GET | `/api/posts/{slug}/` | Get post details | ❌ |
| PUT/PATCH | `/api/posts/{slug}/update/` | Update post | ✅ (Author only) |
| DELETE | `/api/posts/{slug}/delete/` | Delete post | ✅ (Author only) |

### Comments
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/comments/` | List comments | ❌ |
| POST | `/api/comments/create/` | Create comment | ✅ |
| PUT/PATCH | `/api/comments/{id}/update/` | Update comment | ✅ (Author only) |
| DELETE | `/api/comments/{id}/delete/` | Delete comment | ✅ (Author only) |

---

## 🔐 Authentication

This API uses JWT (JSON Web Token) authentication.

### Getting Tokens

**Register:**
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Login:**
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "user": { ... },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Login muvaffaqiyatli!"
}
```

### Using Tokens

Include the access token in the Authorization header:
```bash
Authorization: Bearer <your_access_token>
```

**Example with cURL:**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     http://127.0.0.1:8000/api/auth/profile/
```

---

## 📝 Example Usage

### Create a Blog Post
```bash
POST /api/posts/create/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Getting Started with Django REST Framework",
  "category": 1,
  "content": "Django REST Framework is a powerful toolkit...",
  "excerpt": "Learn DRF basics",
  "status": "published"
}
```

### Add a Comment
```bash
POST /api/comments/create/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "post": 1,
  "content": "Great article! Very helpful.",
  "parent": null
}
```

### Reply to a Comment
```bash
POST /api/comments/create/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "post": 1,
  "content": "Thank you! Glad it helped.",
  "parent": 1
}
```

---

## 🗂️ Project Structure
```
blogAPI/
├── accounts/                # User authentication & profiles
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py            # Admin customization
│   ├── models.py           # User & Profile models
│   ├── serializers.py      # API serializers
│   ├── urls.py             # Auth URLs
│   └── views.py            # Auth views
├── blog/                    # Blog application
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py            # Blog admin
│   ├── models.py           # Post, Category, Comment models
│   ├── serializers.py      # Blog serializers
│   ├── urls.py             # Blog URLs
│   └── views.py            # Blog views
├── blog_api/                # Project settings
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py
├── media/                   # Uploaded files
│   ├── avatars/
│   └── posts/
├── .venv/                   # Virtual environment
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

---

## 🔧 Configuration

### Settings (blog_api/settings.py)

**JWT Token Lifetime:**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

**CORS Settings:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

**Media Files:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 🧪 Testing with Postman

1. Import the API endpoints into Postman
2. Create a new Collection: "Blog API"
3. Set Collection Authorization to "Bearer Token"
4. Add your access token to the collection
5. All requests will inherit the token

**Recommended Test Flow:**
1. Register a new user
2. Login to get tokens
3. Add token to Collection authorization
4. Create categories
5. Create posts
6. Add comments
7. Test all CRUD operations

---

## 🐛 Common Issues

### Issue: Token expired
**Solution:** Use the refresh token to get a new access token
```bash
POST /api/auth/token/refresh/
{
  "refresh": "your_refresh_token"
}
```

### Issue: CORS errors
**Solution:** Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings.py

### Issue: Media files not loading
**Solution:** Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured correctly

---

## 📦 Requirements

Create `requirements.txt`:
```bash
pip freeze > requirements.txt
```

**Main dependencies:**
```
Django==6.0.1
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
django-cors-headers==4.9.0
drf-yasg==1.21.11
Pillow==12.1.0
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up environment variables
- [ ] Configure static/media file serving
- [ ] Enable HTTPS
- [ ] Set strong `SECRET_KEY`
- [ ] Configure CORS properly

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@shjohnn](https://github.com/shjohnn)
- Email: your.email@example.com

---

## 📄 License

This project is licensed under the BSD License.

---

## 🙏 Acknowledgments

- Django REST Framework Documentation
- JWT Authentication Best Practices
- Community tutorials and resources

---

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact: Shjonbek1702@gmail.com

---

**Built with ❤️ using Django REST Framework**