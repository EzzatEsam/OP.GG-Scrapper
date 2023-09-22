from .classes import *
import pandas as pd


def create_dataframe_from_players(players: list[Player]) -> pd.DataFrame:
    df_rows = []
    for player in players:
        row = []
        cols = ['name', 'rank', 'lp', 'level', 'wins', 'losses', 'most_played_champ_1', 'most_played_champ_2', 'most_played_champ_3']
        row.append(player.name)
        row.append(player.rank)
        row.append(player.lp)
        row.append(player.level)
        row.append(player.wins)
        row.append(player.losses)
        row += player.most_played_champs

        df_rows.append(row)
    
    return pd.DataFrame(df_rows, columns=cols)


def create_dataframe_from_game_records(game_records: list[GameRecord]) -> pd.DataFrame:

    """Creates a DataFrame from a list of GameRecords.

    Args:
        game_records: A list of GameRecord objects.

    Returns:
        A DataFrame containing the data from the GameRecord objects.
    """

    # Create a list to store the DataFrame rows.
    df_rows = []

    # Iterate over the GameRecord objects.
    for game_record in game_records:

        # Get the data from the GameRecord object.
        result = game_record.result
        winning_team = game_record.winning_team
        game_time_seconds = game_record.game_time_seconds
        red_team_players = game_record.red_team_players
        blue_team_players = game_record.blue_team_players
        red_team_barons = game_record.red_team_barons
        blue_team_barons = game_record.blue_team_barons
        red_team_dragons = game_record.red_team_dragons
        blue_team_dragons = game_record.blue_team_dragons
        red_team_towers = game_record.red_team_towers
        blue_team_towers = game_record.blue_team_towers
        record_owner = game_record.record_owner
        owner_champion = game_record.owner_champion
        
        # Create a list to store the data for the current row.
        row = []
        cols = []

        # Add the data for the current GameRecord object to the row.
        row.append(game_record.game_type)
        cols.append("type")

        row.append(result)
        cols.append("result")

        row.append(winning_team)
        cols.append("winning team")

        row.append(game_time_seconds)
        cols.append("game time")

        row.append(red_team_barons)
        cols.append("red team barons")

        row.append(red_team_dragons)
        cols.append("red team dragons")

        row.append(red_team_towers)
        cols.append("red team towers")

        row.append(blue_team_barons)
        cols.append("blue team barons")

        row.append(blue_team_dragons)
        cols.append("blue team dragons")

        row.append(blue_team_towers)
        cols.append("blue team towers")


        # Iterate over the red team players.
        for i, player in enumerate (red_team_players):
            row.append(player.name)
            row.append(player.champion)
            row.append(player.rank)
            row.append(player.kda)
            row.append(player.damage_given)
            row.append(player.damage_taken)
            row.append(player.cs)

            cols.append(f"red team player {i+1} name")
            cols.append(f"red team player {i+1} champion")
            cols.append(f"red team player {i+1} rank")
            cols.append(f"red team player {i+1} kda")
            cols.append(f"red team player {i+1} damage given")
            cols.append(f"red team player {i+1} damage taken")
            cols.append(f"red team player {i+1} cs")


            # Add the player's vision data to the row.
            for j,vision_stat in enumerate(player.vision):
                row.append(vision_stat)
                cols.append(f"red team player {i+1} vision {j+1}")

            # Add the player's summoner spells to the row.
            for j,summoner_spell in enumerate (player.summoner_spells):
                row.append(summoner_spell)
                cols.append(f"red team player {i+1} summoner spell {j+1}")

            # Add the player's runes to the row.
            for j,rune in enumerate (player.runes):
                row.append(rune)
                cols.append(f"red team player {i+1} rune {j+1}")

            # Add the player's items to the row.
            #print(len(player.items))
            for  j in range(7):
                if j < len(player.items) :
                    item = player.items[j]
                else :
                    item = None
                row.append(item)
                cols.append(f"red team player {i+1} item {j+1}")

        # Iterate over the blue team players.
        for i, player in enumerate (blue_team_players):
            row.append(player.name)
            row.append(player.champion)
            row.append(player.rank)
            row.append(player.kda)
            row.append(player.damage_given)
            row.append(player.damage_taken)
            row.append(player.cs)

            cols.append(f"blue team player {i+1} name")
            cols.append(f"blue team player {i+1} champion")
            cols.append(f"blue team player {i+1} rank")
            cols.append(f"blue team player {i+1} kda")
            cols.append(f"blue team player {i+1} damage given")
            cols.append(f"blue team player {i+1} damage taken")
            cols.append(f"blue team player {i+1} cs")
            

            # Add the player's vision data to the row.
            for j,vision_stat in enumerate(player.vision):
                row.append(vision_stat)
                cols.append(f"blue team player {i+1} vision {j+1}")

            # Add the player's summoner spells to the row.
            for j,summoner_spell in enumerate (player.summoner_spells):
                row.append(summoner_spell)
                cols.append(f"blue team player {i+1} summoner spell {j+1}")

            #print(len(player.items))
            # Add the player's runes to the row.
            for j,rune in enumerate (player.runes):
                row.append(rune)
                cols.append(f"blue team player {i+1} rune {j+1}")
            
            # Add the player's items to the row.
            for  j in range(7):
                if j < len(player.items) :
                    item = player.items[j]
                else :
                    item = None
                row.append(item)
                cols.append(f"blue team player {i+1} item {j+1}")


        # Add the record owner and owner champion to the row.
        row.append(record_owner)
        cols.append("record owner")
        
        row.append(owner_champion)
        cols.append("owner champion")

        #print(len(row) , len(cols))
        # Add the row to the list of DataFrame rows.
        df_rows.append(row)

    # Create the DataFrame
    df = pd.DataFrame(df_rows , columns=cols)
    return df
