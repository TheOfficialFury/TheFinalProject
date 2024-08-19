#Importing the necessary libraries.
from stockfish import Stockfish
import pandas as pd

#Initialising Stockfish.
stockfish = Stockfish(path="Stockfish-16.1.exe")

#Creating global variables.
appstate = 0
choice = 0
inputFEN = ""
analyseChoice = 0
bestMoves = 0
topMoveList = []

#Main Logic
while True:
    
    #Resetting all the variables
    appstate = 0
    choice = 0
    inputFEN = ""
    analyseChoice = 0
    bestMoves = 0
    topMoveList = []
    
    if appstate == 0:
        
        #Showing text-based menu.
        print('''
              Please choose one of the following - 
              
              1) Analyse Position from FEN
              2) Play against Stockfish 16.1
              3) Analyse position from input
              4) Exit program
              ''')
              
        #Getting input from user.
        try:
            choice = int(input("Please enter the menu item number corresponding to what you want to do - "))
        except:
            print("Please enter a valid input.")
            
        #Evaluating choices.
        if choice == 1:
            appstate = 1
        if choice == 2:
            appstate = 2
        if choice == 3:
            appstate = 3
        if choice == 4:
            break        
        
    if appstate == 1:
        inputFEN = input("Please enter the FEN of the position you wish to evaluate - ")
        if stockfish.is_fen_valid(inputFEN):
            stockfish.set_fen_position(inputFEN)
            while appstate == 1:
                print('''
            Please select one of the followung - 
            
            1) Show board visual (in ASCII format)
            2) Evaluate the position
            3) Show the top 'n' moves in given position
            4) Give the best move in the given position
            5) Exit to Main Menu
                      ''')
                try:
                    analyseChoice = int(input("Please enter the menu item number corresponding to what you want to do - "))
                except:
                    print("Please enter a valid input.")
                
                if analyseChoice == 1:
                    print(stockfish.get_board_visual())
                elif analyseChoice == 2:
                    if stockfish.get_evaluation()["type"] == "cp":
                        print("This position is evaluated as :", (float(stockfish.get_evaluation()["value"]) / 100))
                    elif stockfish.get_evaluation()["type"] == "mate":
                        if stockfish.get_evaluation()["value"] > 0:
                            print("This position is evaluated as forced checkmate in ", stockfish.get_evaluation()["value"])
                        if stockfish.get_evaluation()["value"] < 0:
                            print("This position is evaluated as forced checkmate in ", (stockfish.get_evaluation()["value"] * (-1)))
                elif analyseChoice == 3:
                    try:
                        bestMoves = int(input("Please enter the number of best moves you wish to get - "))
                        print("The top", bestMoves, "moves in this position are as follows - ")
                        topMoveList = stockfish.get_top_moves(bestMoves)
                        for x in topMoveList:
                            print(int(topMoveList.index(x) + 1), "- Move :", x["Move"], "( Evaluation -", (x['Centipawn'] / 100), ")")
                    except:
                        print("Please enter a valid input.")
                elif analyseChoice == 4:
                    print("The best move in this position is -", str(stockfish.get_best_move()))
                elif analyseChoice == 5:
                    appstate = 0