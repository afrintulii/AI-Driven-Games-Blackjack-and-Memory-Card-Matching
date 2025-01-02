# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 18:59:37 2024

@author: Hp
"""

# black jack in python wth pygame!
import copy
import random
import pygame
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from button import Button
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

pygame.init()
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

values= {
  "2": 2,
  "3": 3,
  "4": 4,
  "5": 5,
  "6": 6,
  "7": 7,
  "8": 8,
  "9": 9,
  "10": 10,
  "A": 11,
  "J": 10,
  "K": 10,
  "Q": 10,

}


one_deck = 4 * cards
decks = 4
WIDTH = 1500
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT],pygame.FULLSCREEN)
bg_img = pygame.image.load('bg.jpg')
bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
bg_img2 = pygame.image.load('front.jpg')
bg_img2 = pygame.transform.scale(bg_img2,(WIDTH,HEIGHT))
bg_img1= pygame.image.load('bg.jpg')
bg_img1= pygame.transform.scale(bg_img1,(WIDTH,HEIGHT-100))

runing = True


pygame.display.set_caption('Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 25)
smaller_font = pygame.font.Font('freesansbold.ttf', 20)
active = 2 
# win, loss, draw,AI
records = [0, 0, 0, 0]
score_board = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
AI_hand = []
AI_score = 0
dealer_hand = []
outcome = 0
game_deck = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
s_board = [0,0,0]
results = ['', 'PLAYER BUSTED o_O and Dealer and AI wins ^_^', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...','AI_WINS! ^_^','AI and Dealer Tie','AI and Player Tie','Dealer and Player Tie']


# dealing cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# drawing scores for player and dealer on screen

def draw_scores(player, dealer,ai):
    screen.blit(font.render(f'Player_Point[{player}]', True, 'white'), (550, 400))
    screen.blit(font.render(f'AI_Point[{ai}]', True, 'white'), (1050, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer_Point[{dealer}]', True, 'white'), (250, 400))
       


# drawing cards visually onto screen
def draw_cards(player, dealer, reveal,AI):
    
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [500 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (505 + 70 * i, 165 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (505 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'red', [500 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
        
    for i in range(len(AI)):
        pygame.draw.rect(screen, 'white', [1000 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(AI[i], True, 'black'), (1005 + 70 * i, 165 + 5 * i))
        screen.blit(font.render(AI[i], True, 'black'), (1005+ 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'yellow', [1000 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
        

    # dealer hide one card as reavel dealer is false
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# Score is calculated
def calculate_score(hand):
 
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
 
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
       
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        
        elif hand[i] == 'A':
            hand_score += 11
    
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score
# Heuristic approach
def AI_cards(hand, current_deck, dealer_hand, reveal_dealer):
    value = calculate_score(hand)
    dealer_value = calculate_score(dealer_hand if reveal_dealer else dealer_hand[1:])
    
   
    if value >= 17:
        return hand, current_deck

    need = 21 - value
    more = 0
    less = 0
    card_A = 0
    total_card = len(current_deck)

    for i in range(total_card):
        if current_deck[i] == "A":
            card_A += 1
        if values[current_deck[i]] <= need:
            less += 1
        else:
            more += 1

    prob_higher = float(more / total_card * 1.0)
    prob_lower = float(less / total_card * 1.0)
    risk = float(card_A / total_card * 1.0)

   
    if value < 12:
        
        hand, current_deck = deal_cards(hand, current_deck)
    elif value >= 12 and value < 17:
        if (prob_lower + (2 * risk)) >= prob_higher or prob_higher - prob_lower < 0.001:
            hand, current_deck = deal_cards(hand, current_deck)
    else:
        if dealer_value >= 7 and value < 17:
            hand, current_deck = deal_cards(hand, current_deck)
        else:
            
            return hand, current_deck

    return hand, current_deck

def AI_cards_fuzzy(hand, current_deck, dealer_hand, reveal_dealer):
    ai_score = calculate_score(hand)
    dealer_score = calculate_score(dealer_hand if reveal_dealer else dealer_hand[1:])
    
    print(f"AI Score: {ai_score}, Dealer Score: {dealer_score}")

    ai_score_lv = ctrl.Antecedent(np.arange(0, 32, 1), 'ai_score')
    dealer_score_lv = ctrl.Antecedent(np.arange(0, 32, 1), 'dealer_score')
    decision = ctrl.Consequent(np.arange(0, 2, 1), 'decision')
    
    
    ai_score_lv['very_low'] = fuzz.trapmf(ai_score_lv.universe, [0, 0, 5, 10])
    ai_score_lv['low'] = fuzz.trimf(ai_score_lv.universe, [5, 10, 15])
    ai_score_lv['medium'] = fuzz.trimf(ai_score_lv.universe, [10, 15, 18])
    ai_score_lv['high'] = fuzz.trimf(ai_score_lv.universe, [15, 18, 21])
    ai_score_lv['very_high'] = fuzz.trapmf(ai_score_lv.universe, [18, 21, 32, 32])
    
    dealer_score_lv['very_low'] = fuzz.trapmf(dealer_score_lv.universe, [0, 0, 5, 10])
    dealer_score_lv['low'] = fuzz.trimf(dealer_score_lv.universe, [5, 10, 15])
    dealer_score_lv['medium'] = fuzz.trimf(dealer_score_lv.universe, [10, 15, 18])
    dealer_score_lv['high'] = fuzz.trimf(dealer_score_lv.universe, [15, 18, 21])
    dealer_score_lv['very_high'] = fuzz.trapmf(dealer_score_lv.universe, [18, 21, 32, 32])
    
   
    decision['stand'] = fuzz.trimf(decision.universe, [0, 0, 1])
    decision['hit'] = fuzz.trimf(decision.universe, [0, 1, 1])
    
    
    rule1 = ctrl.Rule(ai_score_lv['very_low'] | (ai_score_lv['low'] & dealer_score_lv['very_high']), decision['hit'])
    rule2 = ctrl.Rule(ai_score_lv['medium'] & dealer_score_lv['medium'], decision['hit'])
    rule3 = ctrl.Rule(ai_score_lv['high'] & dealer_score_lv['low'], decision['stand'])
    rule4 = ctrl.Rule(ai_score_lv['very_high'], decision['stand'])
    rule5 = ctrl.Rule(ai_score_lv['low'] & dealer_score_lv['high'], decision['hit'])
    rule6 = ctrl.Rule(ai_score_lv['very_low'] & dealer_score_lv['very_low'], decision['hit'])
    rule7 = ctrl.Rule(ai_score_lv['medium'] & dealer_score_lv['very_low'], decision['hit'])
    rule8 = ctrl.Rule(ai_score_lv['high'] & dealer_score_lv['very_high'], decision['stand'])
    rule9 = ctrl.Rule(ai_score_lv['low'] & dealer_score_lv['medium'], decision['hit'])
    rule10 = ctrl.Rule(ai_score_lv['medium'] & dealer_score_lv['high'], decision['stand'])
    
    ai_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
    ai_decision = ctrl.ControlSystemSimulation(ai_ctrl)
    
    
    ai_decision.input['ai_score'] = ai_score
    ai_decision.input['dealer_score'] = dealer_score
    
    try:
        ai_decision.compute()
        decision_value = ai_decision.output['decision']
        
    except Exception as e:
        #print(f"Error in Fuzzy Logic Computation: {e}")
        return hand, current_deck
    
   
    if decision_value >= 0.5:
        potential_score = calculate_score(hand + [current_deck[0]])  
        if potential_score <= 21:
            hand, current_deck = deal_cards(hand, current_deck)
        else:
            
            decision_value = 0.0
    
    return hand, current_deck

def alphabeta(current_deck, dealer_hand, is_maximizing_player, depth, alpha, beta):
    if depth == 0 or is_terminal_state(current_deck, dealer_hand):
        return evaluate_hand(dealer_hand)

    if is_maximizing_player:
        max_eval = -float('inf')
        for card in current_deck:
            new_deck = current_deck.copy()
            new_deck.remove(card)
            dealer_hand.append(card)
            eval = alphabeta(new_deck, dealer_hand, False, depth - 1, alpha, beta)
            dealer_hand.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for card in current_deck:
            new_deck = current_deck.copy()
            new_deck.remove(card)
            dealer_hand.append(card)
            eval = alphabeta(new_deck, dealer_hand, True, depth - 1, alpha, beta)
            dealer_hand.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def is_terminal_state(current_deck, dealer_hand):
    return calculate_score(dealer_hand) >= 21

def evaluate_hand(dealer_hand):
    score = calculate_score(dealer_hand)
    if score > 21:
        return -1
    return score

def AI_cards_alphabeta(hand, current_deck, dealer_hand, reveal_dealer):
    if calculate_score(hand) >= 17:
        return hand, current_deck

    best_move = None
    best_score = -float('inf')

    for card in current_deck:
        new_hand = hand.copy()
        new_hand.append(card)
        new_deck = current_deck.copy()
        new_deck.remove(card)

        score = alphabeta(new_deck, new_hand, False, 3, -float('inf'), float('inf'))
        if score > best_score:
            best_score = score
            best_move = card

    if best_move:
        hand.append(best_move)
        current_deck.remove(best_move)

    return hand, current_deck
    
def get_font(size): 
    return pygame.font.Font("font.ttf", size)


def draw_game(act, record=[0,0,0,0], result=[0,0,0],s_board=[0,0,0]):
    button_list = []
   
    if act == 0:
        screen.blit(bg_img,(0,0))
        deal1 = pygame.draw.rect(screen, 'white', [900, 50, 300, 80], 0, 2)
        pygame.draw.rect(screen, 'black', [900, 50, 300, 80], 3, 5)
        deal_text = font.render('Black Jack', True, 'black')
        screen.blit(deal_text, (970, 80))
        button_list.append(deal1)
        deal2 = pygame.draw.rect(screen, 'white', [900, 250, 300, 80], 0, 2)
        pygame.draw.rect(screen, 'black', [900, 250, 300, 80], 3, 5)
        deal_text = font.render('Card Matching', True, 'black')
        screen.blit(deal_text, (970, 280))
        button_list.append(deal2)
        deal3 = pygame.draw.rect(screen, 'white', [900, 450, 300, 80], 0, 2)
        pygame.draw.rect(screen, 'black', [900, 450, 300, 80], 3, 5)
        deal_text = font.render('Wanna Back?', True, 'black')
        screen.blit(deal_text, (970, 480))
        button_list.append(deal3)
        
        
    
    elif act == 2:
            screen.blit(bg_img2,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(40).render("BLACK JACK and Card Matching", True, "Yellow")
            MENU_RECT = MENU_TEXT.get_rect(center=(700, 200))


            color = "#000000"

            PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(700, 350), 
                                text_input="PLAY", font=get_font(55), base_color=color, hovering_color="White")
           
            
            QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(700, 550), 
                                text_input="QUIT", font=get_font(55), base_color=color, hovering_color="White")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.change(MENU_MOUSE_POS)
                button.update(screen)
            return PLAY_BUTTON,QUIT_BUTTON,MENU_MOUSE_POS
    elif act == 1:
       
        hit = pygame.draw.rect(screen, 'white', [0, 550, 300, 50], 0, 5)
        pygame.draw.rect(screen, 'black', [0, 550, 300, 50], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (105, 565))
        button_list.append(hit)
        
        stand = pygame.draw.rect(screen, 'white', [300, 550, 300, 50], 0, 5)
        pygame.draw.rect(screen, 'black', [300, 550, 300,50], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (405, 565))
        button_list.append(stand)
        
        quite = pygame.draw.rect(screen, 'white', [600, 550, 300, 50], 0, 5)
        pygame.draw.rect(screen, 'black', [600, 550, 300,50], 3, 5)
        stand_text = font.render('QUIT', True, 'black')
        screen.blit(stand_text, (705, 565))
        button_list.append(quite)
        
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}  AI : {record[3]}', True, 'white')
        screen.blit(score_text, (5, 640))
        
        score_text = smaller_font.render(f'Players score: {s_board[0]}   Dealers score: {s_board[1]}   AI score: {s_board[2]}', True, 'white')
        screen.blit(score_text, (5, 660))
        
        
    
    if result != 0 and active == 1:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 120], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 120], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 117], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit( deal_text, (165, 250))
        button_list.append(deal)
    return button_list




#results = ['', 'PLAYER BUSTED o_O ', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...','AI_WINS! ^_^','AI and Dealer Tie','AI and Player Tie','Dealer and Player Tie']

def check_endgame(AI_S,hand_act, deal_score, play_score, result, totals, add,sc_board):
    
    
    if not hand_act and deal_score >= 17:
        if play_score > 21 :
            result =  1
        elif play_score <= 21 and ((play_score > dealer_score or dealer_score>21)and (play_score > AI_S or AI_S>21)): 
            result = 2   
            
        elif dealer_score <=21 and ((dealer_score > play_score or player_score >21) and (AI_S>21 or  dealer_score > AI_S)):
            result = 3
        elif (AI_S == play_score and AI_S == deal_score and AI_S<=21 ):
            result = 4
        elif (AI_S<=21 and ((AI_S>deal_score or deal_score>21)) and (AI_S>play_score or play_score>21)):
            result = 5    
        elif (AI_S==deal_score and AI_S<=21 and (AI_S>play_score or play_score>21)) :
            result = 6  
        elif (AI_S==play_score and AI_S<=21 and (AI_S>deal_score or deal_score>21)) :
            result = 7 
        elif (deal_score==play_score and deal_score<=21 and (AI_S<deal_score or AI_S>21)) :
            result = 8            
            
        if add:
            #0-player 1-Dealer 2-Tie 3-AI
            if result == 1 :
                totals[1] += 1
                totals[3] += 1
                sc_board[0] = sc_board[0] 
                sc_board[1] = sc_board[1] + 15
                sc_board[2] = sc_board[2] + 15
                
            elif result == 2:
                totals[0] += 1
                sc_board[0] = sc_board[0] + 30
                sc_board[1] = sc_board[1] 
                sc_board[2] = sc_board[2]

            elif result == 3:
                totals[1] += 1
                sc_board[0] = sc_board[0] 
                sc_board[1] = sc_board[1] + 30
                sc_board[2] = sc_board[2]

            elif result == 4:
                totals[2] += 1
                sc_board[0] = sc_board[0] + 10
                sc_board[1] = sc_board[1] + 10
                sc_board[2] = sc_board[2] + 10       
                
            elif result == 5 :
                totals[3]+=1
                sc_board[0] = sc_board[0] 
                sc_board[1] = sc_board[1] 
                sc_board[2] = sc_board[2] + 30
            elif result == 6:     
                totals[1] += 1
                totals[3] += 1
                sc_board[0] = sc_board[0] 
                sc_board[1] = sc_board[1] + 15
                sc_board[2] = sc_board[2] + 15
            elif result == 7:     
                totals[0] += 1
                totals[3] += 1
                sc_board[0] = sc_board[0] + 15
                sc_board[1] = sc_board[1] 
                sc_board[2] = sc_board[2] + 15  
            else :     
                totals[1] += 1
                totals[0] += 1
                sc_board[0] = sc_board[0] + 15
                sc_board[1] = sc_board[1] + 15
                sc_board[2] = sc_board[2]     


                
            add = False
            
    return result, totals, add, score_board


def exit_app():
    ask_yn = messagebox.askyesno('Question', 'Confirm Quit?')
    if not ask_yn:
        return
    root.destroy()

label = 1


#version2 starting
class Mem:
    player_turn=True
    logo_frame=None
    New_card=None
    First_card=None
    all_clicks=0
    click_player_count=0
    click_ai_count=0
    player_score=0
    ai_score=0
    total_player_score=0
    total_ai_score=0
    found_matches=0
    match_list=[]
    blank_cards=[]
    card_images=[]
    target_clicks=24
    stat_bar=None
    card=None
    num_pairs=12
    level=1
    player_score_label = None
    ai_score_label = None
    unmatched_pairs=[]
    population_size = 20
    generations = 100
    mutation_rate = 0.01
def updt_status_bar(txt):
    Mem.stat_bar.config(text=txt)
def logo():
    Mem.logo_frame = tk.Frame(root)
    Mem.logo_frame.grid(row=0, columnspan=10)
    logo_image = Image.open('bb.jpg')
    new_size = (1200, 150)
    logo_image = logo_image.resize(new_size, Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(Mem.logo_frame, image=logo_photo)
    logo_label.logo_image = logo_photo
    logo_label.grid(padx=0, pady=0, row=0, column=0)
def get_png_list(loc):
    pngs = [f for f in os.listdir(loc) if f[-4:] == '.png']
    return [os.path.join(loc, f) for f in pngs]
def initialize_card_sequence():
    image_dir = os.path.join(os.path.dirname(__file__), 'png')
    image_array = get_png_list(image_dir)
    image_pairs = image_array[0:Mem.num_pairs]
    image_pairs = image_pairs * 2
    random.shuffle(image_pairs)
    Mem.card_sequence = image_pairs  # Store the shuffled sequence

def create_game_board():
    button = tk.Button(root, text="QUIT", command=on_button_click, font=("Arial", 10), fg="white")
    button.config(width=10, height=5)
    button.configure(bg="purple")
    button.grid(row=0, column=0, padx=30, pady=20, sticky=tk.SE)

    card_dir = os.path.join(os.path.dirname(__file__), 'card.png')
    Mem.card = tk.PhotoImage(file=card_dir)


    image_pairs = Mem.card_sequence

    ro = 0
    col = 0

    game_board_frame = tk.Frame(root)
    game_board_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')
    game_board_frame.configure(background='#502963')

    for i in range(len(image_pairs)):
        Mem.blank_cards.append(tk.Label(game_board_frame))
        Mem.card_images.append(tk.PhotoImage(file=image_pairs[i]))
        Mem.blank_cards[i].img = Mem.card
        Mem.blank_cards[i].config(image=Mem.blank_cards[i].img)
        Mem.blank_cards[i].config(text=image_pairs[i])

        Mem.blank_cards[i].grid(row=ro, column=col, padx=10, pady=10)
        Mem.blank_cards[i].bind('<Button-1>', on_click)

        col += 1
        if col == 8:
            col = 0
            ro += 1

    for row in range(ro):
        game_board_frame.grid_rowconfigure(row, weight=1, minsize=150)

    for col in range(8):
        game_board_frame.grid_columnconfigure(col, weight=1, minsize=150)
        
    updt_status_bar(f'Complete Level {Mem.level} within {Mem.target_clicks} clicks')
    

def create_status_bar():
    stat_frame = tk.Frame(root)
    stat_frame.grid(padx=20, pady=0, row=4, columnspan=8,sticky='nsew')

    Mem.stat_bar = tk.Label(stat_frame, bg='#CBC3E3', fg='black', font=('ariel, 16'), text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
    Mem.stat_bar.pack(side=tk.BOTTOM, fill=tk.X)

    score_frame = tk.Frame(root)
    score_frame.grid(row=5, columnspan=8, sticky=tk.W + tk.E)

    Mem.player_score_label = tk.Label(score_frame, text=f'Player Score: {Mem.player_score}', font=('ariel', 14))
    Mem.player_score_label.pack(side=tk.LEFT, padx=20)

    Mem.ai_score_label = tk.Label(score_frame, text=f'AI Score: {Mem.ai_score}', font=('ariel', 14))
    Mem.ai_score_label.pack(side=tk.LEFT, padx=20)
    
def update_scores():
    Mem.player_score_label.config(text=f'Player Score: {Mem.player_score}')
    Mem.ai_score_label.config(text=f'AI Score: {Mem.ai_score}')
    
def flip_card(card, show_front):
    if show_front:
        img = tk.PhotoImage(file=card.cget('text'))
    else:
        img = Mem.card
    card.img = img
    card.config(image=img)

def flip_back_cards(cards):
    for card in cards:
        flip_card(card, show_front=False)
        card.bind('<Button-1>', on_click)
def on_button_click():
    global active
    active = 2
    root.destroy()
def highlight_card(card, color):
    card.config(highlightbackground=color, highlightcolor=color, highlightthickness=5)   
def unhighlight_card(card):
    card.config(highlightbackground="white")
    
#player turn
def on_click(event):
     
    if Mem.player_turn:
        Mem.click_player_count += 1
        Mem.new_card = event.widget
        flip_card(Mem.new_card,True)

        if Mem.click_player_count == 1:
            Mem.first_card = Mem.new_card
            print(Mem.first_card)
            Mem.all_clicks += 1
            if Mem.all_clicks > Mem.target_clicks:
                we_have_a_winner()
            highlight_card(Mem.first_card, 'green')
            Mem.first_card.unbind('<Button-1>')

        else:
            Mem.new_card.unbind('<Button-1>')
            highlight_card(Mem.new_card, 'green')
            Mem.all_clicks += 1
            if Mem.all_clicks > Mem.target_clicks:
                we_have_a_winner()
            
            if Mem.new_card.cget('text') == Mem.first_card.cget('text'):
              
                Mem.player_score += 1
                Mem.total_player_score += 1
                Mem.match_list.append(Mem.new_card.cget('text'))
                Mem.found_matches += 1
                if Mem.found_matches==Mem.num_pairs:
                    we_have_a_winner()
                update_scores()
                Mem.first_card=None
                Mem.new_card=None
                Mem.click_player_count = 0
                updt_status_bar('AI\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
                Mem.player_turn = False
                if Mem.level==1:
                    root.after(1000,ai_turn_genetic) 
                elif Mem.level==2:
                    root.after(1000,ai_turn_genetic_heuristic) 
            
            else:

                Mem.unmatched_pairs.append([Mem.first_card,Mem.new_card])
                unhighlight_card(Mem.first_card)
                unhighlight_card(Mem.new_card)
                root.after(500, lambda: flip_back_cards([Mem.first_card, Mem.new_card]))
                Mem.click_player_count = 0
                updt_status_bar('AI\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
                Mem.player_turn = False
                if Mem.level==1:
                    root.after(1000,ai_turn_genetic)
                elif Mem.level==2:
                    root.after(1000,ai_turn_genetic_heuristic) 

def fitness(sequence):
    matches=set()  
    for pick in sequence:
        txt=pick.cget('text')
        for second_pick in sequence:
            if second_pick!=pick and second_pick.cget('text')==txt:
                matches.add(txt)
    return len(matches)
 
def select_parents(population, fitness_scores):
    fitness_scores = [score + 1 for score in fitness_scores]
    return random.choices(population, weights=fitness_scores, k=2)

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(sequence):
    for i in range(len(sequence)):
        if random.random() < Mem.mutation_rate:
            sequence[i] = random.choice([card for card in Mem.blank_cards if card.cget('text') not in Mem.match_list])
    return sequence

def generate_initial_population():
    population = []
    for _ in range(Mem.population_size):
        if len(Mem.match_list)<=Mem.num_pairs: 
            sequence = [random.choice([card for card in Mem.blank_cards if card.cget('text') not in Mem.match_list]) for _ in range(Mem.num_pairs) ]
        else:
            sequence = [random.choice([card for card in Mem.blank_cards if card.cget('text') not in Mem.match_list]) for _ in range(24-len(Mem.match_list)) ]       
        population.append(sequence)
    return population
def ai_turn_genetic():
    population = generate_initial_population()
    for _ in range(Mem.generations):
        fitness_scores = [fitness(individual) for individual in population]
        new_population = []
        for _ in range(Mem.population_size // 2):
            parent1, parent2 = select_parents(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population

    best_sequence = max(population, key=fitness)
        
    Mem.first_card=random.choice(best_sequence)
    Mem.all_clicks+=1
    if Mem.all_clicks > Mem.target_clicks:
        we_have_a_winner()
    flip_card(Mem.first_card,True)
    img = tk.PhotoImage(file=Mem.first_card.cget('text'))
    Mem.first_card.img = img
    Mem.first_card.config(image=img)
    highlight_card(Mem.first_card, 'red')
    
    available_cards_genetic=[card for card in best_sequence if card!=Mem.first_card]
    
    if available_cards_genetic:
        Mem.new_card=random.choice(available_cards_genetic)
      
    else:
        we_have_a_winner()
    
    flip_card(Mem.new_card,True)
    Mem.all_clicks+=1
    if Mem.all_clicks > Mem.target_clicks:
        we_have_a_winner()
    img = tk.PhotoImage(file=Mem.new_card.cget('text'))
    Mem.new_card.img = img
    Mem.new_card.config(image=img)
    highlight_card(Mem.new_card, 'red')
    if Mem.new_card.cget('text') == Mem.first_card.cget('text'):
   
        Mem.ai_score += 1
        Mem.total_ai_score+=1
        Mem.match_list.append(Mem.new_card.cget('text'))
        Mem.found_matches += 1
        if Mem.found_matches==Mem.num_pairs:
            we_have_a_winner()
        update_scores()
        Mem.click_ai_count=0
        updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
        Mem.player_turn=True
        for item in Mem.blank_cards:
             if item.cget('text') not in Mem.match_list:   
                 item.bind('<Button-1>', on_click)
                 updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
         
    else:
        Mem.unmatched_pairs.append([Mem.first_card,Mem.new_card])
        unhighlight_card(Mem.first_card)
        unhighlight_card(Mem.new_card)
        root.after(500, lambda: flip_back_cards([Mem.first_card, Mem.new_card]))
        update_scores()
        updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
        Mem.click_ai_count=0
        Mem.player_turn=True
        for item in Mem.blank_cards:
             if item.cget('text') not in Mem.match_list:   
                 item.bind('<Button-1>', on_click)
                 updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
          
    
              

def ai_turn_genetic_heuristic():
    population = generate_initial_population()
    for _ in range(Mem.generations):
        fitness_scores = [fitness(individual) for individual in population]
        new_population = []
        for _ in range(Mem.population_size // 2):
            parent1, parent2 = select_parents(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population

    best_sequence = max(population, key=fitness)
        
    Mem.first_card=random.choice(best_sequence)
    Mem.all_clicks+=1
    if Mem.all_clicks > Mem.target_clicks:
        we_have_a_winner()
    flip_card(Mem.first_card,True)
    img = tk.PhotoImage(file=Mem.first_card.cget('text'))
    Mem.first_card.img = img
    Mem.first_card.config(image=img)
    highlight_card(Mem.first_card, 'red')

    flag=0
    for item in Mem.unmatched_pairs:
        if Mem.first_card==item[0]:
            flag=1
            available_cards_genetic = [card for card in best_sequence if (card != Mem.first_card) and (card!=item[1])] 
        elif Mem.first_card==item[1]:
            flag=1
            available_cards_genetic = [card for card in best_sequence if (card != Mem.first_card) and (card!=item[0])] 
    if flag==0:
        available_cards_genetic = [card for card in best_sequence if card != Mem.first_card]

    
    if available_cards_genetic:
        Mem.new_card=random.choice(available_cards_genetic)
        
    else:
        we_have_a_winner()
    
    flip_card(Mem.new_card,True)
    Mem.all_clicks+=1
    if Mem.all_clicks > Mem.target_clicks:
        we_have_a_winner()
    img = tk.PhotoImage(file=Mem.new_card.cget('text'))
    Mem.new_card.img = img
    Mem.new_card.config(image=img)
    highlight_card(Mem.new_card, 'red')
    if Mem.new_card.cget('text') == Mem.first_card.cget('text'):
   
        Mem.ai_score += 1
        Mem.total_ai_score+=1
        Mem.match_list.append(Mem.new_card.cget('text'))
        Mem.found_matches += 1
        if Mem.found_matches==Mem.num_pairs:
            we_have_a_winner()
        update_scores()
        Mem.click_ai_count=0
        updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
        Mem.player_turn=True
        for item in Mem.blank_cards:
             if item.cget('text') not in Mem.match_list:   
                 item.bind('<Button-1>', on_click)
                 updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
         
    else:
        Mem.unmatched_pairs.append([Mem.first_card,Mem.new_card])
        unhighlight_card(Mem.first_card)
        unhighlight_card(Mem.new_card)
        root.after(500, lambda: flip_back_cards([Mem.first_card, Mem.new_card]))
        update_scores()
        updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
        Mem.click_ai_count=0
        Mem.player_turn=True
        for item in Mem.blank_cards:
             if item.cget('text') not in Mem.match_list:   
                 item.bind('<Button-1>', on_click)
                 updt_status_bar('Player\'s turn. Clicks:' + str(Mem.all_clicks) + '-' + str(Mem.target_clicks))
          
    
              
        
def show_custom_message(txt):
    custom_message = tk.Toplevel()
    custom_message.title('Winner')
    message_label = tk.Label(custom_message, text=txt, padx=20, pady=20, font=('Arial', 14))
    message_label.pack()
    custom_message.geometry('300x150')   
    Mem.new_card = None
    Mem.first_card = None
    Mem.click_player_count = 0
    Mem.click_ai_count = 0
    Mem.found_matches = 0
    Mem.match_list = []
    Mem.blank_cards = []
    Mem.card_images = []
    Mem.all_clicks = 0
    Mem.ai_memory = {}
    create_status_bar()
    create_game_board()
    if Mem.level==1:
        Mem.player_score=0
        Mem.ai_score=0
        Mem.level=2
    elif Mem.level==2:
        Mem.player_score = 0
        Mem.ai_score = 0
        Mem.total_player_score=0
        Mem.total_ai_score=0
        Mem.level=1
        Mem.unmatched_pairs=[]
        
    updt_status_bar(f'Complete Level {Mem.level} within {Mem.target_clicks} clicks')
    custom_message.mainloop()
def we_have_a_winner():
    if Mem.level==1:
        if Mem.total_player_score>Mem.total_ai_score:
            result_text=f'Winner: Player Score: {Mem.player_score}'
            show_custom_message(result_text)
        elif Mem.total_player_score<Mem.total_ai_score:
            result_text=f'Winner: AI Score: {Mem.ai_score}'
            show_custom_message(result_text)
        else:
            result_text=f'Draw Game Score: {Mem.player_score}'
            show_custom_message(result_text)
    elif Mem.level==2:
        if Mem.total_player_score>Mem.total_ai_score:
            result_text=f'Final Winner: Player Score: {Mem.total_player_score}'
            show_custom_message(result_text)
        elif Mem.total_player_score<Mem.total_ai_score:
            result_text=f'Final Winner: AI Score: {Mem.total_ai_score}'
            show_custom_message(result_text)
        else:
            result_text=f'Final Result:Draw Game Score: {Mem.total_player_score}'
            show_custom_message(result_text)      


# main game loop
run = True
while run:
    
    timer.tick(fps)
    screen.fill('#000000')
    
    
    if initial_deal:
        for i in range(2):
            AI_hand, game_deck = deal_cards(AI_hand, game_deck)
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            
        initial_deal = False

    
    if active == 1:
        player_score = calculate_score(my_hand)
        AI_score = calculate_score(AI_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer, AI_hand)

        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score, AI_score)

    if active != 2:
        buttons = draw_game(active, records, outcome, score_board)
    else:
        PLAY_BUTTON, QUIT_BUTTON, MENU_MOUSE_POS = draw_game(active, records, outcome, score_board)

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if active == 2:
                for button in [PLAY_BUTTON, QUIT_BUTTON]:
                    button.change(MENU_MOUSE_POS)
                    button.update(screen)
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    active = 0
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                pygame.display.update()
            elif active == 0:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    AI_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
                elif buttons[2].collidepoint(event.pos):
                    active = 2
                elif buttons[1].collidepoint(event.pos):
                    root = tk.Tk()
                    root.title('Black Jack 2.0    Level 1')
                    root.attributes("-fullscreen", True)
                    root.resizable(False, False)
                    root.geometry('+550+300')
                    logo()
                    initialize_card_sequence()
                    create_status_bar()
                    create_game_board()
                    root.protocol('WM_DELETE_WINDOW', exit_app)
                    root.mainloop()
                    pygame.display.update()
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                    if label == 1:
                        AI_hand, game_deck = AI_cards(AI_hand, game_deck,dealer_hand,reveal_dealer)
                        label=2
                    elif label == 2:
                        AI_hand, game_deck = AI_cards_fuzzy(AI_hand, game_deck,dealer_hand,reveal_dealer)
                        label =3
                    elif label == 3:
                        AI_hand, game_deck = AI_cards_alphabeta(AI_hand, game_deck,dealer_hand,reveal_dealer)
                        label = 1
                        

                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif buttons[2].collidepoint(event.pos):
                    screen.fill('Black')
                    active = 2
                elif len(buttons) == 4:
                    if buttons[3].collidepoint(event.pos):
                        active = 1
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        AI_hand = []
                        dealer_hand = []
                        outcome = 0
                        score_board = [0, 0, 0]
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score >= 21   :
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score, score_board = check_endgame(AI_score, hand_active, dealer_score, player_score, outcome, records, add_score, score_board)

    pygame.display.flip()

pygame.quit()
