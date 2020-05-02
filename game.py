'''
TODO:
In how_many_players, make it so entering a non int results in being reprompted, not an error
Figure out a way to get a player's hand to print side by side for better readibility
'''

import random

# allows you to make Card objects that store the image of the card, its rank, and its value
class Card:
  def __init__(self, picture, rank, value):
    self.picture = picture
    self.rank = rank
    self.value = value


# allows you to make Player objects that store the player's name, hand, and their books
class Player:
  def __init__(self, name, hand, books):
    self.name = name
    self.hand = hand
    self.books = books


# populates an empty list with Card objects to make a traditional deck
def create_deck():
  '''
  return deck: a list of 52 standard cards
  '''
  deck = []
  rank = ['2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']
  value = [2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]

  # clubs
  for i, each in enumerate(rank):
      deck.append(Card(' ______\n|      |\n|♣     |\n|  {}   |\n|     ♣|\n|______|'.format(each), each, value[i]))
  deck.append(Card(' ______\n|      |\n|♣     |\n|  10  |\n|     ♣|\n|______|', '10', 10))
  
  # spades
  for i, each in enumerate(rank):
      deck.append(Card(' ______\n|      |\n|♠     |\n|  {}   |\n|     ♠|\n|______|'.format(each), each, value[i]))
  deck.append(Card(' ______\n|      |\n|♠     |\n|  10  |\n|     ♠|\n|______|', '10', 10))

  # hearts
  for i, each in enumerate(rank):
      deck.append(Card(' ______\n|      |\n|♥     |\n|  {}   |\n|     ♥|\n|______|'.format(each), each, value[i]))
  deck.append(Card(' ______\n|      |\n|♥     |\n|  10  |\n|     ♥|\n|______|', '10', 10))

  # diamonds
  for i, each in enumerate(rank):
      deck.append(Card(' ______\n|      |\n|♦     |\n|  {}   |\n|     ♦|\n|______|'.format(each), each, value[i]))
  deck.append(Card(' ______\n|      |\n|♦     |\n|  10  |\n|     ♦|\n|______|', '10', 10))

  return deck


# shuffles the deck by selecting a random card and making it swap places with the card at index i
def shuffle(deck):
  """
  param deck: a list of 52 standard cards
  """
  for i in range(len(deck)):
      card = random.choice(deck)
      temp = deck.index(card)
      deck[temp] = deck[i]
      deck[i] = card
  

# determines how many people are playing, has to be between 2 and 6
def how_many_players():
  '''
  return numberOfPlayers: variable representing how many people are going to play the game
  '''
  numberOfPlayers = 0
  while numberOfPlayers < 2 or numberOfPlayers > 6:
      numberOfPlayers = int(input('How many people are playing? (Must be 2-6) '))
  return numberOfPlayers


# populates an empty list with Player objects, setting their names and leaving hand and books as empty lists
def names(numberOfPlayers):
  '''
  param numberOfPlayers: variable representing how many people are playing
  return players: a list of Player objects
  '''
  players = []
  #start is 1 and end is numberOfPlayers + 1 so there isn't a Player 0
  for i in range(1, numberOfPlayers + 1):
      name = input('Player {}, what is your name? '.format(i))
      players.append(Player(name, [], []))

  return players


# deals 7 cards to each player if 2 or 3 are playing, deals 5 if more than 3 playing by appending the appropriate amount of cards to each player's hand
def deal(deck, numberOfPlayers, players):
  '''
  param deck: a list of 52 cards shuffled
  param numberOfPlayers: the number of people playing
  param players: a list of Player objects
  '''
  if numberOfPlayers < 4:
    for i in range(numberOfPlayers):
      for x in range(7):
        players[i].hand.append(deck[0])
        del deck[0]
  else:
    for i in range(numberOfPlayers):
      for x in range(5):
        players[i].hand.append(deck[0])
        del deck[0]

           
# sorts the players' hands so that they are from lowest value to highest value
def sort(players):
  '''
  param players: list of Player objects
  '''
  for each in players:
    # the outer loop causes the inner loop to look at less of the hand being sorted each time since the highest value cards will reach their spots first
    for x in range(len(each.hand) - 1, 0, -1):
      for y in range(x):
        if each.hand[y].value > each.hand[y + 1].value:
          each.hand[y], each.hand[y + 1] = each.hand[y + 1], each.hand[y]
  

# prints the game: the current player's cards face up, the other players' cards facedown, each players' books, and how many cards are left in the deck
def print_game(players, deck, turn):
  '''
  param players: list of Player objects
  param deck: list of cards left in the deck
  param turn: variable that helps determine which player's turn it is 
  '''
  for each in players:
    print(each.name)
    for x in each.hand:
      if each == players[turn]:
        print(x.picture)
      else:
        print(' ______\n|//////|\n|//////|\n|//////|\n|//////|\n|//////|')
    print(each.name + '\'s Books')
    for y in each.books:
      print('')
      for z in y:
        print(z.picture)
  print('Cards Left in Deck: ' + str(len(deck)))


# allows a player to select which rank they are looking for and which player they are targeting
def select(players, turn):
  '''
  param players: list of Player objects
  param turn: variable that helps determine which player's turn it is
  return rank: the player's chosen rank
  return playerindex: the index of the chosen player in the list players
  '''
  x = False
  while x == False:
    rank = input('{}, what rank of cards are you looking for? '.format(players[turn].name))
    # they must actually have at least one of the rank they are asking for in their hand
    for each in players[turn].hand:
      if each.rank == rank:
        x = True
             
  y = False
  while y == False:
    player = input('Which player would you like to ask for cards? ')
    for each in players:
      if each.name == player and players[turn].name != player:
        y = True
        playerindex = players.index(each)

  return rank, playerindex


# determines whether the selected rank is in the selected player's hand, if so, it takes that(those) card(s) and if not, signals to pass the turn to the next player
def take(players, rank, playerindex, turn, streak):
  '''
  param players: list of Player objects
  param rank: the player's chosen rank
  param playerindex: the index of the chosen player in the list players
  param turn: variable that helps determine which player's turn it is 
  param streak: determines whether or not to let the player to continue asking for cards
  return streak: returns True if the player is allowed to continue asking for cards, returns False if the player's turn should end
  '''
  hit = 0
  # reversed because if it went forwards through the list, removing cards would cause other cards to be skipped over
  for each in reversed(players[playerindex].hand):
    if each.rank == rank:
      players[turn].hand.append(each)
      players[playerindex].hand.remove(each)
      hit = 1
      
  if hit == 0:
    streak = False

  return streak


# tells the player to "Go Fish" and gives them one card from the deck
def go_fish(players, turn, deck):
  '''
  param players: list of Player objects
  param turn: variable that helps determine which player's turn it is 
  param deck: list of cards left in the deck
  '''

  print("╔══╗╔═╗    ╔══╗╔══╗╔══╗╔╗╔╗\n║╔═╣║║║    ║═╦╝╚║║╝║══╣║╚╝║\n║╚╗║║║║    ║╔╝ ╔║║╗╠══║║╔╗║\n╚══╝╚═╝    ╚╝  ╚══╝╚══╝╚╝╚╝\n ")
  players[turn].hand.append(deck[0])
  del deck[0]


# checks if the player can create a book by looking for 4 cards of the same rank in a row, if so, it makes a list of those cards and then appends that list to the books list in the associated Player object and deletes the 4 cards from the players hand
def create_books(players, turn):
  '''
  param players: list of Player objects
  param turn: variable that helps determine which player's turn it is 
  '''

  looking = True
  x = 0
  while x < len(players[turn].hand) - 3 and looking == True:
    if players[turn].hand[x].rank == players[turn].hand[x + 1].rank and players[turn].hand[x].rank == players[turn].hand[x + 2].rank and players[turn].hand[x].rank == players[turn].hand[x + 3].rank:
      
      One = players[turn].hand[x]
      Two = players[turn].hand[x + 1]
      Three = players[turn].hand[x + 2]
      Four = players[turn].hand[x + 3]

      book = [One, Two, Three, Four]
      players[turn].books.append(book)

      players[turn].hand.remove(One)
      players[turn].hand.remove(Two)
      players[turn].hand.remove(Three)
      players[turn].hand.remove(Four)

      looking = False
    
    x += 1
        

# checks if the deck or any player's hand is empty, if so returns True which will signal that the game should end
def game_over(players, deck):
  '''
  param players: list of Player objects
  param deck: list of cards left in the deck
  return: returns True if the game should end
  '''
  if len(deck) == 0:
    return True
  else:
    for each in players:
      if len(each.hand) == 0:
        return True
  

# determines which player(s) won the game by appending the amount of books each player had to an empty list and then using max() to find who had the most. it then deletes this number from the list and looks to see if any other players had that many books
def who_won(players):
  '''
  param players: list of Player objects
  '''
  booklist = []

  for each in players:
    booklist.append(len(each.books))

  large = max(booklist)
  index = booklist.index(large)

  print(players[index].name + ' is the winner!')

  del booklist[index]

  for i in range(len(booklist)):
    if booklist[i] == large:
      # plus 1 to account for the removed element
      print(players[i + 1].name + ' is also a winner!')


def main():

  deck = create_deck()
  shuffle(deck)

  numberOfPlayers = how_many_players()
  players = names(numberOfPlayers)

  deal(deck, numberOfPlayers, players)
  
  sort(players)  

  break_a = False
  break_b = False
  # use break_a to break out of this loop
  # will loop until the game is over, resets the for loop so it goes back to the first player after the last player finishes their turn
  while True:

    #use break_b to break out of this loop
    # the variable turn represents the index of the current player in the list players, basically this loop is what causes the turns to happen
    for turn in range(numberOfPlayers):

        # streak indicates whether the current player's turn should continue or end
        streak = True
        # this loop is what allows a player to continue guessing as long as they are right
        while streak == True:

          print_game(players, deck, turn)
        
          rank, playerindex = select(players, turn)
          streak = take(players, rank, playerindex, turn, streak)

          sort(players)

          # 4 cards in a book so no point in calling create_books if there is less than 4 cards in the player's hand, also it will cause the index to go out of range
          if len(players[turn].hand) >= 4:
            create_books(players, turn)

          if game_over(players, deck) == True:
            break_a = True
            break_b = True  
            break

        if break_b == True:
          break

        go_fish(players, turn, deck)

        sort(players)

        if len(players[turn].hand) >= 4:
            create_books(players, turn)

        if game_over(players, deck) == True:
          break_a = True  
          break

    if break_a == True:
      break

  who_won(players)

if __name__ == '__main__':
    main()
