import streamlit as st
import pandas as pd
import sqlite3
from scraper import get_product_details
from database import init_db, add_price_record

# Initialize the database
init_db()

# --- STREAMLIT WEB PAGE DESIGN ---
st.title("🛒 Smart E-Commerce Price Tracker")
st.write("Enter a product URL to fetch live prices and track price history securely in the database.")

# 1. Input field for the product URL
url_input = st.text_input("Enter Product URL:", "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")

# 2. Track Price Action Button
if st.button("Track Price"):
    if url_input:
        with st.spinner("Fetching product details from the website... Please wait."):
            # Call the scraper function to extract title and price
            title, price = get_product_details(url_input)
            
            if title and price > 0:
                # Success message display
                st.success("Product successfully fetched!")
                
                # Display metrics in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Product Name", value=title)
                with col2:
                    st.metric(label="Current Price", value=f"£{price}")
                
                # Save the record to the database
                add_price_record(title, price)
                
            else:
                st.error("Failed to fetch product details. Please verify the URL.")
    else:
                st.warning("Please enter a valid product URL first.")

st.markdown("---")
st.subheader("📊 Price History & Database Records")

# 3. Load historical data from the database for visualization
def load_data():
    conn = sqlite3.connect("tracker.db")
    # Load SQL data into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM price_history", conn)
    conn.close()
    return df

df_data = load_data()

if not df_data.empty:
    # Display data table
    st.dataframe(df_data)
    
    # Display a line chart if multiple historical records exist
    if len(df_data) > 1:
        st.subheader("📈 Price Trend Graph")
        # Streamlit native line chart visualization
        st.line_chart(df_data.set_index("date_recorded")["price"])
else:
    st.info("No records found in the database yet. Enter a URL above and click 'Track Price' to start.")