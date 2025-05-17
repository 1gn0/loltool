import csv
import requests
import time
import apicalls

pool = [
    "aatrox", "ahri", "akali", "akshan", "alistar", "ambessa", "amumu", "anivia", "annie", "aphelios",
    "ashe", "aurelion sol", "aurora", "azir", "bard", "bel'veth", "blitzcrank", "brand", "braum", "briar",
    "caitlyn", "camille", "cassiopeia", "cho'gath", "corki", "darius", "diana", "dr. mundo", "draven", "ekko",
    "elise", "evelynn", "ezreal", "fiddlesticks", "fiora", "fizz", "galio", "gangplank", "garen", "gnar",
    "gragas", "graves", "gwen", "hecarim", "heimerdinger", "hwei", "illaoi", "irelia", "ivern", "janna",
    "jarvan iv", "jax", "jayce", "jhin", "jinx", "k'sante", "kai'sa", "kalista", "karma", "karthus",
    "kassadin", "katarina", "kayle", "kayn", "kennen", "kha'zix", "kindred", "kled", "kog'maw", "leblanc",
    "lee sin", "leona", "lillia", "lissandra", "lucian", "lulu", "lux", "malphite", "malzahar", "maokai",
    "master yi", "mel", "milio", "miss fortune", "mordekaiser", "morgana", "naafiri", "nami", "nasus", "nautilus",
    "neeko", "nidalee", "nilah", "nocturne", "nunu & willump", "olaf", "orianna", "ornn", "pantheon", "poppy",
    "pyke", "qiyana", "quinn", "rakan", "rammus", "rek'sai", "rell", "renata glasc", "renekton", "rengar",
    "riven", "rumble", "ryze", "samira", "sejuani", "senna", "seraphine", "sett", "shaco", "shen",    
    "shyvana", "singed", "sion", "sivir", "skarner", "smolder", "sona", "soraka", "swain", "sylas",
    "syndra", "tahm kench", "taliyah", "talon", "taric", "teemo", "thresh", "tristana", "trundle", "tryndamere",
    "twisted fate", "twitch", "udyr", "urgot", "varus", "vayne", "veigar", "vel'koz", "vex", "vi",
    "viego", "viktor", "vladimir", "volibear", "warwick", "wukong", "xayah", "xerath", "xin zhao", "yasuo",
    "yone", "yorick", "yuumi", "zac", "zed", "zeri", "ziggs", "zilean", "zoe", "zyra"
]

def check_pool(champion):
    if champion not in pool:
        print("Champion not in pool")
        return False 
    return True

def clear_csv():
    clear = input("Clear csv? (y/n): ")
    try :
        if clear == "y":
            with open("games.csv", "r+", encoding="utf-8") as f:
                f.truncate(0)  
                f.seek(0) 
    except:
        main()

def read_matchup():
    my_champ = input("Champion: ").strip()
    while not check_pool(my_champ):
        my_champ = input("Champion: ").strip()

    enemy_champ = input("Enemy Champion: ").strip()
    while not check_pool(enemy_champ):
        enemy_champ = input("Enemy Champion: ").strip()

    with open("games.csv", "r", newline='', encoding="utf-8") as f:
        total_games_with_cs = 0
        lines = f.readlines()
        n = 0
        n_games_with_cs = 0
        wins = 0
        looses = 0
        CS_15min_global = 0
        CS_15min_matchup = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            champ = parts[1].strip()
            enemy = parts[2].strip()
            result = parts[6].strip().lower()  # "win" ou "loss"
            CS_15min = parts[5].strip() if parts[5].strip() != "N/A" else "N/A"
            CS_15min_global += int(CS_15min) if CS_15min != "N/A" else 0
            total_games_with_cs += 1 if CS_15min != "N/A" else 0
            
            if champ == my_champ and enemy == enemy_champ:
                n += 1
                n_games_with_cs += 1 if CS_15min != "N/A" else 0
                CS_15min_matchup += int(CS_15min) if CS_15min != "N/A" else 0
                if result == "win":
                    wins += 1
                else:
                    looses += 1
            
    average_cs = CS_15min_global/total_games_with_cs
    print(f"you played {n} games against {enemy_champ}")

    if n != 0:
    
        print(f"you won {wins/n*100:.2f}% of the time")
        print(f"you farm {CS_15min_matchup/n_games_with_cs} CS at 15min against this champion which is " + "inferior to average CS" if CS_15min_matchup/n_games_with_cs < average_cs else "superior to average CS") 


def player_stats():
    with open("games.csv", "r", newline='', encoding="utf-8") as f:
        lines = f.readlines()
        n = 0
        n_games_with_cs = 0
        wins = 0
        looses = 0
        CS_15min_global = 0
        CS_15min_matchup = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            champ = parts[1].strip()
            enemy = parts[2].strip()
            result = parts[6].strip().lower()  # "win" ou "loss"
            CS_15min = parts[5].strip() if parts[5].strip() != "N/A" else "N/A"
            CS_15min_global += int(CS_15min) if CS_15min != "N/A" else 0
            n += 1
            n_games_with_cs += 1 if CS_15min != "N/A" else 0
            if result == "win":
                wins += 1
            else:
                looses += 1
            
    average_cs = CS_15min_global/len(lines)
    print(f"you registered {n} games in total")
    print(f"With a winrate of {wins/n*100:.2f}%")
    print(f"you farm {CS_15min_global/n_games_with_cs} CS at 15min on average which is " + "inferior to 80 (actual objective)" if CS_15min_global/n_games_with_cs < 80 else "superior to 80 (actual objective)")

def actualise_profile():
    player_name = input("Enter your riot name: ")
    tag_line = input("Enter your tag line: ")
    n_of_games = input("How many games do you want to register ? ")
    try:
        games_dict = apicalls.get_matches_infos(int(n_of_games), player_name, tag_line)
    except:
        print("Error while getting games infos")
        main()

    ids = []
    with open("games.csv", "r", newline='', encoding="utf-8") as f:
        lines = f.readlines()
        id = [line.split("|")[0] for line in lines]
        ids = list(set(id))
        f.close()
    with open("games.csv", "a", newline='\n', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for game in games_dict:
            match_id = game
            my_champ = games_dict[match_id][0].lower()
            enemy_champ = games_dict[match_id][1].lower()
            kda = games_dict[match_id][2]
            CS_total = games_dict[match_id][3]
            CS_15min = games_dict[match_id][4]
            result = "win" if games_dict[match_id][5] == "Victory" else "lose"
            if match_id not in ids:
                writer.writerow([match_id, my_champ, enemy_champ, kda, CS_total, CS_15min, result])
    f.close()

def main():
    
    print("Select an option:")
    print("[1] Register your last games")
    print("[2] Clear csv")
    print("[3] Read matchup")
    print("[4] Player stats")
    print("[5] Exit")
    
    while True:
        option = input("Option: ")
        if option == "1":
            actualise_profile()
            main()
        elif option == "2":
            clear_csv()
            main()
        elif option == "3":
            read_matchup()
            main()
        elif option == "4":
            player_stats()
            main()
        elif option == "5": 
            exit(0)
        else:
            print("Invalid option")
            main()



if __name__ == "__main__":
    print("[+] Welcome to LolTool")
    main()
