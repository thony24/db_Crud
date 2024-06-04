import psycopg2
from app.db import connection

def connect_and_execute(query, params=None):
    try:
        connection_db = connection.connect_db()
        cursor = connection_db.cursor()
        cursor.execute(query, params)
        connection_db.commit()
        if query.lower().startswith("select"):
            results = cursor.fetchall()
            return cursor, results
        return cursor
    except psycopg2.Error as error:
        print(f"Error connecting or executing query: {error}")
        raise  # Re-raise the exception to propagate it to the caller
    finally:
        if connection_db:
            if cursor:
                cursor.close()
            connection.close_db(connection_db)

def insert_product(name, price, stock, purchasable):
    query = """
        INSERT INTO products (name, price, stock, purchasable)
        VALUES (%s, %s, %s, %s)
    """
    return connect_and_execute(query, (name, price, stock, purchasable))

def get_products():
    query = "SELECT * FROM products ORDER BY id"
    cursor, results = connect_and_execute(query)
    products = []
    for row in results:
        product = {
            "id": row[0],
            "name": row[2],
            "price": row[3],
            "stock": row[4],
            "purchasable": row[5]
        }
        products.append(product)
    return products

def update_product(id_product, name, price, stock, purchasable):
    query = """
        UPDATE products
        SET name = %s, price = %s, stock = %s, purchasable = %s
        WHERE id = %s
    """
    return connect_and_execute(query, (name, price, stock, purchasable, id_product))

def delete_product(id_product):
    query = "DELETE FROM products WHERE id = %s"
    return connect_and_execute(query, (id_product,))

