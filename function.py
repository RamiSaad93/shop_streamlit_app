import pandas as pd
#import numpy as np
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text
from pass_file import password
from datetime import date
import streamlit as st


db = "shop_project"
connection_string = f'mysql+pymysql://root:{password}@localhost/'+db
engine = create_engine(connection_string)
engine

## Add Customer (Sign Up)


def sign_up(engine, customer_name, customer_email, customer_pass):
    import pymysql
    from sqlalchemy import create_engine
    from sqlalchemy import text 
    with engine.connect() as connection:
        query = text(f'''
            INSERT INTO shop_project.customers (Customer_Name, Email, Password)
            VALUES ("{customer_name}", "{customer_email}", "{customer_pass}");
        ''')
        connection.execute(query)
        connection.commit()   # commit changes to DB
    return print("✅ Sign-up successful!")

## Log In

def check_login(engine, email, password):
    with engine.connect() as connection:
        query = text(f"""SELECT 
                            CASE
                                WHEN EXISTS (SELECT 1 FROM shop_project.customers WHERE email = "{email}" AND password = "{password}")
                                    THEN 'You can log in'
                                WHEN NOT EXISTS (SELECT 1 FROM shop_project.customers WHERE email = "{email}")
                                    THEN 'You are not a member'
                                ELSE 'Wrong password'
                            END AS message
        """)
        result = connection.execute(query)
        return result.scalar()


## View Products

def view_products(engine):
    with engine.connect() as connection:
        txt = f'''SELECT Product_id, Name, Price, Stock
                  FROM shop_project.products;'''
        query = text(txt)
        result = connection.execute(query)
        products_df = pd.DataFrame(result.all())
        return products_df

    
def place_order(engine):  # removed  customer_id, cart
    with engine.connect() as conn:  
        
        customer_id_query = text("""
            SELECT Customer_id 
            FROM shop_project.customers
            WHERE Email = :email
        """)
        customer_result = conn.execute(customer_id_query, {"email": customer_email})
        customer_id = customer_result.lastrowid


        order_query = text("""
            INSERT INTO orders (Order_Date, Customer_id)
            VALUES (:order_date, :cust_id)
        """)
        order_result = conn.execute(order_query, {"order_date": date.today(), "cust_id": customer_id})
        order_id = order_result.lastrowid

        product_name = st.selectbox("Which jersey you would like to buy?",
                                    ("Manchester United Home Jersey 2024/25",
                                        "Real Madrid Away Jersey 2024/25",
                                        "FC Barcelona Third Jersey 2024/25",
                                        "Liverpool Home Jersey 2024/25",
                                        "Chelsea Away Jersey 2024/25",
                                        "Bayern Munich Home Jersey 2024/25",
                                        "Paris Saint-Germain Home Jersey 2024/25",
                                        "Juventus Away Jersey 2024/25",
                                        "Arsenal Third Jersey 2024/25",
                                        "AC Milan Home Jersey 2024/25"))
        
        product_id_query = text(f"""
            SELECT product_id
            FROM shop_project.products
            WHERE Name = :product_name
        """)
        product_id_result = conn.execute(product_id_query, {"product_name": product_name})
        product_id = product_id_result.lastrowid

        qty = st.number_input("How many pieces do you want to buy?")

        cart = (product_id, qty)
        # Step 2: Loop through the cart
        for product_id, qty in cart:

            # Check stock and get price
            stock_query = text("SELECT Stock, Price FROM products WHERE Product_id = :pid")
            stock_result = conn.execute(stock_query, {"pid": product_id}).fetchone()

            if not stock_result:
                raise Exception(f"Product {product_id} does not exist.")

            stock, price = stock_result

            if stock < qty:
                raise Exception(f"Not enough stock for Product {product_name}. Available: {stock}, Requested: {qty}")

            # Insert into order_items
            insert_item = text("""
                INSERT INTO order_items (Product_id, Order_id, Quantity, Price)
                VALUES (:pid, :oid, :qty, :price)
            """)
            conn.execute(insert_item, {"pid": product_id, "oid": order_id, "qty": qty, "price": price})

            # Update stock
            update_stock = text("UPDATE products SET Stock = Stock - :qty WHERE Product_id = :pid")
            conn.execute(update_stock, {"qty": qty, "pid": product_id})
        conn.commit()

    return f"✅ Order {order_id} placed successfully!"