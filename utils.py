from requests import get
from bs4 import BeautifulSoup
import unicodedata

def get_game_suffix(date, team1, team2):
    r = get(f'https://www.basketball-reference.com/boxscores/index.fcgi?year={date.year}&month={date.month}&day={date.day}')
    suffix = None
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for table in soup.find_all('table', attrs={'class': 'teams'}):
            for anchor in table.find_all('a'):
                if 'boxscores' in anchor.attrs['href']:
                    if team1 in anchor.attrs['href'] or team2 in anchor.attrs['href']:
                        suffix = anchor.attrs['href']
    return suffix

"""Alexis changes: added name normalization and special character controls to account for
   uncommon and foreign player names. Removed odd unicode whitespace being unexplainably
   introduced by the replace or split function. Where the old function would fail in constructing
   a valid suffix, this one simply hard-constructs the player suffix. However, it can easily deprecate.
   Added the option to overwrite the original code and access a hard coded player suffix."""
def get_player_suffix(name, overwrite):
    normalized_name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    names = normalized_name.split(' ')[1:]
    for last_name in names:
        initial = last_name[0].lower()
        if not overwrite:
            r = get(f'https://www.basketball-reference.com/players/{initial}')
            if r.status_code==200:
                soup = BeautifulSoup(r.content, 'html.parser')
                for table in soup.find_all('table', attrs={'id': 'players'}):
                    for anchor in table.find_all('a'):
                        if anchor.text in name:
                            suffix = anchor.attrs['href']
                            return suffix
    
    names = normalized_name.split()
    names[0] = names[0].replace('\x8d','').lower()
    names[1] = names[1].replace('\x8d','').lower()
    names[0] = names[0].replace('\x81','').lower()
    names[1] = names[1].replace('\x81','').lower()
    suffix = "/players/" + initial + "/" + names[1][:5] + names[0][:2] + "01.html"
    return suffix
