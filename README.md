# Ilemela NGO Project

This document provides a step-by-step guide to setting up and running the **Ilemela NGO** project on your local machine.

## Prerequisites
Ensure you have the following installed:
- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Setup Instructions

### 1. Create the Project Directory
```bash
mkdir ilemela-NGO
```

### 2. Clone the Repository
```bash
git clone https://github.com/Dullah2k/ilemela-ngo.git
```

### 3. Navigate into the Project Directory
```bash
cd ilemela-ngo
```

### 4. Set Up Virtual Environment
```bash
python -m venv env
```

### 5. Activate Virtual Environment
#### On Windows:
```bash
.\env\Scripts\activate
```
#### On macOS/Linux:
```bash
source env/bin/activate
```

### 6. Install Dependencies
You can install dependencies using one of the following options:
#### Option 1:
```bash
pip install -r requirements.txt
```
#### Option 2 (Using Tsinghua Mirror):
```bash
pip install -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 7. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

### 9. Access the Application
Open your web browser and go to:
```
http://127.0.0.1:8000/
```

---

## Contributing
Feel free to fork this repository and submit pull requests for improvements.

## License
This project is licensed under the MIT License.

---

### Happy Coding! 🚀
