# django-junior 🐣

A collection of simple, beginner-friendly Django projects designed to help you learn Django step by step through practical, hands-on examples.

If you're new to Django and looking for small, self-contained projects instead of one giant tutorial, this repo is for you. Each project focuses on a specific concept or feature, so you can pick whatever you want to learn and dive right in.

## 📚 What's Inside

This repository contains a series of mini-projects, each demonstrating a core Django concept, such as:

- Models, views, and templates (MVT basics)
- Forms and form validation
- User authentication (login, logout, signup)
- The Django admin panel
- CRUD operations (Create, Read, Update, Delete)
- Static and media files
- Class-based views vs. function-based views
- Basic REST API examples
- Database relationships (ForeignKey, ManyToMany, etc.)

> Note: Update this list to match the actual projects/folders in your repo.

## 🗂️ Project Structure

```
django-junior/
├── project-01/
├── project-02/
├── project-03/
├── project-04/
├── ...
└── README.md
```

Each folder is a standalone Django project with its own `README.md` explaining what it does and how to run it.

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed
- pip (Python package manager)
- Basic understanding of Python

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/django-junior.git
   cd django-junior
   ```

2. Navigate to a project folder:
   ```bash
   cd project-01-hello-django
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. Open your browser at `http://127.0.0.1:8000/`

## 🎯 Who Is This For?

- Absolute beginners taking their first steps with Django
- Python developers who want a practical, project-based way to learn Django
- Anyone who prefers learning by building small, focused examples over long tutorials

## 🤝 Contributing

Contributions are welcome! If you'd like to add a new beginner-friendly project or improve an existing one:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-project`)
3. Commit your changes
4. Open a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⭐ Support

If you find this repo helpful for learning Django, consider giving it a star — it helps others discover it too!
