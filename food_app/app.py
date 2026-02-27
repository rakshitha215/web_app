from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# ===============================
# DATABASE INITIALIZATION
# ===============================
def init_db():
    conn = sqlite3.connect("food.db")
    cursor = conn.cursor()

    # Restaurant Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurant (
        restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT
    )
    """)

    # Food Item Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_item (
        food_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        restaurant_id INTEGER,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
    )
    """)

    # Delivery Person Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS delivery_person (
        delivery_person_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    # Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT,
        delivery_person_id INTEGER,
        FOREIGN KEY (delivery_person_id) REFERENCES delivery_person(delivery_person_id)
    )
    """)

    # Order Item Table (M:N)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_item (
        order_id INTEGER,
        food_id INTEGER,
        quantity INTEGER,
        subtotal REAL,
        PRIMARY KEY (order_id, food_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (food_id) REFERENCES food_item(food_id)
    )
    """)

    # Insert Sample Data (only once)
    cursor.execute("SELECT COUNT(*) FROM restaurant")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO restaurant (name, location) VALUES ('Pizza Hub', 'Bangalore')")
        cursor.execute("INSERT INTO restaurant (name, location) VALUES ('Burger Town', 'Bangalore')")
        cursor.execute("INSERT INTO restaurant (name, location) VALUES ('Coffee Cup', 'Bangalore')")
        cursor.execute("INSERT INTO restaurant (name, location) VALUES ('Sushi Bar', 'Bangalore')")
        cursor.execute("INSERT INTO restaurant (name, location) VALUES ('Taco Bell', 'Bangalore')")
        cursor.execute("INSERT INTO restaurant (name, location) VALUES ('Pasta Place', 'Bangalore')")
        cursor.execute("INSERT INTO restaurant (name, location) VALUES ('Salad Stop', 'Bangalore')")    

        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Margherita', 199, 1)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Pepperoni', 249, 1)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Cheese Burger', 149, 2)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Chicken Burger', 179, 2)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Espresso', 99, 3)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Cappuccino', 129, 3)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('California Roll', 299, 4)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Spicy Tuna Roll', 349, 4)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Crunchy Taco', 89, 5)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Soft Taco', 79, 5)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Veggie Taco', 69, 5)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Spaghetti', 199, 6)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Fettuccine', 219, 6)")  
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Caesar Salad', 149, 7)")
        cursor.execute("INSERT INTO food_item (name, price, restaurant_id) VALUES ('Greek Salad', 159, 7)")

        cursor.execute("INSERT INTO delivery_person (name) VALUES ('Rahul')")
        cursor.execute("INSERT INTO delivery_person (name) VALUES ('Amit')")
        cursor.execute("INSERT INTO delivery_person (name) VALUES ('Sneha')")   
        cursor.execute("INSERT INTO delivery_person (name) VALUES ('Priya')")

    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect("food.db")
    conn.row_factory = sqlite3.Row
    return conn


# ===============================
# ROUTES
# ===============================

@app.route("/")
def home():
    conn = get_db()
    restaurants = conn.execute("SELECT * FROM restaurant").fetchall()
    conn.close()
    return render_template("home.html", restaurants=restaurants)


@app.route("/menu/<int:restaurant_id>")
def menu(restaurant_id):
    conn = get_db()
    foods = conn.execute(
        "SELECT * FROM food_item WHERE restaurant_id=?",
        (restaurant_id,)
    ).fetchall()
    conn.close()

    # Image Mapping
    food_images = {
        "Margherita": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
        "Pepperoni": "https://images.unsplash.com/photo-1548365328-9f547fb0953c",
        "Cheese Burger": "https://images.unsplash.com/photo-1550547660-d9450f859349",
        "Chicken Burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
        "Espresso": "https://images.unsplash.com/photo-1509042239860-f550ce710b93",
        "Cappuccino": "https://images.unsplash.com/photo-1509042239860-f550ce710b93",
        "California Roll": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351",
        "Spicy Tuna Roll": "https://images.unsplash.com/photo-1562158070-57b1e8b1f68b",
        "Crunchy Taco": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b",
        "Soft Taco": "https://images.unsplash.com/photo-1600891964092-4316c288032e",
        "Veggie Taco": "https://images.unsplash.com/photo-1599974579688-8dbdd335c77f",
        "Spaghetti": "https://images.unsplash.com/photo-1589302168068-964664d93dc0",
        "Fettuccine": "https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9",
        "Greek Salad": "https://images.unsplash.com/photo-1568605114967-8130f3a36994",
        "Caesar Salad": "https://images.unsplash.com/photo-1568605114967-8130f3a36994"
    }

    return render_template("menu.html", foods=foods, food_images=food_images)


@app.route("/add_to_cart/<int:food_id>")
def add_to_cart(food_id):
    conn = get_db()
    food = conn.execute("SELECT * FROM food_item WHERE food_id=?", (food_id,)).fetchone()

    # Create temporary order if not exists
    conn.execute("INSERT INTO orders (status, delivery_person_id) VALUES (?, ?)", ("Pending", 1))
    order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    conn.execute("""
        INSERT INTO order_item (order_id, food_id, quantity, subtotal)
        VALUES (?, ?, ?, ?)
    """, (order_id, food_id, 1, food["price"]))

    conn.commit()
    conn.close()

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    conn = get_db()
    items = conn.execute("""
        SELECT food_item.name, order_item.quantity, order_item.subtotal
        FROM order_item
        JOIN food_item ON order_item.food_id = food_item.food_id
    """).fetchall()
    conn.close()
    return render_template("cart.html", cart_items=items)


@app.route("/place_order")
def place_order():
    conn = get_db()
    conn.execute("UPDATE orders SET status='Placed'")
    conn.commit()
    conn.close()
    return redirect(url_for("orders"))


@app.route("/orders")
def orders():
    conn = get_db()
    orders = conn.execute("""
        SELECT orders.order_id, orders.status, delivery_person.name as delivery_person
        FROM orders
        JOIN delivery_person ON orders.delivery_person_id = delivery_person.delivery_person_id
    """).fetchall()
    conn.close()
    return render_template("orders.html", orders=orders)


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)