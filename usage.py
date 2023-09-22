import opgg_scrapper

# initialize drive 
driver = opgg_scrapper.get_chrome( headless=True , adblock_extenstion_path='extension_2023_9_10_1131.crx')

# get top 500 players in euw and save
players =  opgg_scrapper.get_top_N_players(500,driver , region='euw')
opgg_scrapper.create_dataframe_from_players(players).to_csv('players_euw.csv')

# get the first 200 ranked games of the top player in euw
games = opgg_scrapper.get_player_N_games( player_name= "Δ Desperate" ,region='eune', driver_insance=driver , N=200 , force_update= False, force_ranked_only=True) 
opgg_scrapper.create_dataframe_from_game_records(games).to_csv('games_first_euw.csv')


# get the top 500 players in eune and save
players =  opgg_scrapper.get_top_N_players(500,driver , region='eune')
opgg_scrapper.create_dataframe_from_players(players).to_csv('players_eune.csv')

# get the first 200 ranked games of the top player in eune
games = opgg_scrapper.get_player_N_games( player_name= players[0].name ,region='eune', driver_insance=driver , N=200 ,force_ranked_only=True)
opgg_scrapper.create_dataframe_from_game_records(games).to_csv('games_first_eune.csv')