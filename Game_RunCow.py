# 1. Masukkan Library
import sys, pygame, random, time

# 1.1 Inisialisasi game
pygame.init()

# 1.1atur windowsnya dengan konstanta biar lebih mudah
# variabel baru
size_x = 800  # lebar
size_y = 512  # tinggi
FPS = 30

# list variabel
cowwidth = size_x / 9
cowheight = size_y / 4
RECTWIDTH = size_x / 32
RECTHEIGHT = size_y / 16
RUMPUTHIJAUSIZE = size_x / 16
RUMPUTKUNINGSIZE = size_x / 16
BATU_SIZE = size_x / 16
YDIFF = size_y / 8

STEP = 5

Lives = 3

# 1 buat jendelanya
# buat variabel dengan nama SCREEN

clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((size_x, size_y))

# assets
cow = pygame.image.load('assets/belakang-sapii.png')
cow_after_crash = pygame.image.load('assets/belakang-sapii_2.png')
bg_img = pygame.image.load('assets/lawn_bg.jpg')
rumputhijau = pygame.image.load('assets/grass.png')
rumputkuning = pygame.image.load('assets/rumput_kuning.png')
batu = pygame.image.load('assets/stone.png')
ikon = pygame.image.load('assets/icon_cow.png')
# menu screen
menu_screen = pygame.image.load('assets/home.jpg')

# musik
pointsound = pygame.mixer.Sound('assets/cow_talk.wav')

# kuningsound = pygame.mixer.Sound('assets/soundtwo.wav')
# edited soundtwo, removed around 0.6 second withoud any effects
kuningsound = pygame.mixer.Sound('assets/soundtwo2.wav')

stone_crash_sound = pygame.mixer.Sound('assets/stone_crash.wav')

created_font = pygame.font.SysFont("Verdana", 20)
game_font = pygame.font.SysFont("Verdana", 30)
menufont = pygame.font.SysFont("Verdana", 40)
gofont = pygame.font.SysFont("Verdana", 60)

pygame.display.set_caption("Run Cow Game")
pygame.display.set_icon(ikon)


# 2 buat function
# looping
def gamecow():

    # start background music
    background_music()

    # new instance of Crash object
    crash = Crash()
    menu_game()



    points = 0
    global Lives
    Lives = 3
    # crash = False
    after_crash_timer = 3

    # buat rectangle
    RECTX, RECTY = size_x / 2, 0
    CowX, CowY = size_x / 2, size_y / 2 + cowheight
    RUMPUTHIJAUX, RUMPUTHIJAUY = random.randrange(0.2 * size_x, 0.8 * size_x, STEP), 0
    RUMPUTKUNINGX, RUMPUTKUNINGY = random.randrange(0.1 * size_x, 0.8 * size_x, STEP), 0
    BATUX, BATUY = random.randrange(0.2 * size_x, 0.8 * size_x, STEP), 0

    # 3.buat movement tombol
    direction = -1  # -1 itu kiri, 1 itu kanan
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 3 bikin button
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = -1
                # CowX -=10 dihapus
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                elif event.key == pygame.K_UP:
                    direction = 0
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if direction == -1:
            CowX -= STEP
        elif direction == 1:
            CowX += STEP

        if CowX <= 0:
            direction = 0
            CowX = 100
            # start = time.time()
            if crash.crash():
                gameover()
        # crash = True
        # gameover()
        elif CowX > size_x - 100:
            direction = 0
            CowX = size_x - 200
            if crash.crash():
                gameover()
        # start = time.time()
        # crash = True
        # gameover()
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(bg_img, (0, 0))  # 4backgorund

        # if cow get green grass
        if (check_rumputhijau(CowX, CowY, RUMPUTHIJAUX, RUMPUTHIJAUY)):
            RUMPUTHIJAUX, RUMPUTHIJAUY = random.randrange(0.2 * size_x, 0.8 * size_x, STEP), 0
            points += 1
            print(points)

        if (check_rumputkuning(CowX, CowY, RUMPUTKUNINGX, RUMPUTKUNINGY)):
            RUMPUTKUNINGX, RUMPUTKUNINGY = random.randrange(0.2 * size_x, 0.8 * size_x, STEP), 0
            if points > 0:
                points -= 1
            print(points)

        RECTY += STEP
        RECTY = RECTY % YDIFF
        RUMPUTHIJAUY += STEP
        RUMPUTKUNINGY += STEP
        BATUY += 1 * STEP

        if RUMPUTHIJAUY >= size_y:
            RUMPUTHIJAUX, RUMPUTHIJAUY = random.randrange(0.2 * size_x, 0.8 * size_x, STEP), 0

        if BATUY >= size_y:
            BATUX, BATUY = random.randrange(0.2 * size_x, 0.8 * size_x, STEP), 0

        if RUMPUTKUNINGY >= size_y:
            RUMPUTKUNINGX, RUMPUTKUNINGY = random.randrange(0.2 * size_x, 0.8 * size_x, STEP), 0
        for i in range(-1, 8):
            pygame.draw.rect(SCREEN, (0, 255, 0), [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])

        SCREEN.blit(rumputhijau, (RUMPUTHIJAUX, RUMPUTHIJAUY))
        SCREEN.blit(rumputkuning, (RUMPUTKUNINGX, RUMPUTKUNINGY))
        SCREEN.blit(batu, (BATUX, BATUY))

        if crash.crash_b:
            lives_text_color = (255, 0, 0)
            SCREEN.blit(cow_after_crash, (CowX, CowY))
            crash.crash()
        else:
            lives_text_color = (255, 255, 255)
            SCREEN.blit(cow, (CowX, CowY))

        # text object utk game_font
        text_lives = game_font.render('Lives: ' + str(Lives),  True, lives_text_color)
        text_points = game_font.render('Score: ' + str(points), True, (255, 255, 255))
        SCREEN.blit(text_lives, (120, 0))
        SCREEN.blit(text_points, (250, 0))

        # if cow crash with stone
        if cowcrash(CowX, CowY, BATUX, BATUY):
            if crash.crash():
                stone_crash_sound.play()
                gameover()

        cek_step_out(CowX)
        clock.tick(FPS)
        pygame.display.update()

# 4 membuat score
# rumput hijau dapat poin 1
def check_rumputhijau(CowX, CowY, RUMPUTHIJAUX, RUMPUTHIJAUY):
    if (CowX - RUMPUTHIJAUX) <= RUMPUTHIJAUSIZE and (RUMPUTHIJAUX - CowX) <= cowwidth:
        if (CowY - RUMPUTHIJAUY) <= RUMPUTHIJAUSIZE and (RUMPUTHIJAUY - CowY) <= cowheight:
            pointsound.play()
            return True
    return False

# rumput kuning dikurangi 1 poin
def check_rumputkuning(CowX, CowY, RUMPUTKUNINGX, RUMPUTKUNINGY):
    if (CowX - RUMPUTKUNINGX) <= RUMPUTKUNINGSIZE and (RUMPUTKUNINGX - CowX) <= cowwidth:
        if (CowY - RUMPUTKUNINGY) <= RUMPUTKUNINGSIZE and (RUMPUTKUNINGY - CowY) <= cowheight:
            kuningsound.play()
            return True
    return False

#membuat function crush
def cowcrash(CowX, CowY, BATUX, BATUY):
    if (CowX - BATUX) <= BATU_SIZE and (BATUX - CowX) <= cowwidth:
        if (CowY - BATUY) <= BATU_SIZE and (BATUY - CowY) <= cowheight:
            return True
    return False

#menu game 
def menu_game():
    points = 0
    print_menu(points)
    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    points += 1
                    points = points % 2
                    print_menu(points)
                elif event.key == pygame.K_UP:
                    points -= 1
                    points = points % 2
                    print_menu(points)
                elif event.key == pygame.K_RETURN:
                    if points == 0:
                        return True
                    elif points == 1:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


def print_menu(points):

    SCREEN.blit(menu_screen, (0, 0))  # 4backgorund

    print_created_by()

    if points == 0:
        color_a = (128, 0, 0)
        color_b = (0, 0, 0)
    else:
        color_b = (128, 0, 0)
        color_a = (0, 0, 0)

    mulai = menufont.render('START GAME', True, color_a)
    keluar = menufont.render('QUIT GAME', True, color_b)
    SCREEN.blit(mulai, (size_x / 10, size_y / 10))
    SCREEN.blit(keluar, (size_x / 10, 3 * size_y / 10))

    print(" ... ")
    points = points % 2
    pygame.display.update()

#tampilan screen diawal game berisi data kelompok
def print_created_by():
    text_color = (100, 0, 0)
    print_name = created_font.render("Game created by : Kelompok 1", True, text_color)
    SCREEN.blit(print_name, (size_x / 10, 5 * size_y / 10))

    created_by = ["Arny Lattu", "Yusiana", "Deka Nirmala", "Rizki Nurmala"]
    name_y_pos = 6
    number = 1
    for name in created_by:
        print_name = created_font.render(str(number) + ": " + name, True, text_color)
        SCREEN.blit(print_name, (size_x / 10, name_y_pos * size_y / 10))
        name_y_pos += 1
        number += 1

def background_music():
    # volume level available values from 0.0 to 1.0
    volume = 0.05
    pygame.mixer.init()
    pygame.mixer.music.load('assets/backsound.wav')
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1, 0.0)
    # pygame.mixer.music.play(loops, start)


def gameover():
    global Lives
    if Lives > 1:
        Lives -= 1
        print(" -1 Live")
    else:
        print(" Game Over ***")
        SCREEN.fill((200, 200, 200))
        crash = gofont.render('TERTABRAK', True, (0, 0, 0))
        game_over = gofont.render('GAME END', True, (0, 0, 0))
        SCREEN.blit(crash, (size_x / 10, size_y / 10))
        SCREEN.blit(game_over, (size_x / 10, 3 * size_y / 10))

        print_created_by()

        pygame.display.update()
        # 9 tambahkan library time
        time.sleep(2)
        gamecow()


def cek_step_out(CowX):
    if CowX < 0.1 * size_x or CowX > 0.78 * size_x:
        return True
    return False


# object for controlling crashes
# function crash() returns True when is time to decrease number of lives
# function crash() returns False for 2.5 seconds after last clash event
class Crash:
    timer = 2.5
    crash_b = False
    image_change = False
    start = 0
    end = 0

    def crash(self):
        if not self.crash_b:
            self.start = time.time()
            self.crash_b = True
            print(" __crash __ ")
            return True
        else:
            self.end = time.time()
            if self.end - self.start > self.timer:
                self.crash_b = False
        return False


gamecow()
