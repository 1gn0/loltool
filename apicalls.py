import requests
import time
import keys

API_KEY = keys.API_KEY
headers = {"X-Riot-Token": API_KEY}


def get_puuid(summoner_name, tag_line):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    res = requests.get(url, headers=headers)
    return res.json()["puuid"]


def get_match_ids(puuid, count=20):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    res = requests.get(url, headers=headers)
    return res.json()


def get_match_data(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=headers)
    try:
        data = res.json()
        if "info" in data:
            return data
        else:
            print(f"[!] Erreur de récupération pour le match {match_id} : {data}")
            return {}
    except Exception as e:
        print(f"[!] Erreur JSON pour le match {match_id}: {e}")
        return {}


def get_participant_id(puuid, match_data):
    participants = match_data.get("info", {}).get("participants", [])
    for i, participant in enumerate(participants, 1):  # IDs de 1 à 10
        if participant["puuid"] == puuid:
            return i
    return None


def get_cs_15min(match_id, participant_id=None):
    if participant_id is None:
        return "N/A"

    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    res = requests.get(url, headers=headers)
    try:
        timeline = res.json()
        frames = timeline.get("info", {}).get("frames", [])
        if len(frames) >= 16:
            frame_15 = frames[15]
            participant_frames = frame_15["participantFrames"]
            data = participant_frames[str(participant_id)]
            return data["minionsKilled"] + data["jungleMinionsKilled"]
        else:
            return "N/A"
    except Exception as e:
        print(f"[!] Erreur CS 15min pour le match {match_id}: {e}")
        return "N/A"


def extract_info(match_data, puuid):
    info = match_data.get("info", {})
    if info.get("queueId") != 420:  # Ne garder que les solo/duo
        return None

    participants = info["participants"]
    player = next(p for p in participants if p["puuid"] == puuid)

    team_pos = player["teamPosition"]
    enemy_team = 100 if player["teamId"] == 200 else 200
    enemy = next((p for p in participants if p["teamId"] == enemy_team and p["teamPosition"] == team_pos), None)

    return {
        "champion": player["championName"],
        "enemy": enemy["championName"] if enemy else "Unknown",
        "kda": f'{player["kills"]}/{player["deaths"]}/{player["assists"]}',
        "cs_total": player["totalMinionsKilled"] + player["neutralMinionsKilled"],
        "cs_15min": player.get("challenges", {}).get("laneMinionsFirst15Minutes", "N/A"),
        "result": "Victory" if player["win"] else "Defeat"
    }


def get_matches_infos(count=100, summoner_name="1gn0", tag_line="000"): 
    games = {}
    puuid = get_puuid(summoner_name, tag_line)
    match_ids = get_match_ids(puuid, count)

    for match_id in match_ids:
        match_data = get_match_data(match_id)
        if not match_data:
            continue

        info = extract_info(match_data, puuid)
        if info:
            participant_id = get_participant_id(puuid, match_data)
            cs_15min = get_cs_15min(match_id, participant_id)
            games[match_id] = [
                info["champion".lower()],
                info["enemy".lower()],
                info["kda"],
                info["cs_total"],
                cs_15min,
                info["result"]
            ]

        time.sleep(1.2)  # Respect des limites d'appel API

    return games

