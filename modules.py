import random

# Create Deck
def create_deck():
    # Create of sub lists for the final deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen',
             'King', 'Ace']
    # Create deck as a dictionary
    deck_of_cards = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
    # Shuffle Deck
    random.shuffle(deck_of_cards)
    # Return Deck
    return deck_of_cards

# Calculate score of hand
def calculate_score(hand):
    # Initialize variables
    score = 0
    aces = 0
    # Calculate score
    for card in hand:
        rank = card['rank']
        if rank in ['Jack', 'Queen', 'King']:
            # if Jack, Queen, King add 10 score
            score += 10
        elif rank == 'Ace':
            # if Ace add one to initial variable
            aces += 1
            # Calculate aces as 11 score initially
            score += 11
        else:
            # if it is normal card add value of card at score
            score += int(rank)

    # Adjust the score of Aces if necessary
    while score > 21 and aces:
        score -= 10
        aces -= 1
    #return the score
    return score


# Check state of game according to score
def check_blackjack_or_bust(hand):
    # Calculate score
    score = calculate_score(hand)

    if score == 21:
        return "Blackjack"
    elif score > 21:
        return "Bust"
    # If score below 21 continue
    return "Continue"


# Deal card
def deal_card(deck):
    return deck.pop() if deck else None


# Play of dealer
def dealer_play(deck, dealer_hand):
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
    return dealer_hand


# Determine winner
def determine_winner(player_hand, dealer_hand):
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if player_score > 21:
        return "Dealer wins (Player busted)"
    elif dealer_score > 21:
        return "Player wins (Dealer busted)"
    elif player_score > dealer_score:
        return "Player wins"
    elif player_score < dealer_score:
        return "Dealer wins"
    else:
        return "Tie"



if __name__ == "__main__":
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print("Player's Initial Hand:", player_hand)
    print("Dealer's Initial Hand:", dealer_hand[:1], "Hidden")

    # Player's turn
    while True:
        print("\nPlayer's Hand:", player_hand, "Score:",
              calculate_score(player_hand))
        status = check_blackjack_or_bust(player_hand)
        if status == "Blackjack":
            print("Player has Blackjack!")
            break
        elif status == "Bust":
            print("Player busted!")
            break

        action = input("Do you want to Hit or Stand? (h/s): ").lower()
        if action == 'h':
            player_hand.append(deal_card(deck))
        elif action == 's':
            break

    # Dealer's turn
    if check_blackjack_or_bust(player_hand) != "Bust":
        dealer_hand = dealer_play(deck, dealer_hand)

    print("\nDealer's Hand:", dealer_hand, "Score:",
          calculate_score(dealer_hand))
    print(determine_winner(player_hand, dealer_hand))
