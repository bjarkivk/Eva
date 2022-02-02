import requests
from bs4 import BeautifulSoup
import os
import json

# Functions
# def get_section_id(main_title, last_h2, last_h3, last_h4, last_h5):
#     if(last_h2):
#         if(last_h3):
#             if(last_h4):
#                 if(last_h5):
#                     return main_title+'/'+last_h2+'/'+last_h3+'/'+last_h4+'/'+last_h5
#                 return main_title+'/'+last_h2+'/'+last_h3+'/'+last_h4
#             return main_title+'/'+last_h2+'/'+last_h3
#         return main_title+'/'+last_h2
#     return main_title


#################
# Start of code #
#################

# Open a txt file for search queries(title/section/...) and for paragraph texts
if(os.path.exists("queries.txt")):
    os.remove("queries.txt")
if(os.path.exists("paragraphs.json")):
    os.remove("paragraphs.json")
queries_file = open("queries.txt", "a")
paragraphs_file = open("paragraphs.json", "a")

# Open the list of articles to read
article_file = open('../articleSampler/articles.txt', 'r')
lines = article_file.readlines()

# Loop over Wikipedia articles stated in articles.txt
for index, line in enumerate(lines):

    # Scrape the webpage of the article with BeautifulSoup
    line = line.replace('\n', '') 
    response = requests.get(url=line)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Write main title to the queries file
    main_title = soup.find(id="firstHeading").get_text()
    queries_file.write(main_title)
    queries_file.write('\n')

    # find next html element
    last_element = soup.find(id="bodyContent").find(id="mw-content-text").find(class_="mw-parser-output").find_next()

    last_h2 = ''
    last_h3 = ''
    last_h4 = ''
    last_h5 = ''

    # Loop through all html elements on this level and read the text to file
    while last_element:
        if last_element.name =='h2' or last_element.name =='h3' or last_element.name =='h4' or last_element.name =='h5' or last_element.name =='p' or last_element.name =='ul' or last_element.name =='ol':
            if(last_element.name == 'h2'):
                last_h3 = ''
                last_h4 = ''
                last_h5 = ''
                last_h2 = last_element.find("span", class_="mw-headline").get_text()
                if ( last_h2 == 'Se även' or last_h2 == 'Referenser' or last_h2 == 'Externa länkar' or last_h2 == 'Noter och referenser' or last_h2 == 'Källor' or last_h2 == 'Noter' or last_h2 == 'Vidare läsning' or last_h2 == 'Fotnoter'):
                    break
                queries_file.write(main_title + '/' + last_h2)
                queries_file.write('\n')
            elif(last_element.name == 'h3'):
                last_h4 = ''
                last_h5 = ''
                last_h3 = last_element.find("span", class_="mw-headline").get_text()
                queries_file.write(main_title + '/' + last_h2 + '/' + last_h3)
                queries_file.write('\n')
            elif(last_element.name == 'h4'):
                last_h5 = ''
                last_h4 = last_element.find("span", class_="mw-headline").get_text()
                queries_file.write(main_title + '/' + last_h2 + '/' + last_h3 + '/' + last_h4)
                queries_file.write('\n')
            elif(last_element.name == 'h5'):
                last_h5 = last_element.find("span", class_="mw-headline").get_text()
                queries_file.write(main_title + '/' + last_h2 + '/' + last_h3 + '/' + last_h4 + '/' + last_h5)
                queries_file.write('\n')
            elif(last_element.name =='p' or last_element.name =='ul' or last_element.name =='ol'):
                # section_id = get_section_id(main_title, last_h2, last_h3, last_h4, last_h5)
                paragraph = last_element.get_text()
                paragraph = paragraph.replace('\n', ' ') # if last character is a newline character, then replace it with space
                paragraph = paragraph.strip() # remove whitespace in beginning and at the end of string
                if paragraph !='':
                    # Write paragraph to file on a json format

                    x = {
                        "id1": main_title,
                        "id2": last_h2,
                        "id3": last_h3,
                        "id4": last_h4,
                        "id5": last_h5,
                        "paragraph" : paragraph
                    }
                    json_paragraph = json.dumps(x, ensure_ascii=False)

                    paragraphs_file.write('{"index":{}}') # According to Elasticsearch documentation we have to seperate each paragraoh with this json object
                    paragraphs_file.write('\n')
                    paragraphs_file.write(json_paragraph)
                    paragraphs_file.write('\n')

            
        last_element = last_element.find_next_sibling()





# Close file connections
article_file.close()
queries_file.close()
paragraphs_file.close()
