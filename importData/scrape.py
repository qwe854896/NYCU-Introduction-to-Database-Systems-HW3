import requests
import pandas as pd

from bs4 import BeautifulSoup
import lxml.html as lh


def find_console_tags(soup):
    # Console tags are stored as images, so we find the image tag and record its 'alt' value as text
    consoles = list()
    for img in soup.find_all('img'):
        if 'images/consoles'in img['src']:
            # Cut file path elements from string
            console_tag = (img['src'][17:-6])
            consoles.append(img['alt'])
    return consoles


# Find the names of games from the links
def find_names_column(table_path):
    names_list = list()
    for row in table_path.xpath('.//tr'):
        for td in row.xpath('.//td'):
            if not td.find('a') is None:
                names_list.append(td.find('a').text.strip()) 
    return names_list


# Write a function that takes in a VGChartz URL and gives us all the data in their video game database
def scrape_vgchartz_videogame_db_page(url):
    
    response = requests.get(url)

    ### Check the Status
    assert(response.status_code == 200)," Website not OK " # status code = 200 => OK
    
    #Store the contents of the website under doc
    page=response.text
    soup = BeautifulSoup(page, "lxml")
    doc = lh.fromstring(response.content)
    
    # Selects the table with all the data in it on HTML using xpath
    target_table_path = doc.xpath('//*[@id="generalBody"]/table')[0]

    # Find column values that won't be scraped correctly with .text option
    names_list = find_names_column(target_table_path)
    consoles = find_console_tags(soup)
    if len(names_list) == 0:
        return pd.DataFrame()
    
    # Parse non-image and non-URL info from the data table to a pandas DataFrame
    row_dict={}
    df=pd.DataFrame()
    row_list= list()
    for counter,row in enumerate(target_table_path.xpath(".//tr")):
        if counter > 2: # To skip header rows
            row_list=[td.text for td in row.xpath(".//td")]
            row_dict[counter] = row_list

    df=pd.DataFrame.from_dict(row_dict).transpose()
    df.columns = ['position','game','blank','console','publisher','developer','vgchart_score',\
                 'critic_score','user_score','total_shipped','total_sales',\
                  'na_sales','pal_sales','japan_sales','other_sales',\
                  'release_date','last_update']
    
    # Correct the console and game columns using scraped values
    
    df=df.reset_index().drop(columns = ['index','position', 'blank', 'total_shipped','last_update', 'vgchart_score'])
    for i in df:
        for j in range(len(df[i])):
            df[i][j] = df[i][j].strip()
            if df[i][j] == 'N/A':
                df[i][j] = None
    for i in range(len(df['release_date'])):
        if df['release_date'][i] != None:
            x = int(df['release_date'][i][-2:])
            if x < 40:
                x += 2000
            else:
                x += 1900
            df['release_date'][i] = str(x)
        if df['na_sales'][i] != None:
            df['na_sales'][i] = df['na_sales'][i][:-1]
        if df['japan_sales'][i] != None:
            df['japan_sales'][i] = df['japan_sales'][i][:-1]
        if df['pal_sales'][i] != None:
            df['pal_sales'][i] = df['pal_sales'][i][:-1]
        if df['other_sales'][i] != None:
            df['other_sales'][i] = df['other_sales'][i][:-1]
        if df['total_sales'][i] != None:
            df['total_sales'][i] = df['total_sales'][i][:-1]

    df['console'] = consoles
    df['game'] = names_list
    df = df.rename(columns = {
        'game' : 'Name', 
        'console' : 'Platform', 
        'publisher': 'Publisher',
        'developer': 'Developer',
        'critic_score': 'Critic_Score',
        'user_score' : 'User_Score',
        'total_sales': 'Global_Sales',
        'na_sales' : 'NA_Sales',
        'pal_sales' : 'EU_Sales',
        'japan_sales' : 'JP_Sales',
        'other_sales' : 'Other_Sales',
        'release_date' : 'Year_of_Release'})
    return df


# We can 'hack' the URL to display any number of results per page. I'll leave it as an argument.
def scrape_all_vg_chartz_videogame_db(results_per_page):
    df = pd.DataFrame()
    Genres="Action,Action-Adventure,Adventure,Board,Game,Education,Fighting,Misc,MMO,Music,Party,Platform,Puzzle,Racing,Role-Playing,Sandbox,Shooter,Simulation,Sports,Strategy,VisualNovel"
    Genres = Genres.split(',')
    # print(Genres)
    games_left = True
    not_changed = True
    # use this for test
    #for i in Genres[0:1]:
    for i in Genres:
        # print(i)
        current_page = 1
        while True:
            url = "https://www.vgchartz.com/games/games.php?page="+str(current_page)+"&name=&keyword=&console=&region=All&developer=&publisher=&goty_year=&genre=" + i + "&boxart=Both&banner=Both&ownership=Both&showmultiplat=No&results="+ str(results_per_page) + "&order=Sales&showtotalsales=1&showtotalsales=1&showpublisher=1&showpublisher=1&showvgchartzscore=1&showvgchartzscore=1&shownasales=1&shownasales=1&showdeveloper=1&showdeveloper=1&showcriticscore=1&showcriticscore=1&showpalsales=1&showpalsales=1&showreleasedate=1&showreleasedate=1&showuserscore=1&showuserscore=1&showjapansales=1&showjapansales=1&showlastupdate=1&showlastupdate=1&showothersales=1&showothersales=1&showshipped=1&showshipped=1"
            # print(url)
            new_df = scrape_vgchartz_videogame_db_page(url)
            current_page += 1
            if len(new_df) == 0:
                break
            l = []
            N = []
            for j in range(len(new_df)):
                l.append(i)
                N.append(None)
            new_df['Genre'] = l
            new_df['Critic_Count'] = N
            new_df['User_Count'] = N
            new_df['Rating'] = N
            new_df = new_df[['Name', 'Platform','Year_of_Release', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales', 'Critic_Score', 'Critic_Count', 'User_Score', 'User_Count', 'Developer', 'Rating']]
            if not_changed:
                df = new_df
                not_changed = False
                continue
            df = df.append(new_df)
            break

    return df

def scrapeTodf():
    # Run the code to scrape! I did 10,000 rows per page to speed things up.
    # use this for test
    # df=scrape_all_vg_chartz_videogame_db(1)
    df=scrape_all_vg_chartz_videogame_db(10000)
    # Compress and store for later!
    # Change 
    df["NA_Sales"] = pd.to_numeric(df["NA_Sales"])
    df["EU_Sales"] = pd.to_numeric(df["EU_Sales"])
    df["JP_Sales"] = pd.to_numeric(df["JP_Sales"])
    df["Other_Sales"] = pd.to_numeric(df["Other_Sales"])
    df["Global_Sales"] = pd.to_numeric(df["Global_Sales"])
    df["Critic_Score"] = pd.to_numeric(df["Critic_Score"])
    df["Critic_Count"] = pd.to_numeric(df["Critic_Count"])
    df["User_Count"] = pd.to_numeric(df["User_Count"])
    return df
