import requests
from bs4 import BeautifulSoup
import os


# Functions

# Retruns True if we should keep the article, False otherwise
def should_we_keep_article(soup):
    h2_elements = soup.find(id="bodyContent").find(id="mw-content-text").find(class_="mw-parser-output").findAll("h2",recursive=False) # find all h2
    number_of_h2 = len(h2_elements)
    # print(h2_elements)
    # print(number_of_h2)

    illegal_h2_elements = 0 
    for j in h2_elements:
        header = j.find("span", class_="mw-headline").get_text()
        if(header == 'Se även' or header == 'Referenser' or header == 'Externa länkar' or header == 'Noter och referenser' or header == 'Källor' or header == 'Noter' or header == 'Vidare läsning' or header == 'Fotnoter'):
            illegal_h2_elements += 1
    
    legal_elements = number_of_h2 - illegal_h2_elements

    # If article has less than 2 h2 headers then it has less than 3 sections => Discard
    # Note: the section below the main title does not have any h2 therefore we use the number 2 here.
    if(legal_elements < 2): 
        return False

    cat_list = soup.find("div", id="catlinks").find("ul").find_all("a") # List of categories
    categories = [x.get_text() for x in cat_list] # get the string

    for i in categories:
        if i == 'Män' or i == 'Kvinnor': # Discard people
            return False
        if i == 'Förgreningssidor': # Discard disambiguation pages
            return False
    return True





#################
# Start of code #
#################

# Open a txt file for search queries(title/section/...) and for paragraph texts
if(os.path.exists("articles.txt")):
    os.remove("articles.txt")
articles_file = open("articles.txt", "a")

test=["https://sv.wikipedia.org/wiki/Polisen_i_Finland", "https://sv.wikipedia.org/wiki/Gr%C3%A4nsbevakningsv%C3%A4sendet", "https://sv.wikipedia.org/wiki/F%C3%B6runders%C3%B6kning", "https://sv.wikipedia.org/wiki/The_Beatles"]

n=len(test)
# n = 200

legal_article_count = 0


# test=["https://sv.wikipedia.org/wiki/Anja_P%C3%A4rson", "https://sv.wikipedia.org/wiki/Mustafa_Sandal", "https://sv.wikipedia.org/wiki/USA"]

# for index in range(10):
for index in test:
    # response = requests.get(url="https://slumpartikel.toolforge.org/") # random Swedish Wikipedia article not created by a bot
    response = requests.get(url=index)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get url of random article
    path = soup.find("link", rel="canonical")['href']

    #Check if we want to discard article
    should_keep = should_we_keep_article(soup) # boolean value returned
    if(should_keep):
        # Write path of article to file
        articles_file.write(path)
        articles_file.write('\n')
        legal_article_count += 1


print("Sampling finished!")
print(legal_article_count, "of", n, "articles saved.")
print()


# Close file connections
articles_file.close()
