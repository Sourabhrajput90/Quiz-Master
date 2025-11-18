# Quiz_Master

A fully functional Quiz Application built using Python (Django) and Bootstrap.
Users can take quizzes, view their scores instantly, and admins can easily manage quiz content through Django Admin.

📌 Repository

🔗 GitHub: https://github.com/Sourabhrajput90/quiz_master

✨ Features Overview
Feature	Description
📝 Quiz Management	Create, update, and delete quizzes via Django Admin
❓ MCQ Support	Add multiple-choice questions with correct answers
📊 Auto Scoring	Score calculation after each quiz attempt
📱 Responsive UI	Clean Bootstrap-based user interface
🔐 Admin Panel	Full control over quizzes & questions
⚡ Fast & Lightweight	Uses Django ORM and simple Bootstrap frontend
🛠️ Tech Stack
Backend

Python 3

Django Framework

Frontend

HTML5

CSS3

Bootstrap 4/5

Database

SQLite (default, easy setup)

🚀 Getting Started

Follow the steps below to run the project locally.

1️⃣ Clone the repository
git clone https://github.com/Sourabhrajput90/quiz_master.git
cd quiz_master

2️⃣ Create and activate a virtual environment
Windows
python -m venv venv
venv\Scripts\activate

macOS / Linux
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Apply migrations
python manage.py migrate

5️⃣ Run the server
python manage.py runserver


Open in browser:
👉 http://127.0.0.1:8000/

👨‍💼 Admin Panel

Create a superuser:

python manage.py createsuperuser


Admin login:
👉 http://127.0.0.1:8000/admin

📂 Project Structure
quiz_master/
│
├── quiz/               # Main quiz app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── static/             # CSS, JS, images
├── templates/          # Global templates
├── quiz_master/        # Project settings and URLs
├── manage.py
└── requirements.txt

If you want, I can help you create a GIF from screen recording.

⭐ Support the Project

If you like this project, please give it a ⭐ star on GitHub!
It motivates further development 😊

🤝 Contributing

Contributions are welcome!
Feel free to submit issues or pull requests.
