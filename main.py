import json
import requests
from config import MAIN_URL
from bs4 import BeautifulSoup
import re


def get_hometab():
    try:
        response = requests.get(MAIN_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # ul_element = soup.find('ul', class_='home__brand')
            # print(ul_element)

            # Find all labels with class 'tab' within the 'tabs' div
            tab_objects = soup.select('.tabs .tab')

            # Create an empty list to store tab objects
            listTab = []

            # Loop through each label and extract the data
            for tab in tab_objects:
                name = tab.h4.text.strip()  # Extracting the text from the 'h4' tag
                img_src = tab.img['src']    # Extracting the 'src' attribute from the 'img' tag

                # Create a dictionary (tabObject) with the extracted data
                tab_object = {
                    'title': name,
                    'image_url': img_src
                }
                
                # Append the tab_object to the listTab
                listTab.append(tab_object)

            print(listTab)
            return listTab

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_contenttab(tabname):
    try:
        response = requests.get(MAIN_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # for content from tab, in future make Leafy is parameterise from tab active
            # Find the div element with id "Leafy-panel"
            # 
            leafy_panel = soup.find('div', {'id': f"{tabname}-panel"})

            # Check if the Leafy-panel div is found
            if leafy_panel:
                # Find the script tag inside the Leafy-panel div
                script_tag = leafy_panel.find('script', type='application/ld+json')
                # Check if the script tag is found
                if script_tag:
                    # Extract the content of the script tag (JSON data)
                    json_data = script_tag.string

                    # Clean up the JSON string
                    cleaned_json_data = json_data.replace('\n', '').replace('\xa0', ' ').strip()
                    
                     # Load the cleaned JSON data into a Python dictionary
                    data_dict = json.loads(cleaned_json_data)
                    # print(cleaned_json_data)

                     # Check if "itemListElement" is present in the dictionary
                    if "itemListElement" in data_dict:
                        # Extract the "itemListElement" part
                        item_list = data_dict["itemListElement"]
                        
                        # Return only the "itemListElement"
                        print(item_list)
                        return item_list
                    else:
                        return "Key 'itemListElement' not found in the JSON data."
                else:
                    print("Script tag not found inside Leafy-panel.")
            else:
                print("Leafy-panel div not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def search_product(search_key):
    url = f"{MAIN_URL}/search?q={search_key}"
    print(url)
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Initialize a list to store the product information
            product_list = []
            
            # Find the first div with class="sixteen columns"
            sixteen_columns_div = soup.find('div', class_='sixteen columns')
             # Check if the sixteen_columns_div is found
            if sixteen_columns_div:
                # Find all divs with class="product_row" inside the sixteen_columns_div
                product_row_divs = sixteen_columns_div.find_all('div', class_='product_row')

                # Loop through each product_row_div
                for product_row_div in product_row_divs:
                    # Extract sub_title link and value
                    sub_title_a = product_row_div.find('h5', class_='sub_title').find('a')
                    sub_title_link = sub_title_a['href']
                    sub_title_value = sub_title_a.get_text(strip=True)

                    # Extract was_price and money
                    was_price_span = product_row_div.find('span', class_='was_price')
                    was_price = was_price_span.find('span', class_='money').get_text(strip=True) if was_price_span else None

                    price_span = product_row_div.find('span', class_='price')
                    money = price_span.find('span', class_='money').get_text(strip=True) if price_span else None

                    # Extract description (p tag)
                    description_p = product_row_div.find('p').get_text(strip=True) if product_row_div.find('p') else None

                    # Create a dictionary for the current product
                    product_dict = {
                        "sub_title_link": sub_title_link,
                        "sub_title_value": sub_title_value,
                        "was_price": was_price,
                        "money": money,
                        "description": description_p
                    }

                    # Add the product dictionary to the list
                    product_list.append(product_dict)

                    # Print or use the extracted information as needed
                    # print("Sub Title Link:", sub_title_link)
                    # print("Sub Title Value:", sub_title_value)
                    # print("Was Price:", was_price)
                    # print("Money:", money)
                    # print("Description:", description_p)
                    # print("------")
                
                # Convert the list of products to JSON
                # json_result = json.dumps(product_list, indent=2)
                # print(json_result)

                return product_list

            else:
                print("No div with class 'sixteen columns' found.")


    except Exception as e:
        print(f"An error occurred: {str(e)}")
   

def main():
    # get_hometab()
    get_contenttab("Leafy")
    # search_product("tofu")

if __name__ == '__main__':
    main()