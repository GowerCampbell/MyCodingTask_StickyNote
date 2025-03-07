
# Sticky Notes Application - README

<img src="staticfiles/images/layout.png" alt="My Image" width="1200" style="display: block; margin: 0 auto;">


## Overview
The Sticky Notes Application is my first Django-based web application designed to help users create, view, update, and delete personal sticky notes. With a vintage paper aesthetic and a corkboard-inspired interface, it offers a simple yet engaging tool for note management. Built with Django's core features—models, views, forms, and templates—and enhanced with Bootstrap and custom CSS, this project combines robust backend functionality with a user-friendly front-end design.

This application is production-ready and extensible, making it an excellent foundation for further customization. As of March 06, 2025, it reflects modern web development practices and my ongoing efforts to refine its design and functionality.

## Features

### User Authentication
- **Register, Log In, Log Out**: Secure user authentication with a custom user model (`CustomUser`) that includes additional fields like `bio`.
- **Responsive Templates**: Authentication pages styled as sticky notes pinned to a corkboard background.

### Sticky Notes Management
- **CRUD Operations**: Create, read, update, and delete sticky notes with ease.
- **Drag-and-Drop**: Notes can be repositioned on the corkboard, with positions saved using local storage for persistence across sessions.
- **Delete Confirmation**: A modal prompts users to confirm deletions, enhancing the user experience.

### Front-End Design
- **Bootstrap 5.3**: Provides a clean, modern layout via CDN integration.
- **Custom CSS**: Vintage paper texture for sticky notes, a corkboard background, and a pinned-note aesthetic with hover effects.
- **Responsive Design**: Adapts seamlessly to various screen sizes, including mobile devices.

### Backend
- **Django ORM**: Manages database interactions efficiently.
- **SQLite Database**: Default setup, easily swappable for PostgreSQL or MySQL.
- **Security**: Includes CSRF protection and secure authentication practices.

## Installation

### Prerequisites
- **Python**: 3.8 or higher
- **Django**: 5.1 or higher
- **Bootstrap**: 5.3 (included via CDN)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/sticky-notes-app.git
   cd sticky-notes-app
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage

### Register and Log In
- **Register**: Visit `http://127.0.0.1:8000/accounts/register/` to create an account.
- **Log In**: Use your credentials at `http://127.0.0.1:8000/accounts/login/`.

### Manage Sticky Notes
- **Create a Note**: Click "Add Note" in the navbar, fill out the form, and submit.
- **Edit a Note**: Click "Edit" on a sticky note, update it, and save changes.
- **Delete a Note**: Click "Delete," confirm in the modal, and the note is removed.
- **Reposition Notes**: Drag notes by their pins; positions persist via local storage.

## Project Structure
```
sticky_notes/
├── accounts/                  # User authentication and management
│   ├── migrations/            # Database migrations
│   ├── templates/             # Authentication templates (login, logout, register)
│   ├── admin.py               # Admin configuration
│   ├── apps.py                # App configuration
│   ├── forms.py               # Forms for registration and login
│   ├── models.py              # CustomUser model
│   ├── urls.py                # URL routing for accounts
│   ├── views.py               # Authentication views
├── notes/                     # Sticky notes functionality
│   ├── migrations/            # Database migrations
│   ├── templates/             # Notes templates (list, create, update)
|   |── templatetags/          # Custom Filters
│   ├── admin.py               # Admin configuration
│   ├── apps.py                # App configuration
│   ├── forms.py               # Forms for notes
│   ├── models.py              # Note model
│   ├── urls.py                # URL routing for notes
│   ├── views.py               # Notes views
├── static/                    # Static files
│   ├── css/                   # Custom CSS (style.css)
│   └── images/                # Images (e.g., pin.png, corkboard.jpg)
├── templates/                 # Base templates
│   └── base.html              # Base template for all pages
├── manage.py                  # Django management script
├── requirements.txt           # Dependencies
├── README.md
└── sticky_notes/              # Project settings
    ├── settings.py            # Django settings
    ├── urls.py                # Main URL routing
    ├── wsgi.py                # WSGI configuration
    └── asgi.py                # ASGI configuration
```

---

## Customization

### Add Custom Fields to the User Model
Modify `accounts/models.py` to extend `CustomUser`:
```python
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
```

### Change the Database
I should learn how to switch from SQLite to PostgreSQL or MySQL by updating `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Add More Features
- **Tags**: Add a `tags` field to the `Note` model for categorization and filtering.
- **Search**: Implement a search bar to filter notes by title or content.
- **Enhanced Drag-and-Drop**: Persist note positions in the database instead of local storage.

---

## Conclusion
The Sticky Notes Application is a fully functional Django project as of March 06, 2025, showcasing CRUD operations, user authentication, and a visually appealing corkboard interface. By leveraging Django’s best practices and enhancing it with custom styling, I’ve created a scalable and maintainable tool. I continue to refine its design—particularly the vintage aesthetic—and deepen my expertise in web development through this project.

---

## Bibliography
- Django Software Foundation. *Django Documentation*. https://docs.djangoproject.com/en/stable/
- Python Software Foundation. *Python Documentation*. https://docs.python.org/3/
- Mozilla Developer Network. *HTTP Cookies*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
- Bootstrap. *Bootstrap Documentation*. https://getbootstrap.com/docs/5.3/
- W3Schools. *CSS Tutorial*. https://www.w3schools.com/css/
- Simple is Better Than Complex. *How to Use Bootstrap with Django*. https://simpleisbetterthancomplex.com

---

## Author
- **[Gower Campbell]**
- **[[Gower.Campbell@gmail.com]]**
- **[[Github](https://github.com/GowerCampbell)]**

## Acknowledgments
- Gratitude to the HyperionDev for their comprehensive documentation and support.
- Thanks to Bootstrap for a robust front-end framework that streamlined development.

---# codingTasks
