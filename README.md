Online Bookstore - Full Stack Web Application

A modern, feature-rich online bookstore built with Flask and Bootstrap 5.

FEATURES

Core Features
- User Authentication (Register, Login, Logout)
- Product Catalog with 18+ Books
- Advanced Search & Filters (Price, Author, Category)
- Shopping Cart with Real-time Updates
- Wishlist Functionality
- Checkout & Order Processing
- Order History
- Admin Dashboard

Advanced Features
- Best Sellers Section (Dynamic)
- Stock Indicators (Low Stock, Out of Stock)
- Product Sorting (Name, Price)
- Social Media Sharing
- Responsive Design (Mobile, Tablet, Desktop)
- Professional UI with Animations

TECH STACK

Backend:
- Python 3.x
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- SQLite Database

Frontend:
- HTML5
- CSS3 (Custom + Bootstrap 5)
- JavaScript
- Bootstrap 5.3.0
- Bootstrap Icons

INSTALLATION

1. Clone the repository
git clone <repository-url>
cd Book

2. Install dependencies
pip install -r requirements.txt

3. Run the application
python app.py

4. Access the application
http://127.0.0.1:5000

DEFAULT ADMIN ACCOUNT

Username: admin
Password: admin123
Email: admin@bookstore.com

PROJECT STRUCTURE

Book/
├── app.py                 (Main application file)
├── models.py              (Database models)
├── config.py              (Configuration settings)
├── requirements.txt       (Python dependencies)
├── static/
│   └── css/
│       └── style.css      (Custom styles)
├── templates/
│   ├── base.html          (Base template)
│   ├── home.html          (Homepage)
│   ├── products.html      (Books listing)
│   ├── product_detail.html
│   ├── cart.html
│   ├── wishlist.html
│   ├── checkout.html
│   ├── order_confirmation.html
│   ├── my_orders.html
│   ├── contact.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── admin/
│       ├── dashboard.html
│       ├── products.html
│       ├── add_product.html
│       └── edit_product.html
└── instance/
    └── bookstore.db       (SQLite database)

FEATURES BREAKDOWN

User Features:
- Browse books by category
- Search books by title/author
- Filter by price range
- Add books to cart
- Save books to wishlist
- Place orders
- View order history
- Share books on social media

Admin Features:
- View dashboard with statistics
- Add new books
- Edit existing books
- Delete books
- View all orders
- Manage inventory

BONUS FEATURES IMPLEMENTED

- Admin Panel (+5 marks)
- Advanced Search & Filters (+3 marks)
- Social Media Integration (+2 marks)

Total Bonus: +10 marks

DESIGN HIGHLIGHTS

- Modern color scheme (Blue/Purple gradient)
- Smooth animations and transitions
- Hover effects on cards
- Professional typography (Inter font)
- Responsive navbar with dropdown
- Best sellers section with rankings
- Stock status indicators
- Star ratings display

DATABASE SCHEMA

Tables:
- Users (id, username, email, password_hash, is_admin)
- Products (id, title, author, description, price, stock, category_id, image_url)
- Categories (id, name)
- CartItems (id, user_id, product_id, quantity)
- Wishlist (id, user_id, product_id, created_at)
- Orders (id, user_id, total, status, created_at)
- OrderItems (id, order_id, product_id, quantity, price)

KEY FUNCTIONALITIES

1. Authentication System
   - Secure password hashing
   - Session management
   - Login required decorators

2. Shopping Cart
   - Add/Update/Remove items
   - Real-time cart count badge
   - Stock validation

3. Order Management
   - Order processing
   - Stock reduction
   - Order history tracking

4. Admin Dashboard
   - Product CRUD operations
   - Sales statistics
   - User management

LEARNING OUTCOMES

- Full-stack web development
- Database design and relationships
- User authentication and authorization
- RESTful routing
- Responsive web design
- State management
- Form validation
- Security best practices

COMMON ERRORS AND SOLUTIONS

1. Database Locked Error
   Problem: "database is locked" error when running the application
   Solution: Stop all running Python processes and delete the database file
   Command: taskkill /F /IM python.exe && del instance\bookstore.db
   Then restart the application with: python app.py

2. Import Error
   Problem: "No module named 'flask'" or similar import errors
   Solution: Install all required dependencies
   Command: pip install -r requirements.txt

3. Template Not Found Error
   Problem: "TemplateNotFound" error
   Solution: Ensure all template files are in the correct folders
   Check that templates/ folder structure matches the project structure above

4. Login Required Error
   Problem: Redirected to login page when accessing cart or wishlist
   Solution: This is expected behavior - users must be logged in to access these features
   Create an account or login with admin credentials

FUTURE ENHANCEMENTS

- Payment gateway integration
- Email notifications
- Product reviews and ratings
- Advanced analytics
- Multi-language support
- PDF invoice generation

DEVELOPER

Created as a full-stack web development project demonstrating modern web technologies and best practices.

LICENSE

This project is created for educational purposes.

Made with Flask and Bootstrap
