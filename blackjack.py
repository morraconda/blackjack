from random import randint
from tkinter import *

root = Tk()
root.title("Blackjack")
root.geometry("320x120")

class player:
    def __init__(self, name, cards, hand_value, ace_flag, cards_label, hand_value_label):
        self.name = name
        self.cards = cards
        self.hand_value = hand_value
        self.ace_flag = ace_flag    

        # there's surely a better way to display and update separate labels than this
        self.cards_label = cards_label
        self.hand_value_label = hand_value_label

# hardcoded text because i'm lazy      
user = player("User", [], 0, False,
    Label(root, text="User Hand: []"), Label(root, text="(0)"))
dealer = player("Dealer", [], 0, False,
    Label(root, text="Dealer Hand: []"), Label(root, text="(0)"))

# variable initialisation
money = 50
bet = 0
user_can_bet = True
user_can_hit = False

start_label = Label(root, text="To start a new hand, press a bet button.")
bet_label = Label(root, text=("Bet: $-"))
money_label = Label(root, text=("Money: ${}").format(money))
result_label = Label(root, text=("Result: -"))

start_label.place(rely=1, anchor=SW)
bet_label.grid(row=2, column=3)
money_label.grid(row=1, column=3)
result_label.grid(row=0, column=3)

user.cards_label.grid(row=1, column=1)
dealer.cards_label.grid(row=0, column=1)
user.hand_value_label.grid(row=1, column=2)
dealer.hand_value_label.grid(row=0, column=2)

# sets user bet to the specified amount, starts the hand
def bet_amount(amount):
    global bet, money, user_can_bet, user_can_hit
    if user_can_bet == True:
        user_can_bet = False
        user_can_hit = True
        start_label.config(text="hand currently in progress")
        
        # calculate and display new bet and money
        bet = amount
        money -= bet
        bet_label.config(text=("Bet: ${}").format(bet))
        money_label.config(text=("Money: ${}").format(money))
        result_label.config(text=("Result: -"))

        # start hand
        draw(dealer)
        draw(user)
        draw(user)
        
# draws one card to someone's hand and updates her hand value accordingly    
def draw(player):
    if user_can_hit == True or player == dealer:
        new_card = randint(2, 14)
        # special casing for face cards
        if new_card > 10:
            if new_card == 11:
                    player.hand_value += 10
                    player.cards.append("J")
            elif new_card == 12:
                player.hand_value += 10
                player.cards.append("Q")
            elif new_card == 13:
                player.hand_value += 10
                player.cards.append("K")
            else:
                player.hand_value += 11
                player.cards.append("A")
                player.ace_flag = True
        else:
            player.hand_value += new_card
            player.cards.append(new_card)
        # check for bust
        if player.hand_value > 21:
            # if hand appears bust but hand has a high ace, make it a low ace
            if player.ace_flag == True:
                player.hand_value -= 10
                player.ace_flag = False
            else:
                player.hand_value = "BUST"
                
        # update cards & hand value
        player.cards_label.config(text="{} Hand: {}".format(player.name, player.cards))
        player.hand_value_label.config(text="({})".format(player.hand_value))
        # end user turn and resolve if 21 or Bust
        if player.name == "User":
            if player.hand_value == 21 or player.hand_value == "BUST":
                resolve()
            
# after user's turn has ended, resolve dealer hand and user reward 
def resolve():
    # only resolve if both it is the user's turn and they've bet something
    global user_can_bet, user_can_hit, money 
    if user_can_bet == False and user_can_hit == True:
        user_can_bet = True
        user_can_hit = False
        # dealer hits below hard 17 ruleset
        while dealer.hand_value < 17 or (dealer.hand_value == 17 and dealer.ace_flag == True):
            # delay 200ms before each dealer draw
            # doesn't update the GUI after every draw for some reason
            root.after(200, draw(dealer))
            if dealer.hand_value == "BUST":
                break
            
        # rewards the user based on the result of the hand and her bet
        if user.hand_value == "BUST":
            reward = 0
            result = "Bust"
        elif dealer.hand_value == "BUST":
            reward = 2*bet
            result = "Dealer Bust"
        elif user.hand_value > dealer.hand_value:
            reward = 2*bet
            result = "Win"
        elif user.hand_value == dealer.hand_value:
            reward = bet
            result = "Tie"
        else:
            reward = 0
            result = "Loss"

        # displays hand result, reward, money
        money += reward
        result_label.config(text=("Result: {}").format(result))
        bet_label.config(text=("Reward: ${}").format(reward))
        money_label.config(text=("Money: ${}").format(money))

        # reset hands
        user.cards, dealer.cards = [],[]
        user.hand_value, dealer.hand_value = 0,0
        user.ace_flag, dealer.ace_flag = False,False
        start_label.config(text="To start a new hand, press a bet button.")
     
# buttons, each should be fairly self-explanatory 
b1 = Button(root, text="Bet $1", command=lambda: bet_amount(1))
b2 = Button(root, text="Bet $2", command=lambda: bet_amount(2))
b5 = Button(root, text="Bet $5", command=lambda: bet_amount(5))
b10 = Button(root, text="Bet $10", command=lambda: bet_amount(10))
hit = Button(root, text="Hit", command=lambda: draw(user))
stick = Button(root, text="Stick", command=resolve)

# arrange buttons on GUI
b1.grid(row=3, column=0)
b2.grid(row=3, column=1)
b5.grid(row=3, column=2)
b10.grid(row=3, column=3)
hit.grid(row=2, column=1)
stick.grid(row=2, column=2)

root.mainloop()
        
        
        
            
    



