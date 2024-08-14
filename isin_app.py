import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Streamlit app
st.title("PSE Stock Data Scraper")

# Sidebar input for company ID range
start_id = st.sidebar.number_input("Start Company ID", min_value=0, value=184)
end_id = st.sidebar.number_input("End Company ID", min_value=0, value=185)

# Button to start scraping
if st.button("Start Scraping"):
    # Initialize an empty list to store data
    data = []

    for company_id in range(start_id, end_id + 1):
        # Define the URL with the current company ID
        url = f"https://edge.pse.com.ph/companyPage/stockData.do?cmpy_id={company_id}"
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract the Stock Code (Company)
            stock_code_tag = soup.find('option', selected=True)
            stock_code = stock_code_tag.text.strip() if stock_code_tag else "Stock Code not found"
            
            # Extract the ISIN
            isin_tag = soup.find('th', text='ISIN')
            isin = isin_tag.find_next('td').text.strip() if isin_tag else "ISIN not found"
            
            # Append data to the list
            data.append({"Company ID": company_id, "Stock Code": stock_code, "ISIN": isin})
        else:
            data.append({"Company ID": company_id, "Stock Code": "Failed to retrieve", "ISIN": "Failed to retrieve"})

    # Convert the list to a DataFrame
    df = pd.DataFrame(data)
    
    # Display the DataFrame
    st.write(df)

    # Optionally, allow the user to download the data as a CSV file
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download data as CSV", data=csv, file_name='pse_stock_data.csv', mime='text/csv')
