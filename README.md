# Library Management System 

## About the Project
The Library Management System is a Django-based web application designed to manage library operations efficiently. It allows librarians to manage books, track loans, and handle user registrations, providing a simple system for all library activities.

## System Requirements
- **Operating System:** Windows / Linux
- **Libraries:** Listed in the `requirements.txt` file

## Installation and first launch
To set up the Library Management System on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YahooMing/Zarzadzanie-Biblioteka.git
   cd <repository_directory>
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv env
   ```
4. **Activate the virtual environment:**
   On Windows:
   ```bash
   .\env\Scripts\activate
   ```
   On Unix or MacOS:
   ```bash
   source env/bin/activate
   ```
4. **Install the required libraries:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
6. **Create a superuser to access the admin panel:**
   ```bash
   python manage.py createsuperuser
   ```
7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
8. **Access the application:**
   
   Open your web browser and go to http://127.0.0.1:8000 to see the Library Management System in action.

## Additional Notes
Make sure you have Python installed on your system. You can download it from the official Python website.
For more advanced configurations and deployment instructions, refer to the official Django documentation.
Enjoy managing your library with ease using the Library Management System!
