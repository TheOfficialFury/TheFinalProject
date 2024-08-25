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
    howmanymoves = []
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
        
    if appstate == 1:
        
        # Taking FEN input from user.
        inputFEN = input("Please enter the FEN of the position you wish to evaluate - ")
        
        # Validating FEN and proceeding as necessary.
        if stockfish.is_fen_valid(inputFEN):
            
            # After validation, use FEN to set position.
            stockfish.set_fen_position(inputFEN)
            while True:
                
                # Prining text menu for choices.
                print('''
Please select one of the following - 

1) Show board visual (in ASCII format)
2) Evaluate the position
3) Show the top 'n' moves in given position
4) Give the best move in the given position
5) Exit to Main Menu
                      ''')
                      
                # Taking input and proceeding.
                try:
                    analyseChoice = int(input("Please enter the menu item number corresponding to what you want to do - "))
                except:
                    print("Please enter a valid input.")
                
                if analyseChoice == 1:
                    
                    # Prining board in ASCII.
                    print(stockfish.get_board_visual())
                    
                elif analyseChoice == 2:
                    
                    # Printing evaluation based on the type, and formatting output as necessary.
                    if stockfish.get_evaluation()["type"] == "cp":
                        print("This position is evaluated as :", (float(stockfish.get_evaluation()["value"]) / 100))
                    elif stockfish.get_evaluation()["type"] == "mate":
                        if stockfish.get_evaluation()["value"] > 0:
                            print("This position is evaluated as forced checkmate in ", stockfish.get_evaluation()["value"])
                        if stockfish.get_evaluation()["value"] < 0:
                            print("This position is evaluated as forced checkmate in ", (stockfish.get_evaluation()["value"] * (-1)))
                            
                
                elif analyseChoice == 3:
                    
                    # Taking number of best moves required and querying for the said number of best moves.
                    try:
                        bestMoves = int(input("Please enter the number of best moves you wish to get - "))
                        print("The top", bestMoves, "moves in this position are as follows - ")
                        topMoveList = stockfish.get_top_moves(bestMoves)
                        for x in topMoveList:
                            
                            # Outputting top moves with relevant formatting and evaluation.
                            print(int(topMoveList.index(x) + 1), "- Move :", x["Move"], "( Evaluation -", (x['Centipawn'] / 100), ")")
                    except:
                        print("Please enter a valid input.")
                elif analyseChoice == 4:
                    
                    # Outputting best move.
                    print("The best move in this position is -", str(stockfish.get_best_move()))
                elif analyseChoice == 5:
                    
                    # Break loop.
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
                    seeboard()             
      
    if appstate == 3:
        
        # Print the menu.
        print('''
Please choose one of the following - 

1) Enter game move-by-move
2) Import from CSV file (must be in correct format)
              ''')
              
        #Getting input from user.
        try:
            inputChoice = int(input("Please enter the menu item number corresponding to what you want to do - "))
        except:
            print("Please enter a valid input.")
        
        # Regardless of choice, some part of the code between the two options is common.
        if inputChoice == 1 or inputChoice == 2:
            
            # Some code specific to the second option.
            if inputChoice == 2:
                
                # Grabbing path to CSV.
                path = input("Please enter the path to the CSV file (or type 'exit' to leave this section) - ")
                
                # Adding option to abort.
                if path == "exit":
                    pass
                
                # For all inputs apart from abortion, assume path is being provided.
                else:
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
                            
                            # Show erroe message.
                            print("Please enter a valid path or CSV, or type 'exit' to exit this section.")
                            break
                        
            # Start loop once all prior conditions are fulfilled (if any).
            while True:
                
                # Asking for input.
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
                    
                    # Recording moves.
                    if moveIter == 0:  
                        moveFrame.append([moveChoice])
                        moveIter = 1
                    elif moveIter == 1: 
                        moveFrame[-1].append(moveChoice)
                        moveIter = 0
                    
                    # Evaluation
                    if stockfish.get_evaluation()['type'] == 'cp':
                        
                        # If evaluation is in centipawns, then format output as follows.
                        print("Evaluation -", str(stockfish.get_evaluation()['value'] / 100))
                        print("Best move -", str(stockfish.get_best_move()))
                        
                    elif checkformate():
                        
                        # Check for checkmate and proceed to ask for saving as CSV.
                        print("Checkmate!")
                        print(stockfish.get_board_visual())
                        
                        # Taking confirmation for save to CSV functionality.
                        if input("Please enter 1 if you would like to save the moves in this game as CSV - ") == "1":
                            
                            # Convert move data to Dataframe and export to CSV.
                            moveFrame = pd.DataFrame(moveFrame, columns=["White", "Black"])
                            while True:
                                try:
                                    moveFrame.to_csv(str((input("Please enter a filename - ") + ".csv")))
                                    print("Saved successfully!")
                                    break
                                except:
                                    print("Please enter a valid input.")
                            
                            # Break loop.
                            break
                        
                        else:
                            print("Exiting without saving...")
                            break
                            
                    elif stockfish.get_evaluation()['type'] == 'mate':
                        
                        # For evalution of the 'mate' proceed as follows...
                        print("Evaluation - Mate in", str(stockfish.get_evaluation()['value']))
                        print("Best move -", str(stockfish.get_best_move()))
                    
                    # Print the board.
                    print(stockfish.get_board_visual())
                
                elif str(moveChoice.lower()) == 'eval':
                    
                    # Reset the board using the FEN of a blank board.
                    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                    
                    # Taking backup of move data.
                    moveList = moveFrame
                    
                    #COnverting List-of-Lists to DataFrame.
                    moveFrame = pd.DataFrame(moveFrame)
                    
                    # Iterating through move data and evaluating each position.
                    for x in moveFrame.T:
                        if list(moveFrame.T[x])[0] != np.NaN:
                            stockfish.make_moves_from_current_position([str(list(moveFrame.T[x])[0])])
                            evalMove.append(stockfish.get_evaluation())
                            if type(list(moveFrame.T[x])[1]) == str:
                                stockfish.make_moves_from_current_position([str(list(moveFrame.T[x])[1])])
                                evalMove.append(stockfish.get_evaluation())
                    
                    # Reverting to List-of-Lists format.
                    moveFrame = moveList
                    
                    # Converting all evaluations to centipawn format.
                    for x in evalMove:
                        if x['type'] == 'mate':
                            evalMove[evalMove.index(x)] = 100.0
                        else:
                            evalMove[evalMove.index(x)] = x['value'] / 100
                    
                    # Creating a list that will act as x-axis of plot.
                    for x in evalMove:
                        howmanymoves.append(int(evalMove.index(x) + 1))
                        
                    # Plotting graph and displaying it.
                    plt.plot(howmanymoves, evalMove, marker="s")
                    plt.title("Evaluation of position for every move")
                    plt.xlabel("Moves")
                    plt.ylabel("Evaluation")
                    plt.show()
                    
                else:
                    print("Please enter a valid move/command.")