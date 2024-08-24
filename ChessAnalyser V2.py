#Importing the necessary libraries.
from stockfish import Stockfish
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Initialising Stockfish.
stockfish = Stockfish(path="Stockfish-16.1.exe")


# Custom function that checks for checkmate in a position.
def checkformate():
    if stockfish.get_evaluation()["type"] == 'mate' and stockfish.get_evaluation()["value"] == 0:
        return True
    else:
        return False

def seeboard():
    if colorCharacter == "b":
        print(stockfish.get_board_visual(perspective_white=False))
    else:
        print(stockfish.get_board_visual())

#Main Logic
while True:
    
    #Resetting all the variables
    appstate = 0
    choice = 0
    inputFEN = ""
    analyseChoice = 0
    bestMoves = 0
    topMoveList = []
    playChoice = 0
    colorChoice = 0
    moveChoice = ""
    inputChoice = 0
    moveIter = 0
    moveFrame = []
    CSVmove = ""
    moveList = []
    evalMove = []
    howmanymoves = 0
    
    importChoice = 0
    colorCharacter = ""
    
    # Resetting board position.
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    
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
                    
    if appstate == 2:
        
        #Showing text-based menu.
        print('''
Please choose one of the following - 

1) Play from starting position
2) Play from custom position
              ''')
              
        #Getting input from user.
        try:
            playChoice = int(input("Please enter the menu item number corresponding to what you want to do - "))
        except:
            print("Please enter a valid input.")
        
        # Asking for color choice.
        if playChoice == 1 or playChoice == 2:
            print('''
Please choose one of the following -

1) White
2) Black
                  ''')
                  
            # Taking input.
            try:
                colorChoice = int(input("Please enter the menu item number corresponding to what you want to do - "))
            except:
                print("Please enter a valid input.")
                
            if colorChoice == 1:
                colorCharacter = "w"
            elif colorChoice == 2:
                colorCharacter = "b"
            
            if playChoice == 2:
                print('''
Please select one of the following - 

1) Use an FEN
2) Import from CSV
                     ''')
            
                importChoice = int(input("Please enter the menu item number corresponding to what you want to do - "))
                if importChoice == 1:
                    while True:
                        inputFEN = input("Please enter an FEN - ")
                        if stockfish.is_fen_valid(inputFEN):
                            stockfish.set_fen_position(inputFEN)
                            if inputFEN[-12] != colorCharacter:
                                seeboard()
                                print("Stockfish plays the move -", stockfish.get_best_move())   
                                stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                                seeboard()
                            break
                        else:
                            print("Please enter a valid FEN.")
                elif importChoice == 2:
                    # Grabbing path to CSV.
                    path = input("Please enter the path to the CSV file - ")
                    
                    while True:
                        
                        # Check for path accuracy import data.
                        try:
                            CSVmove = pd.read_csv(path)
                            
                            # Convert data to usable format.
                            for x in CSVmove.T:
                                if list(CSVmove.T[x])[1] != np.NaN:
                                    stockfish.make_moves_from_current_position([str(list(CSVmove.T[x])[1])])
                                    moveFrame.append([str(list(CSVmove.T[x])[1])])
                                    if type(list(CSVmove.T[x])[2]) == str:
                                        stockfish.make_moves_from_current_position([str(list(CSVmove.T[x])[2])])
                                        moveFrame[-1].append(str(list(CSVmove.T[x])[2]))
                            
                            # No need to loop again.
                            break
                        
                        except:
                            
                            # Show error message.
                            print("Please enter a valid path or CSV.")
                            break
                    
                    seeboard()
                    
                    if colorCharacter == "w" and len(moveFrame[-1]) == 1:
                        print("Stockfish plays the move -", stockfish.get_best_move())    
                        stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                        seeboard()
                    elif colorCharacter == "b" and len(moveFrame[-1]) == 2:
                        print("Stockfish plays the move -", stockfish.get_best_move())
                        stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                        seeboard()
                    
            
                while True:
                    # Asking for input.
                    if moveIter == 0:
                        moveChoice = input("Please enter your move (or type 'help' if you dont know what to do) - ")
                        # Display help message.
                        if str(moveChoice.lower()) == 'help':
                            print('''
Please enter moves in the format [present square of piece][future square of piece]. For example, to move a pawn to e4 from e2, enter 'e2e4'. Moves need not specify the piece being moved. Only the squares from where to where the piece is moving.

To see a comprehensive analysis history of all the moves played so far, type 'eval'.

To exit play, please enter 'exit'. To this help at any point during the game, type 'help'.
                            ''')
                            
                        # Exit option.
                        elif str(moveChoice.lower()) == 'exit':
                            break
                        
                        # Incase an actual move is entered, do the following.
                        elif stockfish.is_move_correct(moveChoice):
                            
                            # Update the board.
                            stockfish.make_moves_from_current_position([str(moveChoice)])
                                
                        moveIter = 1
                    elif moveIter == 1:
                        print("Stockfish plays the move -", stockfish.get_best_move())   
                        stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                        moveIter = 0
                    
                    # Print the board.
                    print(stockfish.get_board_visual())           