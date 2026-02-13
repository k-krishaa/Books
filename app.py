from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Product, Category, CartItem, Wishlist, Order, OrderItem
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
    sort = request.args.get('sort', 'name_asc')
    
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.title.contains(search) | Product.author.contains(search))
    
    # Sorting
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'name_desc':
        query = query.order_by(Product.title.desc())
    else:  # name_asc
        query = query.order_by(Product.title.asc())
    
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

# Contact route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# Cart routes
@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(request.referrer or url_for('products'))

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    quantity = int(request.form['quantity'])
    
    if quantity > 0:
        cart_item.quantity = quantity
    else:
        db.session.delete(cart_item)
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'success')
    return redirect(url_for('cart'))

# Context processor for cart count
@app.context_processor
def cart_count():
    if current_user.is_authenticated:
        count = CartItem.query.filter_by(user_id=current_user.id).count()
        wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()
        return {'cart_count': count, 'wishlist_count': wishlist_count}
    return {'cart_count': 0, 'wishlist_count': 0}

# Wishlist routes
@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/add_to_wishlist/<int:product_id>')
@login_required
def add_to_wishlist(product_id):
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if not existing:
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Added to wishlist!', 'success')
    else:
        flash('Already in wishlist!', 'info')
    
    return redirect(request.referrer or url_for('products'))

@app.route('/remove_from_wishlist/<int:item_id>')
@login_required
def remove_from_wishlist(item_id):
    wishlist_item = Wishlist.query.get_or_404(item_id)
    db.session.delete(wishlist_item)
    db.session.commit()
    flash('Removed from wishlist', 'success')
    return redirect(url_for('wishlist'))

# Checkout routes
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('products'))
    
    if request.method == 'POST':
        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order(user_id=current_user.id, total=total, status='completed')
        db.session.add(order)
        
        for item in cart_items:
            order_item = OrderItem(order=order, product_id=item.product_id, 
                                   quantity=item.quantity, price=item.product.price)
            db.session.add(order_item)
            
            product = Product.query.get(item.product_id)
            product.stock -= item.quantity
        
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/order_confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('home'))
    
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total)).scalar() or 0
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_orders=total_orders, 
                         total_users=total_users,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('home'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        product = Product(
            title=request.form['title'],
            author=request.form['author'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            category_id=int(request.form['category_id']),
            image_url=request.form['image_url']
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(id):
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('home'))
    
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.title = request.form['title']
        product.author = request.form['author']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category_id = int(request.form['category_id'])
        product.image_url = request.form['image_url']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/product/delete/<int:id>')
@login_required
def admin_delete_product(id):
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('home'))
    
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))

# User order history
@app.route('/my-orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

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
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@bookstore.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create sample products if not exist
        if Product.query.count() == 0:
            products = [
                # Fiction
                Product(title='The Great Gatsby', author='F. Scott Fitzgerald', 
                        description='A classic American novel set in the Jazz Age', price=12.99, stock=50, 
                        category_id=1, image_url='https://covers.openlibrary.org/b/id/7222246-L.jpg'),
                Product(title='To Kill a Mockingbird', author='Harper Lee', 
                        description='A gripping tale of racial injustice and childhood innocence', price=14.99, stock=40, 
                        category_id=1, image_url='https://covers.openlibrary.org/b/id/8228691-L.jpg'),
                Product(title='1984', author='George Orwell', 
                        description='A dystopian social science fiction novel', price=13.99, stock=60, 
                        category_id=1, image_url='https://covers.openlibrary.org/b/id/7222246-L.jpg'),
                Product(title='Pride and Prejudice', author='Jane Austen', 
                        description='A romantic novel of manners', price=11.99, stock=45, 
                        category_id=1, image_url='https://covers.openlibrary.org/b/id/8235886-L.jpg'),
                # Non-Fiction
                Product(title='Sapiens', author='Yuval Noah Harari', 
                        description='A brief history of humankind', price=18.99, stock=30, 
                        category_id=2, image_url='https://covers.openlibrary.org/b/id/8235826-L.jpg'),
                Product(title='Atomic Habits', author='James Clear', 
                        description='An easy and proven way to build good habits', price=16.99, stock=55, 
                        category_id=2, image_url='https://covers.openlibrary.org/b/id/10958382-L.jpg'),
                Product(title='Thinking, Fast and Slow', author='Daniel Kahneman', 
                        description='Explores the two systems that drive the way we think', price=17.99, stock=35, 
                        category_id=2, image_url='https://covers.openlibrary.org/b/id/7897651-L.jpg'),
                # Science
                Product(title='A Brief History of Time', author='Stephen Hawking', 
                        description='From the Big Bang to Black Holes', price=15.99, stock=35, 
                        category_id=3, image_url='https://covers.openlibrary.org/b/id/7884607-L.jpg'),
                Product(title='Cosmos', author='Carl Sagan', 
                        description='A journey through space and time', price=14.99, stock=40, 
                        category_id=3, image_url='https://covers.openlibrary.org/b/id/6979861-L.jpg'),
                Product(title='The Selfish Gene', author='Richard Dawkins', 
                        description='A gene-centered view of evolution', price=13.99, stock=30, 
                        category_id=3, image_url='https://covers.openlibrary.org/b/id/8235890-L.jpg'),
                # History
                Product(title='The Diary of a Young Girl', author='Anne Frank', 
                        description='The writings from the Dutch language diary', price=12.99, stock=50, 
                        category_id=4, image_url='https://covers.openlibrary.org/b/id/8235891-L.jpg'),
                Product(title='Guns, Germs, and Steel', author='Jared Diamond', 
                        description='The fates of human societies', price=16.99, stock=25, 
                        category_id=4, image_url='https://covers.openlibrary.org/b/id/8235892-L.jpg'),
                # Biography
                Product(title='Educated', author='Tara Westover', 
                        description='A memoir about a young woman who leaves her survivalist family', price=16.99, stock=25, 
                        category_id=5, image_url='https://covers.openlibrary.org/b/id/8739185-L.jpg'),
                Product(title='Steve Jobs', author='Walter Isaacson', 
                        description='The exclusive biography', price=19.99, stock=30, 
                        category_id=5, image_url='https://covers.openlibrary.org/b/id/8235893-L.jpg'),
                Product(title='Becoming', author='Michelle Obama', 
                        description='Memoir by the former First Lady', price=18.99, stock=40, 
                        category_id=5, image_url='https://covers.openlibrary.org/b/id/8739186-L.jpg'),
                # Children
                Product(title='Harry Potter and the Sorcerer\'s Stone', author='J.K. Rowling', 
                        description='The first book in the Harry Potter series', price=14.99, stock=60, 
                        category_id=6, image_url='https://covers.openlibrary.org/b/id/10521270-L.jpg'),
                Product(title='The Cat in the Hat', author='Dr. Seuss', 
                        description='A classic children\'s book', price=9.99, stock=70, 
                        category_id=6, image_url='https://covers.openlibrary.org/b/id/8235894-L.jpg'),
                Product(title='Charlotte\'s Web', author='E.B. White', 
                        description='A story of friendship and loyalty', price=11.99, stock=55, 
                        category_id=6, image_url='https://covers.openlibrary.org/b/id/8235895-L.jpg'),
            ]
            for product in products:
                db.session.add(product)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
