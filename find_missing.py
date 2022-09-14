import glob
import re
import datetime
from tabnanny import check

from regex import B

def check_name(text):
    return True if re.fullmatch("YT playlist backup [0-9][0-9]\.[0-9][0-9]\.[0-9][0-9][0-9][0-9] [0-9][0-9] [0-9][0-9] [0-9][0-9]\.txt",text) else False

def get_date(filename):
    date = filename.split(" ")[3]
    return datetime.datetime(int(date.split(".")[2]),
                             int(date.split(".")[1]),
                             int(date.split(".")[0]),
                             int(filename.split(" ")[4]),
                             int(filename.split(" ")[5]),
                             int(filename.split(" ")[6][:2]))

def simplify_title(title):

    if "(" in title:
        title = title.split("(")[0]

    if "[" in title:
        title = title.split("[")[0]

    title = title.lower()

    for character in """!@#$%^&*()-+[]{}=_:;",./<>?'\\-–|""":
        title = title.replace(character,"")

    title = re.sub(' +', ' ',title).split(" ")

    for word in ["official", "music", "video", "oficjalny", "officiel", "ufficiale", "teledysk", 
                 "sanremo", "eesti", "laul", "eurovision", "melodi", "grand", "prix", "lyric",
                 "lyrics", "clip", "edit","reverb", "videoclip", "theme", "song", "contest", 
                 "audio", "visual", "tiktok", "version", "hd", "feat", "featuring", "x", "", ""]:
        try:
            title.remove(word)
        except ValueError:
            pass

    return title

def match_strings(a,b):
    count = 0
    correct = 0
    for word in a:
        if word in b:
            correct+=1
        count+=1
    return correct/count if count != 0 else 0

files = glob.glob("*.txt")
filtered_files = sorted(list(filter(check_name,files)),key=get_date)
newest_file = filtered_files[-1]

res = ""

playlists = {}      #schema: playlists[playlist id] -> ([titles & channel names], [simple titles], 
                    #                                   [curr titles & channel names], [curr simple titles], 
                    #                                   missing_count, playlist title,
                    #                                   [ids_old],[ids_new])

for file in filtered_files[:-1]:
    print(file)
    with open(file,encoding="UTF-8") as f:
        for line in f:
            if line.startswith("playlist: "):
                playlist_id = line.split(" ")[1].split("\t")[0]
                if playlist_id not in playlists:
                    playlists[playlist_id] = [[],[],[],[],0,line.split("\t")[2][15:-1],[],[]]

            elif len(line) > 0 and line[0].isdecimal():
                dot = line.find(".")
                title = line[dot+2 : -1]
                nxt = next(f)

                if "channel" not in nxt:
                    continue

                channel = nxt.split("\t")[1][9:]
                video_id = nxt.split("\t")[2][10:]
                
                if title + " channel: " + channel not in playlists[playlist_id][0]:
                    playlists[playlist_id][0].append(title + " channel: " + channel)
                    playlists[playlist_id][1].append(simplify_title(title))
                    playlists[playlist_id][6].append(video_id)

with open(newest_file,encoding="UTF-8") as f:
    for line in f:
        if line.startswith("playlist: "):
            playlist_id = line.split(" ")[1].split("\t")[0]

        elif len(line) > 0 and line[0].isdecimal():
            
            if playlist_id not in playlists:
                continue

            dot = line.find(".")
            title = line[dot+2 : -1]
            nxt = next(f) 
            
            if "channel" not in nxt:
                    #playlists[playlist_id][4] += 1
                    continue

            channel = nxt.split("\t")[1][9:]
            video_id = nxt.split("\t")[2][10:]
            
            if title + " channel: " + channel not in playlists[playlist_id][2]:
                    playlists[playlist_id][2].append(title + " channel: " + channel)
                    playlists[playlist_id][3].append(simplify_title(title))
                    playlists[playlist_id][7].append(video_id)

for key in playlists.keys():
    res += "-"*100 + "\n"
    res += "playlist: " + playlists[key][5] + "\n\n"
    #res += "missing: " + str(playlists[key][4]) + "\n"
    for i,video in enumerate(playlists[key][0]):
        if video not in playlists[key][2] and playlists[key][6][i] not in playlists[key][7]:
            res += "\t"+video+"\n"
            missing = playlists[key][1][i]
            matches = []
            for possible_video in playlists[key][3]:
                if match_strings(missing,possible_video) > 0.5:
                    if (possible_video,match_strings(missing,possible_video)) not in matches:
                        matches.append((possible_video,match_strings(missing,possible_video)))
            for match in sorted(matches,key=lambda x: x[1],reverse=True):
                indices = [ind for ind, x in enumerate(playlists[key][3]) if x == match[0]]
                for index in indices:
                    res += "\t\t" + playlists[key][2][index] + " match: " + str(int(match[1]*100)) + "%\n"


with open("res.txt","w",encoding="UTF-8") as f:
    f.write(res)
    f.write("end")

#print(res)
