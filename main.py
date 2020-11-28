#NEA task 1
#Shell only (no visuals)

import random
import csv
import tempfile
import shutil
import time
import copy
import os

usersFile = "CSV files/NEA_Users.csv"
usersFileHeader = ["Username", "Password", "Highscore", "Wins"]

musicFile = "CSV files/NEA_Music.csv"
musicFileHeader = ["Artist", "Song"]

typeFast = 160
typeMid = 120
typeSlow = 80

# --- PRE COMPOSITES ---
def preInput(max):
    choice = 0
    while choice not in [i for i in range(1,max+1)]:
        try:
            choice = int(input(">"))
        except:
            choice = preInput(max)
    return choice

def preFileFind(fname):
    try:
        find = open(fname, "r")
    except:
        preType("Files moved, searching for new file path\n To avoid this move the 'data' files next to the code file",1,0,typeSlow)
        preType("Alerternativly change the file path in the source code",1,0.5,typeSlow)

        #find the file path
        for root, dirs, files in os.walk("/Users"):
            for name in files:
                if name == fname:
                    filePath =  os.path.abspath(os.path.join(root, name))
        
        return(filePath)

    #if file found return file name
    return(fname)

def preType(string, gap, wait, typingSpeed):
    for l in string:
        print(l,end="")
        time.sleep(random.random() * 10 / typingSpeed)

    for i in range(gap):
        print("")
    time.sleep(wait)

# --- USERS FILE ---
def usersRead(fileName, fileheader):
    global usersList
    usersList = []
    itemsList = []

    with open(fileName) as file:
        reader = csv.DictReader(file)

        for row in reader:
            itemsList.append(row["Username"])
            itemsList.append(row["Password"])
            itemsList.append(int(row["Highscore"]))
            itemsList.append(int(row["Wins"]))

        for i in range(0, len(itemsList), 4):
            itemsSeperated = itemsList[i:i + 4]
            usersList.append(itemsSeperated)

def usersNew(fileName, fileheader):
    userAll = [item[0] for item in usersList]

    preType("choose a username",1,0,typeMid)
    user = input(">")
    while user in userAll:
        preType("that username is taken\n choose another username",1,0,typeSlow)
        user = input(">")
    
    preType("choose password",1,0,typeMid)
    password = input(">")

    with open(fileName, "a", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames = fileheader)
        
        writer.writerow({
        "Username" : user,
        "Password" : password,
        "Highscore" : 0,
        "Wins" : 0
        })

    preType("\nAccount created,",1,0.2,typeSlow)

def usersWrite(fileName, fileheader, user, password, highscore, wins):
    #open a temporary file and the original 
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    
    with temp_file as csvfileTemp:
        writer = csv.DictWriter(csvfileTemp, fieldnames = fileheader)
        writer.writeheader()

        with open(fileName) as csvfileOG:
            reader = csv.DictReader(csvfileOG)

            for row in reader:
                #find row to change
                if row["Username"] == user:
                    
                    #write new data
                    writer.writerow({
                        "Username" : row["Username"],
                        "Password" : row["Password"],
                        "Highscore" : highscore,
                        "Wins" : wins
                    })

                #write original   
                else:
                    writer.writerow({
                        "Username" : row["Username"],
                        "Password" : row["Password"],
                        "Highscore" : row["Highscore"],
                        "Wins" : row["Wins"]
                    })
                    
    shutil.move(temp_file.name, fileName)

def usersLogin():
    global usersCurrent
    usersCurrent = []
    
    preType("\nUsername",1,0,typeFast)
    user = input(">")
    preType("\nPassword",1,0,typeFast)
    password = input(">")

    for i in range(len(usersList)):
        if user == usersList[i][0]:
            if password == usersList[i][1]:

                usersCurrent.append(usersList[i][0])
                usersCurrent.append(usersList[i][1])
                usersCurrent.append(int(usersList[i][2]))
                usersCurrent.append(int(usersList[i][3]))
                preType("\nlogin sucsesful",1,0,typeMid)
                return True

    if usersCurrent == []:
        preType("Incorrent Username or Password, remember both are case sensitive",1,0.2,typeMid)
        return False

# --- MUSIC FILE ---
def musicRead(fileName, fileheader):
    global musicList
    musicList = []
    itemsList = []

    with open(fileName) as file:
        reader = csv.DictReader(file)

        for row in reader:
            itemsList.append(row["Artist"])
            itemsList.append((row["Song"]).lower())

        for i in range(0, len(itemsList), 2):
            itemsSeperated = itemsList[i:i + 2]
            musicList.append(itemsSeperated)

def musicAdd(fileName, fileheader):
    preType("Artist name",1,0,typeFast)
    artist = input(">")

    preType("\nSong title",1,0,typeFast)
    song = input(">")

    songAll = [item[1] for item in musicList]
    print (songAll)

    if song not in songAll:
        with open(fileName, "a", newline = "") as file:
            writer = csv.DictWriter(file, fieldnames = fileheader)
            
            writer.writerow({
            "Artist" : artist,
            "Song" : song
            })

        preType("Song added!",1,0.5,typeMid)
    else:
        preType("That song is allready added\nReturning to main menu",1,0.5,typeMid)

def musicOrder(fileName, fileheader):
    musicOrdered = sorted(musicList, key=lambda x: x[0], reverse=False)

    with open(fileName, "w", newline = "") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fileheader)
        writer.writeheader()

        for i in range(len(musicOrdered)):
            writer.writerow({
            "Artist" : musicOrdered[i][0],
            "Song" : musicOrdered[i][1]
            })

# --- GAME ---
def gameRound():
    ran = random.randint(0,len(musicNotUsed)-1)
    ranArtist = musicNotUsed[ran][0]
    ranSong = musicNotUsed[ran][1]

    musicNotUsed.pop(ran) #so that no songs are repeated

    #splitting
    songNameList = ranSong.split()  #song in the format [a,b]
    songCharsList = []     #song in the format [[a1, a2],[b1,b2]]
    songHidden = []     #song in the format [a__,b__]
    songFirstChars = []   #only first letters

    for i in range (len(songNameList)):
        songHiddenChars = []
        songCharsList.append(list(songNameList[i]))
        #songFirstChars.append(songCharsList[i][0])
        songHiddenChars.append(songCharsList[i][0])

        for j in range(len(songCharsList[i])-1):
            songHiddenChars.append("_")
        songHidden.append("".join(songHiddenChars))

    #User interaction
    guess = 0
    preType("Song by {0}".format(ranArtist),1,0.5,typeMid)
    preType("What's the name of this song?",1,0,typeMid)
    preType(" ".join(songHidden).upper(),2,0,typeMid)
    
    while guess < 2:
        songGuess = input(">").lower()

        if (songGuess == ranSong) or (songGuess == ranSong[1:]):
            preType("correct",1,0.2,typeMid)
            break
        else:
            preType("incorrect",1,0.2,typeMid)
            guess += 1

    return(guess) 

def gameMain(rounds):
    global musicNotUsed
    musicNotUsed = musicList
    
    score = rounds * 2

    while rounds > 0:
        preType("\nRound {0}\n".format(11 - rounds),1,0.5,typeMid)
        score -= gameRound()
        rounds -= 1
    
    preType("\nYou Scored {0}".format(score),1,0.5,typeSlow)
    return(score)

def gameHighScore(score):
    if score > usersCurrent[2]:
        usersCurrent[2] = score
        usersWrite(usersFile,usersFileHeader,usersCurrent[0],usersCurrent[1],usersCurrent[2],usersCurrent[3])
        preType("New highscore!",1,0.5,typeSlow)

    elif score == usersCurrent[2] and score != 20:
        preType("you tied for your highscore of {0}!".format(usersCurrent[2]),1,0.5,typeSlow)

    else:
        target = usersCurrent[2] - score
        preType("you need {0} more points to reach your highscore of {1}!".format(target,usersCurrent[2]),1,0.5,typeSlow)

    if score == 20:
        usersCurrent[3] += 1
        usersWrite(usersFile,usersFileHeader,usersCurrent[0],usersCurrent[1],usersCurrent[2],usersCurrent[3])

def gameLeaderboard(hide,speed):
    #lamba messes with the list, so i make a copy
    usersListCopy = copy.deepcopy(usersList)
    usersTop = sorted(usersListCopy, key=lambda x: x[2] + x[3], reverse=True)
    
    for i in range(len(usersTop)):
        usersTop[i].pop(1)

    preType("""
          Scores
 ==== Top ===== Perfect ==== """,1,0,typeMid)
    x = 1
    for item in usersTop:
        if x == 6 and hide == True:
            break
        
        if item[1] < 10:
            preType("{0}.    {2}         {3}      by {1}".format(x,item[0],item[1],item[2]),1,0,speed)
        else:
            preType("{0}.    {2}        {3}      by {1}".format(x,item[0],item[1],item[2]),1,0,speed)
            
        x += 1

    if hide == True:
        preType("\nShow all scores (1)\nReturn to menu  (2)",1,0,typeSlow)
        choice = preInput(2)

        if choice == 1:
            gameLeaderboard(False,typeFast*2)
        else:
            return
    else:
        preType("\nReturning to main menu",1,0.5,typeSlow)

# --- INTERFACE ---
def start():
    global usersFile,musicFile
    usersFile = preFileFind(usersFile)
    musicFile = preFileFind(musicFile)

    musicRead(musicFile, musicFileHeader)
    usersRead(usersFile,usersFileHeader)
    musicOrder(musicFile, musicFileHeader)
    
    preType(" === WELCOME TO THE MUSIC GAME === ",1,0.5,typeSlow)

    preType("Login    (1)\nSign up  (2)",1,0,typeSlow)
    choice = preInput(2)

    if choice == 2:
        usersNew(usersFile,usersFileHeader)
        usersRead(usersFile,usersFileHeader)
        preType("\nLogin",1,0,typeSlow)

    while usersLogin() == False:
        pass
    
def main(speed):
    preType("\nStartGame   (1)\nHighscores  (2)\nYour Stats  (3)\nHow to Play (4)\nAdd a Song  (5)\nLogout      (6)",1,0,speed)
    choice = preInput(6)

    if choice == 1:
        preType("\nStarting Game",1,0,speed)
        score = gameMain(10)
        gameHighScore(score)

    elif choice == 2:
        usersRead(usersFile,usersFileHeader)
        gameLeaderboard(True,120)

    elif choice == 3:
        global usersCurrent
        preType("\n === User {0} ===\n === Best Score {1} ===\n === Perfect Scores {2} ===".format(
                usersCurrent[0],usersCurrent[2],usersCurrent[3]),1,0,typeMid)

    elif choice == 4:
        preType("""
 ================== Thanks for playing Guess that Song! ==================
          # To play, simply choose "Start Game" in the menu #     
     # Only the first letters of the words in the song are shown #
             # Guess the whole name of the song correctly #
                  # You have 2 guesses for each song #             
     # You can add your own song and view highscores in the main menu #
 ========================= Code by Jachym Tolar ==========================
              """,1,0,speed)

    elif choice == 5:
        preType("\nChoose a song to add to the game",1,0.2,speed)
        musicAdd(musicFile, musicFileHeader)
        musicOrder(musicFile, musicFileHeader)
        musicRead(musicFile, musicFileHeader)

    elif choice == 6:
        preType("\nExiting game",1,0,speed)
        exit()

    else:
        preType("\nInvalid choice, try again",1,0.2,speed)
        
    main(typeFast)

# --- DRIVER ---
if __name__ == "__main__":
    start()
    main(typeSlow)
