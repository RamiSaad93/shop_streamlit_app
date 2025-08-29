# app_3

import streamlit as st
from function import sign_up, check_login, view_products
from sqlalchemy import create_engine, text
from datetime import date
from pass_file import password

image_list = ["1.jpg", "2.jpg", "3.jpg", "4.jpg",
              "5.jpg", "6.jpg","7.jpg", "8.jpg",
              "9.jpg", "10.jpg"]


connection_string = f'mysql+pymysql://root:{password}@localhost:3306/shop_project'
engine = create_engine(connection_string)

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "customer_email" not in st.session_state:
    st.session_state.customer_email = None
if "show_products" not in st.session_state:
    st.session_state.show_products = False
if "order_message" not in st.session_state:
    st.session_state.order_message = None
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "selected_qty" not in st.session_state:
    st.session_state.selected_qty = 1

st.header("Welcome to Manchester United rocks For Jerseys 👕⚽")



# --- Sign Up / Login ---
choice = st.radio("Are you a Member", ["Sign Up", "Log In"])

if choice == "Sign Up":
    st.subheader("Create a new account")
    customer_name = st.text_input("Enter your full name")
    customer_email = st.text_input("Enter your email")
    customer_password = st.text_input("Enter your password", type="password")
    if st.button("Sign Up"):
        sign_up(engine, customer_name, customer_email, customer_password)
        st.success("✅ Sign up successful! Please log in.")

elif choice == "Log In":
    st.subheader("Log In")
    customer_email = st.text_input("Enter your email")
    customer_password = st.text_input("Enter your password", type="password")
    if st.button("Log In"):
        result = check_login(engine, customer_email, customer_password)
        if result == "You can log in":
            st.session_state.logged_in = True
            st.session_state.customer_email = customer_email
            st.success("✅ Login successful!")
        elif result == "You are not a member":
            st.session_state.logged_in = False
            st.error("❌ You are not a member. Please sign up.")
        else:
            st.session_state.logged_in = False
            st.error("❌ Wrong password. Try again.")




# --- Products ---
if st.session_state.logged_in:
    st.subheader("Available Products")
    if st.button("View Products"):
        st.session_state.show_products = True
    if st.session_state.show_products:
        products = view_products(engine)
        for image, product_id, laptop, price, stock in zip(image_list, products['Product_id'], products['Name'], products['Price'], products['Stock']):
            st.write(product_id, laptop)
            st.write("Price:", price, "$")
            st.write("Available Stock:", stock)
            st.image(image, width=200)
else:
    st.info("🔒 Please log in to view products.")


def place_order(engine):
    customer_email = st.session_state.customer_email  
    with engine.connect() as conn:  

        customer_id_query = text("""
            SELECT Customer_id 
            FROM shop_project.customers
            WHERE Email = :email
        """)
        customer_result = conn.execute(customer_id_query, {"email": customer_email})
        customer_id = customer_result.fetchone()[0]

        order_query = text("""
            INSERT INTO orders (Order_Date, Customer_id)
            VALUES (:order_date, :cust_id)
        """)
        order_result = conn.execute(order_query, {"order_date": date.today(), "cust_id": customer_id})
        order_id = order_result.lastrowid

        product_name = st.session_state.selected_product
        qty = st.session_state.selected_qty

        product_id_query = text("""
            SELECT product_id
            FROM shop_project.products
            WHERE Name = :product_name
        """)
        product_id_result = conn.execute(product_id_query, {"product_name": product_name})
        product_id = product_id_result.fetchone()[0]

        stock_query = text("SELECT Stock, Price FROM products WHERE Product_id = :pid")
        stock_result = conn.execute(stock_query, {"pid": product_id}).fetchone()
        stock, price = stock_result

        if stock < qty:
            raise Exception(f"Not enough stock for {product_name}. Available: {stock}, Requested: {qty}")

        insert_item = text("""
            INSERT INTO order_items (Product_id, Order_id, Quantity, Price)
            VALUES (:pid, :oid, :qty, :price)
        """)
        conn.execute(insert_item, {"pid": product_id, "oid": order_id, "qty": qty, "price": price*qty})

        update_stock = text("UPDATE products SET Stock = Stock - :qty WHERE Product_id = :pid")
        conn.execute(update_stock, {"qty": qty, "pid": product_id})

        conn.commit()

    return f"✅ Order {order_id} placed successfully!"


if st.session_state.logged_in:
    st.subheader("Place an Order")

    st.session_state.selected_product = st.selectbox(
        "Which jersey would you like to buy?",
        (
            "Manchester United Home Jersey 2024/25",
            "Real Madrid Away Jersey 2024/25",
            "FC Barcelona Third Jersey 2024/25",
            "Liverpool Home Jersey 2024/25",
            "Chelsea Away Jersey 2024/25",
            "Bayern Munich Home Jersey 2024/25",
            "Paris Saint-Germain Home Jersey 2024/25",
            "Juventus Away Jersey 2024/25",
            "Arsenal Third Jersey 2024/25",
            "AC Milan Home Jersey 2024/25",
        )
    )

    st.session_state.selected_qty = st.number_input("How many pieces do you want to buy?", min_value=1, value=1)

    if st.button("Make an order"):
        try:
            st.session_state.order_message = place_order(engine)
        except Exception as e:
            st.session_state.order_message = f"❌ {e}"

    if st.session_state.order_message:
        st.success(st.session_state.order_message)
