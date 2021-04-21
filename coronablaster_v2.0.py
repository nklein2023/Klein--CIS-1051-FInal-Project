# Code for the core gameplay was partly derived from the code found in the video in this link: https://www.youtube.com/watch?v=FfWpgLFMI7w 
# Additions of lives, fast enemy, main menu, and high scores are all origional code made by myself

import pygame as pg
import random, math, time, PIL.Image, PIL.ImageTk
from tkinter import *
from pygame import mixer

#High Scores Checker
max_score = 0
initials = ''
high_scores = open('high_scores_corona_blaster.csv','r')
lines = high_scores.readlines()
for line in lines:
    newline = line.strip().split(',')
    if int(newline[0]) > int(max_score):
        max_score = newline[0]
        initials = newline[1]

# Tkinter Menu Work
root = Tk()
root.geometry('600x900')
root.title('Corona Blaster')
root.iconbitmap("coronavirus.ico")

image = PIL.Image.open("coronamenubg.png")
photo = PIL.ImageTk.PhotoImage(image)

label = Label(image=photo)
label.pack()

var = StringVar()
diff_label = Label(root,text="Difficulty: ",width=8,bg='black',fg='white',font=('Ariel',20))
diff_label.place(x=150,y=420)
levels = ['Easy','Medium','Hard']
droplist = OptionMenu(root,var,*levels)
var.set("Easy")
droplist.config(width=15)
droplist.place(x=300,y=425)

high_score_label = Label(root,text="High Score: ",width=10,bg='black',fg='white',font=('Ariel',20))
high_score_label.place(x=130,y=750)
score_label = Label(root,text=str(max_score) + " by " + str(initials),width=10,bg='black',fg='white',font=('Ariel',20))
score_label.place(x=330,y=750)

def startGame():
    global difficulty
    global bullet_state
    difficulty = var.get()
    root.destroy()

    # Initialize PyGame
    pg.init()

    # Create Screen
    screen = pg.display.set_mode((600,900))

    # Create Background
    background = pg.image.load("Coronabg.jpg")

    # Backgound Music
    mixer.music.load("maingamesound.wav")
    mixer.music.play(-1)

    # Title and Icon
    pg.display.set_caption("Corona Blaster")
    icon = pg.image.load("coronavirus.png")
    pg.display.set_icon(icon)

    # Player image
    playerImage = pg.image.load("syringe.png")
    playerX = 270
    playerY = 780
    playerX_change = 0

    # Enemy image
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []

    # Difficulty Adjustments
    if difficulty == 'Hard':
        num_of_enemies = 8
    elif difficulty == 'Medium':
        num_of_enemies = 6
    elif difficulty == 'Easy':
        num_of_enemies = 4

    def create_enemies():
        for _ in range(num_of_enemies):
            enemyImg.append(pg.image.load("coronavirus.png"))
            enemyX.append(random.randint(0,535))
            enemyY.append(random.randint(50,150))
            enemyX_change.append(1)
            enemyY_change.append(40)

    create_enemies()

    # Fast Enemy Image
    fastenemyImg = pg.image.load("fastcoronavirus.png")
    fastenemyX = random.randint(0,535)
    fastenemyY = 50
    fastenemyX_change = 2
    fastenemyY_change = 40
    fast = True

    # Bullet image
    bulletImage = pg.image.load("drops.png")
    bulletX = 0
    bulletY = 760
    bulletY_change = 3.5
    bullet_state = 'ready'

    # Extra life
    extraImg = pg.image.load("mask (1).png")
    ghostX = random.randint(0,580)
    ghostY = 30

    #Score
    score_value = 0
    font = pg.font.Font("FreeSansBold.ttf",32)

    textX = 10
    textY = 10

    # Game Over text
    over_font = pg.font.Font('FreeSansBold.ttf',64)

    #Lives
    lives_value = 3
    life_font = pg.font.Font("FreeSansBold.ttf",32)
    lifeX = 435
    lifeY = 10

    # Image Functions

    def show_score(x,y):
        score = font.render("Score: " + str(score_value),True,(0,255,0))
        screen.blit(score,(x,y))

    def game_over_text():
        over_text = over_font.render("GAME OVER",True,(0,255,0))
        screen.blit(over_text,(115,150))

    def final_score_text():
        final_text = over_font.render("Final Score: " + str(score_value),True,(0,255,0))
        screen.blit(final_text,(50,600))
    
    def high_score_text():
        high_score_text = over_font.render("High Score! " + str(score_value),True,(0,255,0))
        initials_text = font.render("Click X then enter your initials below",True,(0,255,0))
        screen.blit(high_score_text,(50,600))
        screen.blit(initials_text,(18,700))

    def show_lives(x,y):
        lives = font.render("Lives " + "X"*lives_value,True,(0,255,0))
        screen.blit(lives,(x,y))

    def extra(x,y):
        screen.blit(extraImg,(x,y))

    def player(x,y):
        screen.blit(playerImage,(x,y))

    def enemy(x,y,i):
        screen.blit(enemyImg[i],(x,y))

    def fastenemy(x,y):
        screen.blit(fastenemyImg,(x,y))

    def fire_bullet(x,y):
        global bullet_state
        bullet_state = 'fire'
        screen.blit(bulletImage,(x+16,y+10))

    def isCollision(enemyX,enemyY,bulletX,bulletY):
        distance = math.sqrt((bulletX-enemyX)**2+(bulletY-enemyY)**2)
        if distance < 27:
            return True
        else:
            return False
        
    # Game Loop
    running = True
    while running:

        # RGB
        screen.fill((0,0,0))
        # Backgounds
        screen.blit(background,(0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
            # Key binding
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    playerX_change = -0.7
                if event.key == pg.K_RIGHT:
                    playerX_change = 0.7
                if event.key == pg.K_SPACE:
                    if bullet_state == 'ready':
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)
                        bullet_sound = mixer.Sound("syringesound.mp3")
                        bullet_sound.play()
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 536:
            playerX = 536
        
        # Fast Enemy
        
        if fast == True:
            fastenemy(fastenemyX,fastenemyY)
            fastenemyX += fastenemyX_change
            
            # Movement (Fast)
            if fastenemyX <= 0:
                fastenemyX_change = 2
                fastenemyY += fastenemyY_change
            elif fastenemyX >= 536:
                fastenemyX_change = -2
                fastenemyY += fastenemyY_change
            
            # Collision (Fast)
            collision = isCollision(fastenemyX,fastenemyY,bulletX,bulletY)
            if collision == True:
                impactsound = mixer.Sound("Impact4.wav")
                impactsound.play()
                bulletY = 760
                bullet_state = 'ready'
                score_value += 50
                fastenemyX = random.randint(0,535)
                fastenemyY = 50

        for i in range(num_of_enemies):

            # Game over
            if lives_value == 0:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                    fastenemyY = 2000
                    game_over_text()
                    mixer.music.pause()
                    if int(score_value) > int(max_score):
                        high_score_text()
                    else:
                        final_score_text()
                    fast = False
                break
                
            if enemyY[i] > 740 or fastenemyY > 740:
                lives_value -= 1
                enemyImg = []
                enemyX = []
                enemyY = []
                enemyX_change = []
                enemyY_change = []
                fastenemyY = 3000
                mixer.music.pause()
                lifelost = mixer.Sound("Explosion24.wav")
                lifelost.play()
                time.sleep(3)
                create_enemies()
                fastenemyX = random.randint(0,535)
                fastenemyY = 50   
                mixer.music.unpause()
            # Enemy Movement         

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 536:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
            if collision == True:
                impactsound = mixer.Sound("Impact4.wav")
                impactsound.play()
                bulletY = 760
                bullet_state = 'ready'
                score_value += 10
                enemyX[i] = random.randint(0,535)
                enemyY[i] = random.randint(50,150)

            enemy(enemyX[i],enemyY[i],i)
        # Bullet Movement
        if bulletY <= 0:
            bulletY = 760
            bullet_state = 'ready'

        if bullet_state == "fire":
            fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change

        # Extra Life
        if lives_value < 3 and (score_value >= 1000 and score_value < 1050) or (2000<= score_value < 2050):
            extra(ghostX,ghostY)
            collision = isCollision(ghostX,ghostY,bulletX,bulletY)
            if collision == True:
                bulletY = 770
                bullet_state = 'ready'
                lives_value += 1
                extra(2000,2000)
  
        player(playerX,playerY)
        show_score(textX,textY)
        show_lives(lifeX,lifeY)
        pg.display.update()

    if int(score_value) > int(max_score):
        high_scores = open('high_scores_corona_blaster.csv','a')
        high_scores.write(str(score_value) + "," + input("Enter your initials: "))
        high_scores.write("\n")
        high_scores.close()

start_but = Button(root,text="Start Game",width=24,height = 6,bg='black',fg='white',command=startGame)
start_but.place(x=210,y=560)

root.mainloop()
