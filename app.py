from flask import Flask, render_template
from models import db, Category
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Home route
@app.route('/')
def home():
    categories = Category.query.all()
    return render_template('home.html', categories=categories)

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
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
