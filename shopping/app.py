from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'yoursecretkey'

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT, image TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:id>')
def product(id):
    conn = sqlite3.connect('database.db')
    product = conn.execute('SELECT * FROM products WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if "cart" not in session:
        session['cart'] = []
    session['cart'].append(id)
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if "cart" not in session:
        return render_template('cart.html', cart_items=[], total=0)
    conn = sqlite3.connect('database.db')
    items = []
    total = 0
    for pid in session['cart']:
        product = conn.execute('SELECT * FROM products WHERE id=?', (pid,)).fetchone()
        items.append(product)
        total += product[2]
    conn.close()
    return render_template('cart.html', cart_items=items, total=total)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO users (username, password) VALUES (?,?)', (uname, pwd))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('database.db')
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (uname, pwd)).fetchone()
        conn.close()
        if user:
            session['user'] = uname
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        desc = request.form['description']
        image = request.form['image']
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO products (name, price, description, image) VALUES (?,?,?,?)',
                     (name, price, desc, image))
        conn.commit()
        conn.close()
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# Insert sample products if table is empty
products = c.execute('SELECT * FROM products').fetchall()
if not products:
    c.execute("INSERT INTO products (name, price, description, image) VALUES (?, ?, ?, ?)",
              ("Demo Product", 99.99, "This is a sample product", "https://via.placeholder.com/150"))

conn.commit()
