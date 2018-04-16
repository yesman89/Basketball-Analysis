import bs4 as bs
from urllib.request import urlopen
import pandas as pd

def getBarkleyData(first_name, last_name):
    """
    :param first_name: string (required) first name of the basketball player
    :param last_name: string (required) last name of the basketball player
    :return: panda data frame of with data the contains all of the stats of the basketball player in his career

    """
    x = 'https://www.basketball-reference.com/players/'
    if len(last_name) < 6:
        url = x + last_name.lower()[0] + '/' + last_name.lower() + first_name.lower()[0:2] + '01.html'
    else:
        url = x + last_name.lower()[0] + '/' + last_name.lower()[0:5] + first_name.lower()[0:2] + '01.html'

    sauce1 = urlopen(url)
    sauce2 = sauce1.read()
    barkley = bs.BeautifulSoup(sauce2, 'lxml')

    table = barkley.table
    table_rows = table.find_all('tr')

    count = 0
    count2 = 0
    header = ['Season', 'Tm', 'Lg']
    header2 = ['Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
               'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    table = []
    table2 = []

    for tr in table_rows:
        h = tr.find_all('a')
        row = [i.text for i in h]
        if count > 0 and row and len(row) > 2:
            table.append(row)
        count += 1

    df = pd.DataFrame(table, columns=header)

    for tr in table_rows:
        td = tr.find_all('td')
        row2 = [i.text for i in td]
        if count2 > 0 and row2[0] != '':
            table2.append(row2)
        count2 += 1

    full_df = pd.DataFrame(table2, columns=header2, index=df["Season"])
    
    full_df[['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
               'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']] = full_df[['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%',
               'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']].astype('float64')
    full_df[['Tm', 'Lg', 'Pos']] = full_df[['Tm', 'Lg', 'Pos']].astype('str')

    return full_df