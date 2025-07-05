# 🪪 Business Card API (Django REST Framework)

This is a Django REST API application that allows users to create and manage multiple digital business cards. Each business card can act as a mini-website containing:

- Business profile
- Address
- Contact info
- Social media links
- Services offered
- Image gallery

Users can access business card data publicly using a **unique name slug**.

---

## 📁 Features

✅ JWT-based authentication  
✅ Role-based access (only owners can manage their cards)  
✅ Public endpoint to view a card by unique name  
✅ Modular and scalable design  
✅ RESTful API with filtering & permissions  
✅ Ready for deployment (Docker, gunicorn, etc. optional)

---

## 📦 Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- Simple JWT
- SQLite/PostgreSQL
- Pillow (for image uploads)

---

## 🔧 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourname/business-card-api.git
cd business-card-api
```
