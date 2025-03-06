# ShopSmart E-Commerce

A full-featured e-commerce platform built with Django.

## Features
- User Authentication
- Product Management
- Shopping Cart
- Order Processing
- Payment Integration (Razorpay)
- Order Tracking
- Password Reset

## Setup
1. Clone the repository
2. Create a virtual environment:
   ```python
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```python
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Create .env file
   - Add necessary credentials (Database, Razorpay, Email)

5. Run migrations:
   ```python
   python manage.py migrate
   ```

6. Create superuser:
   ```python
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```python
   python manage.py runserver
   ```

## Environment Variables
Create a .env file in the project root with:
