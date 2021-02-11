import tkinter as tk
from tkinter import *
import os
import random

dealerWins = 0
playerWins = 0


class Card():
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value
        strTemp = "img/" + self.getPath() + ".gif"
        self.cardImg = PhotoImage(file=strTemp)

    # Print for test purposes
    # def print(self):
    #    print("{} of {} with value: {}".format(
    #       self.name, self.suit, self.value))

    # Returns in the format of image file paths
    def getPath(self):
        return self.suit+self.name


class Deck():
    def __init__(self):
        self.cards = []
        self.create()

    # Creates a deck of 52 unique cards
    def create(self):
        self.cards.clear()
        for suit in ["club", "diamond", "heart", "spade"]:
            for val in range(1, 14):
                if(val == 1):
                    self.cards.append(Card("Ace", suit, 11))
                elif(val < 11):
                    self.cards.append(Card(str(val), suit, val))
                elif(val == 11):
                    self.cards.append(Card("Jack", suit, 10))
                elif(val == 12):
                    self.cards.append(Card("Queen", suit, 10))
                elif(val == 13):
                    self.cards.append(Card("King", suit, 10))

    # Show for test purposes
    # def show(self):
    #    for c in self.cards:
    #        c.print()

    # Randomly selects and removes a card from the deck. Alternative to shuffling
    def removeCard(self):
        rNum = random.randint(0, len(self.cards)-1)
        return self.cards.pop(rNum)


class Player():
    def __init__(self):
        self.hand = []
        self.handVal = 0

    # Adds card and value to the player's hand
    def draw(self, deck):
        tempCard = deck.removeCard()
        self.hand.append(tempCard)
        self.handVal += tempCard.value

    # Print for testing purposes
    # def showHand(self):
    #    for card in self.hand:
    #        card.print()

    # Displays the cards in the player's hand to the table
    def renderHand(self, ypos):
        for card in self.hand:
            canvas.create_image((self.hand.index(card)*100) +
                                200, ypos, tag="card_tag", image=card.cardImg)

    def clearHand(self):
        self.hand.clear()
        self.handVal = 0

    # This automatically decides whether or not aces should count as 1 or 11.
    def aceCheck(self):
        for card in self.hand:
            if(self.handVal > 21):
                if(card.name == "Ace" and card.value == 11):
                    card.value = 1
                    self.handVal -= 10


# Deals 2 cards to the player and the dealer at the start of each round.
def deal():
    player.draw(deck)
    dealer.draw(deck)
    player.draw(deck)
    player.aceCheck()
    global faceDownCard
    faceDownCard = deck.removeCard()
    canvas.delete("card_tag")
    dealer.renderHand(150)
    canvas.create_image(300, 150, tag="down_card_tag", image=downCard)
    player.renderHand(400)
    canvas.itemconfigure(dealerScore, text=str(dealer.handVal))
    canvas.itemconfigure(playerScore, text=str(player.handVal))
    if(dealer.handVal >= 21 or player.handVal >= 21):
        gameOver()


# Used to add a card to the player's hand. Triggered by the hit button.
def hit():
    player.draw(deck)
    canvas.delete("card_tag")
    dealer.renderHand(150)
    player.renderHand(400)
    player.aceCheck()
    canvas.itemconfigure(dealerScore, text=str(dealer.handVal))
    canvas.itemconfigure(playerScore, text=str(player.handVal))
    if(dealer.handVal >= 21 or player.handVal >= 21):
        gameOver()


# Plays out the dealer's hand after the player decides to stand. Triggered by the stand button.
def stand():
    dealer.hand.append(faceDownCard)
    dealer.handVal += faceDownCard.value
    dealer.aceCheck()
    while(dealer.handVal < 17):
        dealer.draw(deck)
        dealer.aceCheck()
    canvas.delete("card_tag")
    canvas.delete("down_card_tag")
    dealer.renderHand(150)
    player.renderHand(400)
    canvas.itemconfigure(dealerScore, text=str(dealer.handVal))
    gameOver()


# Decides the results based on the players' hands. Called in the hit and stand functions.
def gameOver():
    hitButton["state"] = DISABLED
    standButton["state"] = DISABLED
    if(player.handVal == dealer.handVal):
        canvas.itemconfigure(drawMessage, state=NORMAL)
    elif((player.handVal == 21 or dealer.handVal > 21 or player.handVal > dealer.handVal) and player.handVal <= 21):
        canvas.itemconfigure(winMessage, state=NORMAL)
        global playerWins
        playerWins += 1
        canvas.itemconfigure(
            playerWinsText, text="Player Wins: " + str(playerWins))
    else:
        canvas.itemconfigure(loseMessage, state=NORMAL)
        global dealerWins
        dealerWins += 1
        canvas.itemconfigure(
            dealerWinsText, text="Dealer Wins: " + str(dealerWins))
    againButton.place(x=335, y=290)


# Resets the deck and players for the next round. Triggered by the play again button.
def playAgain():
    deck.create()
    player.clearHand()
    dealer.clearHand()
    canvas.itemconfigure(dealerScore, text=str(dealer.handVal))
    canvas.itemconfigure(playerScore, text=str(player.handVal))

    hitButton["state"] = NORMAL
    standButton["state"] = NORMAL
    canvas.itemconfigure(drawMessage, state=HIDDEN)
    canvas.itemconfigure(winMessage, state=HIDDEN)
    canvas.itemconfigure(loseMessage, state=HIDDEN)
    againButton.place_forget()
    deal()


# Create application window
root = tk.Tk()
root.title('Blackjack')
icon = PhotoImage(file="img/icon.gif")
root.iconphoto(False, icon)
root.geometry("800x600")
root.resizable(width=False, height=False)
root.configure(bg="#173517")
downCard = PhotoImage(file="img/blueBack.gif")

canvas = tk.Canvas(root, bg="#173517", bd=0, highlightthickness=0)
canvas.pack(fill="both", expand=True)


# Create deck and players
deck = Deck()
dealer = Player()
player = Player()


# Creates the text that will be displayed
dealerWinsText = canvas.create_text(400, 20, fill="white",
                                    font=("Calibri", 14, "normal"), text="Dealer Wins: " + str(dealerWins))
playerWinsText = canvas.create_text(400, 540, fill="white",
                                    font=("Calibri", 14, "normal"), text="Player Wins: " + str(playerWins))
canvas.create_text(70, 100, fill="white", font=(
    "Calibri", 16, "bold"), text="Dealer ")
canvas.create_text(70, 350, fill="white", font=(
    "Calibri", 16, "bold"), text="Player ")
dealerScore = canvas.create_text(
    65, 150, fill="white", font=(
        "Calibri", 14, "normal"), text=str(dealer.handVal))
playerScore = canvas.create_text(
    65, 400, fill="white", font=(
        "Calibri", 14, "normal"), text=str(player.handVal))
drawMessage = canvas.create_text(
    400, 250, fill="yellow", state=HIDDEN, font=("Calibri", 40, "bold"), text="Draw!")
winMessage = canvas.create_text(
    400, 250, fill="green", state=HIDDEN, font=("Calibri", 40, "bold"), text="You Win!")
loseMessage = canvas.create_text(
    400, 250, fill="red", state=HIDDEN, font=("Calibri", 40, "bold"), text="You Lose!")


# Hit Button
hitButton = tk.Button(root, text="Hit", padx=50,
                      pady=10, fg="white", bg="#45311d", activebackground="#543b23", relief="raised", borderwidth=1, command=hit)
hitButton.place_forget()


# Stand Button
standButton = tk.Button(root, text="Stand", padx=45,
                        pady=10, fg="white", bg="#45311d", activebackground="#543b23", relief="raised", borderwidth=1, command=stand)
standButton.place_forget()


# Play Again Button
againButton = tk.Button(root, text="Play Again?", padx=30,
                        pady=10, fg="white", bg="#45311d", activebackground="#543b23", relief="raised", borderwidth=1, command=playAgain)
againButton.place_forget()


# Enables buttons and starts the game. Triggered by the start button.
def start():
    startButton.place_forget()
    hitButton.place(x=275, y=557)
    standButton.place(x=400, y=557)
    deal()


# Start Button
startButton = tk.Button(root, text="Start", padx=30,
                        pady=20, fg="white", bg="#45311d", activebackground="#543b23", relief="raised", borderwidth=1, command=start)
startButton.place(x=360, y=270)

root.mainloop()
