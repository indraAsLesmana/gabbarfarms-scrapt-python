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
                    'name': name,
                    'imgSrc': img_src
                }
                
                # Append the tab_object to the listTab
                listTab.append(tab_object)

            print(listTab)

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


def main():
    # get_hometab()
    get_contenttab("Leafy")

if __name__ == '__main__':
    main()