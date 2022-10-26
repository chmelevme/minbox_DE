import psycopg2
import os


def create_tables(conn):
    commands = (
        """
        CREATE TABLE products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE categories (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE category_product (
                product_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                PRIMARY KEY (category_id , product_id),
                FOREIGN KEY (product_id)
                    REFERENCES products (product_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (category_id)
                    REFERENCES categories (category_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    try:
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_product(product_name, conn):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO products(product_name)
             VALUES(%s) RETURNING product_id;"""
    try:

        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (product_name,))
        # get the generated id back
        product_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return product_id


def insert_category(category_name, conn):
    """ insert a new category into the categories table """
    sql = """INSERT INTO categories(category_name)
             VALUES(%s) RETURNING category_id;"""
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (category_name,))
        # get the generated id back
        category_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return category_id


def insert_product_category(product_id, category_id, conn):
    sql = """INSERT INTO category_product(product_id, category_id)
             VALUES(%s, %s);"""
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (product_id, category_id))
        # get the generated id back

        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return category_id


def select_product_categories(conn):
    sql = """SELECT products.product_name, string_agg(categories.category_name, ', ')
  FROM products
LEFT OUTER JOIN category_product
  ON products.product_id = category_product.product_id
LEFT OUTER JOIN categories
  ON category_product.category_id = categories.category_id
group by products.product_name"""
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        res = cur.fetchall()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return res


def select_category_products(conn):
    sql = """SELECT categories.category_name, string_agg(products.product_name, ', ')
  FROM categories
LEFT OUTER JOIN category_product
  ON categories.category_id = category_product.category_id
LEFT OUTER JOIN products
  ON category_product.product_id = products.product_id
group by categories.category_name"""
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        res = cur.fetchall()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return res


def select_pairs(conn):
    sql = """SELECT categories.category_name, products.product_name 
from category_product
LEFT OUTER JOIN categories
ON category_product.category_id = categories.category_id
LEFT OUTER JOIN products
ON category_product.product_id = products.product_id"""
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        res = cur.fetchall()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return res


if __name__ == '__main__':
    conn = psycopg2.connect(
        f'dbname={os.getenv("POSTGRES_DB_NAME")} user={os.getenv("POSTGRES_USER")} password={os.getenv("POSTGRES_PASSWORD")}',
        host=os.getenv('POSTGRES_URL'))
    create_tables(conn)
    for x in ["Печенье", "Хлеб", "Сахар"]:
        insert_product(x, conn)
    for x in ["Бакалея", "К чаю", "Развес"]:
        insert_category(x, conn)
    insert_product_category(1, 1, conn)
    insert_product_category(2, 1, conn)
    insert_product_category(1, 2, conn)
    insert_product_category(3, 2, conn)
    insert_product_category(3, 3, conn)
    conn.close()
