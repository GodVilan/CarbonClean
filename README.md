# CarbonClean 🌱

**Measure. Manage. Minimize.**

CarbonClean is a full-stack web application designed to help individuals understand, track, and reduce their carbon footprint. The platform allows users to calculate carbon emissions based on daily activities, view detailed reports, and receive personalized recommendations to promote sustainable living.

## 📌 Features

- 🔐 **User Authentication** (Register, Login, Password Reset)
- 📊 **Carbon Emission Calculation**
  - Household energy usage
  - Transportation habits
  - Industrial/manufacturing activities
- 🗂️ **Emission History & Reports**
- 💡 **Personalized Recommendations** to reduce emissions
- 🧾 **CRUD Operations** for user data and emission records
- 👥 **Multi-user & Multi-role support**
- 🔒 **Strong Security Practices** (CSRF, HTTPS cookies, session security)

---

## 🛠️ Tech Stack

### Backend
- **Python**
- **Django** (MVC framework)
- **MySQL** (Relational Database)
- **Azure Database for MySQL**

### Frontend
- **HTML5**
- **CSS3** (Flexbox & Grid for responsive UI)
- **JavaScript**
- **Django Templates**

### Deployment
- **Azure App Service**

---

## 🗄️ Database Design

The database is designed to efficiently store and manage emission-related data.

### Key Tables
- `Users` – User profiles and authentication data
- `Carbon_Emission_Records` – Emission data by category and subcategory
- `Emission_Factors` – Predefined factors used for calculations
- `Recommendations` – Personalized emission reduction suggestions
- `Activity_Logs` – User interactions and history

The schema follows relational design principles and supports scalability, concurrency control, and data integrity.

---

## 🧩 Use Case Overview

- Guest users can explore information about causes, effects, and solutions
- Registered users can:
  - Input activity data
  - Calculate emissions
  - View reports and history
  - Receive recommendations
  - Manage profile and delete data

---

## 🔐 Security Features

- Restricted allowed hosts
- CSRF protection enabled
- HTTPS-only session cookies
- Strong password validation
- Secure email configuration using environment variables
- Clickjacking and middleware protections

---

## ⚙️ Installation & Setup (Local)

```bash
# Clone the repository
git clone https://github.com/GodVilan/CarbonClean.git
cd CarbonClean

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# (Database credentials, email settings, secret key)

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
```

## 🎯 Project Goal

CarbonClean aims to raise awareness about carbon emissions and empower users to make eco-conscious decisions by providing actionable insights and data-driven recommendations.

---

## 📄 License

This project is developed for academic purposes. You are free to explore and learn from the codebase.

---

✨ *Small actions, when multiplied by millions of people, can transform the world.*

