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


def main():
    get_hometab()

if __name__ == '__main__':
    main()