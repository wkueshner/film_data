#import the required libraries  
import requests   
from bs4 import BeautifulSoup
import re
import csv

request = requests.get("https://en.wikipedia.org/wiki/List_of_films:_numbers")  
  
#Parsing the webpage   
parsed_page = BeautifulSoup(  
    request.text,   
    "html.parser")  
  
a_tags = parsed_page.find_all('a')  
  
# Returns a list of extracted attributes   
def get_attr_values(  
    list_of_tags,  
    attribute  
    ):  
  
    #initialize empty list to store values  
    list_of_values = []  
  
    # Iterate through list of tags  
    for tag in list_of_tags:  
  
        # Extract attributes  
        attribute_value = tag.get(attribute)  
        list_of_values.append(attribute_value)  
  
    return list(  
        set(list_of_values) #get unique values  
        )  
  
#apply function  
list_of_movie_titles = get_attr_values(a_tags, 'title')

def find_attributes(  
    pattern,   
    request,  
    tag,  
    attribute):   
  
    #regex pattern    
    compiled_pattern = re.compile(pattern)  
      
    # request website  
    res = requests.get(  
    request)  
  
    #Parse the request and get attributes   
    found_attributes = BeautifulSoup(res.text,'html.parser').find_all(tag,{attribute: compiled_pattern })
      
    return found_attributes  
  
href_attributes = find_attributes(  
    pattern = '^/wiki/List_of_films',  
    request = 'https://en.wikipedia.org/wiki/List_of_films:_numbers',  
    tag = 'a',  
    attribute = 'href'  
)  
  
relative_link_list = get_attr_values(href_attributes, 'href')


def scrape_wiki_mvtitles():  
       
    #initialize list to capture movie   
    list_of_titles = []  
      
    #Domain string   
    domain_str = 'https://en.wikipedia.org/'  
    
    # Get list of relative links   
    relative_link_list = get_attr_values(href_attributes, 'href')  
  
    #loop through list of relative links   
    for relative_link in relative_link_list :  
          
        #Concatenate domain string withrelative string  
        request_complete_link = requests.get(domain_str + relative_link)  
  
        #Parse site   
        parse_page = BeautifulSoup(  
            request_complete_link.text,  
            'html.parser'  
            )  
  
        a_tags = parse_page.find_all('a')  
  
        title_attributes =  get_attr_values(  
            a_tags,  
            'title'  
        )  
        #append list of titles   
        list_of_titles += title_attributes  
      
    return list_of_titles  
  
movie_titles = scrape_wiki_mvtitles()  

# Save to CSV
try:
    filepath = 'C:/Users/wkues/film_data/movie_titles.csv'
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['movie', 'year'])
        successful_rows = 0
        for title in movie_titles:
            if title:  # Check if title is not None
                # Regex to find a year within parentheses if present
                year_match = re.search(r'\((\d{4})[^)]*\)', title)
                if year_match:
                    year = year_match.group(1)
                else:
                    year = ''

                # Regex to remove any text within parentheses at the end of the title, including any preceding space
                title = re.sub(r'\s*\([^)]*\)$', '', title).strip()

                writer.writerow([title, year])
                successful_rows += 1
    print(f"CSV file has been written to {filepath}")
    print(f"Successfully wrote {successful_rows} rows.")
except Exception as e:
    print(f"An error occurred: {e}")

print(len(movie_titles))  
print(movie_titles[0:10])
