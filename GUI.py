import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
import modules as m

# Main PyQt5 Blackjack Class
class BlackjackGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack")
        self.deck = m.create_deck()
        self.player_hand = []
        self.dealer_hand = []

        # Layouts
        self.main_layout = QVBoxLayout()
        self.player_layout = QHBoxLayout()
        self.dealer_layout = QHBoxLayout()
        self.controls_layout = QHBoxLayout()

        # Labels
        self.player_label = QLabel("Player's Hand:")
        self.dealer_label = QLabel("Dealer's Hand:")

        self.player_score_label = QLabel("Player Score: 0")
        self.dealer_score_label = QLabel("Dealer Score: 0")

        # Buttons
        self.hit_button = QPushButton("Hit")
        self.stand_button = QPushButton("Stand")
        self.new_game_button = QPushButton("New Game")

        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)
        self.new_game_button.clicked.connect(self.new_game)

        # Add widgets to layouts
        self.main_layout.addWidget(self.dealer_label)
        self.main_layout.addLayout(self.dealer_layout)
        self.main_layout.addWidget(self.dealer_score_label)

        self.main_layout.addWidget(self.player_label)
        self.main_layout.addLayout(self.player_layout)
        self.main_layout.addWidget(self.player_score_label)

        self.controls_layout.addWidget(self.hit_button)
        self.controls_layout.addWidget(self.stand_button)
        self.controls_layout.addWidget(self.new_game_button)
        self.main_layout.addLayout(self.controls_layout)

        self.setLayout(self.main_layout)
        self.new_game()

    def load_card_image(self, card):
        """Load a card image"""
        card_key = f"{card['rank']}_of_{card['suit']}.png"
        return QPixmap(f"images/{card_key}")

    def display_cards(self, layout, hand):
        """Display cards in the given layout"""
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        for card in hand:
            card_image = self.load_card_image(card)
            card_label = QLabel()
            card_label.setPixmap(card_image.scaled(80, 120))
            layout.addWidget(card_label)

    def update_ui(self):
        """Update the UI with current hand states"""
        self.display_cards(self.player_layout, self.player_hand)
        self.display_cards(self.dealer_layout, self.dealer_hand)

        self.player_score_label.setText(f"Player Score: {m.calculate_score(self.player_hand)}")
        self.dealer_score_label.setText(f"Dealer Score: {m.calculate_score(self.dealer_hand)}")

    def hit(self):
        """Player hits and draws a card"""
        self.player_hand.append(self.deck.pop())
        self.update_ui()
        if m.calculate_score(self.player_hand) > 21:
            QMessageBox.information(self, "Game Over", "Player busted! Dealer wins.")
            self.end_game()

    def stand(self):
        """Player stands and dealer plays"""
        self.dealer_hand = m.dealer_play(self.deck, self.dealer_hand)
        self.update_ui()
        result = m.determine_winner(self.player_hand, self.dealer_hand)
        QMessageBox.information(self, "Game Over", result)
        self.end_game()

    def new_game(self):
        """Start a new game"""
        self.deck = m.create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop()]
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.update_ui()

    def end_game(self):
        """End the game and disable controls"""
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = BlackjackGame()
    game.resize(800, 600)
    game.show()
    sys.exit(app.exec_())
