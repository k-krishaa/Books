from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Product, Category
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('home.html', categories=categories)

# Products routes
@app.route('/products')
def products():
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.title.contains(search) | Product.author.contains(search))
    
    products = query.all()
    categories = Category.query.all()
    return render_template('products.html', products=products, categories=categories)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create categories if not exist
        if Category.query.count() == 0:
            categories = ['Fiction', 'Non-Fiction', 'Science', 'History', 'Biography', 'Children']
            for cat_name in categories:
                category = Category(name=cat_name)
                db.session.add(category)
        
        # Create sample products if not exist
        if Product.query.count() == 0:
            products = [
                Product(title='The Great Gatsby', author='F. Scott Fitzgerald', 
                        description='A classic American novel set in the Jazz Age', price=12.99, stock=50, 
                        category_id=1, image_url='https://covers.openlibrary.org/b/id/7222246-L.jpg'),
                Product(title='To Kill a Mockingbird', author='Harper Lee', 
                        description='A gripping tale of racial injustice and childhood innocence', price=14.99, stock=40, 
                        category_id=1, image_url='https://covers.openlibrary.org/b/id/8228691-L.jpg'),
                Product(title='1984', author='George Orwell', 
                        description='A dystopian social science fiction novel', price=13.99, stock=60, 
                        category_id=1, image_url='https://covers.openlibrary.org/b/id/7222246-L.jpg'),
                Product(title='Sapiens', author='Yuval Noah Harari', 
                        description='A brief history of humankind', price=18.99, stock=30, 
                        category_id=2, image_url='https://covers.openlibrary.org/b/id/8235826-L.jpg'),
                Product(title='Educated', author='Tara Westover', 
                        description='A memoir about a young woman who leaves her survivalist family', price=16.99, stock=25, 
                        category_id=5, image_url='https://covers.openlibrary.org/b/id/8739185-L.jpg'),
                Product(title='A Brief History of Time', author='Stephen Hawking', 
                        description='From the Big Bang to Black Holes', price=15.99, stock=35, 
                        category_id=3, image_url='https://covers.openlibrary.org/b/id/7884607-L.jpg'),
            ]
            for product in products:
                db.session.add(product)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
