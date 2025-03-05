# Markdown File: Breakdown of my "Sticky Notes" Django Application Development

## Research Overview

### How HTTP Applications Preserve State Across Request-Response Cycles, Especially for User Authentication and Session Management?

What I learned was that HTTP is naturally stateless, meaning each request and response operates independently without retaining information from previous interactions. 

To maintain state across multiple requests, web applications like Django use techniques such as cookies, sessions, and tokens:

- **Cookies**: Small text files stored on a user’s device (e.g., computer, smartphone) containing key-value pairs. Managed by the browser, they’re sent back to the server with each request to the same domain.
- **Tokens**: In Django, tokens enhance security, particularly for authentication and preventing Cross-Site Request Forgery (CSRF) attacks. Forms modifying data (POST requests) include `{% csrf_token %}` to verify against the user’s session token.
- **Sessions**: Django’s session framework stores user-specific data across requests, tracking activity (e.g., keeping users logged in) even for anonymous users.

In Django, the state preservation for user authentication and session management relies on its session framework. When a user logs in, Django creates a session on the server, stores relevant data (e.g., user ID) in a database or cache, and sends a unique session ID to the user’s browser via a cookie. On subsequent requests, the browser sends this session ID back, allowing Django to retrieve the user’s session data and maintain a different users activity online, such as keeping the user logged in. This approach bridges the stateless nature of HTTP, ensuring a seamless experience across multiple interactions.

### Procedures for Performing Django Database Migrations to a Server-Based Relational Database Like MariaDB

Django uses SQLite as its default database, which is fine for small projects and local development. However, as your project grows, I may need a more powerful, scalable, and production-ready database like MariaDB (or MySQL, PostgreSQL, etc.). For example, in my task manager app, if multiple users are querying the database while Django processes requests, an overloaded system could slow everything down. A dedicated database server prevents this bottleneck so we can a migrate a Django application to a server-based relational database like MariaDB. 

I would start by setting up the MariaDB server and installing a Python driver, such as `mysqlclient`, to connect Django to MariaDB. In Django’s `settings.py`, I’d have updated the `DATABASES` configuration to use `'ENGINE': 'django.db.backends.mysql'`, specifying the database name, username, password, host, and port. Locally, I’d generate migration files with `python manage.py makemigrations` based on any model changes, then apply those migrations to MariaDB using `python manage.py migrate`. For a production server, I’d deploy the project, install the required dependencies, and run the `migrate` command again. 

1. Set up a MariaDB server and install a Python driver (e.g., `mysqlclient`).
2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'sticky_notes',
           'USER': 'username',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
3. Locally, generate and apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. On the production server, create the database (e.g., `CREATE DATABASE sticky_notes;`), deploy the project, install dependencies, and run `migrate` again.
5. Use environment variables for secure credential management.

Beforehand, I’d would have to created the database schema on MariaDB (e.g., `CREATE DATABASE sticky_notes;`) and use environment variables to securely manage database credentials, ensuring a smooth migration process. This approach not only resolves potential bottlenecks—like those in your task manager app—but also prepares your application for production-ready deployment, ensuring its transition and long-term life.

---

## Practical Task Breakdown: Part 1

### 1. Design Techniques and Principles for the Sticky Notes Application
I applied design principles learned during the bootcamp, focusing on modularity, scalability, and user experience. I created the following diagrams (submitted separately alongside this project):
- **Use Case Diagram**: Illustrated user interactions, such as creating, viewing, editing, and deleting sticky notes, with actors like "User" performing these actions.
- **Sequence Diagram**: Detailed the flow of interactions between the user, views, models, and database for CRUD operations (e.g., a user submits a form, triggering a view to save data to the database).
- **Class Diagram**: Modeled the `Note` class with attributes (`title`, `content`, `created_at`, `updated_at`) and relationships, ensuring a clear structure for the application.

These diagrams guided the development process, ensuring a well-structured and user-friendly application.

### 2. Create a New Django Project Called `sticky_notes`
I created the project using:
```bash
django-admin startproject Sticky_Notes
cd Sticky_Notes
```
This generated the project structure with `manage.py` and the `Sticky_Notes` directory for settings.

### 3. Install the App in `settings.py` and Configure the Project
I created a `notes` app:
```bash
python manage.py startapp notes
```
Then, I updated `Sticky_Notes/settings.py` to include the app:
```python
INSTALLED_APPS = [
    ...
    'notes.apps.NotesConfig',
]
```
I also configured static files for CSS and images:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "notes/static",
]
```

### 4. Design and Define the Model for the Sticky Notes Application
I defined the `Note` model in `notes/models.py`:
```python
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

### 5. Implement and Run Database Migrations
I ran the following commands to apply the model to the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
This created the necessary tables in the SQLite database (default for development) or MariaDB if configured.

### 6. Develop Views for CRUD Functionality
I implemented views in `notes/views.py` to handle Create, Read, Update, and Delete operations:
```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm

def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/note_list.html', {'notes': notes})

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')
    return render(request, 'notes/note_confirm.html', {'note': note})
```

### 7. Build Forms for Sticky Notes Content
I created `notes/forms.py` to handle note input and editing:
```python
from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
```

### 8. Set Up URL Patterns
I configured `notes/urls.py` for the app’s URLs:
```python
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('create/', views.note_create, name='note_create'),
    path('<int:pk>/update/', views.note_update, name='note_update'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),
]
```
Then, I included these in `Sticky_Notes/urls.py`:
```python
from django.contrib import admin
from django.urls import include, path, redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),
    path('', lambda request: redirect('notes:note_list'), name='root'),
]
```

### 9. Create a Base HTML Template
I created `notes/templates/notes/base.html` as the foundation for other templates:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sticky Notes {% block title %}{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'notes/css/styles.css' %}">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="{% url 'notes:note_list' %}">Sticky Notes</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'notes:note_create' %}">Add Note</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>

    <!-- Bootstrap JS (for modals, etc.) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
```

### 10. Design HTML Templates for Displaying Sticky Notes
I created specific templates in `notes/templates/notes/`:
- **`note_list.html`**:
  ```html
  {% extends 'notes/base.html' %}
  {% block title %} - Home{% endblock %}

  {% block content %}
      <h1 class="mb-4 text-center">Your Sticky Notes</h1>
      <div class="row">
          {% for note in notes %}
              <div class="col-md-4 mb-4">
                  <div class="card h-100 shadow-sm">
                      <div class="card-body">
                          <h5 class="card-title">{{ note.title }}</h5>
                          <p class="card-text">{{ note.content|truncatewords:20 }}</p>
                      </div>
                      <div class="card-footer bg-transparent">
                          <a href="{% url 'notes:note_update' note.pk %}" class="btn btn-primary btn-sm">Edit</a>
                          <form method="post" action="{% url 'notes:note_delete' note.pk %}" style="display:inline;">
                              {% csrf_token %}
                              <button type="submit" class="btn btn-danger">Delete</button>
                          </form>
                      </div>
                  </div>
              </div>

              <!-- Delete Confirmation Modal -->
              <div class="modal fade" id="deleteModal{{ note.pk }}" tabindex="-1" aria-labelledby="deleteModalLabel{{ note.pk }}" aria-hidden="true">
                  <div class="modal-dialog">
                      <div class="modal-content">
                          <div class="modal-header">
                              <h5 class="modal-title" id="deleteModalLabel{{ note.pk }}">Confirm Delete</h5>
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                          </div>
                          <div class="modal-body">
                              Are you sure you want to delete "{{ note.title }}"?
                          </div>
                          <div class="modal-footer">
                              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                              <form method="post" action="{% url 'notes:note_delete' note.pk %}" style="display:inline;">
                                  {% csrf_token %}
                                  <button type="submit" class="btn btn-danger">Delete</button>
                              </form>
                          </div>
                      </div>
                  </div>
              </div>
          {% empty %}
              <div class="col-12 text-center">
                  <p class="text-muted">No notes yet. Add one above!</p>
              </div>
          {% endfor %}
      </div>
  {% endblock %}
  ```
- **`note_form.html`**:
  ```html
  {% extends 'notes/base.html' %}
  {% load form_tags %}
  {% block title %} - {% if form.instance.pk %}Edit{% else %}Add{% endif %} Note{% endblock %}

  {% block content %}
      <h1 class="mb-4">{% if form.instance.pk %}Edit Note{% else %}Add New Note{% endif %}</h1>
      <div class="row justify-content-center">
          <div class="col-md-8">
              <div class="card">
                  <div class="card-body">
                      <form method="post">
                          {% csrf_token %}
                          <div class="mb-3">
                              <label for="{{ form.title.id_for_label }}" class="form-label">Title</label>
                              {{ form.title|add_attrs:"class:form-control" }}
                          </div>
                          <div class="mb-3">
                              <label for="{{ form.content.id_for_label }}" class="form-label">Content</label>
                              {{ form.content|add_attrs:"class:form-control|rows:5" }}
                          </div>
                          <button type="submit" class="btn btn-success">Save</button>
                          <a href="{% url 'notes:note_list' %}" class="btn btn-secondary">Cancel</a>
                      </form>
                  </div>
              </div>
          </div>
      </div>
  {% endblock %}
  ```
- **`note_confirm.html`**:
  ```html
  {% extends 'notes/base.html' %}
  {% block title %} - Delete Note{% endblock %}

  {% block content %}
      <h1 class="mb-4">Delete Note</h1>
      <div class="row justify-content-center">
          <div class="col-md-6">
              <div class="card">
                  <div class="card-body">
                      <p>Are you sure you want to delete "{{ note.title }}"?</p>
                      <form method="post">
                          {% csrf_token %}
                          <button type="submit" class="btn btn-danger">Delete</button>
                          <a href="{% url 'notes:note_list' %}" class="btn btn-secondary">Cancel</a>
                      </form>
                  </div>
              </div>
          </div>
      </div>
  {% endblock %}
  ```

### 11. Style the Application with CSS
I added CSS in `notes/static/notes/css/style.css` to enhance the visual appeal, using Bootstrap for faster development:
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
}

.corkboard {
    background-image: url('../images/corkboard.jpg');
    background-size: cover;
    padding: 20px;
}

.sticky-note {
    background-color: yellow;
    padding: 10px;
    margin: 10px;
    border: 1px solid #ccc;
    position: relative;
}

.sticky-note::after {
    content: url('../images/pin.png');
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
}
```

### 12. Configure Static Files
I ensured static files were collected into a designated directory by configuring `settings.py` as described in Step 3. I placed images (`corkboard.jpg`, `pin.png`) in `notes/static/notes/images/`.

### 13. Rerun Migrations and Test the Application
I verified migrations and tested the app:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
I accessed `http://127.0.0.1:8000/notes/` to test CRUD functionality, ensuring notes could be created, viewed, edited, and deleted with a corkboard-style interface.

### 14. Exclude the `venv` Folder
I excluded the `.venv` folder from my project submission, as it’s unnecessary for review (mentors can recreate it). I also avoided including generated files like migration files or compiled Python files to keep the project lightweight and portable.

### 15. Additional Testing and Debugging for the Future
After running the application and interacting with it, I identified and found a few bugs. These included:
- **User/Account Authentications**: My next version will have a user authengtication for multiple accounts/sessions to view protected knotes and information.
- **Styling Adjustments**: I want to make more minor adjustments to the CSS to improve the user interface, including tweaking the layout of the sticky notes and using images in the background stylesheet.
- **Error Handling**: I could have added error handling for potential issues, such as when a user tries to update or delete a note that doesn’t exist.

### 16. Future Deployment 
Finally, in the future I want to prepare the application for deployment:
- From how to set up a production database (MariaDB) by updating my settings to use this powerful database instead of SQLite, and applying its migrations.
- Also, know how to configure the `ALLOWED_HOSTS` setting in `settings.py` to include the production server domains.

---

### Conclusion
The Sticky Notes Django application is now fully functional, with the ability to create, view, update, and delete sticky notes. By applying best practices in Django development—such as using models, forms, and views—I was able to create a scalable and maintainable application. Additionally, I applied front-end design principles and made sure the app is ready for production deployment. I still work how design specfic styles for the website but this project has helped solidify my understanding of Django’s core features, as well as web development concepts in general and I will continue to practice my craft.

---

## Bibliography

- Django Software Foundation. *Django Documentation*. https://docs.djangoproject.com/en/stable/
- Python Software Foundation. *Python Documentation*. https://docs.python.org/3/
- Mozilla Developer Network. *HTTP Cookies*. https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
- Django REST Framework. *Token Authentication*. https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
- Django Software Foundation. *Django Sessions*. https://docs.djangoproject.com/en/stable/ref/sessions/
- MariaDB Foundation. *MariaDB Documentation*. https://mariadb.org/
- Bootstrap. *Bootstrap Documentation*. https://getbootstrap.com/docs/5.3/
- W3Schools. *CSS Tutorial*. https://www.w3schools.com/css/
- Stack Overflow. "CRUD Operations in Django." https://stackoverflow.com/questions/15274016/creating-crud-operations-in-django
- Simple is Better Than Complex. "How to Use Bootstrap with Django." https://simpleisbetterthancomplex.com
- Django Software Foundation. *Django ORM Queries*. https://docs.djangoproject.com/en/stable/topics/db/queries/
