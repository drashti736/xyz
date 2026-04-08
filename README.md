# Brand Influencer Platform

A web-based platform built with **Python and Django** that connects **brands with social media influencers**.
Brands can create campaigns and collaborate with influencers, while influencers can discover brand deals and manage partnerships.

---

## 🚀 Features

* 👤 **User Authentication**

  * Secure signup and login
  * Separate roles for **Brands** and **Influencers**

* 📢 **Campaign Management**

  * Brands can create, edit, and delete campaigns
  * Campaign details include budget, requirements, and deadlines

* 🤝 **Influencer Collaboration**

  * Influencers can browse available campaigns
  * Apply or request collaboration with brands

* 📊 **Dashboard**

  * Brand dashboard to manage campaigns
  * Influencer dashboard to track collaborations

* 💬 **Communication System**

  * Messaging or collaboration requests between brands and influencers

* 🔍 **Search & Filters**

  * Brands can search influencers by niche, followers, and engagement
  * Influencers can find campaigns relevant to their category

---

## 🛠 Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript, Bootstrap
* **Database:** SQLite / PostgreSQL
* **Authentication:** Django Authentication System

---

## 📂 Project Structure

```
brand-influencer-platform/
│
├── influencer_platform/     # Main Django project
│
├── accounts/                # User authentication and profiles
├── campaigns/               # Campaign creation and management
├── collaborations/          # Influencer-brand partnerships
│
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
│
├── db.sqlite3               # Database
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/brand-influencer-platform.git
cd brand-influencer-platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run migrations

```bash
python manage.py migrate
```

---

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

---

### 6. Run the development server

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## 📸 Screenshots

Add screenshots of:

* Login Page
* Brand Dashboard
* Influencer Dashboard
* Campaign Creation Page

---

## 🔒 Environment Variables (Optional)

If using external services:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
```

---

## 📈 Future Improvements

* Payment integration for campaigns
* Influencer analytics dashboard
* AI-based influencer recommendations
* Social media API integration
* Notification system

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Developed by **Your Name**

If you like this project, please ⭐ the repository!
