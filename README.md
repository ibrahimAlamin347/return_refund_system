# Return and Refund System

A Django-based web application for managing product returns and refunds. This system allows users to submit return requests, refund requests, and handle disputes.

## Features

- Submit return requests
- Process refund requests
- Handle customer disputes
- User-friendly forms
- Modern UI design

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd return_refund_system
```

2. Create a virtual environment and activate it:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## License

This project is licensed under the MIT License. 