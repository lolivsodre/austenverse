import pandas as pd
import re
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Fetch the content of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Jane_Austen_in_popular_culture"
response = requests.get(url)
soup = bs(response.content, 'html.parser')

# Initialize lists to store adaptation data
sense_direct_adaptations = []
sense_loose_adaptations = []
sense_theatre_adaptations = []
sense_other_references = []

# Function to extract direct adaptations from wikitables
def extract_sense_direct_adaptations(soup):
    for table in soup.find_all('table', class_='wikitable', style=re.compile(r'font-size:95%;.*background: #ccccff')):
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 2:
                year = cols[0].get_text(strip=True)
                adaptation_cell = cols[1]
                title_tag = adaptation_cell.find('a')
                title = title_tag.get_text(strip=True) if title_tag else adaptation_cell.get_text(strip=True)
                medium_tag = adaptation_cell.find('small')
                based_on = "Sense and Sensibility"  # Default assumption

                # Correct the 'Based On' field based on the adaptation title
                if "Pride and Prejudice" in title or "Orgoglio e pregiudizio" in title or "De vier dochters Bennet" in title or "Orgullo y prejuicio" in title:
                    based_on = "Pride and Prejudice"

                # Determine Medium and Medium Type
                medium = "Unknown"
                medium_type = "Unknown"
                if medium_tag:
                    medium_text = medium_tag.get_text().lower()
                    if "film" in medium_text:
                        medium = "Film"
                        medium_type = "Feature Film" if "Feature film" in medium_text else "Television Film"
                    elif "television" in medium_text or "miniseries" in medium_text:
                        medium = "Television"
                        medium_type = "Television Series"
                    elif "stage" in medium_text or "play" in medium_text:
                        medium = "Theatre"
                        medium_type = "Stage Play"
                    elif "musical" in medium_text:
                        medium = "Theatre"
                        medium_type = "Musical"

                # Append the parsed data to the list
                sense_direct_adaptations.append({
                    "Title": title,
                    "Year": year,
                    "Medium": medium,
                    "Medium Type": medium_type,
                    "Based On": based_on,
                    "Direct or Loose Adaptation": "Direct"
                })

# Function to extract looser adaptations
def extract_sense_loose_adaptations(soup):
    looser_adaptations_header = soup.find('h4', id='Looser_adaptations')
    if looser_adaptations_header:
        looser_list = looser_adaptations_header.find_next('ul')
        for li in looser_list.find_all('li'):
            title_tag = li.find('i')
            title = title_tag.get_text(strip=True) if title_tag else li.get_text(strip=True)
            year_match = re.search(r'\((\d{4})\)', li.get_text())
            year = year_match.group(1) if year_match else "Unknown"
            text = li.get_text().lower()

            # Determine Medium and Medium Type
            medium = "Unknown"
            medium_type = "Unknown"
            if "film" in text:
                medium = "Film"
                medium_type = "Feature Film" if "Feature film" in text else "Television Film"
            elif "television" in text or "serial" in text or "tv" in text:
                medium = "Television"
                medium_type = "Television Series"
            elif "web" in text:
                medium = "Web Series"
                medium_type = "Web Series"
            elif "theatre" in text:
                medium = "Theatre"
                medium_type = "Stage Play"

            sense_loose_adaptations.append({
                "Title": title,
                "Year": year,
                "Medium": medium,
                "Medium Type": medium_type,
                "Based On": "Sense and Sensibility",
                "Direct or Loose Adaptation": "Loose"
            })

pride_adaptations = []
# Function to extract direct adaptations for "Pride and Prejudice"
def extract_pride_direct_adaptations(soup):
    # Find the specific section for "Pride and Prejudice"
    pride_section = soup.find('span', id='Pride_and_Prejudice_.281813.29')
    if pride_section:
        # Look for the wikitable following this section
        wikitable = pride_section.find_next('table', class_='wikitable')
        if wikitable:
            for row in wikitable.find_all('tr')[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 2:
                    year = cols[0].get_text(strip=True)
                    title_tag = cols[1].find('b')
                    title = title_tag.get_text(strip=True) if title_tag else cols[1].get_text(strip=True)
                    medium_tag = cols[1].find('small')
                    medium_text = medium_tag.get_text(strip=True).lower() if medium_tag else "Unknown"

                    # Determine Medium and Medium Type
                    if "film" in medium_text:
                        medium = "Film"
                        medium_type = "Feature Film" if "Feature film" in medium_text else "Television Film"
                    elif "television" in medium_text or "tv" in medium_text or "series" in medium_text or "miniseries" in medium_text:
                        medium = "Television"
                        medium_type = "Television Series" if "series" in medium_text else "Television Episode"
                    elif "stage" in medium_text or "theatre" in medium_text:
                        medium = "Theatre"
                        medium_type = "Stage Play"
                    elif "musical" in medium_text:
                        medium = "Theatre"
                        medium_type = "Musical"
                    else:
                        medium = "Unknown"
                        medium_type = "Unknown"

                    pride_adaptations.append({
                        "Title": title,
                        "Year": year,
                        "Medium": medium,
                        "Medium Type": medium_type,
                        "Based On": "Pride and Prejudice",
                        "Direct or Loose Adaptation": "Direct"
                    })

# Function to extract looser adaptations
def extract_loose_adaptations():
    loose_adaptations_data = [
        {"Title": 'Wishbone\'s "Furst Impressions"', "Year": "1995", "Medium": "Television", "Medium Type": "Episode"},
        {"Title": 'Red Dwarf\'s "Beyond a Joke"', "Year": "1997", "Medium": "Television", "Medium Type": "Episode"},
        {"Title": "Bridget Jones's Diary", "Year": "2001", "Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": "Bride and Prejudice", "Year": "2004", "Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": "Pride & Prejudice: A Latter-Day Comedy", "Year": "2003", "Medium": "Film", "Medium Type": "Independent Film"},
        {"Title": "Kahiin Toh Hoga", "Year": "2003–2007", "Medium": "Television", "Medium Type": "Soap Opera"},
        {"Title": "Lost in Austen", "Year": "2008", "Medium": "Television", "Medium Type": "Television Series"},
        {"Title": "What is needed for a bachelor", "Year": "2008", "Medium": "Television", "Medium Type": "Television Series"},
        {"Title": "The Lizzie Bennet Diaries", "Year": "2012–2013", "Medium": "Web Series", "Medium Type": "Web Series"},
        {"Title": "Austenland", "Year": "2013", "Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": "Death Comes to Pemberley", "Year": "2013", "Medium": "Television", "Medium Type": "Television Series"},
        {"Title": "Pride and Prejudice and Zombies", "Year": "2016", "Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": "Before the Fall", "Year": "2016", "Medium": "Independent Film"},
        {"Title": "Unleashing Mr. Darcy", "Year": "2016", "Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": "Orgulho e Paixão", "Year": "2018", "Medium": "Television", "Medium Type": "Soap Opera"},
        {"Title": "Marrying Mr Darcy", "Year": "2018", "Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": "Pride and Prejudice: Atlanta", "Year": "2019", "Medium": "Television" ,"Medium Type": "Movie"},
        {"Title": "Pride and Prejudice, Cut", "Year": "2019", "Medium": "Television" , "Medium Type": "Movie"},
        {"Title": "Fire Island", "Year": "2022","Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": "An American in Austen", "Year": "2024", "Medium": "Film", "Medium Type": "Feature Film"},
        {"Title": 'Futurama\'s "The Day the Earth Stood Stupid"', "Year": "2001", "Medium": "Television", "Medium Type": "Episode"},
        {"Title": 'Doctor Who\'s "The Caretaker"', "Year": "2014", "Medium": "Television", "Medium Type": "Episode"},
        {"Title": "Marrying Mr Darcy", "Year": "2014", "Medium": "Board Game", "Medium Type": "Game"},
    ]
    
    for adaptation in loose_adaptations_data:
        # Set Medium type based on medium
        medium = adaptation["Medium"].lower()
        if "Feature film" in medium or "independent film" in medium:
            adaptation_type = "Feature Film"
            medium = "Film"
        elif "Television movie" in medium or "television film" in medium:
            adaptation_type = "Television Movie"
            medium = "Television"
        elif "television series" in medium or "web series" in medium or "soap opera" in medium:
            adaptation_type = "Television Series"
            medium = "Television"
        elif "television episode" in medium:
            adaptation_type = "Television Episode"
            medium = "Television"
        elif "stage play" in medium or "musical" in medium:
            adaptation_type = "Stage Play" if "stage play" in medium else "Musical"
            medium = "Theatre"
        elif "board game" in medium:
            adaptation_type = "Board Game"
            medium = "Game"
        else:
            adaptation_type = "Unknown"

        pride_adaptations.append({
            "Title": adaptation["Title"],
            "Year": adaptation["Year"],
            "Medium": medium.capitalize(),
            "Medium Type": adaptation_type,
            "Based On": "Pride and Prejudice",
            "Direct or Loose Adaptation": "Loose"
        })

# Function to extract theater adaptations
def extract_theater_adaptations():
    theater_adaptations_data = [
        {"Title": "The Bennets: A Play Without a Plot", "Year": "1901", "Medium": "Stage Play"},
        {"Title": "Pride and Prejudice (1935)", "Year": "1935", "Medium": "Stage Play"},
        {"Title": "First Impressions", "Year": "1959", "Medium": "Broadway Musical"},
        {"Title": "Pride and Prejudice by Jon Jory", "Year": "2006", "Medium": "Stage Play"},
        {"Title": "Pride and Prejudice (1995)", "Year": "1995", "Medium": "Musical"},
        {"Title": "I Love You Because", "Year": "2019", "Medium": "Musical"},
        {"Title": "Miss Bennet: Christmas at Pemberley", "Year": "2016", "Medium": "Stage Play"},
        {"Title": "Kate Hamill's Pride and Prejudice", "Year": "2017", "Medium": "Stage Play"},
        {"Title": "Pride and Prejudice* (*sort of)", "Year": "2018", "Medium": "Stage Play"}
    ]
    
    for adaptation in theater_adaptations_data:
        medium = adaptation["Medium"].lower()
        adaptation_type = "Stage Play" if "stage play" in medium else "Musical"
        medium = "Theatre"
        
        pride_adaptations.append({
            "Title": adaptation["Title"],
            "Year": adaptation["Year"],
            "Medium": medium,
            "Medium Type": adaptation_type,
            "Based On": "Pride and Prejudice",
            "Direct or Loose Adaptation": "Loose"
        })

# Step 2: Extract the data
extract_pride_direct_adaptations(soup)
extract_loose_adaptations()
extract_theater_adaptations()

# Step 3: Convert the list to a DataFrame
pride_adaptations_df = pd.DataFrame(pride_adaptations)

# Step 4: Display the combined DataFrame
print(pride_adaptations_df)

# Initialize lists to store adaptation data for Mansfield Park
mansfield_park_adaptations = []

# Function to extract direct adaptations for "Mansfield Park"
def extract_mansfield_park_direct_adaptations(soup):
   mansfield_section = soup.find('span', id='Mansfield_Park_.281814.29')
   if mansfield_section:
       wikitable = mansfield_section.find_next('table', class_='wikitable')
       if wikitable:
           for row in wikitable.find_all('tr')[1:]:  # Skip header row
               cols = row.find_all('td')
               if len(cols) >= 2:
                   year = cols[0].get_text(strip=True)
                   title_tag = cols[1].find('b')
                   title = title_tag.get_text(strip=True) if title_tag else cols[1].get_text(strip=True)
                   medium_tag = cols[1].find('small')
                   medium_text = medium_tag.get_text(strip=True).lower() if medium_tag else "Feature Film"  # Default to Feature Film if missing

                   # Verifica se é a adaptação específica de 1930
                   if title == "Mansfield Park" and year == "1930":
                       medium = "Film"
                       medium_type = "Feature Film"
                   else:
                       # Determine Medium and Medium Type (como no código original)
                       if "film" in medium_text:
                           medium = "Film"
                           medium_type = "Feature Film"
                       elif "television" in medium_text or "tv" in medium_text:
                           medium = "Television"
                           medium_type = "Television Film" if "movie" in medium_text else "Television Series"
                       elif "web" in medium_text:
                           medium = "Web Series"
                           medium_type = "Web Series"
                       elif "stage" in medium_text or "opera" in medium_text:
                           medium = "Theatre"
                           medium_type = "Stage Play" if "stage" in medium_text else "Musical" if "musical" in medium_text else "Chamber Opera"
                       else:
                           medium = "Unknown"
                           medium_type = "Unknown"
                  
                   mansfield_park_adaptations.append({
                       "Title": title,
                       "Year": year,
                       "Medium": medium,
                       "Medium Type": medium_type,
                       "Based On": "Mansfield Park",
                       "Direct or Loose Adaptation": "Direct"
                   })

# Function to extract looser adaptations for "Mansfield Park"
def extract_mansfield_park_loose_adaptations():
   loose_adaptations_data = [
       {
           "Title": "Metropolitan",
           "Year": "1990",
           "Medium": "Film",
           "Medium Type": "Feature Film",
           "Based On": "Mansfield Park",
           "Direct or Loose Adaptation": "Loose"
       },
       {
           "Title": "From Mansfield With Love",
           "Year": "2014",
           "Medium": "Web Series",
           "Medium Type": "Web Series",
           "Based On": "Mansfield Park",
           "Direct or Loose Adaptation": "Loose"
       }
   ]
  
   for adaptation in loose_adaptations_data:
       mansfield_park_adaptations.append(adaptation)

# Function to extract theater adaptations for "Mansfield Park"
def extract_mansfield_park_theater_adaptations():
   theater_adaptations_data = [
       {
           "Title": "Mansfield Park (opera)",
           "Year": "2011",
           "Medium": "Theatre",
           "Medium Type": "Chamber Opera",
           "Based On": "Mansfield Park",
           "Direct or Loose Adaptation": "Loose"
       },
       {
           "Title": "Mansfield Park (Stage adaptation)",
           "Year": "2012",
           "Medium": "Theatre",
           "Medium Type": "Stage Play",
           "Based On": "Mansfield Park",
           "Direct or Loose Adaptation": "Loose"
       }
   ]
  
   for adaptation in theater_adaptations_data:
       mansfield_park_adaptations.append(adaptation)

# Step 2: Extract the data
extract_mansfield_park_direct_adaptations(soup)
extract_mansfield_park_loose_adaptations()
extract_mansfield_park_theater_adaptations()

# Step 3: Convert the list to a DataFrame
mansfield_park_adaptations_df = pd.DataFrame(mansfield_park_adaptations)

# Step 4: Display the combined DataFrame
#print(mansfield_park_adaptations_df)

# Initialize list to store adaptation data for Emma
emma_adaptations = []

# Function to extract direct adaptations of "Emma"
def extract_emma_direct_adaptations(soup):
   emma_section = soup.find('span', id='Emma_.281815.29')
   if emma_section:
       wikitable = emma_section.find_next('table', class_='wikitable')
       if wikitable:
           for row in wikitable.find_all('tr')[1:]:  # Skip header row
               cols = row.find_all('td')
               if len(cols) >= 2:
                   year = cols[0].get_text(strip=True)
                   title_tag = cols[1].find('b')
                   title = title_tag.get_text(strip=True) if title_tag else cols[1].get_text(strip=True)
                   medium_tag = cols[1].find('small')
                   medium_text = medium_tag.get_text(strip=True).lower() if medium_tag else "Feature film"  # Default to Feature Film if missing


                   # Determine Medium and Medium Type
                   if "film" in medium_text:
                       medium = "Film"
                       medium_type = "Feature Film"
                   elif "television" in medium_text or "tv" in medium_text:
                       medium = "Television"
                       medium_type = "Television Film" if "movie" in medium_text else "Television Series"
                   elif "web" in medium_text:
                       medium = "Web Series"
                       medium_type = "Web Series"
                   elif "stage" in medium_text or "opera" in medium_text:
                       medium = "Theatre"
                       medium_type = "Stage Play" if "stage" in medium_text else "Musical" if "musical" in medium_text else "Chamber Opera"
                   else:
                       medium = "Unknown"
                       medium_type = "Unknown"


                   emma_adaptations.append({
                       "Title": title,
                       "Year": year,
                       "Medium": medium,
                       "Medium Type": medium_type,
                       "Based On": "Emma",
                       "Direct or Loose Adaptation": "Direct"
                   })

# Function to extract loose adaptations of "Emma"
def extract_emma_loose_adaptations():
   loose_adaptations_data = [
       {
           "Title": "Clueless",
           "Year": "1995",
           "Medium": "Film",
           "Medium Type": "Feature Film",
           "Based On": "Emma",
           "Direct or Loose Adaptation": "Loose"
       },
       {
           "Title": "Clueless",
           "Year": "1996",
           "Medium": "Television",
           "Medium Type": "Television Series",
           "Based On": "Emma",
           "Direct or Loose Adaptation": "Loose"
       },
       {
           "Title": "Aisha",
           "Year": "2010",
           "Medium": "Film",
           "Medium Type": "Feature Film",
           "Based On": "Emma",
           "Direct or Loose Adaptation": "Loose"
       },
       {
           "Title": "Emma Approved",
           "Year": "2013–2014",
           "Medium": "Web Series",
           "Medium Type": "Web Series",
           "Based On": "Emma",
           "Direct or Loose Adaptation": "Loose"
       }
   ]
  
   for adaptation in loose_adaptations_data:
       emma_adaptations.append(adaptation)

# Step 2: Extract direct and loose adaptations data
extract_emma_direct_adaptations(soup)
extract_emma_loose_adaptations()

# Step 3: Convert the list to a DataFrame
emma_adaptations_df = pd.DataFrame(emma_adaptations)

# Step 4: Display the combined DataFrame
#print(emma_adaptations_df)

# Initialize list to store adaptation data for Northanger Abbey
northanger_adaptations = []

# Function to extract direct adaptations for "Northanger Abbey"
def extract_northanger_direct_adaptations(soup):
   northanger_section = soup.find('span', id='Northanger_Abbey_.281817.29')
   if northanger_section:
       wikitable = northanger_section.find_next('table', class_='wikitable')
       if wikitable:
           for row in wikitable.find_all('tr')[1:]:  # Skip header row
               cols = row.find_all('td')
               if len(cols) >= 2:
                   year = cols[0].get_text(strip=True)
                   title_tag = cols[1].find('b')
                   title = title_tag.get_text(strip=True) if title_tag else cols[1].get_text(strip=True)
                   medium_tag = cols[1].find('small')
                   medium_text = medium_tag.get_text(strip=True).lower() if medium_tag else "Feature film"  # Default to Feature Film if missing


                   # Determine Medium and Medium Type
                   if "film" in medium_text:
                       medium = "Film"
                       medium_type = "Feature Film"
                   elif "television" in medium_text or "tv" in medium_text:
                       medium = "Television"
                       medium_type = "Television Film" if "movie" in medium_text else "Television Series"
                   elif "web" in medium_text:
                       medium = "Web Series"
                       medium_type = "Web Series"
                   elif "stage" in medium_text or "opera" in medium_text:
                       medium = "Theatre"
                       medium_type = "Stage Play" if "stage" in medium_text else "Musical" if "musical" in medium_text else "Chamber Opera"
                   else:
                       medium = "Unknown"
                       medium_type = "Unknown"
                  
                   northanger_adaptations.append({
                       "Title": title,
                       "Year": year,
                       "Medium": medium,
                       "Medium Type": medium_type,
                       "Based On": "Northanger Abbey",
                       "Direct or Loose Adaptation": "Direct"
                   })

# Function to extract loose adaptations for "Northanger Abbey"
def extract_northanger_loose_adaptations(soup):
   loose_adaptations_section = soup.find('h4', id='Looser_adaptations_5')
   if loose_adaptations_section:
       ul_tag = loose_adaptations_section.find_next('ul')
       li_tags = ul_tag.find_all('li')
      
       for li in li_tags:
           # Extract the title (often wrapped in <i> or <a> tags)
           title_tag = li.find('i') or li.find('a')
           title = title_tag.get_text(strip=True) if title_tag else li.get_text(strip=True)
          
           # Extract the year from the text using a regex
           year_match = re.search(r'\((\d{4})\)', li.get_text())
           year = year_match.group(1) if year_match else "Unknown"
          
           # Medium and Direct or Loose Adaptation
           if title == "Ruby in Paradise":
               medium = "Film"
               medium_type = "Feature Film"
           elif "Wishbone" in title:
               title = "Wishbone's Pup Fiction"
               medium = "Television"
               medium_type = "Television Episode"
           else:
               text = li.get_text().lower()
               if "film" in text or "movie" in text:
                   medium = "Film"
                   medium_type = "Feature Film"
               elif "television" in text or "tv" in text or "series" in text:
                   medium = "Television"
                   medium_type = "Television Series"
               elif "web" in text or "youtube" in text:
                   medium = "Web Series"
                   medium_type = "Web Series"
               elif "stage" in text or "theatre" in text:
                   medium = "Theatre"
                   medium_type = "Stage Play"
               elif "musical" in text:
                   medium = "Theatre"
                   medium_type = "Musical"
               else:
                   medium = "Unknown"
                   medium_type = "Unknown"
          
           # Append the collected data to the list
           northanger_adaptations.append({
               "Title": title,
               "Year": year,
               "Medium": medium,
               "Medium Type": medium_type,
               "Based On": "Northanger Abbey",
               "Direct or Loose Adaptation": "Loose"
           })

# Extract the adaptations
extract_northanger_direct_adaptations(soup)
extract_northanger_loose_adaptations(soup)

# Convert the list to a DataFrame
northanger_adaptations_df = pd.DataFrame(northanger_adaptations)

# Display the DataFrame
#print(northanger_adaptations_df)

# Initialize list to store adaptation data for Persuasion
persuasion_adaptations = []

# Function to extract direct adaptations of "Persuasion"
def extract_persuasion_direct_adaptations(soup):
   persuasion_section = soup.find('span', id='Persuasion_.281817.29')
   if persuasion_section:
       wikitable = persuasion_section.find_next('table', class_='wikitable')
       if wikitable:
           for row in wikitable.find_all('tr')[1:]:  # Skip header row
               cols = row.find_all('td')
               if len(cols) >= 2:
                   year = cols[0].get_text(strip=True)
                   title_tag = cols[1].find('b')
                   title = title_tag.get_text(strip=True) if title_tag else cols[1].get_text(strip=True)
                   medium_tag = cols[1].find('small')
                   medium_text = medium_tag.get_text(strip=True).lower() if medium_tag else "Feature film"  # Default to Feature Film if missing


                   # Determine Medium and Medium Type
                   if "film" in medium_text:
                       medium = "Film"
                       medium_type = "Feature Film" if "feature" in medium_text else "Television Film"
                   elif "television" in medium_text or "tv" in medium_text:
                       medium = "Television"
                       medium_type = "Television Series" if "miniseries" in medium_text else "Television Series"
                   elif "web" in medium_text:
                       medium = "Web Series"
                       medium_type = "Web Series"
                   else:
                       medium = "Unknown"
                       medium_type = "Unknown"
                  
                   persuasion_adaptations.append({
                       "Title": title,
                       "Year": year,
                       "Medium": medium,
                       "Medium Type": medium_type,
                       "Based On": "Persuasion",
                       "Direct or Loose Adaptation": "Direct"
                   })

# Function to extract loose adaptations of "Persuasion"
def extract_persuasion_loose_adaptations(soup):
   loose_adaptations_section = soup.find('h4', id='Looser_adaptations_6')
   if loose_adaptations_section:
       ul_tag = loose_adaptations_section.find_next('ul')
       li_tags = ul_tag.find_all('li')
      
       for li in li_tags:
           # Extract the title (often wrapped in <i> or <a> tags)
           title_tag = li.find('i') or li.find('a')
           title = title_tag.get_text(strip=True) if title_tag else li.get_text(strip=True)
          
           # Extract the year from the text using a regex
           year_match = re.search(r'\((\d{4})\)', li.get_text())
           year = year_match.group(1) if year_match else "Unknown"
          
           # Determine Medium and Medium Type
           text = li.get_text().lower()
           if "film" in text or "movie" in text:
               medium = "Film"
               medium_type = "Feature Film"
           elif "television" in text or "tv" in text or "series" in text:
               medium = "Television"
               medium_type = "Television Series"
           elif "web" in text or "web series" in text:
               medium = "Web Series"
               medium_type = "Web Series"
           elif "novel" in text or "book" in text:
               medium = "Novel"
               medium_type = "Novel"
           else:
               medium = "Unknown"
               medium_type = "Unknown"
          
           # Append the collected data to the list
           persuasion_adaptations.append({
               "Title": title,
               "Year": year,
               "Medium": medium,
               "Medium Type": medium_type,
               "Based On": "Persuasion",
               "Direct or Loose Adaptation": "Loose"
               })
      
       # Adding manually extracted adaptations as per your request
       loose_adaptations_data = [
           {
               "Title": "Bridget Jones: The Edge of Reason",
               "Year": "2001",
               "Medium": "Novel",
               "Medium Type": "Novel",
               "Based On": "Persuasion",
               "Direct or Loose Adaptation": "Loose"
           },
           {
               "Title": "Rational Creatures",
               "Year": "2020",
               "Medium": "Web Series",
               "Medium Type": "Web Series",
               "Based On": "Persuasion",
               "Direct or Loose Adaptation": "Loose"
           },
           {
               "Title": "Modern Persuasion",
               "Year": "2020",
               "Medium": "Film",
               "Medium Type": "Feature Film",
               "Based On": "Persuasion",
               "Direct or Loose Adaptation": "Loose"
           }
       ]
      
       # Append manually collected loose adaptations data
       for adaptation in loose_adaptations_data:
           persuasion_adaptations.append(adaptation)

# Step 2: Extract data for both direct and loose adaptations
extract_persuasion_direct_adaptations(soup)
extract_persuasion_loose_adaptations(soup)

# Step 3: Convert the list of adaptations to a DataFrame
persuasion_adaptations_df = pd.DataFrame(persuasion_adaptations)

# Step 4: Display the combined DataFrame
print(persuasion_adaptations_df)

# Initialize list to store adaptation data for Sanditon
sanditon_adaptations = []

# Function to extract direct adaptations for "Sanditon"
def extract_sanditon_direct_adaptations(soup):
   sanditon_section = soup.find('span', id='Sanditon_.281817.2F1925.29')
   if sanditon_section:
       wikitable = sanditon_section.find_next('table', class_='wikitable')
       if wikitable:
           for row in wikitable.find_all('tr')[1:]:  # Skip header row
               cols = row.find_all('td')
               if len(cols) >= 2:
                   year = cols[0].get_text(strip=True)
                   title_tag = cols[1].find('a')
                   title = title_tag.get_text(strip=True) if title_tag else cols[1].get_text(strip=True)
                   medium_tag = cols[1].find('small')
                   medium_text = medium_tag.get_text(strip=True).lower() if medium_tag else "Feature film"  # Default to Feature Film if missing


                   # Determine Medium and Medium Type
                   if "film" in medium_text:
                       medium = "Film"
                       medium_type = "Feature Film"
                   elif "television" in medium_text or "tv" in medium_text:
                       medium = "Television"
                       medium_type = "Television Series"
                   elif "web" in medium_text:
                       medium = "Web Series"
                       medium_type = "Web Series"
                   elif "stage" in medium_text or "opera" in medium_text:
                       medium = "Theatre"
                       medium_type = "Stage Play" if "stage" in medium_text else "Musical" if "musical" in medium_text else "Chamber Opera"
                   else:
                       medium = "Unknown"
                       medium_type = "Unknown"
                  
                   sanditon_adaptations.append({
                       "Title": title,
                       "Year": year,
                       "Medium": medium,
                       "Medium Type": medium_type,
                       "Based On": "Sanditon",
                       "Direct or Loose Adaptation": "Direct"
                   })

# Function to extract loose adaptations for "Sanditon"
def extract_sanditon_loose_adaptations(soup):
   loose_adaptations_section = soup.find('span', id='Sanditon_.281817.2F1925.29')
   if loose_adaptations_section:
       # Locate the unordered list following the loose adaptations heading
       loose_heading = loose_adaptations_section.find_next('h4', string=re.compile("Looser adaptations"))
       if loose_heading:
           ul_tag = loose_heading.find_next('ul')
           li_tags = ul_tag.find_all('li')
          
           for li in li_tags:
               # Extract the title (often wrapped in <i> or <a> tags)
               title_tag = li.find('i') or li.find('a')
               title = title_tag.get_text(strip=True) if title_tag else li.get_text(strip=True)
              
               # Extract the year from the text using a regex
               year_match = re.search(r'\((\d{4})\)', li.get_text())
               year = year_match.group(1) if year_match else "Unknown"
              
               # Determine Medium and Direct or Loose Adaptation
               if "Welcome To Sanditon" in title:
                   medium = "Web Series"
                   medium_type = "Web Series"
               else:
                   text = li.get_text().lower()
                   if "film" in text or "movie" in text:
                       medium = "Film"
                       medium_type = "Feature Film"
                   elif "television" in text or "tv" in text or "series" in text:
                       medium = "Television"
                       medium_type = "Television Series"
                   elif "web" in text or "web series" in text:
                       medium = "Web Series"
                       medium_type = "Web Series"
                   elif "stage" in text or "theatre" in text:
                       medium = "Theatre"
                       medium_type = "Stage Play"
                   elif "musical" in text:
                       medium = "Theatre"
                       medium_type = "Musical"
                   else:
                       medium = "Unknown"
                       medium_type = "Unknown"
              
               # Append the collected data to the list
               sanditon_adaptations.append({
                   "Title": title,
                   "Year": year,
                   "Medium": medium,
                   "Medium Type": medium_type,
                   "Based On": "Sanditon",
                   "Direct or Loose Adaptation": "Loose"
               })


# Extract the adaptations
extract_sanditon_direct_adaptations(soup)
extract_sanditon_loose_adaptations(soup)

# Convert the list to a DataFrame
sanditon_adaptations_df = pd.DataFrame(sanditon_adaptations)

# Display the DataFrame
#print(sanditon_adaptations_df)

# Initialize a list to store the data for both Lady Susan and The Watsons adaptations
adaptations = []

# Function to extract direct adaptations of "Lady Susan"
def extract_lady_susan_adaptations(soup):
    # Use the specific section ID for "Lady Susan"
    lady_susan_section = soup.find('span', id='Lady_Susan_.281871.29')
    if lady_susan_section:
        # Find the next table with class 'wikitable'
        wikitable = lady_susan_section.find_next('table', class_='wikitable')
        if wikitable:
            # Iterate over each row, skipping the header
            for row in wikitable.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    year = cols[0].get_text(strip=True)
                    title_tag = cols[1].find('i') or cols[1].find('b')  # Try to find italic or bold text for the title
                    title = title_tag.get_text(strip=True) if title_tag else cols[1].get_text(strip=True)
                    medium_tag = cols[1].find('small')
                    medium = medium_tag.get_text(strip=True) if medium_tag else "Unknown"
                    
                    # Determine the medium type based on medium text
                    medium_type = "Feature Film" if "Feature film" in medium.lower() else "Unknown"
                    
                    # Append the extracted information to the adaptations list
                    adaptations.append({
                        "Title": title,
                        "Year": year,
                        "Medium": "Film",
                        "Medium Type": "Feature Film",  
                        "Based On": "Lady Susan",
                        "Direct or Loose Adaptation": "Direct"
                    })

# Function to extract theatre adaptations of "The Watsons"
def extract_the_watsons_adaptations(soup):
    # Use the specific section ID for "The Watsons"
    watsons_section = soup.find('span', id='The_Watsons_.281871.29')
    if watsons_section:
        # Manually add the known adaptation details for "The Watsons"
        adaptations.append({
            "Title": "Laura Wade's adaptation of 'The Watsons'",
            "Year": "2018",
            "Medium": "Theatre",
            "Medium Type": "Stage Play",  
            "Based On": "The Watsons",
            "Direct or Loose Adaptation": "Loose"
        })

# Step 2: Extract data for adaptations of Lady Susan and The Watsons
extract_lady_susan_adaptations(soup)
extract_the_watsons_adaptations(soup)

# Step 3: Convert the list of adaptations to a DataFrame
adaptations_df = pd.DataFrame(adaptations)

# Step 4: Display the combined DataFrame
#print(adaptations_df)

# Assuming all your adaptation DataFrames are already created as follows:
sense_adaptations = pd.DataFrame(sense_direct_adaptations)
pride_adaptations_df = pd.DataFrame(pride_adaptations)
mansfield_park_adaptations_df = pd.DataFrame(mansfield_park_adaptations)
emma_adaptations_df = pd.DataFrame(emma_adaptations)
northanger_adaptations_df = pd.DataFrame(northanger_adaptations)
persuasion_adaptations_df = pd.DataFrame(persuasion_adaptations)
sanditon_adaptations_df = pd.DataFrame(sanditon_adaptations)
lady_susan_and_watsons_adaptations_df = pd.DataFrame(adaptations)

# Combine all DataFrames into one
all_adaptations = pd.concat([
    sense_adaptations,
    pride_adaptations_df,
    mansfield_park_adaptations_df,
    emma_adaptations_df,
    northanger_adaptations_df,
    persuasion_adaptations_df,
    sanditon_adaptations_df,
    lady_susan_and_watsons_adaptations_df
], ignore_index=True)

# Assuming all_adaptations is your combined DataFrame

# 2. Fill in missing information for specific rows

# Updating 'Sense and Sensibility' 2024 entry
all_adaptations.loc[
    (all_adaptations['Title'] == 'Sense and Sensibility') & (all_adaptations['Year'] == '2024'), 
    ['Medium', 'Medium Type']] = ['Theatre', 'Stage Play']

# Updating 'What is needed for a bachelor?' 2008 entry
all_adaptations.loc[
    (all_adaptations['Title'] == 'What is needed for a bachelor?') & (all_adaptations['Year'] == '2008'), 
    ['Medium', 'Medium Type']] = ['Television', 'Television Series']

# Updating 'The Edge of Reason' 2001 entry
all_adaptations.loc[
    (all_adaptations['Title'] == 'The Edge of Reason') & (all_adaptations['Year'] == '2001'), 
    ['Medium', 'Medium Type']] = ['Novel', 'Novel']

# Updating 'Rational Creatures' 2020 entry
all_adaptations.loc[
    (all_adaptations['Title'] == 'Rational Creatures') & (all_adaptations['Year'] == '2020'), 
    ['Medium', 'Medium Type']] = ['Web Series', 'Web Series']

# Updating 'Modern Persuasion' 2020 entry
all_adaptations.loc[
    (all_adaptations['Title'] == 'Modern Persuasion') & (all_adaptations['Year'] == '2020'), 
    ['Medium', 'Medium Type']] = ['Film', 'Feature Film']

# Display the updated DataFrame
print(all_adaptations)

all_adaptations.to_csv('alladaptations.csv', index=False)

# EDA
print(all_adaptations.describe(include='all'))  # Summary statistics, including categorical data

# Check for Missing Values
print(all_adaptations.isnull().sum())  # Count missing values per column

# Identify Duplicates
print(all_adaptations.duplicated().sum())  # Count duplicate rows

# Data Cleaning

# Handling missing data
all_adaptations['Year'] = all_adaptations['Year'].fillna('Unknown')

# Remove Duplicates
all_adaptations.drop_duplicates(inplace=True)

# Identify Duplicates
print(all_adaptations.duplicated().sum())

# Step 1: Load the CSV file once
df = pd.read_csv('alladaptations.csv')

# Step 2: Drop the specific row with "Rational Creatures"
condition_rational = (df['Title'] == 'Rational Creatures') & \
                    (df['Medium'] == 'Television') & \
                    (df['Medium Type'] == 'Television Series') & \
                    (df['Based On'] == 'Persuasion')
df = df[~condition_rational]

# Step 3: Exclude rows where 'Medium' is 'Novel'
df = df[df['Medium'] != 'Novel']

# Step 4: Modify 'Medium' and 'Medium Type' for 'Television Film' and 'Television Movie'
df.loc[(df['Medium Type'] == 'Television Film') | (df['Medium Type'] == 'Television Movie'), 'Medium'] = 'Television'
df.loc[(df['Medium Type'] == 'Television Film') | (df['Medium Type'] == 'Television Movie'), 'Medium Type'] = 'Television Movie'

# Step 5: Save the cleaned DataFrame to a new CSV file
df.to_csv('alladaptations_cleaned.csv', index=False)

print("Data cleaned and saved as alladaptations_cleaned.csv")
print(df)

# Agrupe os dados por 'Based On' e conte o número de adaptações
adaptations_per_book = df.groupby('Based On')['Title'].count().reset_index()

# Crie o gráfico de barras
plt.figure(figsize=(10, 6))  # Ajuste o tamanho do gráfico
sns.barplot(x='Based On', y='Title', data=adaptations_per_book)

# Adicione um título
plt.title('Adaptações por Obra')

# Adicione labels nos eixos
plt.xlabel('Obra')
plt.ylabel('Número de Adaptações')

# Ajuste a rotação das labels no eixo X para melhor visualização
plt.xticks(rotation=45)

# Mostre o gráfico
plt.show()

# Agrupe os dados por 'Based On' e conte o número de adaptações (como no exemplo anterior)
adaptations_per_book = df.groupby('Based On')['Title'].count().reset_index()

## Ordene as fatias pelo número de adaptações
adaptations_per_book = adaptations_per_book.sort_values(by='Title', ascending=False)

# Agrupe os dados por 'Based On' e 'Medium' e conte o número de adaptações
adaptations_by_book_and_medium = df.groupby(['Based On', 'Medium'])['Title'].count().reset_index()

# Crie o gráfico de barras empilhadas
plt.figure(figsize=(12, 6))
sns.barplot(x='Based On', y='Title', hue='Medium', data=adaptations_by_book_and_medium, dodge=False) 

# Adicione um título
plt.title('Distribuição de Adaptações por Obra e Meio')

# Adicione labels nos eixos
plt.xlabel('Obra')
plt.ylabel('Número de Adaptações')

# Ajuste a rotação das labels no eixo X para melhor visualização
plt.xticks(rotation=45)

# Mostre o gráfico
plt.show()

# Agrupe os dados por 'Medium' e 'Medium Type' e conte o número de adaptações
adaptations_by_medium_and_type = df.groupby(['Medium', 'Medium Type'])['Title'].count().reset_index()

# Crie o gráfico de linhas
plt.figure(figsize=(12, 6))
sns.lineplot(x='Medium', y='Title', hue='Medium Type', data=adaptations_by_medium_and_type, marker='o')

# Adicione um título
plt.title('Distribuição de Adaptações por Tipo de Meio')

# Adicione labels nos eixos
plt.xlabel('Meio')
plt.ylabel('Número de Adaptações')

# Ajuste a rotação das labels no eixo X para melhor visualização
plt.xticks(rotation=45)

# Mostre o gráfico
plt.show()

# Agrupe os dados por 'Based On', 'Medium', e 'Medium Type' e conte o número de adaptações
adaptations_by_book_medium_type = df.groupby(['Based On', 'Medium', 'Medium Type'])['Title'].count().reset_index()

# Criar uma nova coluna que combine 'Medium' e 'Medium Type'
df['Medium_MediumType'] = df['Medium'] + ' - ' + df['Medium Type']

# Agrupar os dados por 'Based On' e 'Medium_MediumType'
adaptations_by_book_medium_type = df.groupby(['Based On', 'Medium_MediumType'])['Title'].count().reset_index()

# Criar o gráfico de barras agrupadas
plt.figure(figsize=(12, 8))
sns.barplot(x='Based On', y='Title', hue='Medium_MediumType', data=adaptations_by_book_medium_type, dodge=True)

# Adicionar título e labels
plt.title('Comparação entre Obras: Número de Adaptações por Meio e Tipo')
plt.xlabel('Obra')
plt.ylabel('Número de Adaptações')

# Ajustar rotação dos labels no eixo X para melhor visualização
plt.xticks(rotation=45)

# Mostrar o gráfico
plt.show()

# Agrupar os dados por 'Based On' e 'Direct or Loose Adaptation'
adaptations_by_type = df.groupby(['Based On', 'Direct or Loose Adaptation'])['Title'].count().reset_index()

# Criar gráfico de barras empilhadas
plt.figure(figsize=(12, 6))
sns.barplot(x='Based On', y='Title', hue='Direct or Loose Adaptation', data=adaptations_by_type)

# Título e rótulos
plt.title('Número de Adaptações Diretas e Livres por Obra')
plt.xlabel('Obra')
plt.ylabel('Número de Adaptações')
plt.xticks(rotation=45)

# Mostrar gráfico
plt.show()

# Filtrar anos válidos e converter para números
df_filtered = df[df['Year'].apply(lambda x: x.isnumeric())]
df_filtered.loc[:, 'Year'] = df_filtered['Year'].fillna('Unknown') 
# OR
# df_filtered['Year'] = df_filtered['Year'].fillna('Unknown') 

# Criar o histograma
plt.figure(figsize=(12, 6))
sns.histplot(df_filtered['Year'], bins=20, kde=False)

# Título e rótulos
plt.title('Distribuição de Adaptações ao Longo do Tempo')
plt.xlabel('Ano')
plt.ylabel('Número de Adaptações')

# Mostrar gráfico
plt.show()

# Contar o número de adaptações por 'Medium'
medium_counts = df['Medium'].value_counts()

# Criar o gráfico de pizza
plt.figure(figsize=(8, 8))
plt.pie(medium_counts, labels=medium_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set2'))

# Título
plt.title('Proporção de Adaptações por Meio')

# Mostrar gráfico
plt.show()

# Contar o número de adaptações por ano e obra
adaptations_per_year = df_filtered.groupby(['Year', 'Based On'])['Title'].count().reset_index()

# Criar o gráfico de linha
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Title', hue='Based On', data=adaptations_per_year, marker='o')

# Título e rótulos
plt.title('Evolução das Adaptações ao Longo do Tempo por Obra')
plt.xlabel('Ano')
plt.ylabel('Número de Adaptações')

# Mostrar gráfico
plt.show()

# Tabela cruzada entre 'Based On' e 'Medium'
heatmap_data = pd.crosstab(df['Based On'], df['Medium'])

# Criar o gráfico de calor
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap="Blues", fmt='d')

# Título
plt.title('Correlação entre Obras e Meios de Adaptação')

# Mostrar gráfico
plt.show()
