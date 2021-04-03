import pygame, sys, os, random, threading  # Importing modules

script_dir = os.path.dirname(os.path.abspath(__file__))  # Defining the file directory for easy access
image_dir = script_dir + "\\Game_Data\\Visuals_Audio\\"  # Location for the Images and Audio folder
image_list = script_dir + "\\Game_Data\\Image_Data.txt"  # Location for the image list
variable_list = script_dir + "\\Game_Data\\Variable_Data.txt"  # Location for the variable list
cards_list = script_dir + "\\Game_Data\\Card_Information.txt"  # Location for the card info list
hover_list = script_dir + "\\Game_Data\\Hover_Effects.txt"  # Location for the hover effect list
test_list = script_dir + "\\Game_Data\\Test_Information.txt"  # Location for the test information list
save_dir = script_dir + "\\Game_Data\\Data_Saves\\"  # Folder with save files
save_1, save_2, save_3 = save_dir + "Save_File_1.txt", save_dir + "Save_File_2.txt", save_dir + "Save_File_3.txt"  # Save file location

pygame.init()  # Setting up the Pygame module
width, height = 1000, 700  # Setting screen size
display = pygame.display.set_mode((width, height))  # Setting up display
clock = pygame.time.Clock()  # Setting up a clock
FPS = 500  # Setting up frame rate
img_data, var_data = ({},) * 2  # Making lists for data
mouse_x, mouse_y, loading_percent = (0,) * 3  # Mouse position (pixels)
pygame.mouse.set_visible(False)  # Setting the mouse cursor invisible

# Defining images before hand (for before the game starts)
game_icon = pygame.transform.scale(pygame.image.load(image_dir + "GameIcon.png").convert_alpha(), (32, 32))
backdrop_1 = pygame.transform.scale(pygame.image.load(image_dir + "Background3.png").convert_alpha(), (1000, 700))
backdrop_2 = pygame.transform.scale(pygame.image.load(image_dir + "Sky1.png").convert_alpha(), (1000, 700))
loading_1 = pygame.transform.scale(pygame.image.load(image_dir + "Loading1.png").convert_alpha(), (1000, 700))
pygame.display.set_caption("Growing Pains the Game"), pygame.display.set_icon(game_icon)

# Defining Hover effect variable names and positions of activation
effect_positions = ["hover_1,400,261", "hover_2,400,371", "hover_3,400,480", "hover_4,400,591", "hover_5,400,261", "hover_6,400,371", "hover_7,400,480", "hover_8,400,261", "hover_9,400,371", "hover_11,400,261", "hover_22,400,371", "hover_33,645,591", "hover_44,645,591", "hover_55,645,591", "hover_66,345,362", "hover_77,530,362", "hover_88,109,324", "hover_111,400,52", "hover_222,400,162", "hover_333,400,272", "hover_444,368,391", "hover_555,512,391", "hover_666,440,489", "hover_777,109,323"]
# Defining available player stats and information regarding these stats
bar_list = ['physical', 'mental', 'social', 'financial', 0, 10, 15, 25]
ethnicity_names = ['arab', 'asian', 'black', 'hispanic', 'indian', 'indigenous', 'iranian', 'islander', 'jewish', 'kurdish', 'latino', 'malay', 'mongols', 'multicultural', 'romani', 'tibetan', 'turkic', 'white']
hobbies = ['violin', 'badminton', 'writing', 'football', 'art', 'piano', 'gaming', 'karate', 'singing', 'movies', 'chess', 'rugby', 'guitar', 'entrepreneur', 'singing', 'developer']
hobby_jobs = ['violinist', 'badminton', 'book_writer', 'football', 'artist', 'pianist', 'paid_gamer', 'dojo_trainer', 'pop_singer', 'producer', 'pro_chess', 'rugby', 'guitarist', 'entrepreneur', 'pop_singer', 'developer']
religions = ['christianity', 'islam', 'hinduism', 'buddhism', 'sikhism']
jobs = ['fast_food', 'accountant', 'blogger', 'cleaner', 'doctor', 'farmer', 'aviator', 'dentist', 'engineer', 'lawyer']
tests = ['maths_test_1', 'general_knowledge_1', 'english_test_1', 'maths_test_2', 'general_knowledge_2', 'english_test_2', 'maths_test_3', 'general_knowledge_3', 'english_test_3', 'maths_test_4', 'general_knowledge_4', 'english_test_4']
# Age of death for males and females of the cohering ethnicity
ethnicity_male_age, ethnicity_female_age = [65, 76, 72, 79, 66, 67, 72, 69, 77, 69, 79, 73, 67, 74, 74, 68, 75, 78], [70, 79, 77, 82, 70, 73, 75, 73, 80, 72, 82, 76, 71, 74, 76, 70, 78, 80]
# Pay for the various jobs
hobby_cards, hobby_jobs_pay = [19, 22, 47, 57, 58, 65, 67, 68, 76, 88, 96, 100, 118, 135, 156, 161], [3, 6, 6, 10, 5, 3, 5, 2, 9, 11, 5, 9, 2, 12, 9, 8]
religion_cards = [78, 97, 148, 174, 177]
job_cards, jobs_pay = [155, 162, 163, 164, 165, 166, 169, 170, 171, 172], [2, 4, 2, 1, 8, 4, 4, 6, 5, 7]
test_cards = [54, 74, 75, 98, 102, 104, 109, 116, 117, 122, 129, 134, 145, 150]
# Impact on individual stats depending on player's ethnicity
ethnicity_impacts = [(1, 1, 1, 1.15), (0.85, 1.2, 0.85, 1), (1.2, 0.8, 0.8, 0.8), (1, 1, 1, 0.9), (0.85, 1.2, 0.85, 1), (0.9, 0.9, 0.9, 0.9), (1, 1, 1, 1.1), (1.1, 0.9, 1.1, 0.9), (1.2, 1, 1, 1.2), (1, 1, 1.1, 1.1), (1, 1, 1, 0.9), (1, 1.1, 1.1, 1), (0.8, 1, 0.8, 0.8), (1.1, 1.1, 1.1, 1.1), (1, 0.95, 1.05, 1), (1, 1.1, 1, 1.1), (1, 1, 1.05, 0.9), (1.15, 1.15, 1.15, 1.15)]

decision_list = []
for i in range(0, 641):  # Appending total number of cards in game into list to cross check for duplicated decisions
    decision_list.append(i)
tip_list = []


def events2(tutorial, loading):  # Function for updating the screen
    global mouse_x, mouse_y, loading_percent
    loading_bar = pygame.transform.scale(pygame.image.load(image_dir + "LoadingBar.png").convert_alpha(), (round(5.49 * loading_percent), 22))
    display.blit(backdrop_2, (0, 0)), display.blit(backdrop_1, (0, 0))
    if loading:  # If the game is currently in loading phase
        if loading_percent < 100:  # Loading the game
            loading_percent += 0.105
            display.blit(loading_bar, (225, 555))
        else:
            loading_percent = 100
        display.blit(loading_1, (0, 0))
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:  # Quit the program
            pygame.quit(), sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and tutorial and var_data['tutorial_page'] <= 7:  # To progress through the tutorial phase
            var_data['tutorial_page'] += 1
    if tutorial and var_data['tutorial_page'] != 7:  # I'm using the first 'tutorial' argument because the dictionary variable doesn't load until after the notepad loop.
        display.blit(img_data['game_backdrop2'], (0, 0)), display.blit(img_data['life_card_pile'], (796, 47)), display.blit(img_data['tutorial_tip_' + str(var_data['tutorial_page'])], (0, 0))
        display.blit(img_data['cursor_1'], (mouse_x - 3, mouse_y - 3))
    pygame.display.update()


class Bunch(object):  # Creating a class to eventually appending values into 2 dictionaries for Images and Variables
    def __init__(self, adict):
        self.__dict__.update(adict)


with open(image_list) as notepad:  # Opening image_list and creating image variables through class (looping)
    loading = False
    x = 0
    x_2 = 0
    lines = notepad.read().splitlines()
    for num, item in enumerate(lines):
        events2(False, True)
        if num >= 3:  # The first 2 lines are to assist users
            data_set = item.split(",")
            img_data[data_set[1]] = pygame.transform.scale(pygame.image.load(image_dir + data_set[2] + ".png").convert_alpha(),(int(data_set[3]), int(data_set[4])))
            list1 = Bunch(img_data)  # Appending into dictionary later on

with open(variable_list) as notepad:    # Opening variable_list and creating variables through class (looping)
    lines = notepad.read().splitlines()
    for num, item in enumerate(lines):
        if num >= 3:  # The first 2 lines are to assist users
            data_set = item.split(" = ")
            if data_set[1] == "Nothing":
                value = data_set[1]
            elif data_set[1] == "True":
                value = True
            elif data_set[1] == "False":
                value = False
            elif data_set[1] != "(":
                value = int(data_set[1])
            var_data[data_set[0]] = value
            list2 = Bunch(var_data)  # Appending into dictionary later on


transparency = 255
var_data['tutorial_page'] = 1
for i in range(1, 40):
    events2(False, True)
    transparency -= 1
    pygame.time.wait(100)  # Special effects to create interest in the loading page
    loading_1.fill((255, 255, 255, transparency), None, pygame.BLEND_RGBA_MULT)

while var_data['tutorial_page'] != 7:  # Once loading phase is complete, tutorial phase commences
    events2(True, False)
timer_bar = pygame.transform.scale(pygame.image.load(image_dir + "TimeBar.png").convert_alpha(), (round(2.88 * var_data['timer']), 18))


def thread_function(time, name, type, physical, mental, social, financial):
    global timer_bar
    if type == "theme_changer":
        if var_data['first_theme2']:
            var_data['first_theme'], var_data['first_theme2'] = (False,) * 2
        elif not var_data['first_theme2']:
            var_data['first_theme'], var_data['first_theme2'] = (True,) * 2
        pygame.time.wait(time)
        var_data['sleeper'] = False

    elif type == "test_timer":
        var_data['test_state'] = 1  # Test states: 0 = completed, 1 = ongoing
        while var_data['timer'] != 0:
            print(mental, social)
            pygame.time.wait(time)
            var_data['timer'] -= 1
            if var_data['placed_1'] and var_data['placed_2'] and var_data['placed_3'] and var_data['placed_4']:
                var_data['timer'] = 0
                stat_changes(physical, mental, social, financial)
            timer_bar = pygame.transform.scale(pygame.image.load(image_dir + "TimeBar.png").convert_alpha(), (round(2.88 * var_data['timer']), 18))
        test_normalize()
        var_data['current_test'], var_data['test_mode'], var_data['timer'], var_data['test_state'] = "Nothing", 0, 100, 0


def life_card_chooser():  # Function for when player chooses life card
    if var_data['card_number'] == 0 and not var_data['saving_process'] and var_data['test_mode'] != 1:
        var_data['life_card_reset'] += 1
        var_data['menu_message'] = True
        card_check_function()  # Picks a random card according to age

        if var_data['card_number'] in decision_list:
            decision_list.remove(var_data['card_number'])  # Removing from list to disallow duplicates
        else:
            while var_data['card_number'] not in decision_list:
                card_check_function()  # Picks a random card according to age
            decision_list.remove(var_data['card_number'])

        if var_data['life_card_reset'] == 4:  # To increase player's age every 4 decisions
            pay_function(), age_function()


def card_check_function():  # Function to check for duplicate cards and for selecting new, random card
    chosen_card_num = random.randint(((int(var_data['age']) * 8) - 7), (int(var_data['age']) * 8))  # Random number between 1-8 according to age, e.g. age 50 means (393, 400)
    while var_data['card_number'] != chosen_card_num:
        with open(cards_list) as notepad:
            lines = notepad.read().splitlines()
            for num, item in enumerate(lines):
                if num >= 3:  # The first 2 lines are to assist users
                    data_set = item.split(",")
                    if len(data_set) > 10 and chosen_card_num == int(data_set[0]) and var_data['physical'] >= int(data_set[10]) and var_data['mental'] >= int(data_set[11]) and var_data['social'] >= int(data_set[12]) and var_data['financial'] >= int(data_set[13]):
                        var_data['card_number'] = chosen_card_num  # Special condition for when the decision requires specific health bar stats
                    elif len(data_set) == 10 and chosen_card_num == int(data_set[0]):
                        var_data['card_number'] = chosen_card_num
                    else:
                        chosen_card_num = random.randint(((int(var_data['age']) * 8) - 7), (int(var_data['age']) * 8))


def age_function():  # Function for increasing player age
    if var_data['gender'] == 1:  # Male life span
        for pos, age in enumerate(ethnicity_male_age):
            if var_data['ethnicity_number'] == pos and var_data['age'] < age:
                var_data['life_card_reset'], var_data['age'] = 0, int(var_data['age']) + 1
            elif var_data['ethnicity_number'] == pos and var_data['age'] == age:
                var_data['game_page'], var_data['death'] = "Game2", True
    elif var_data['gender'] == 2 or var_data['gender'] == 3:  # Female life span
        for pos, age in enumerate(ethnicity_female_age):
            if var_data['ethnicity_number'] == pos and var_data['age'] < age:
                var_data['life_card_reset'], var_data['age'] = 0, int(var_data['age']) + 1
            elif var_data['ethnicity_number'] == pos and var_data['age'] == age:
                var_data['game_page'], var_data['death'] = "Game2", True


def pay_function():
    if var_data['job'] != "Nothing":
        for pos1, hobby_job in enumerate(hobby_jobs):  # Looping through hobbies to check if player's current hobby adheres to their current hobby pay, then paying
            if var_data['job'] == hobby_job:
                for pos, hobby_pay in enumerate(hobby_jobs_pay):
                    if pos == pos1:
                        var_data['financial'] = var_data['financial'] + hobby_pay

        for pos1, job in enumerate(jobs):  # Looping through jobs to check if player's current job adheres to their current job pay, then paying
            if var_data['job'] == job:
                for pos, job_pay in enumerate(jobs_pay):
                    if pos == pos1:
                        var_data['financial'] = var_data['financial'] + job_pay



def play_function():  # Main function for game play
    global tip_list
    var_data['tip_1'] = False
    if not var_data['saving_process']:
        save_button_normalize()

    if var_data['age'] == 23 and var_data['job'] == "Nothing" and var_data['hobby'] != "Nothing":
        print('ddddd')
        for pos, hobby in enumerate(hobbies):
            if var_data['hobby'] == hobby:
                for pos1, hobby_job in enumerate(hobby_jobs):
                    if pos == pos1:
                        var_data['job'] = hobby_job

    if var_data['current_test'] != "Nothing":
        display.blit(img_data[var_data['current_test']], (300, 38))
    display.blit(img_data['game_backdrop' + str(var_data['test_mode'])], (22, 22))  # Displaying backdrop based on whether it's normal or test mode (there are 2 types)

    if var_data['current_test'] != "Nothing":
        if var_data['current_test'][0] == "e":
            test, level, offset_x, offset_y = "english", var_data['current_test'][13], 50, 17
        elif var_data['current_test'][0] == "m":
            test, level, offset_x, offset_y = "maths", var_data['current_test'][11], 15, 15
        elif var_data['current_test'][0] == "g":
            test, level, offset_x, offset_y = "general", var_data['current_test'][18], 35, 15
        for num in range(1, 5):
            if not var_data['picked_' + str(num)] and not var_data['placed_' + str(num)]:
                display.blit(img_data[test + '_' + level + '_result_' + str(num)], (var_data['location_' + str(num) + '_x'], var_data['location_' + str(num) + '_y']))
            elif var_data['placed_' + str(num)]:
                display.blit(img_data[test + '_' + level + '_result_' + str(num)], (var_data[test + '_1_' + str(num) + '_x'], var_data[test + '_1_' + str(num) + '_y']))
            elif var_data['picked_' + str(num)] and not var_data['placed_' + str(num)]:
                display.blit(img_data[test + '_' + level + '_result_' + str(num)], (mouse_x - offset_x, mouse_y - offset_y))

        with open(test_list) as notepad:
            lines = notepad.read().splitlines()
            for num, item in enumerate(lines):
                if num >= 3:  # The first 2 lines are to assist users
                    data_set = item.split(",")
                    if data_set[0] == var_data['current_test']:
                        for i in range(0, 4):  # This is to check if player can pick up the answer
                            if (int(data_set[1 + (i*8)]) <= mouse_x <= int(data_set[2 + (i*8)]) and int(data_set[3 + (i*8)]) <= mouse_y <= int(data_set[4 + (i*8)])) and not var_data['placed_' + str(i+1)]:
                                if not var_data['drag']:
                                    var_data['can_pick_' + str(i+1)] = True
                            else:
                                var_data['can_pick_' + str(i + 1)] = False

                        for i in range(0, 4):  # This is to check if the player has picked up the answer
                            if (int(data_set[1 + (i*8)]) <= mouse_x <= int(data_set[2 + (i*8)]) and int(data_set[3 + (i*8)]) <= mouse_y <= int(data_set[4 + (i*8)])):
                                if var_data['drag'] and var_data['can_pick_' + str(i+1)]:
                                    var_data['picked_' + str(i+1)] = True
                            elif not var_data['drag']:
                                var_data['can_pick_' + str(i + 1)] = True
                                var_data['picked_' + str(i + 1)] = False

                        for i in range(0, 4):  # This is to check if player can place the answer in the right place
                            if (int(data_set[5 + (i * 8)]) <= mouse_x <= int(data_set[6 + (i * 8)]) and int(data_set[7 + (i * 8)]) <= mouse_y <= int(data_set[8 + (i * 8)])):
                                if var_data['picked_' + str(i+1)]:
                                    var_data['can_place_' + str(i+1)] = True
                            else:
                                var_data['can_place_' + str(i + 1)] = False

                        for i in range(0, 4):  # This is to check if player has placed the answer in the correct place
                            if (int(data_set[5 + (i * 8)]) <= mouse_x <= int(data_set[6 + (i * 8)]) and int(data_set[7 + (i * 8)]) <= mouse_y <= int(data_set[8 + (i * 8)])):
                                if not var_data['drag'] and var_data['can_place_' + str(i + 1)]:
                                    var_data['placed_' + str(i + 1)] = True

                        print(var_data["current_test"])


    if var_data['test_mode'] == 1:  # Display the timer bar if the player is doing a test
        display.blit(timer_bar, (382, 418))

    if var_data['test_mode'] != 1 and var_data['game_page'] != "Game2":
        display.blit(img_data['no_button'], (529, 362)), display.blit(img_data['yes_button'], (344, 362))

    if var_data['first_theme2'] and var_data['game_page'] == "Game1":
        display.blit(img_data['day_button'], (109, 385))
    elif not var_data['first_theme2'] and var_data['game_page'] == "Game1":
        display.blit(img_data['night_button'], (109, 385))

    if var_data['card_number'] != 0 and not var_data['death']:
        display.blit(img_data['card_' + str(var_data['card_number'])], (412, 62))

    if len(str(var_data['age'])) > 1:
        display.blit(img_data['num_' + str(var_data['age'])[1]], (846, 511))

    if var_data['religion'] != "Nothing":
        display.blit(img_data['religion_' + var_data['religion']], (864, 555))

    if var_data['hobby'] != "Nothing":
        display.blit(img_data['hobby_' + var_data['hobby']], (855, 596))

    if var_data['job'] != "Nothing":
        display.blit(img_data['job_' + var_data['job']], (837, 618))

    #  Put these through a loop and blit them
    if var_data['game_page'] == "Game2" and not var_data['death']:
        display.blit(img_data['exit_button'], (109, 323))
        for i in range(0, 4):
            if var_data[bar_list[i]] == 0 and var_data['age'] >= bar_list[i+4]:
                display.blit(img_data['death_' + bar_list[i]], (5, 80))
    elif var_data['game_page'] == "Game2" and var_data['death']:
        display.blit(img_data['exit_button'], (109, 323))
        display.blit(img_data['game_won_death'], (5, 80))
    else:
        display.blit(img_data['menu_button'], (109, 323))

    display.blit(img_data['physical_health'], (185, 510), (0, 0, round(5.56 * int(var_data['physical'])), 17))
    display.blit(img_data['mental_health'], (185, 547), (0, 0, round(5.56 * int(var_data['mental'])), 17))
    display.blit(img_data['social_health'], (185, 584), (0, 0, round(5.56 * int(var_data['social'])), 17))
    display.blit(img_data['financial_health'], (185, 621), (0, 0, round(5.56 * int(var_data['financial'])), 17))
    display.blit(img_data['num_' + str(var_data['age'])[0]], (840, 511)), display.blit(img_data['life_card_pile'], (775, 57))
    display.blit(img_data['gender_' + str(var_data['gender'])], (858, 534)), display.blit(img_data['ethnicity_' + var_data['ethnicity']], (869, 576))

    if var_data['current_test'] == "Nothing":
        if 738 <= mouse_x <= 941 and 316 <= mouse_y <= 444:
            if var_data['tip_number'] == 0:
                if len(tip_list) == 47:
                    tip_list = []
                var_data['tip_number'] = random.randint(1, 47)
                if var_data['tip_number'] not in tip_list:
                    tip_list.append(var_data['tip_number'])
                else:
                    while var_data['tip_number'] in tip_list:
                        var_data['tip_number'] = random.randint(1, 47)
                        print(var_data['tip_number'])
            print(len(tip_list))
            display.blit(img_data['player_tip_' + str(var_data['tip_number'])], (742, 321))
        else:
            var_data['tip_number'] = 0
            display.blit(img_data['game_tip_button'], (732, 311))

    if var_data['saving_process'] and var_data['card_number'] == 0 and var_data['test_mode'] != 1:
        display.blit(img_data['warning_background'], (0, 0)), display.blit(img_data['save_file_1'], (400, 52))
        display.blit(img_data['save_file_2'], (400, 162)), display.blit(img_data['save_file_3'], (400, 272))
        display.blit(img_data['warning_save_button'], (368, 391)), display.blit(img_data['warning_back_button'], (512, 391))
        display.blit(img_data['warning_quit_button'], (440, 489))
    else:
        var_data['saving_process'] = False


def save_button_normalize():
    var_data['save_file_1_selected'], var_data['save_file_2_selected'], var_data['save_file_3_selected'] = (False,) * 3


def player_choice():
    if var_data['card_number'] != 0 and not var_data['saving_process'] and var_data['test_mode'] != 1:
        with open(cards_list) as notepad:
            lines = notepad.read().splitlines()
            for num, item in enumerate(lines):
                if num >= 3:  # The first 2 lines are to assist users
                    data_set = item.split(",")
                    if int(data_set[0]) == var_data['card_number']:
                        if data_set[1] == "Binary":
                            if var_data['choice'] == "Yes":
                                stat_changes(int(data_set[2]), int(data_set[3]), int(data_set[4]), int(data_set[5]))

                                for pos, hobby_card in enumerate(hobby_cards):  # Looping through all hobby cards to check if selected card is hobby card and granting it accordingly
                                    if var_data['card_number'] == hobby_card:
                                        for pos1, hobby in enumerate(hobbies):
                                            if pos == pos1:
                                                print(hobby)
                                                var_data['hobby'] = hobby
                                for pos, job_card in enumerate(job_cards):  # Looping through all job cards to check if selected card is job card and setting the player's financial element
                                    if var_data['card_number'] == job_card:
                                        for pos1, job in enumerate(jobs):
                                            if pos == pos1:
                                                var_data['job'] = job
                                for pos, religion_card in enumerate(religion_cards):  # Looping through all religion cards to check if selected card is religion card and setting the player's beliefs
                                    if var_data['card_number'] == religion_card:
                                        for pos1, religion in enumerate(religions):
                                            if pos == pos1:
                                                var_data['religion'] = religion

                            elif var_data['choice'] == "No":
                                stat_changes(int(data_set[6]), int(data_set[7]), int(data_set[8]), int(data_set[9]))

                        elif data_set[1] == "Multiple":
                            if var_data['choice'] == "Yes":
                                for pos, test_card in enumerate(test_cards):  # Looping through all test cards to check if selected card is test card and calling function to allow player to study
                                    if var_data['card_number'] == test_card:
                                        for pos1, test in enumerate(tests):
                                            if pos == pos1:
                                                if var_data['test_mode'] == 0:
                                                    var_data['test_mode'], var_data['current_test'] = 1, test
                                                    t = threading.Thread(target=thread_function, args=(200, 'sleeperFunction', 'test_timer', int(data_set[2]), int(data_set[3]), int(data_set[4]), int(data_set[5]))) #  Using the same theme thread but with a different 3rd argument to act as timer
                                                    t.start()  # Starting the thread

                            elif var_data['choice'] == "No":
                                stat_changes(int(data_set[6]), int(data_set[7]), int(data_set[8]), int(data_set[9]))
        var_data['card_number'], var_data['menu_message'], var_data['special_stat_debuff']  = 0, False, True
    else:
        var_data['choice'] = "Nothing"


def stat_changes(physical, mental, social, financial):
    stat_updates = [physical, mental, social, financial]
    if var_data['gender'] == 2:
        financial, physical, mental = round(financial * 0.8), round(physical * 1.1), round(mental * 1.1)
    elif var_data['gender'] == 3:
        social = round(social * 0.9)

    for pos, ethnicity in enumerate(ethnicity_names):
        if var_data['ethnicity'] == ethnicity:
            for pos1, impact in enumerate(ethnicity_impacts):
                if pos == pos1:
                    physical, mental = round(physical * impact[0]), round(mental * impact[1])
                    social, financial = round(social * impact[2]), round(financial * impact[3])

    for i in range(0, 4):
        if var_data[bar_list[i]] + stat_updates[i] >= 100:
            var_data[bar_list[i]] = 100
            stat_debuff()
        elif var_data[bar_list[i]] + stat_updates[i] > 0:
            var_data[bar_list[i]] += stat_updates[i]
        elif var_data[bar_list[i]] + stat_updates[i] <= 0 and var_data['age'] >= bar_list[i+4]:
            var_data[bar_list[i]], var_data['game_page'] = 0, "Game2"
    var_data['bar_update'] = True


def stat_debuff():
    if var_data['special_stat_debuff']:
        var_data['special_stat_debuff'] = False
        for i in range(0,4):
            if var_data[bar_list[i]] - 1 >= 0:
                var_data[bar_list[i]] -= 1


def effect_remover():
    var_data['hover_1'], var_data['hover_2'], var_data['hover_3'], var_data['hover_4'] = (False,) * 4


def load_function():
    effect_remover()
    var_data['tip_2'] = False
    display.blit(img_data['load_file_1'], (400, 261)), display.blit(img_data['load_file_2'], (400, 371))
    display.blit(img_data['load_file_3'], (400, 480)), display.blit(img_data['files_label'], (400, 591))
    display.blit(img_data['back_button_2'], (645, 591))
    if var_data['load_function_normalize']:
        normalize()
        var_data['load_function_normalize'] = False


def themes_function():
    effect_remover()
    var_data['tip_3'] = False
    display.blit(img_data['theme_1'], (400, 261)), display.blit(img_data['theme_2'], (400, 371))
    display.blit(img_data['themes_button'], (400, 591)), display.blit(img_data['back_button_3'], (645, 591))


def music_function():
    effect_remover()
    var_data['tip_4'] = False
    display.blit(img_data['music_on'], (400, 261)), display.blit(img_data['music_off'], (400, 371))
    display.blit(img_data['music_button'], (400, 591)), display.blit(img_data['back_button_4'], (645, 591))


def menu_function():
    if var_data['game_page'] == "Menu1":
        if var_data['hover_33'] or var_data['hover_44'] or var_data['hover_55']:
            var_data['hover_33'], var_data['hover_44'], var_data['hover_55'] = (False,) * 3
        if not var_data['bar_update']:
            var_data['bar_update'] = True
        display.blit(img_data['play_button'], (400, 261)), display.blit(img_data['load_button'], (400, 371))
        display.blit(img_data['themes_button'], (400, 480)), display.blit(img_data['music_button'], (400, 591))
    elif var_data['game_page'] == "Game1" or var_data['game_page'] == "Game2":
        if var_data['game_button_pause']:
            var_data['game_button_pause'] = False
            if not var_data['save_file_3_debounce']:
                var_data['save_file_3_selected'] = False
            if var_data['new_game'] and not var_data['save_file_1_selected'] and not var_data['save_file_2_selected'] and not var_data['save_file_3_selected'] and var_data['gender'] == 0:
                new_game_randomizer()
        effect_remover()
        play_function()

    if var_data['load_page'] and var_data['game_page'] != "Menu1":
        load_function()
    elif var_data['themes_page'] and var_data['game_page'] != "Menu1":
        themes_function()
    elif var_data['music_page'] and var_data['game_page'] != "Menu1":
        music_function()
    else:
        var_data['load_page'], var_data['themes_page'], var_data['music_page'] = (False,) * 3


def new_game_randomizer():
    var_data['new_game'] = False
    var_data['gender'] = random.randint(1, 3)
    var_data['ethnicity_number'] = random.randint(0, 17)
    for pos, ethnicity in enumerate(ethnicity_names):
        if var_data['ethnicity_number'] == pos:
            var_data['ethnicity'] = ethnicity


def normalize():  # Reset all the variables and return user to main menu
    global decision_list
    if var_data['saving_process'] or var_data['game_page'] == "Menu2" or var_data['game_page'] == "Game2":
        if not var_data['load_function_normalize']:
            var_data['load_page'], var_data['themes_page'], var_data['music_page'], var_data['saving_process'], \
            var_data['save_file_1_selected'], var_data['save_file_3_selected'] = (False,) * 6
            var_data['age'], var_data['card_number'], var_data['life_card_reset'], var_data['choice'], \
            var_data['game_page'] = 1, 0, 0, "Nothing", "Menu1"
        var_data['save_file_3_debounce'], var_data['save_file_2_selected'], var_data['special_stat_debuff'] = (False,)*3
        var_data['game_button_pause'], var_data['new_game'] = (True,) * 2
        var_data['religion'], var_data['ethnicity'], var_data['hobby'], var_data['job'], \
        var_data['current_test'] = ("Nothing",) * 5
        var_data['physical'], var_data['mental'], var_data['social'], var_data['financial'], var_data['age'], \
        var_data['gender'], var_data['ethnicity_number'], var_data['test_mode'], var_data['timer'], \
        var_data['test_state'] = 20, 20, 20, 0, 1, 0, 0, 0, 100, 0
        var_data['death'] = False
        test_normalize()
        decision_list = []
        for i in range(0, 641):
            decision_list.append(i)


def test_normalize():
    var_data['can_pick_1'], var_data['can_pick_2'], var_data['can_pick_3'], var_data['can_pick_4'], \
    var_data['picked_1'], var_data['picked_2'], var_data['picked_3'], var_data['picked_4'], var_data['can_place_1'], \
    var_data['can_place_2'], var_data['can_place_3'], var_data['can_place_4'], var_data['placed_1'], \
    var_data['placed_2'], var_data['placed_3'], var_data['placed_4'] = (False,) * 16


def save_file_selected():
    var_data['save_file_1_selected'], var_data['save_file_2_selected'], var_data['save_file_3_selected'] = (False,) * 3


def save_load():  # Writing into notepad save files
    if var_data['saving_process']:
        for i in range(1, 4):
            if var_data['save_file_' + str(i) + '_selected']:
                f = open(globals()['save_' + str(i)], "w")
                f.write(
                    str(var_data['age']) + ',' + str(var_data['gender']) + ',' + str(var_data['religion']) + ',' + str(
                        var_data['ethnicity']) + ',' + str(var_data['hobby']) + ',' + str(var_data['job']) + ',' + str(
                        var_data['physical']) + ',' + str(var_data['mental']) + ',' + str(
                        var_data['social']) + ',' + str(var_data['financial']) + ',' + str(var_data['ethnicity_number']))
                f.close()
    elif var_data['loading_process']:
        load_list = ['age', 'gender', 'religion', 'ethnicity', 'hobby', 'job', 'physical', 'mental', 'social', 'financial', 'ethnicity_number']
        for i in range(1, 4):
            if var_data['save_file_' + str(i) + '_selected']:
                with open(globals()['save_' + str(i)]) as notepad:
                    lines = notepad.read().splitlines()
                    for item in lines:
                        data_set = item.split(",")
                        for num in range(0, 11):
                            if num == 0 or num == 1 or num >= 6:
                                var_data[load_list[num]] = int(data_set[num])
                            else:
                                var_data[load_list[num]] = data_set[num]


def back():
    if var_data['saving_process']:
        var_data['saving_process'], var_data['save_file_1_selected'], var_data['save_file_2_selected'], var_data['save_file_3_selected'] = (False,) * 4


def events():  # Function for updating the screen
    global mouse_x, mouse_y
    for event in pygame.event.get():
        mouse_x, mouse_y = pygame.mouse.get_pos()

        with open(hover_list) as notepad:
            help_lines = 0
            lines = notepad.read().splitlines()
            for num, item in enumerate(lines):
                if num >= 3:  # The first 2 lines are to assist users
                    data_set = item.split(",")
                    if var_data['game_page'] == data_set[0] and int(data_set[2]) <= mouse_x <= int(data_set[3]) and int(
                            data_set[4]) <= mouse_y <= int(data_set[5]) and int(data_set[2]) != 0 and int(
                            data_set[3]) != 0 and int(data_set[4]) != 0 and int(data_set[5]) != 0:
                        var_data[data_set[1]] = True
                    else:
                        var_data[data_set[1]] = False

        if event.type == pygame.QUIT:
            pygame.quit(), sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            var_data['drag'] = True
            print(mouse_x, mouse_y)

            with open(image_list) as notepad:  # THIS IS WHERE I AM NOW --- Make code less messy and condense!
                lines = notepad.read().splitlines()
                for num, item in enumerate(lines):
                    reset_counter, reset_counter2 = (0,) * 2
                    game_page_img, manipulation_type, var_type, var_name1, function_name, changed_value = ("",) * 6
                    if num >= 3:  # The first 2 lines are to assist users
                        data_set = item.split(",")
                        for data in data_set:
                            reset_counter += 1
                            if var_data['game_page'] == data_set[0] and reset_counter > 9:  # Will Loop this section for controlling multiple variables
                                reset_counter2 += 1
                                if reset_counter2 == 1:
                                    manipulation_type = data
                                elif reset_counter2 == 2:
                                    if manipulation_type == "Variable":
                                        var_type = data
                                    elif manipulation_type == "Function":
                                        function_name = data
                                        if int(data_set[5]) <= mouse_x <= int(data_set[6]) and int(
                                                data_set[7]) <= mouse_y <= int(data_set[8]) and int(
                                                data_set[5]) != 0 and int(data_set[6]) != 0 and int(data_set[7]) != 0 and int(data_set[8]) != 0:
                                            func, reset_counter2 = globals()[function_name](), 0
                                elif reset_counter2 == 3 and manipulation_type == "Variable":
                                    var_name1 = data
                                elif reset_counter2 == 4 and manipulation_type == "Variable":
                                    if var_type == "String":
                                        changed_value = data
                                    elif var_type == "Integer":
                                        changed_value = int(data)
                                    elif var_type == "Boolean":
                                        changed_value = bool(data)
                                    if int(data_set[5]) <= mouse_x <= int(data_set[6]) and int(
                                            data_set[7]) <= mouse_y <= int(data_set[8]) and int(
                                            data_set[5]) != 0 and int(data_set[6]) != 0 and int(data_set[7]) != 0 and int(data_set[8]) != 0:
                                        var_data[var_name1], reset_counter2 = changed_value, 0
        elif event.type == pygame.MOUSEBUTTONUP:
            var_data['drag'] = False


def special_effects():
    #  PREFERABLY A VARIABLE THAT WORKS WHEN HOVERED OVER SOMETHING?
    #  I don't have to run the for loop unless something happens
    if var_data['save_file_1_selected'] and var_data['game_page'] == "Menu2":
        display.blit(img_data['s_effect_1'], (400, 261))
    elif var_data['save_file_2_selected'] and var_data['game_page'] == "Menu2":
        display.blit(img_data['s_effect_1'], (400, 371))
    elif var_data['save_file_3_selected'] and var_data['game_page'] == "Menu2":
        display.blit(img_data['s_effect_1'], (400, 480))
    elif var_data['first_theme'] and var_data['game_page'] == "Menu3":
        display.blit(img_data['s_effect_1'], (400, 261))
    elif not var_data['first_theme'] and var_data['game_page'] == "Menu3":
        display.blit(img_data['s_effect_1'], (400, 371))
    elif var_data['music_is_on'] and var_data['game_page'] == "Menu4":
        display.blit(img_data['s_effect_1'], (400, 261))
    elif not var_data['music_is_on'] and var_data['game_page'] == "Menu4":
        display.blit(img_data['s_effect_1'], (400, 371))
    elif var_data['save_file_1_selected'] and var_data['game_page'] == "Game1" and var_data['saving_process']:
        display.blit(img_data['s_effect_1'], (400, 52))
    elif var_data['save_file_2_selected'] and var_data['game_page'] == "Game1" and var_data['saving_process']:
        display.blit(img_data['s_effect_1'], (400, 162))
    elif var_data['save_file_3_selected'] and var_data['game_page'] == "Game1" and var_data['saving_process']:
        display.blit(img_data['s_effect_1'], (400, 272))

    for i in var_data:  # This is for the hover effects of various buttons throughout the game.
        if "hover_" in i and var_data[i] and "effect_" + i[6] in img_data and len(i) <= 7:
            var_data['hover_type'] = "single"
        elif "hover_" in i and var_data[i] and "effect_" + i[6] in img_data and len(i) <= 8:
            var_data['hover_type'] = "double"
        elif "hover_" in i and var_data[i] and "effect_" + i[6] in img_data and len(i) <= 9:
            if var_data['saving_process'] or var_data['game_page'] == "Game2":
                var_data['hover_type'] = "triple"
        else:
            var_data['hover_type'] = ""

        if var_data['hover_type'] == "triple" or var_data['hover_type'] == "double" or var_data['hover_type'] == "single":
            for j in effect_positions:
                data = j.split(',')
                if i in data and var_data['hover_type'] == "single" and var_data['test_mode'] != 1:
                    display.blit(img_data["effect_" + data[0][6]], (int(data[1]), int(data[2])))
                elif i in data and var_data['hover_type'] == "double" and not var_data['saving_process'] and var_data['test_mode'] != 1:
                    display.blit(img_data["effect_" + data[0][6] + data[0][6]], (int(data[1]), int(data[2])))
                elif i in data and var_data['hover_type'] == "triple":
                    display.blit(img_data["effect_" + data[0][6] + data[0][6] + data[0][6]], (int(data[1]), int(data[2])))

    #  I don't have to run the for loop unless something happens
    for i in var_data:  # This is the tool tip code for various instances. There are many if statements because some buttons overlap and others cause the tip to go off-screen. Need to account for these circumstances.
        if "tip_" in i and var_data[i] and "tip" + i[4] + "_img" in img_data and not var_data['tip_5'] and not var_data['saving_process'] and not var_data['tip_9'] and len(i) <= 5 and var_data['test_mode'] != 1:
            display.blit(img_data["tip" + i[4] + "_img"], (mouse_x + 3, mouse_y - 63)), display.blit(img_data["tip" + i[4] + "_img"], (mouse_x + 3, mouse_y - 63))
        elif "tip_" in i and var_data[i] and "tip" + i[4] + "_img" in img_data and not var_data['tip_5'] and not var_data['saving_process'] and var_data['tip_9'] and var_data['tip_6'] and var_data['test_mode'] != 1:
            display.blit(img_data["tip6_img"], (mouse_x + 3, mouse_y - 63))
        elif "tip_" in i and var_data[i] and "tip" + i[4] + "_img" in img_data and var_data['tip_5'] and not var_data['menu_message'] and not var_data['saving_process'] and var_data['test_mode'] == 1:
            display.blit(img_data["tip8_img"], (mouse_x + 3, mouse_y - 63))
        elif "tip_" in i and var_data[i] and "tip" + i[4] + "_img" in img_data and var_data['tip_5'] and not var_data['menu_message'] and not var_data['saving_process']:
            display.blit(img_data["tip5_img"], (mouse_x + 3, mouse_y - 63))
        elif "tip_" in i and var_data[i] and "tip" + i[4] + "_img" in img_data and var_data['tip_5'] and var_data['menu_message']:
            display.blit(img_data["tip8_img"], (mouse_x + 3, mouse_y - 63))
        elif "tip_" in i and var_data[i] and "tip" + i[4] + "_img" in img_data and var_data['saving_process'] and var_data['tip_9']:
            for j in range(1, 4):
                if var_data['save_file_' + str(j) + '_selected'] and os.stat(save_dir + "Save_File_" + str(j) + ".txt").st_size == 0:
                    display.blit(img_data["tip9_img"], (mouse_x + 3, mouse_y - 63))
                elif var_data['save_file_' + str(j) + '_selected'] and os.stat(save_dir + "Save_File_" + str(j) + ".txt").st_size != 0:
                    display.blit(img_data["tip10_img"], (mouse_x + 3, mouse_y - 63))
        elif "tip_" in i and var_data[i] and "tip" + i[4] + i[4] + "_img" in img_data and not var_data['tip_5'] and not var_data['saving_process'] and not var_data['tip_9'] and len(i) <= 6:
            display.blit(img_data["tip" + i[4] + i[4] + "_img"], (mouse_x + 3, mouse_y - 63)), display.blit(img_data["tip" + i[4] + i[4] + "_img"], (mouse_x + 3, mouse_y - 63))
        elif "tip_" in i and var_data[i] and "tip" + i[4] + i[4] + i[4] + "_img" in img_data and not var_data['tip_5'] and not var_data['saving_process'] and not var_data['tip_9'] and var_data['test_mode'] != 1:
            display.blit(img_data["tip" + i[4] + i[4] + i[4] + "_img"], (mouse_x - 203, mouse_y - 63)), display.blit(img_data["tip" + i[4] + i[4] + i[4] + "_img"], (mouse_x - 203, mouse_y - 63))

    if var_data['game_page'] == "Menu2":
        pos_list = [(400, 598), (261, 331, save_1), (371, 441, save_2), (481, 551, save_3)]
        for i in range(1,4):
            if 400 <= mouse_x <= 598 and pos_list[i][0] <= mouse_y <= pos_list[i][1]:
                if os.path.getsize(pos_list[i][2]) > 0:
                    display.blit(img_data["tip888_img"], (mouse_x + 3, mouse_y - 63))
                else:
                    display.blit(img_data["tip999_img"], (mouse_x + 3, mouse_y - 63))


def music_off():
    var_data['music_is_on'] = False
    pygame.mixer.music.stop()


def music_play():
    if var_data['music_is_on']:
        print(var_data['first_theme'], var_data['first_theme2'])
        if var_data['first_theme'] and var_data['first_theme2']:
            pygame.mixer.music.load(image_dir + "MorningMode.mp3")
            pygame.mixer.music.play(-1)
        elif var_data['first_theme'] and not var_data['first_theme2']:
            pygame.mixer.music.load(image_dir + "NightMode.mp3")
            pygame.mixer.music.play(-1)
        elif not var_data['first_theme'] and not var_data['first_theme2']:
            pygame.mixer.music.load(image_dir + "NightMode.mp3")
            pygame.mixer.music.play(-1)


def theme_2():
    if not var_data['game_page'] == "Game1":
        var_data['first_theme'], var_data['first_theme2'] = (False,) * 2
    if var_data['game_page'] == "Game1" and not var_data['sleeper']:
        var_data['sleeper'] = True
        t = threading.Thread(target=thread_function, args=(500, 'sleeperFunction', 'theme_changer', 0, 0, 0, 0))
        t.start()


def main_loop():
    music_play()
    while True:
        #print(var_data['first_theme'], var_data['first_theme2'])
        events()
        if var_data['first_theme'] and var_data['first_theme2']:
                var_data['display_theme'] = 1
        elif not var_data['first_theme2'] and var_data['first_theme']:
            var_data['display_theme'] = 2
            var_data['first_theme'] = False
        elif not var_data['first_theme'] or not var_data['first_theme2']:
            var_data['display_theme'] = 2

        rel_x2 = int(var_data['x_2']) % img_data['sky_' + str(var_data['display_theme'])].get_rect().width
        display.blit(img_data['sky_' + str(var_data['display_theme'])], (rel_x2 - img_data['sky_' + str(var_data['display_theme'])].get_rect().width, 0))
        if rel_x2 < width:
            display.blit(img_data['sky_' + str(var_data['display_theme'])], (rel_x2, 0))

        rel_x = int(var_data['x']) % img_data['background_' + str(var_data['display_theme'])].get_rect().width
        display.blit(img_data['background_' + str(var_data['display_theme'])], (rel_x - img_data['background_' + str(var_data['display_theme'])].get_rect().width, 0))
        if rel_x < width:
            display.blit(img_data['background_' + str(var_data['display_theme'])], (rel_x, 0))

        var_data['x'] -= 0.13
        var_data['x_2'] += 0.05
        menu_function(), special_effects()
        display.blit(img_data['cursor_1'], (mouse_x - 3, mouse_y - 3))

        pygame.display.update()
        clock.tick(FPS)


var_data['game_page'] = "Menu1"
main_loop()
