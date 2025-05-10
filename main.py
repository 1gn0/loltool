import csv

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

def register_game():

    my_champ = input("Champion: ")
    while not check_pool(my_champ):
        my_champ = input("Champion: ")

    enemy_champ = input("Enemy Champion: ")
    while not check_pool(enemy_champ):
        enemy_champ = input("Enemy Champion: ")

    kda = input("KDA: ")
    try :
        list_kda = list(map(int, kda.split("/")))
        kills = list_kda[0]
        assists = list_kda[1]
        deaths = list_kda[2]
    except:
        print("KDA must be in the form of 'kills/assists/deaths'")
        main()
    
    try:
        CS_total = int(input("CS Total: "))
        CS_15min = int(input("CS 15min: "))
    except :
        print("CS must be an integer")
        main()
    
    result = input("Result: ")
    if result not in ["win", "lose"]:
        print("Result must be 'win' or 'lose'")
        main()
    
    recap = input("Recap (feelings about the game): ")

    with open("games.csv", "a", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([my_champ, enemy_champ, kda, CS_total, CS_15min, result, recap])
        f.close()


def delete_last_game():
    delete_last_game = input("Delete last game? (y/n): ")
    try :
        if delete_last_game == "y":
            with open("games.csv", "r") as f:
                writer = csv.writer(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                lines = f.readlines()
                lines.pop()
            with open("games.csv", "w") as f:
                writer = csv.writer(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                f.writelines(lines)
                f.close()
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
        lines = f.readlines()
    n = 0
    wins = 0
    looses = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        champ = parts[0].strip()
        enemy = parts[1].strip()
        result = parts[5].strip().lower()  # "win" ou "loss"

        if champ == my_champ and enemy == enemy_champ:
            n += 1
            if result == "win":
                wins += 1
            else:
                looses += 1

    print(f"you played {n} games against {enemy_champ}")

    if n != 0:
        print(f"you won {wins} games against {enemy_champ}")
        print(f"you lost {looses} games against {enemy_champ}")
        print(f"you won {wins/n*100:.2f}% of the time")

        recap = input("Do you want to see recap of your last 5 games against this enemy champion? (y/n): ")
        if recap.lower() == "y":
            with open("games.csv", newline='', encoding="utf-8") as f:
                
                reader = csv.reader(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                filtered = []

                for row in reader:
                    if row[0].strip() == my_champ and row[1].strip() == enemy_champ:
                        filtered.append(row)

                last_5 = filtered[-5:]
                print("\nRecap of last 5 games:")
                for game in last_5:
                    print(game[6].strip())  


def main():
    
    print("Select an option:")
    print("[1] Register a game")
    print("[2] Delete last game")
    print("[3] Read matchup")
    print("[4] Exit")
    while True:
        option = input("Option: ")
        if option == "1":
            register_game()
            main()
        elif option == "2":
            delete_last_game()
            main()
        elif option == "3":
            read_matchup()
            main()
        elif option == "4":
            exit(0)
        else:
            print("Invalid option")
            main()



if __name__ == "__main__":
    print("[+] Welcome to LolTool")
    main()
