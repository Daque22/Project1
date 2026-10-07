from flask import Flask, request, jsonify, render_template
import mysql.connector


app = Flask(__name__)

db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="iloveyou123",
        database="inventory_system"
)


# Frontend page
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/Login", methods=["POST"])
def Login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT username, passwords from users")
    users = cursor.fetchall()
    for u in users:
        if u["username"] == username and u["passwords"] == password:
            print("asjbhajhs")
            return jsonify({"users" : users
            })

    return jsonify({"username": username,
                    "password": password
                    })

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/SignUP", methods=["POST"])
def SignUP():
    data = request.json
    username = data["username"]
    password = data["password"]

    cursor = db.cursor()
    cursor.execute(
    "INSERT INTO users (username, passwords) VALUES (%s, %s)",
    (username, password)
    )
    db.commit()
    cursor.close()
    return jsonify({"message": "signup successfully"})


# GET - kuha tanan products
@app.route("/api/products", methods=["GET"])
def get_products():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)


# POST - add product
@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.json
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"]
    }
    print(new_product)
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products(p_id, p_name, price) VALUES (%s, %s, %s)",
        (new_product["id"], new_product["name"], new_product["price"]
         )
        )
    db.commit()
    cursor.close()
 #products.append(new_product)

    return jsonify(new_product), 201


# PUT - update product
@app.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.json
    cursor = db.cursor()
    cursor.execute(
    "UPDATE products SET p_name = %s WHERE p_id = %s",
    (data["name"], id)
    )
    cursor.execute(
        "UPDATE products SET price = %s WHERE p_id = %s",
        (data["price"], id)
        )
    db.commit()
    cursor.close()
    return jsonify({"message": "success"})


# DELETE - delete product
@app.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    cursor = db.cursor()
    cursor.execute(
    "DELETE FROM products WHERE p_id = %s",
    (id,)
)
    db.commit()
    cursor.close()

    return jsonify({"message": "Successfully Deleted"}), 404


if __name__ == "__main__":
    app.run(debug=True)