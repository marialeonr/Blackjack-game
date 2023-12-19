#import the necessary libraries
import os
from tkinter import PhotoImage, messagebox
import random
import tkinter as tk

#Define the class Card for the logic of the game
#There is the constructor firstly, then defining the value of the special cards and how to get the images
class Card:
    def __init__(self, suit: str, value: int):
        self.suit = suit
        self.value = value

    def get_numeric_value(self) -> int:
        if self.value in ['K', 'Q', 'J']:
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)

    def get_image(self):
        return f'/Users/marialeonruiz/Desktop/Programacion_II/Blackjack-game/img/{self.value}_of_{self.suit}.png'

#Define the class deck
#There is the constructor, the composition of the deck, shuffling the cards and dealing them.
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()

#Class english deck, cards have been defined previosuly so no need to define here, calls the instructor of the parent class as it is a subclass
class EnglishDeck(Deck):
    def __init__(self):
        super().__init__()
        self.shuffle()

#The hand of cards
#Can add cards, gives the values
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def value(self) -> int:
        total_value = 0
        ace_count = 0

        for card in self.cards:
            total_value += card.get_numeric_value()
            if card.value == 'A':
                ace_count += 1

        while total_value > 21 and ace_count:
            total_value -= 10
            ace_count -= 1

        return total_value

#The player
#Contains the constructor, defining the hand from the deck when the game starts, playing the cards and determining the winner
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

class BlackjackGame:
    def __init__(self):
        self.deck = EnglishDeck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")

    def start_game(self):
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        for _ in range(2):
            self.player.hand.add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())

    def hit(self) -> bool:
        self.player.hand.add_card(self.deck.deal())
        return self.player.hand.value() <= 21

    def dealer_hit(self) -> bool:
        if self.dealer.hand.value() < 17:
            self.dealer.hand.add_card(self.deck.deal())
            return True
        return False

    def determine_winner(self):
        player_value = self.player.hand.value()
        dealer_value = self.dealer.hand.value()

        if player_value > 21:
            return "Dealer wins!"
        elif dealer_value > 21 or player_value > dealer_value:
            return f"{self.player.name} wins!"
        elif player_value < dealer_value:
            return "Dealer wins!"
        else:
            return "It's a tie!"

class BlackjackGUI:
    def __init__(self, game):
        self.game = game

        self.root = tk.Tk()
        self.root.title("Blackjack")

        # Frames para el jugador y el crupier
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(side=tk.LEFT, padx=10)

        self.deck_frame = tk.Frame(self.root)
        self.deck_frame.pack(side=tk.LEFT, padx=10)

        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.pack(side=tk.RIGHT, padx=10)

        # Botón "Stand"
        self.btn_stand = tk.Button(self.deck_frame, text="Stand", command=self.handle_stand, state=tk.NORMAL)
        self.btn_stand.pack(side=tk.BOTTOM)

        self.start_game()

    def start_game(self):
        self.game.start_game()
        self.update_interface()

    def handle_hit(self, event):
        if self.game.hit():
            self.update_interface()
        else:
            self.end_game("You've busted! The house wins.")

    def handle_stand(self):
        self.btn_stand.config(state=tk.DISABLED)
        while self.game.dealer_hit():
            self.update_interface()
        self.end_game(self.game.determine_winner())

    def update_interface(self):
        # Clean the widgets off of the frame
        for frame in [self.player_frame, self.deck_frame, self.dealer_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        # SHow the player's cards
        for card in self.game.player.hand.cards:
            img = PhotoImage(file=card.get_image())
            lbl = tk.Label(self.player_frame, image=img)
            lbl.image = img
            lbl.pack(side=tk.LEFT, padx=2)

        # Show the dealer's cards
        for card in self.game.dealer.hand.cards:
            img = PhotoImage(file=card.get_image())
            lbl = tk.Label(self.dealer_frame, image=img)
            lbl.image = img
            lbl.pack(side=tk.LEFT, padx=2)

        # Show the bottom and the  "Hit" buttom
        deck_img = PhotoImage(file=r"/Users/marialeonruiz/Desktop/Programacion_II/Blackjack-game/img/card_back_01.png")
        deck_label = tk.Label(self.deck_frame, image=deck_img, cursor="hand2")
        deck_label.image = deck_img
        deck_label.pack(side=tk.TOP, padx=10)
        deck_label.bind("<Button-1>", self.handle_hit)

        self.btn_stand = tk.Button(self.deck_frame, text="Stand", command=self.handle_stand, state=tk.NORMAL)
        self.btn_stand.pack(side=tk.BOTTOM)

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game_logic = BlackjackGame()
    app = BlackjackGUI(game_logic)
    app.run()