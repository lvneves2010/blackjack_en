import random

import os
clear = lambda: os.system('cls')
clear()

playing = False
global chip_pool
chip_pool = 100
bet = 1
restart_phrase = "Type 'd' to deal again, 'r' to restart the stack or  'q' to quit."
naipes = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
val_facial = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
val_carta = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

class Carta:
    def __init__(self, naipe, face):
        self.face = face
        self.naipe = naipe
        
    def __str__(self):
        return self.face + " of " + self.naipe

    def pega_face(self):
        return self.face

    def pega_naipe(self):
        return self.naipe

    def tirar(self):
        print(self.face + " of " + self.naipe)
    
class Mao:
    def __init__(self):
        self.cartas = []
        self.valor = 0
        self.As = False

    def __str__(self):
        mao_comp = ""

        for carta in self.cartas:
            carta_nome = carta.__str__()
            mao_comp += " " + carta_nome

        return "Your Hand now: {}".format(mao_comp)

    def carta_add(self, carta):
        self.cartas.append(carta)

        if carta.face == 'A':
            self.As = True
        self.valor += val_carta[carta.face]
    
    def calc_valor(self):
        if (self.As == True and self.valor < 12):
            return self.valor + 10
        else: 
            return self.valor

    def tirar(self, oculto):
        if oculto == True and playing == True:
            starting_carta = 1
        else:
            starting_carta = 0
        for x in range (starting_carta, len(self.cartas)):
            self.cartas[x].tirar()

class Baralho:
    def __init__(self):
        self.baralho = []

        for naipe in naipes:
            for face in val_facial:
                self.baralho.append(Carta(naipe, face))

    def embaralhar(self):
        random.shuffle(self.baralho)

    def dar_cartas(self):
        carta_solta = self.baralho.pop()
        return carta_solta

    def __str__(self):
        baralho_comp = "" 
        for carta in self.baralho:
            baralho_comp += " " + carta.__str__()
        return "The Deck Has: " + baralho_comp

def fazer_aposta():
    global bet
    bet = 0

    print("Waht is your bet? (Please type an integer )")

    while bet == 0:
        bet_comp = input()
        bet_comp = int(bet_comp)
        if bet_comp >= 1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            if chip_pool != 0:
                print("Invalid bet, You only have " + str(chip_pool) + " chips left")
            else:
                print("You are out of chips , the game will be restarted")
                reset()
                dar_as_cartas()


def dar_as_cartas():
    global resultado, playing, baralho, mao_jogador, mao_dealer, chip_pool, bet

    baralho = Baralho()
    baralho.embaralhar()

    fazer_aposta()

    mao_jogador = Mao()
    mao_dealer = Mao()

    mao_jogador.carta_add(baralho.dar_cartas())
    mao_jogador.carta_add(baralho.dar_cartas())

    mao_dealer.carta_add(baralho.dar_cartas())
    mao_dealer.carta_add(baralho.dar_cartas())

    print("")

    resultado = "Hit or Fold? To get another card type 'c' or press 'p' to pass to the Dealer"

    playing = True
    game_step()

def continuar():
    global resultado, playing, baralho, mao_jogador, mao_dealer, chip_pool, bet

    if playing:
        if mao_jogador.calc_valor() <= 21:
            mao_jogador.carta_add(baralho.dar_cartas())
        #print("e %s"  %mao_jogador)
        print(mao_jogador)

        if mao_jogador.calc_valor() > 21:
            resultado = "Bust!! DEALER WINS!!! " + restart_phrase
            print("")
            chip_pool -= bet
            playing = False

    else:
        resultado = "Sorry , can't continue " + restart_phrase

    game_step()

def parar():
    global resultado, playing, baralho, mao_jogador, mao_dealer, chip_pool, bet

    if playing == False:
        if mao_jogador.calc_valor() > 0:
            resultado = " Sorry, can't stop"

    else:
        while mao_dealer.calc_valor() < 17:
            mao_dealer.carta_add(baralho.dar_cartas())

        if mao_dealer.calc_valor() > 21:
            resultado = "Dealer bust!! YOU WIN!!! " + restart_phrase
            print("")
            chip_pool += bet
            playing = False

        elif mao_dealer.calc_valor() < mao_jogador.calc_valor():
            resultado = " YOU WIN !!!! " + restart_phrase
            print("")
            chip_pool += bet
            playing = False

        elif mao_dealer.calc_valor() == mao_jogador.calc_valor():
            resultado = "TIE !!! " + restart_phrase
            print("")
            playing = False

        else:
            resultado = "DEALER WINS!! " + restart_phrase
            print("")
            chip_pool -=bet
            playing = False
    game_step()

def game_step():
    print("---------------------------------------------------------------------")
    print("")
    print("player's hand: " )
    mao_jogador.tirar(oculto = False)
    print("player's hand: " + str(mao_jogador.calc_valor()))
    
    print("")
    print("dealer's hand: ")
    mao_dealer.tirar(oculto = False)
    print("dealer's hand: " + str(mao_dealer.calc_valor()))

    if playing == False:
        print("")
        print("total chips now: " + str(chip_pool))
        print("")

    print(resultado)

    player_input()

def fim_de_jogo():
    clear()
    print("")
    print("Thanks for playing!!! ")
    print("")
    print('        ****     ')
    print('      **    **   ')
    print('    **        ** ')
    print('   *            *')
    print('   *   **  **   *')
    print('   *   **  **   *')
    print('   *            *')
    print('   *            *')
    print('   *  *      *  *')
    print('   *   *    *   *')
    print('   *    ****    *')
    print('    **   **   ** ')
    print('      **    **   ')
    print('        ****     ')
    print("")
    exit()

def player_input():
    plin = input().lower()

    if plin == 'c':
        continuar()
    elif plin == 'p':
        parar()
    elif plin == 'd':
        dar_as_cartas()
    elif plin == 'q':
        fim_de_jogo()
    elif plin == 'r':
        intro()
        dar_as_cartas()
    else:
        print("Not a valid option.... Type 'c' 'p' 'd' or 'q'")
        player_input()

def intro():
    global chip_pool
    chip_pool = 100
    statement = '''Welcome to the game of Black Jack!!!
    
      Try to get as close to 21 as possible without popping.!!
      Dealer will continue until reaching 17, Aces count as 1 or 11. You start with 100 chips.
      Good Luck !!!
      '''
    print(statement)
    print("total chips now: " + str(chip_pool))
    print("")

def reset():
    intro()

baralho = Baralho()
baralho.embaralhar()

mao_jogador = Mao()
mao_dealer = Mao()

intro()
dar_as_cartas()