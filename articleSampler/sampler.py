import requests
from bs4 import BeautifulSoup
import os
import time


# Functions

# Retruns True if we should keep the article, False otherwise
def should_we_keep_article(soup):
    try:
        h2_elements = soup.find(id="bodyContent").find(id="mw-content-text").find(class_="mw-parser-output").findAll("h2",recursive=False) # find all h2
    except:
        print("An exception occurred when finding all h2")
        return False
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

    return True





#################
# Start of code #
#################




set_of_articles = set()
articles_file = open("articles.txt", "r") # Open a txt file Wikipedia paths
lines = articles_file.readlines()

# Write already collected urls to set so we don't sample old articles again
for line in lines:
    line = line.replace('\n', '') 
    if line != '':
        set_of_articles.add(line)
articles_file.close()

old_articles_count = len(set_of_articles)




# test=["https://sv.wikipedia.org/wiki/Polisen_i_Finland", "https://sv.wikipedia.org/wiki/Fritz_Bengtson"]

# n=len(test)
n = 2000 # Number of articles to sample
start = time.time()


# Sample n random articles and keep if they fit the criteria of should_we_keep_article() function
for index in range(n):
# for index in test:
    response = requests.get(url="https://slumpartikel.toolforge.org/") # random Swedish Wikipedia article not created by a bot
    # response = requests.get(url=index)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Get url of random article
    path = soup.find("link", rel="canonical")['href']

    #Check if we want to discard article
    should_keep = should_we_keep_article(soup) # boolean value returned
    if(should_keep):
        set_of_articles.add(path)

    print(index+1)
    print(path)

end = time.time()

print("Sampling finished!")
print(len(set_of_articles) - old_articles_count, "of", n, "articles saved.")
print("Articles saved before this run:", old_articles_count)
print("Total articles now in file:", len(set_of_articles))
end = time.time()
print("Time elapsed:", end - start)
print()


# Open file again
if(os.path.exists("articles.txt")):
    os.remove("articles.txt")
articles_file = open("articles.txt", "a")

# Write path of article to file
print('Writing articles to file...')
for val in set_of_articles:
    articles_file.write(val)
    articles_file.write('\n')
print('Finished writing.')

# Close file connections
articles_file.close()
