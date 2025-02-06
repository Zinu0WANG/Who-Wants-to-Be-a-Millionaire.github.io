import pygame as py
import os
import requests
import json
from dotenv import load_dotenv
import re
import random
import sys

black = py.Color(0, 0, 0)
red = py.Color(255, 0, 0)
white = py.Color(255,255,255)

class Maingame:
    '''The “Maingame” class is the main class for managing the game, including initializing the game,
handling the game state, and executing the game loop'''

    def __init__(self):
        '''Function: Initializes the game window, loads resources, creates game objects, and sets the initial state.'''
        self.money=['$2000','$5000','$10000','$20000','$50000','$100000','$200000','$500000','$1000000']
        self.HEIGHT = 700
        self.WIDTH = 1000
        self.window = py.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background_image = py.image.load('stage.png')
        self.background_image = py.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        self.PLAYER = Player(self.WIDTH, self.HEIGHT,self.window)
        self.Choice = Choice(self.WIDTH, self.HEIGHT,self.window,self.PLAYER)  
        self.Host = Host(self.WIDTH, self.HEIGHT,self.window)  
        self.countdown=CountdownTimer(60)
        self.music = Music()
        self.clock = py.time.Clock()
        self.current_question_index = 0
        self.total_questions = 9
        self.questions = [Question(self.WIDTH,self.HEIGHT,self.window,self.PLAYER) for _ in range(self.total_questions)]
        self.answers = []
        for i in range(self.total_questions):
            self.questions[i].get_question_from_AI()
            answer = Answer(self.questions[i], self.window)
            answer.fetch_answer()
            self.answers.append(answer)
        
        self.numbers = []  
        self.selected_option = ''  
        self.initialize_answers()
        self.Tool = Toolbox(self.WIDTH,self.HEIGHT,self.window,self.PLAYER,self.background_image,self.numbers,self.selected_option)
        self.GUI = py.image.load('GUI.jpg')
        self.GUI = py.transform.scale(self.GUI, (self.WIDTH, self.HEIGHT))

    def initialize_answers(self):
        if self.answers:
            self.correct_answer = self.answers[self.current_question_index].correct_option
            self.wrong_answer = [
                option for option in ['A', 'B', 'C', 'D']
                if option != self.correct_answer
            ]
        self.update_correct_wrong_numbers()

    def update_correct_wrong_numbers(self):
        if self.correct_answer == 'A':
            self.numbers = random.sample([1, 2, 3], 2)
            self.numbers.append(0)
            self.numbers = sorted(self.numbers)
        elif self.correct_answer == 'B':
            self.numbers = random.sample([0, 2, 3], 2)
            self.numbers.append(1)
            self.numbers = sorted(self.numbers)
        elif self.correct_answer == 'C':
            self.numbers = random.sample([0, 1, 3], 2)
            self.numbers.append(2)
            self.numbers = sorted(self.numbers)
        elif self.correct_answer == 'D':
            self.numbers = random.sample([0, 1, 2], 2)
            self.numbers.append(3)
            self.numbers = sorted(self.numbers)
        
        if self.numbers == [1, 2, 3]:
            self.selected_option = random.choices(['A', 'B', 'C', 'D'], [64, 12, 12, 12])[0]
        elif self.numbers == [0, 2, 3]:
            self.selected_option = random.choices(['A', 'B', 'C', 'D'], [12, 64, 12, 12])[0]
        elif self.numbers == [0, 1, 3]:
            self.selected_option = random.choices(['A', 'B', 'C', 'D'], [12, 12, 64, 12])[0]
        elif self.numbers == [0, 1, 2]:
            self.selected_option = random.choices(['A', 'B', 'C', 'D'], [12, 12, 12, 64])[0]
        
        
        
        
        
        
 
       
    def Gamestart(self):
        py.display.set_caption('WHO WANTS TO BE A MILLIONAIR')
        game_started = False  
        py.mixer.init()
        play = True
        self.question = self.questions[self.current_question_index]
        self.answer = self.answers[self.current_question_index]
        
        self.music.displaymusic1()
        
        while not game_started:
            
            self.window.blit(self.GUI, (0, 0))
            
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.endGame()
                elif event.type == py.KEYDOWN and event.key == py.K_RETURN: 
                    game_started = True  
            py.display.flip()
            self.clock.tick(60)

        self.music.displaymusic2()

        while play:
            self.window.blit(self.background_image, (0, 0))
            self.Host.displayhost()
            font = py.font.Font(None, 32)
            text_line1 = "Welcome to WHO WANTS TO BE A MILLIONAIRE"
            text_line2 = "In today's game, players can win millions of dollars by answering 12 questions correctly"
            text_line3='Let\'s welcome the first player'
            text_surface1 = font.render(text_line1, True, (255, 255, 255))
            text_rect1 = text_surface1.get_rect(center=(500,100))
            self.window.blit(text_surface1, text_rect1)

            
            text_surface2 = font.render(text_line2, True, (255, 255, 255))
            text_rect2 = text_surface2.get_rect(center=(500,150))
            self.window.blit(text_surface2, text_rect2)
            text_surface3 = font.render(text_line3, True, (255, 255, 255))
            text_rect3 = text_surface3.get_rect(center=(500,200))
            self.window.blit(text_surface3, text_rect3)
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.endGame()
                elif event.type == py.KEYDOWN and event.key == py.K_RETURN: 
                    play= False 
                    

            py.display.flip()
            self.clock.tick(60)
        self.Continuegame()
            
        
    def Continuegame(self):
        '''Function: Continues the game and starts the Q&A session for the current question.'''
        while True:
            self.question = self.questions[self.current_question_index]
            self.answer = self.answers[self.current_question_index]
            self.initialize_answers()
            self.getEvent()
            self.window.blit(self.background_image, (0, 0))
            self.question.display_question()
            self.PLAYER.displayPlayer()
            self.Choice.displaychoice()
            self.Host.displayhost()
            self.choice=self.Choice.remove_rect() 
            self.countdown.render(self.window,(0,0))
            self.countdown.update()
            if self.countdown.is_finished():                
                self.Wrong()
            if self.choice == 'T':      
                self.Tool.displaytoolbox()
                self.choice2 = self.Tool.Choosetool()
                if self.choice2 == self.correct_answer:
                    self.Correct()
                elif self.choice2 in self.wrong_answer:
                    self.Wrong()    
            elif self.choice == self.correct_answer:
                self.Correct()
            elif self.choice in self.wrong_answer:
                self.Wrong()
            if self.PLAYER and not self.PLAYER.stop:
                self.PLAYER.move()
            py.display.flip()
            self.clock.tick(60)  

          
    def getEvent(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.endGame()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_LEFT:
                    self.PLAYER.direction = 'L'
                    self.PLAYER.stop = False
                elif event.key == py.K_RIGHT:
                    self.PLAYER.direction = 'R'
                    self.PLAYER.stop = False
                elif event.key == py.K_UP:
                    self.PLAYER.direction = 'U'
                    self.PLAYER.stop = False
                elif event.key == py.K_DOWN:
                    self.PLAYER.direction = 'D'
                    self.PLAYER.stop = False  
            elif event.type == py.KEYUP:
                self.PLAYER.stop = True

    def Correct(self):
        '''Function: Handles the scenario where the correct answer is given.'''
        correct = True
        choice = None
        if self.current_question_index ==8:
            self.window.blit(self.background_image, (0, 0))
            end = True
            while end:
                biggest_prize=Prize(self.window, self.money, self.current_question_index,self.current_question_index)
                end= biggest_prize.winner()
            self.new_game_reset()
            self.Gamestart()
            
        while correct:
            self.window.blit(self.background_image, (0, 0))
            font = py.font.Font(None, 32)
            text_line1="Your answer is correct"            
            text_line2=f"You already won {self.money[self.current_question_index]}, do you want to continue to win more?"
            text_line3="Press esc to leave with money. Press enter to continue."

            text_surface1 = font.render(text_line1, True, (255, 255, 255))
            text_rect1 = text_surface1.get_rect(center=(500,100))
            self.window.blit(text_surface1, text_rect1)
            
            text_surface2 = font.render(text_line2, True, (255, 255, 255))
            text_rect2 = text_surface2.get_rect(center=(500,150))
            self.window.blit(text_surface2, text_rect2)
            
            
            text_surface3 = font.render(text_line3, True, (255, 255, 255))
            text_rect3 = text_surface3.get_rect(center=(500,200))
            self.window.blit(text_surface3, text_rect3)
            
            py.display.flip()
            
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.endGame()
                elif event.type == py.KEYDOWN and event.key == py.K_RETURN:                    
                    choice = 1                  
                    correct = False              
                elif event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                    self.window.blit(self.background_image, (0, 0))
                    correct = False
                    choice = 2
       
        if choice == 1:
            self.current_question_index += 1
            self.new_game_reset()
            self.Continuegame()
        elif choice == 2:
            prize = Prize(self.window, self.money, self.current_question_index, self.current_question_index)
            end = True
            while end:
                end = prize.displayprize()
            self.reset_game_state()
            self.Gamestart()
        

    def Wrong(self):
        '''Function: Handles the scenario where the wrong answer is given.'''
        wrong = True
        while wrong:
            self.window.blit(self.background_image, (0, 0))
            text_line1 = "Sorry, you lose"
            text_line2 = "Press enter to restart"
            font = py.font.Font(None, 32)
            text_surface1 = font.render(text_line1, True, (255, 255, 255))
            text_rect1 = text_surface1.get_rect(center=(500,100))
            self.window.blit(text_surface1, text_rect1)

            text_surface2 = font.render(text_line2, True, (255, 255, 255))
            text_rect2 = text_surface2.get_rect(center=(500,150))
            self.window.blit(text_surface2, text_rect2)

            py.display.flip()

            for event in py.event.get():
                if event.type == py.QUIT:
                    wrong=False
                    self.endGame()
                elif event.type == py.KEYDOWN and event.key == py.K_RETURN: 
                    wrong = False
                    self.reset_game_state()
                    self.Gamestart()  
        
    
    def reset_game_state(self):
        self.current_question_index = 0
        self.money = ['$2000','$5000','$10000','$20000','$50000','$100000','$200000','$500000','$1000000']
        self.PLAYER = Player(self.WIDTH, self.HEIGHT, self.window)
        self.Choice = Choice(self.WIDTH, self.HEIGHT, self.window, self.PLAYER)
        self.Host = Host(self.WIDTH, self.HEIGHT, self.window)
        self.questions = [Question(self.WIDTH, self.HEIGHT, self.window, self.PLAYER) for _ in range(self.total_questions)]
        self.answers = []
        for i in range(self.total_questions):
            self.questions[i].get_question_from_AI()
            answer = Answer(self.questions[i], self.window)
            answer.fetch_answer()
            self.answers.append(answer)
        self.numbers = []
        self.Tool = Toolbox(self.WIDTH,self.HEIGHT,self.window,self.PLAYER,self.background_image,self.numbers,self.selected_option)
        self.selected_option = ''
        self.countdown = CountdownTimer(60)
        self.initialize_answers()

    def new_game_reset(self):
        self.PLAYER = Player(self.WIDTH, self.HEIGHT, self.window)
        self.Choice = Choice(self.WIDTH, self.HEIGHT, self.window, self.PLAYER)
        self.Host = Host(self.WIDTH, self.HEIGHT, self.window)
        self.numbers = random.sample(range(4), 3)
        self.countdown = CountdownTimer(60)
        self.Tool = Toolbox(self.WIDTH,self.HEIGHT,self.window,self.PLAYER,self.background_image,self.numbers,self.selected_option)
        self.choice = None
        self.choice2 = None
        self.initialize_answers()                
    
    def endGame(self):
        py.quit()
        sys.exit()
            


class Player(Maingame):
    '''The Player class manages player-related logic, including displaying and moving the player.'''
    def __init__(self, width, height,window):
        self.images = {
            'U': py.image.load('U.png'),
            'D': py.image.load('D.png'),
            'L': py.image.load('L.png'),
            'R': py.image.load('R.png')
        }
        self.direction = 'U'
        self.WIDTH=width
        self.HEIGHT= height
        for item in self.images.items():
           
            self.images[item[0]]= py.transform.scale(item[1], (60,60))
        self.rect = self.images[self.direction].get_rect()
        self.rect.centerx = self.WIDTH // 2
        self.rect.centery = self.HEIGHT // 2+10
        self.speed = 8
        self.stop = True
        self.reached_destination = False
        self.window = window

    def move(self):
        '''Function: Moves the player based on the current direction.'''
        if self.direction == 'L':
            if self.rect.left > 200:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < 800:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top  >300:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < 450:
                self.rect.top += self.speed
        
    def displayPlayer(self):
        self.image = self.images[self.direction].convert_alpha()
        self.window.blit(self.image, self.rect)
        
class Question:
    '''Represents a single trivia question in the game.'''
    def __init__(self,width,height,window,player):
        self.HEIGHT = height
        self.WIDTH = width
        self.window = window
        self.PLAYER = player
        self.question_text = ""
        self.choices = []  
    
    def get_question_from_AI(self):
        '''Function: Fetches a question from OpenAI.'''
        load_dotenv()
        URL = (
            "https://cuhk-api-dev1-apim1.azure-api.net/openai/"
            "deployments/gpt-35-turbo/chat/completions?api-version=2023-05-15"
        )
        payload = json.dumps({
            "model": "gpt-35-turbo",
            "messages": [{"role": "user", "content": "Give me a MC question with 4 choices."}]
        })
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': os.getenv("APIM_SUBSCRIPTION_KEY")
        }
        response = requests.request("POST", URL, headers=headers, data=payload)
        data = response.json()
        self.question_text = data['choices'][0]['message']['content']
        self.process_question_text()

    def process_question_text(self):
        lines = self.question_text.split('\n')
        self.question_text = lines[0]
        self.choices = lines[1:]
    def display_question(self):
        py.font.init()
        font = py.font.Font(None, 28) 
    
        x, y = 170,70

        self.render_text(self.window, self.question_text, (x, y), font, white, max_width=700)
        y += font.size(self.question_text)[1] + 20  
    
        for choice in self.choices:
            self.render_text(self.window, choice, (x, y), font, white, max_width=700)
            y += font.size(choice)[1] + 30  
    
    


    def render_text(self, surface, text, pos, font, color=(255,255,255), max_width=None):
        words = [word.split(' ') for word in text.splitlines()]  
        space = font.size(' ')[0]  
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  
                    y += word_height 
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  
            y += word_height  

class Answer:
    '''Handles fetching and displaying the correct answer to a question.'''
    def __init__(self, question, window):
        self.question = question
        self.window = window
        self.answer_text = ''
        self.correct_option = ''

    def fetch_answer(self):
        '''Function: Fetches the answer to the question from OpenAI.'''
        choice_text = "\n".join(self.question.choices) 
        complete_question = self.question.question_text + "\n" + choice_text
        answer_url = "https://cuhk-api-dev1-apim1.azure-api.net/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-05-15"
        answer_payload = {
            "model": "gpt-35-turbo",
            "messages": [{"role": "user", "content": "Give me only the answer to the MC question: " + complete_question }]
        }
        answer_headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': os.getenv("APIM_SUBSCRIPTION_KEY")
        }
        answer_response = requests.post(answer_url, headers=answer_headers, data=json.dumps(answer_payload))
        answer_data = answer_response.json()
        self.answer_text = answer_data['choices'][0]['message']['content']
        if ":" in self.answer_text:
            self.correct_option = self.answer_text.split(':')[0].strip()
            self.correct_option=self.correct_option.upper()
        else:
            self.correct_option = self.answer_text.strip().split(')')[0].strip()
            self.correct_option=self.correct_option.upper()

    def display_answer(self):
        font = py.font.Font(None, 32)
        text_surface = font.render(self.answer_text, True, py.Color('white'))
        text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() - 50))
        self.window.blit(text_surface, text_rect) 
    
    def display_answer(self):
        self.fetch_answer()
        font = py.font.Font(None, 32)
        text_surface = font.render(self.answer_text, True, py.Color('white'))
        text_rect = text_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() - 50))
        self.window.blit(text_surface, text_rect)



class Choice():
    '''Manages the display of answer choices for the player to select from.'''
    def __init__(self, width, height, window, player):
        '''Function: Initializes the choice.'''
        self.PLAYER = player
        py.font.init()
        self.window = window
        self.WIDTH = width
        self.HEIGHT = height
        self.rects = [
            py.Rect(self.WIDTH // 4 + 10, self.HEIGHT // 4 + 160, 50, 50),
            py.Rect(self.WIDTH // 4 + 10, self.HEIGHT * 3 // 4 - 110, 50, 50),
            py.Rect(self.WIDTH * 3 // 4 - 30, self.HEIGHT // 4 + 160, 50, 50),
            py.Rect(self.WIDTH * 3 // 4 - 30, self.HEIGHT * 3 // 4 - 110, 50, 50),
            py.Rect(self.WIDTH // 2-20,self.HEIGHT * 3 // 4 - 100 , 50, 50)
        ]
        self.texts = [
            'A', 'B', 'C', 'D', 'T'
        ]
        self.font = py.font.Font(None, 36)
        
        self.showtoolbox = False
        self.choice_touched = False  
        self.re = None

    def displaychoice(self):
        for i in range(len(self.texts)):
            if not self.showtoolbox or self.texts[i] == 'T':
                py.draw.rect(self.window, white, self.rects[i], 2)

        text_surfaces = []
        text_rects = []
        for i in range(len(self.texts)):
            if not self.showtoolbox or self.texts[i] == 'T':
                text_surface = self.font.render(self.texts[i], True, white)
                text_surfaces.append(text_surface)
                text_rect = text_surface.get_rect(center=self.rects[i].center)
                text_rects.append(text_rect)

        for i in range(len(self.texts)):
            if not self.showtoolbox or self.texts[i] == 'T':
                self.window.blit(text_surfaces[i], text_rects[i])

    def remove_rect(self):
        '''Function: Checks the answer options selected by the player.'''
        for i in range(len(self.texts)):
            if self.rects[i].colliderect(self.PLAYER.rect):
                if self.texts[i] == 'T':
                    if not self.choice_touched:
                        self.showtoolbox = True
                        self.choice_touched = True  
                        for j in range(len(self.texts)):
                            self.rects[j] = py.Rect(0, 0, 0, 0)
                            self.texts[j] = ''
                        self.re = 'T'
                elif self.texts[i] ==  'A':
                    self.re = 'A'
                elif self.texts[i] == 'B':
                    self.re= 'B'
                elif self.texts[i] == 'C':
                    self.re =  'C'
                elif self.texts[i]== 'D':
                    self.re = 'D'
        return self.re
                
class Host():
    '''Represents the game host who assists the player during the game.'''
    def __init__(self,width,height,window):
        self.window=window
        self.WIDTH=width
        self.HEIGHT=height
        self.image = py.image.load('host.png')
        self.image = py.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.WIDTH // 2
        self.rect.centery = self.HEIGHT // 2-70
    def displayhost(self):
        self.window.blit(self.image, self.rect)

class CountdownTimer(Maingame):
    '''Manages the countdown timer during gameplay.'''
    def __init__(self, duration):
        self.duration = duration  
        self.remaining_time = duration 
        self.font = py.font.Font(None, 36)  

    def update(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1/60
        else :
            self.remaining = 0

    def is_finished(self):
        if self.remaining_time <= 0:
            return True
        else:
            return False
    def render(self, surface, position):
        
        text_surface = self.font.render("Countdown: {:.0f}".format(self.remaining_time), True, black)
        surface.blit(text_surface, (0,0))

class Toolbox():
    '''Manages the display and functionality of tools the player can use during the game.'''
    def __init__(self,width,height,window,player,image,numbers,selected_option):
        self.numbers=numbers
        self.touch1=False
        self.touch2=False
        self.font = py.font.Font(None, 36)
        self.line1 = self.font.render("You have two tools", True, (255, 255, 255))
        self.line2 = self.font.render("A is to delete an incorrect answer", True, (255, 255, 255))
        self.line3 = self.font.render("B is to ask the audience but their answer may not be correct", True, (255, 255, 255))
        self.background_image=image
        self.PLAYER=player
        self.WIDTH=width
        self.HEIGHT = height
        self.window = window
        self.rect = [
            py.Rect(self.WIDTH // 2 - 100, self.HEIGHT * 3 // 4-100 , 50, 50),
            py.Rect(self.WIDTH // 2 +100, self.HEIGHT * 3 // 4 - 100, 50, 50)            
            
        ]
        self.rects= None
        self.texts = [
            'A', 'B'
        ]
        self.selected_option = selected_option
        
    def displaytoolbox(self):
        text_rect1 = self.line1.get_rect()
        text_rect2 = self.line2.get_rect()
        text_rect3 = self.line3.get_rect()

        text_rect1.centerx = self.window.get_width() // 2
        text_rect1.bottom = self.window.get_height() - 85
        text_rect2.centerx = self.window.get_width() // 2
        text_rect2.bottom = self.window.get_height() - 55
        text_rect3.centerx = self.window.get_width() // 2
        text_rect3.bottom = self.window.get_height() - 25

        self.window.blit(self.line1, text_rect1)
        self.window.blit(self.line2, text_rect2)
        self.window.blit(self.line3, text_rect3)

        for i in range(len(self.texts)):
            py.draw.rect(self.window, white, self.rect[i], 2)

        text_surfaces = []
        text_rects = []
        for i in range(len(self.texts)):
            text_surface = self.font.render(self.texts[i], True, white)
            text_surfaces.append(text_surface)
            text_rect = text_surface.get_rect(center=self.rect[i].center)
            text_rects.append(text_rect)

        for i in range(len(self.texts)):
            self.window.blit(text_surfaces[i], text_rects[i])
    
    
            
        
    

    def Choosetool(self):
        '''Function: handles the player's interaction with the toolbox.'''
        if self.rect[0].colliderect(self.PLAYER.rect):
            self.rect[0]=py.Rect(0,0,0,0)
            self.rect[1]=py.Rect(0,0,0,0)
            self.texts[0]=''
            self.texts[1]=''
            self.line1 = self.font.render("", True, (255, 255, 255))
            self.line2 = self.font.render("", True, (255, 255, 255))
            self.line3 = self.font.render("", True, (255, 255, 255))
            self.touch1 =True
            
        if  self.touch1:        
            return self.ToolA()
        
        if self.rect[1].colliderect(self.PLAYER.rect):
            self.line1 = self.font.render("Choose one person to ask, but the answer may not be correct", True, (255, 255, 255))
            self.line2 = self.font.render("", True, (255, 255, 255))
            self.line3 = self.font.render("", True, (255, 255, 255))
            self.rect[0]=py.Rect(0,0,0,0)
            self.rect[1]=py.Rect(0,0,0,0)
            self.texts[0]=''
            self.texts[1]=''
            self.touch2 = True

        if self.touch2:
            return self.ToolB()

    def ToolA(self):
        options = ['A', 'B', 'C', 'D']
        

        self.rects = [
            py.Rect(self.WIDTH // 4 + 10, self.HEIGHT // 4 + 160, 50, 50),
            py.Rect(self.WIDTH // 4 + 10, self.HEIGHT * 3 // 4 - 110, 50, 50),
            py.Rect(self.WIDTH * 3 // 4 - 30, self.HEIGHT // 4 + 160, 50, 50),
            py.Rect(self.WIDTH * 3 // 4 - 30, self.HEIGHT * 3 // 4 - 110, 50, 50)
        ]

        for i in self.numbers:
            py.draw.rect(self.window, white, self.rects[i],2)
            text = self.font.render(options[i], True, white)
            text_rect = text.get_rect(center=self.rects[i].center)
            self.window.blit(text, text_rect)

        py.display.flip()

        for i in self.numbers:
            if self.rects[i].colliderect(self.PLAYER.rect):
                return options[i]
    def ToolB(self):
        
        self.line1 = self.font.render(f"An audience member said choose {self.selected_option}", True, (255, 255, 255))
        options = ['A', 'B', 'C', 'D']
        self.rects = [
          py.Rect(self.WIDTH // 4 + 10, self.HEIGHT // 4 + 160, 50, 50),
            py.Rect(self.WIDTH // 4 + 10, self.HEIGHT * 3 // 4 - 110, 50, 50),
            py.Rect(self.WIDTH * 3 // 4 - 30, self.HEIGHT // 4 + 160, 50, 50),
            py.Rect(self.WIDTH * 3 // 4 - 30, self.HEIGHT * 3 // 4 - 110, 50, 50)
        ]

        for i in range(4):
            py.draw.rect(self.window, white, self.rects[i],2)
            text = self.font.render(options[i], True, white)
            text_rect = text.get_rect(center=self.rects[i].center)
            self.window.blit(text, text_rect)
        py.display.flip()
        
        for i in range(4):
            if self.rects[i].colliderect(self.PLAYER.rect):
                return options[i]


        

    

            
class Music():
    '''Handles playing and pausing background music during different phases of the game.'''
    def __init__(self):
        pass

    def displaymusic1(self):
        py.mixer.music.load("GUI MUSIC.wav")

        py.mixer.music.set_volume(0.4)

        py.mixer.music.play(loops=-1)

    def displaymusic2(self):
        py.mixer.music.pause()
        py.mixer.music.load('GUI MUSIC2.wav')
        py.mixer.music.set_volume(0.6)
        py.mixer.music.play(loops=-1)

class Prize():
    '''Manages the display of messages when the player wins or completes the game.'''
    def __init__(self,window,prize,count,current_question_index):
        self.window = window
        self.prize = prize
        self.count =count
        self.current_question_index =current_question_index

    def displayprize(self):
        '''Function: displays a message to the player when they win a prize at a certain question level.'''
        text1=f'Congratulations! You win {self.prize[self.current_question_index]}'
        text2='Thank you for playing our game'
        text3='Press enter to play angin'
        font = py.font.Font(None, 32)
        text_surface1 = font.render(text1, True, (255, 255, 255))
        text_rect1 = text_surface1.get_rect(center=(500,100))
        self.window.blit(text_surface1, text_rect1)
        text_surface2 = font.render(text2, True, (255, 255, 255))
        text_rect2 = text_surface1.get_rect(center=(500,150))
        self.window.blit(text_surface2, text_rect2)
        text_surface3 = font.render(text3, True, (255, 255, 255))
        text_rect3 = text_surface3.get_rect(center=(500,200))
        self.window.blit(text_surface3, text_rect3)
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                    py,quit
                    sys.exit
            elif event.type == py.KEYDOWN and event.key == py.K_RETURN: 
                    return False
        return True

    def winner(self):
        text1='Congratulations! You answered all the questions'
        text2='Now, you become a millioniar!'
        text3='Thank you for playing our game'
        text4='Press enter to play angin'
        font = py.font.Font(None, 32)
        text_surface1 = font.render(text1, True, (255, 255, 255))
        text_rect1 = text_surface1.get_rect(center=(500,100))
        self.window.blit(text_surface1, text_rect1)
        text_surface2 = font.render(text2, True, (255, 255, 255))
        text_rect2 = text_surface1.get_rect(center=(500,150))
        self.window.blit(text_surface2, text_rect2)
        text_surface3 = font.render(text3, True, (255, 255, 255))
        text_rect3 = text_surface3.get_rect(center=(500,200))
        self.window.blit(text_surface3, text_rect3)
        text_surface4 = font.render(text4, True, (255, 255, 255))
        text_rect4 = text_surface4.get_rect(center=(500,250))
        self.window.blit(text_surface4, text_rect4)
        py.display.flip()

        for event in py.event.get():
            if event.type == py.QUIT:
                    py,quit
                    sys.exit
            elif event.type == py.KEYDOWN and event.key == py.K_RETURN: 
                    return False
        return True
    

game = Maingame()
game.Gamestart()
