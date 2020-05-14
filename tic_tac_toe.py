
import time
from src.computer_t_gates import computer_ai

board = [" " for x in range(10)]
count = 0


def printBoard():
    print("   |   |   ")
    print(" " + board[0] + " | " + board[1] + " | " + board[2] + "  ")
    print("---|---|---")
    print("   |   |")
    print(" " + board[3] + " | " + board[4] + " | " + board[5] + "  ")
    print("---|---|---")
    print("   |   |")
    print(" " + board[6] + " | " + board[7] + " | " + board[8] + "  ")


def check_win(board):
    for indx in [0, 3, 6]:
        if board[indx] and (board[indx] == board[indx + 1] == board[indx + 2]):
            return board[indx]
    for indx in [0, 1, 2]:
        if board[indx] and (board[indx] == board[indx + 3] == board[indx + 6]):
            return board[indx]
    if board[0] and (board[0] == board[4] == board[8]):
        return board[0]
    elif board[2] and (board[2] == board[4] == board[6]):
        return board[2]
    return -1 if any([x is " " for x in board]) else 0


def player_round():
    global board
    choice = input("Please choose an empty space for X. ").upper()
    choice = int(choice)
    if board[choice] == " ":
        board[choice] = "X"
    else:
        print("Sorry, that space is not empty!")
        player_round()
        time.sleep(1)

def computer_round():
    global board
    com = computer_ai(board)
    com.best_move()
    num = com.move
    board[num] = "O"



while True:
    printBoard()
    print("Player round:")
    player_round()
    printBoard()
    if check_win(board) == 0:
        print("draw")
        break
    elif check_win(board) == "X":
        print("The winner is Player")
        break
    print("computer round:")
    computer_round()

    printBoard()
    if check_win(board) == 0:
        print("draw")
        break
    elif check_win(board) == "O":
        print("The winner is computer")
        break



