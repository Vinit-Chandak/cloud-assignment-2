from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

# Database Configuration
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=cloud-assignment-2.database.windows.net;DATABASE=Product Information;UID=notadmin;PWD=Admin@474")

# Initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # Optional
app.secret_key = 'your_strong_secret_key'  # Replace with a strong secret string

db = SQLAlchemy(app)

# Product Model (No changes needed)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False) 
    quantity = db.Column(db.Float, nullable=False)

# Initialize the database if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/') 
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        quantity = request.form['quantity']

        # Input Validation 
        if not name:
            flash('Product Name is required', 'danger')
        elif not price:
            flash('Price is required', 'danger')
        elif not quantity:
            flash('Quantity is required', 'danger')
        else:
            try:
                price = float(price)
                quantity = float(quantity)
                new_product = Product(name=name, description=description, price=price, quantity=quantity)
                db.session.add(new_product)
                db.session.commit()
                flash("Product added successfully!", "success")
                return redirect('/')

            except ValueError:
                flash('Price and Quantity must be numeric', 'danger')
            except Exception as e:  # Catch more general database errors 
                flash(f"Error adding product: {str(e)}", "danger")

    return render_template('add_product.html') 

if __name__ == '__main__':
    app.secret_key = 'your_strong_secret_key' 
    app.run(debug=True) 
