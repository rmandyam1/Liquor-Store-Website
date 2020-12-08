# CS 348 Project
from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("begin.html", title="Village Bottle Shoppe")


@app.route("/viewproducts")
def view_products():
    data = select_all_ps("Product")
    return render_template("viewproducts.html", data=data)


@app.route("/viewinventory")
def view_inventory():
    data = select_all_ps("Product")
    return render_template("inventory.html", data=data)


def get_cart_id(customer_id):
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor(prepared=True)
    query = """SELECT orderId FROM Orders WHERE customerId = %s AND completedDate IS NULL"""  # Finding CartID
    cursor.execute(query, (customer_id, ))
    data = cursor.fetchone()
    cnx.commit()

    cursor.close()
    cnx.close()
    return data


def customer_order_history(customer_id):
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor(prepared=True)
    cart_id = get_cart_id(customer_id)
    # Finding OrderIds that are not cart
    query = "SELECT orderId, transactionAmount, customerId FROM Orders WHERE orderId <> %s" % cart_id
    cursor.execute(query)
    data = cursor.fetchall()
    cnx.commit()

    cursor.close()
    cnx.close()
    return data


@app.route("/salesbycustomer")
def sales_by_customer():
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    # Finding OrderIds by customer
    query = "SELECT Orders.customerId, Customer.firstName, Customer.lastName, COUNT(orderId), SUM(transactionAmount), AVG(transactionAmount) FROM Orders INNER JOIN Customer ON Orders.customerId = Customer.customerId WHERE orderId IS NOT NULL GROUP BY Orders.customerId"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    cnx.close()
    return render_template("salesbycustomer.html", data=data)


def select_all_ps(table_name):
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    query = "SELECT * FROM %s" % table_name
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    cnx.close()

    return data


def completed_orders_ps():
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    query = "SELECT orderId FROM Orders WHERE completedDate IS NOT NULL"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    cnx.close()
    return data


@app.route("/bestsellers")
def view_top_sellers():
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    query = "SELECT DISTINCT p.productId, p.name, p.category, p.description, p.price, o.quantity, p.inventoryQuantity FROM Product p, OrderItem o WHERE o.productId = p.productId AND o.orderId IN (SELECT orderId FROM Orders WHERE completedDate IS NOT NULL) ORDER BY o.quantity DESC LIMIT 5;"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    cnx.close()
    return render_template("bestsellers.html", data=data)


def add_to_cart(customer_id, qty, product_id):
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    order_id = get_cart_id(customer_id)
    checkIfExists = "SELECT quantity FROM OrderItem WHERE orderId = %s AND productId = %s" % (
        order_id, product_id)
    cursor.execute(checkIfExists)
    data = cursor.fetchall()
    num = cursor.rowcount
    if (num == 0):
        query = "INSERT INTO OrderItem VALUES(%s, %s, %s)" % (
            order_id, product_id, qty)
        cursor.execute(query)
    else:
        query = "UPDATE OrderItem SET qty = %s WHERE orderId = %s AND productId = %s" % (
            qty, order_id, product_id)
        cursor.execute(query)

    cursor.close()
    cnx.close()
    return data


def check_inventory(customer_id, qty, product_id):
    try:
        cnx = mysql.connector.connect(
            user='root', password='12345', host='104.154.215.223', database='village_bottle_shoppe')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    checkQty = "SELECT inventoryQuantity FROM Product WHERE productId = %s" % product_id
    cursor.execute(checkQty)
    data = cursor.fetchone()
    if (data[0] - qty < 0):
        cursor.close()
        cnx.close()
        return False
    else:
        cursor.close()
        cnx.close()
        return True


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        qty = result.get("quantity")
        product_id = result.get("productId")
        bool_add = update_inventory(customer_id, qty, product_id)

        if (bool_add):
            add_to_cart(customer_id, qty, productId)
    #   Update qty for particular item
        return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
    render_template("begin.html")


# @app.route("/")
# def homepage():
#     return render_template("index.html", title="HOME PAGE")

# @app.route("/docs")
# def docs():
#     return render_template("index.html", title="docs page")

# @app.route("/about")
# def about():
#     return render_template("index.html", title="about page")

# if __name__ == "__main__":
#     app.run(debug=True)
