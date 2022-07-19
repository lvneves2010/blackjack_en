import random

import os
clear = lambda: os.system('cls')
clear()

playing = False
global chip_pool
chip_pool = 100
bet = 1
restart_phrase = "Digite 'd' para embaralhar de novo, 'r' para reiniciar o numero de fichas ou 'q' para sair."
naipes = ('Copas', 'Ouros', 'Paus', 'Espadas')
val_facial = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
val_carta = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

class Carta:
    def __init__(self, naipe, face):
        self.face = face
        self.naipe = naipe
        
    def __str__(self):
        return self.face + " de " + self.naipe

    def pega_face(self):
        return self.face

    def pega_naipe(self):
        return self.naipe

    def tirar(self):
        print(self.face + " de " + self.naipe)
    
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

        return "Sua mao tem agora {}".format(mao_comp)

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
        return "O baralho tem " + baralho_comp

def fazer_aposta():
    global bet
    bet = 0

    print("Quanto voce quer apostar? (Digite um numero inteiro por favor)")

    while bet == 0:
        bet_comp = input()
        bet_comp = int(bet_comp)
        if bet_comp >= 1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            if chip_pool != 0:
                print("Aposta invalida, Voce tem somente " + str(chip_pool) + " fichas sobrando")
            else:
                print("Voce não tem mais fichas , o jogo será reiniciado")
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

    resultado = "Continuar ou parar? Para ganhar mais uma carta digite 'c' ou então 'p' para dar a vez ao Dealer"

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
            resultado = "Estourou!! DEALER GANHOU!!! " + restart_phrase
            print("")
            chip_pool -= bet
            playing = False

    else:
        resultado = "Desculpe , nao podemos continuar " + restart_phrase

    game_step()

def parar():
    global resultado, playing, baralho, mao_jogador, mao_dealer, chip_pool, bet

    if playing == False:
        if mao_jogador.calc_valor() > 0:
            resultado = " Desculpe, nao podemos parar"

    else:
        while mao_dealer.calc_valor() < 17:
            mao_dealer.carta_add(baralho.dar_cartas())

        if mao_dealer.calc_valor() > 21:
            resultado = "Dealer estourou!! VOCE GANHOU!!! " + restart_phrase
            print("")
            chip_pool += bet
            playing = False

        elif mao_dealer.calc_valor() < mao_jogador.calc_valor():
            resultado = " VOCE GANHOU !!!! " + restart_phrase
            print("")
            chip_pool += bet
            playing = False

        elif mao_dealer.calc_valor() == mao_jogador.calc_valor():
            resultado = "EMPATE !!! " + restart_phrase
            print("")
            playing = False

        else:
            resultado = "DEALER GANHOU!! " + restart_phrase
            print("")
            chip_pool -=bet
            playing = False
    game_step()

def game_step():
    print("---------------------------------------------------------------------")
    print("")
    print("Mao do jogador é: " )
    mao_jogador.tirar(oculto = False)
    print("Mao do Jogador é: " + str(mao_jogador.calc_valor()))
    
    print("")
    print("Mao do Dealer é: ")
    mao_dealer.tirar(oculto = False)
    print("Mao do Dealer é: " + str(mao_dealer.calc_valor()))

    if playing == False:
        print("")
        print("totals de fichas agora é: " + str(chip_pool))
        print("")

    print(resultado)

    player_input()

def fim_de_jogo():
    clear()
    print("")
    print("Obrigado por Jogar!!! ")
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
        print("Opcao Invalida.... Digite 'c' 'p' 'd' ou 'q'")
        player_input()

def intro():
    global chip_pool
    chip_pool = 100
    statement = '''Bem vindo  ao jogo de Black Jack!!!
    
      Tente chegar o mais proximo possivel de 21 sem estourar!!
      Dealer vai continuar até atingir 17, Ases contam como 1 ou 11. Voce começa com 100 fichas.
      Boa Sorte !!!
      '''
    print(statement)
    print("totals de fichas: " + str(chip_pool))
    print("")

def reset():
    intro()

baralho = Baralho()
baralho.embaralhar()

mao_jogador = Mao()
mao_dealer = Mao()

intro()
dar_as_cartas()