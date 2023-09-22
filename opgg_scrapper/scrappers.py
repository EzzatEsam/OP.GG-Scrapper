import time
from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import tqdm
from .classes import *
from .helpers import *

def GetPlayers(leader_board_table : BeautifulSoup) -> list[Player] :
    players = leader_board_table.find_all('tr')

    players_instances = []
    for player in players :
        fields = player.find_all('td')
        player_name = fields[1].text
        player_rank = fields[2].text
        player_lp = int( fields[3].text[:-3].replace(',',''))
        champs = fields[4].findAll('a')
        champs = [champ.get('href').replace('/champions/' , '') for champ in champs]
        level = int(fields[5].text)
        wins = int(fields[6].find(class_ = 'w').text.replace('W',''))
        losses = int(fields[6].find(class_ = 'l').text.replace('L',''))
        
        players_instances.append(
            Player(
                name = player_name,
                rank = player_rank,
                lp = player_lp,
                level = level,
                wins = wins,
                losses = losses,
                most_played_champs= champs,
                games=[]
            )
        )
    return players_instances

def get_top_N_players(N : int , driver_insance : webdriver , region : str = 'eune') -> list[Player] :
    """
    Retrieves the top N players from the leaderboards.
    
    Parameters:
        - N (int): The number of top players to retrieve.
        - driver_instance (webdriver): The webdriver instance used to navigate the web.
        - region (str, optional): The region to retrieve players from. Defaults to 'eune'.
        
    Returns:
        - list[Player]: A list of Player objects representing the top N players.
    """
    num_pages = int(np.ceil(N /100)) 
    players = []
    for i in tqdm.tqdm (range(num_pages)) :
        link = f'https://www.op.gg/leaderboards/tier?page={i+1}&region={region.lower()}'
        load_page_with_timeout(driver_insance , link , 10)
        soup = BeautifulSoup(driver_insance.page_source, 'lxml')
        leader_board_table = soup.find('tbody')
        page_players =  GetPlayers(leader_board_table)
        #print(page_players)
        players += page_players
    
    return players[:N]



def extract_team_players(team_div ):
    # team_div = BeautifulSoup(team_div, 'lxml').find('table')
    #print(team_div)
    players = team_div.find('tbody' ,recursive=False ).find_all('tr' , recursive=False)
    players_instances = []
    for player in players:
        #print(player)
        champion = player.find('td', class_='champion').find('img')['alt']
        #print(f'Champion : {champion}')
        spells = [element['alt'] for element in player.find('td', class_='spells').find_all('img')]
        #print(spells[0] , spells[1])
        runes = [element['alt'] for element in player.find('td', class_='runes').find_all('img')]
        #print(runes[0] , runes[1])
        name = player.find('td', class_='name').find('a' , recursive=False).text
        #print(f"name : {name}")
        rank = player.find('td', class_='name').find('div',recursive = False).text
        #print(f"rank : {rank}")
        kda = player.find('div', class_='k-d-a').text
        #print(f"Kda : {kda}")
        damage_given = int(player.find('div', class_='dealt').text.replace(',',''))
        damage_taken = int(player.find('div', class_='taken').text.replace(',',''))
        wards = player.find('td', class_='ward').text.replace('\n','/').split('/')
        wards = [int(num) for num in wards]
        cs = int(player.find('td', class_='cs').find_all('div' , recursive=False)[0].text)
        items = [item['alt'] for item in player.find('td', class_='items').find_all('img')]
        players_instances.append(
            GameRecordPlayer(
                name = name,
                champion = champion,
                summoner_spells = spells,
                runes = runes,
                rank = rank,
                kda = kda,
                damage_given = damage_given,
                damage_taken = damage_taken,
                
                vision = wards,
                cs = cs,
                items = items
            )
        )
    return players_instances

def extract_game_data(game):
    soup = BeautifulSoup(game.get_attribute('outerHTML'), 'lxml').find('li')

    result = soup.find('div', class_='result').text
    game_type = soup.find('div', class_='type').text
    #print(result)
    if result == 'Victory':
        game_result = GameResult.WIN
    elif result == 'Defeat':
        game_result = GameResult.LOSE
    else:
        game_result = GameResult.REMAKE

    length_html = soup.find('div', class_='length').text
    game_length = time_string_to_seconds(length_html)

    champion_name = soup.find('div', class_='info').find('div', class_='champion').find('img')['alt']
    #print(champion_name)
    player_team_div = soup.find_all('div' , recursive=False)[1].find_all('div' , recursive=False)[0].find('table')

    player_team_label  = player_team_div.find('thead').find('tr').find('th').text

    other_team_div = soup.find_all('div' , recursive=False)[1].find_all('div' , recursive=False)[0].find('table')

    if game_result != GameResult.REMAKE :
        player_team_summaries = soup.find_all('div' , recursive=False)[1].find_all('div' , recursive=False)[0].find('div' ,class_='summary').find_all('div' , recursive=False)[0]

        other_team_summaries = soup.find_all('div' , recursive=False)[1].find_all('div' , recursive=False)[0].find('div' ,class_='summary').find_all('div' , recursive=False)[2]

    game_state = player_team_div['result']

    if 'blue' in player_team_label.lower() :
        
        red_team_div , blue_team_div = other_team_div , player_team_div
        if game_state == 'WIN'  :
            winning_team = Team.BLUE
            red_team_summaries , blue_team_summaries = other_team_summaries , player_team_summaries
        elif game_state == 'LOSE' :
            winning_team = Team.RED
            red_team_summaries , blue_team_summaries = other_team_summaries , player_team_summaries
        else :
            winning_team = None
    else :
        
        red_team_div , blue_team_div = player_team_div , other_team_div
        
        if game_state == 'WIN'  :
            winning_team = Team.RED
            red_team_summaries , blue_team_summaries = player_team_summaries , other_team_summaries
        elif game_state == 'LOSE' :
            winning_team = Team.BLUE
            red_team_summaries , blue_team_summaries = player_team_summaries , other_team_summaries
        else :
            winning_team = None

    if game_result != GameResult.REMAKE:
        red_data = red_team_summaries.find_all('div' , class_ = 'object' , recursive=False)
        red_barons = int(red_data[0].text)
        red_dragon_kills = int(red_data[1].text)
        red_towers = int(red_data[2].text)

        blue_data = blue_team_summaries.find_all('div' , class_ = 'object' , recursive=False)
        blue_barons = int(blue_data[0].text)
        blue_dragon_kills = int(blue_data[1].text)
        blue_towers = int(blue_data[2].text)
    else :
        red_barons = 0
        red_dragon_kills = 0
        red_towers = 0
        blue_barons = 0
        blue_dragon_kills = 0
        blue_towers = 0

    red_players = extract_team_players(red_team_div)
    blue_players = extract_team_players(blue_team_div)

    return GameRecord(
        result = game_result,
        winning_team = winning_team,
        game_type = game_type,
        game_time_seconds = game_length,
        red_team_players = red_players,
        blue_team_players = blue_players,
        red_team_barons= red_barons,
        red_team_dragons = red_dragon_kills,
        red_team_towers = red_towers,
        blue_team_barons = blue_barons,
        blue_team_dragons = blue_dragon_kills,
        blue_team_towers = blue_towers,
        record_owner = None,
        owner_champion=champion_name
    )

def get_player_N_games(player_name : str  , driver_insance : webdriver ,N : int = None, region : str = 'eune' , force_update = False  ,force_ranked_only = False ,sleep_after_select_ranked = 1.2) -> list[GameRecord] :
    print(f"Getting {N} games for {player_name} on server {region}")
    player_url = f'https://www.op.gg/summoners/{region.lower()}/{player_name}/'
    
    load_page_with_timeout(driver_insance , player_url , 15)
    if force_update :   # this will update the player data , takes time as it waits the website to update
        print("Force update")
        button = driver_insance.find_element("xpath","//button[contains(text(),'Update')]")
        button.click()
        elabsed = 0
        try :   # op.gg can send an alert
            alert = driver_insance.switch_to.alert
            alert.accept()
        except :
            while elabsed < 5 : 
                time.sleep(0.5)
                if button.text in ["Update" , "Updated"]:
                    break
                elabsed += 0.5

    # select ranked matches
    if force_ranked_only :
        print("Getting only ranked games")
        driver_insance.find_element(By.XPATH, "//button[@value = 'SOLORANKED']").click()
        time.sleep(sleep_after_select_ranked)


    # get games
    def get_games() -> list :
        div = driver_insance.find_element("xpath","//div[@class='css-164r41r e17ux5u10']")
        games = div.find_elements('xpath','./li')
        return games
    
    def get_games_bs4() -> list :
        soup = BeautifulSoup(driver_insance.page_source, 'lxml')
        div = soup.find('div', class_='css-164r41r e17ux5u10')
        games = div.find_all('li' , recursive=False)
        return games
    
    games = get_games()
    while len(games) < N :
        print("Getting more games")
        while 1:
            try:
                button = driver_insance.find_element("xpath","//button[contains(text(),'Show More')]")
                button.click()
                break
            except:
                time.sleep(0.3)
        old_len = len(games)
        while len(get_games()) == old_len :
            time.sleep(0.5)

        games = get_games()
        print(f'Current games length {len(games)}')
        
    games = games[:N]
    game_instances = []
    buttons = []
    print("Getting buttons") 
    for game in tqdm.tqdm(games):
        buttons.append(game.find_element('xpath','./div/div[2]/button[@class = "detail"]')) 

    print("Extracting game data")
    
    for btn, game in tqdm.tqdm(zip(buttons , games)):
        btn.click()
        game_instances.append(extract_game_data(game))
        btn.click()

    for game in game_instances :
        game.RecordOwner = player_name
    
    return game_instances    