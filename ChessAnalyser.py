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
playChoice = 0
colorChoice = 0
moveChoice = ""
inputChoice = 0
moveIter = 0
moveFrame = []

def checkformate():
    if stockfish.get_evaluation()["type"] == 'mate' and stockfish.get_evaluation()["value"] == 0:
        return True
    else:
        return False

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
        
        if playChoice == 1:
            print('''
                  Please choose one of the following -
                  
                  1) White
                  2) Black
                  ''')
                  
            try:
                colorChoice = int(input("Please enter the menu item number corresponding to what you want to do - "))
            except:
                print("Please enter a valid input.")
            
            if colorChoice == 1:
                while True:
                    print(stockfish.get_board_visual())
                    moveChoice = input("Please enter your move (or type 'help' if you dont know what to do) - ")
                    if str(moveChoice.lower()) == 'help':
                        print('''
                              Please enter moves in the format [present square of piece][future square of piece]. For example, to move a pawn to e4 from e2, enter 'e2e4'. Moves need not specify the piece being moved. Only the squares from where to where the piece is moving.
                              
                              To exit play, please enter 'exit'. To this help at any point during the game, type 'help'.''')
                    elif str(moveChoice.lower()) == 'exit':
                        break
                    elif stockfish.is_move_correct(moveChoice):
                            stockfish.make_moves_from_current_position([str(moveChoice)])
                            print("White (user) plays the move -", moveChoice)
                            if checkformate() == True:
                                print("White checkmates Black!")
                                print(stockfish.get_board_visual())
                                break
                            print("Black (Stockfish) plays the move -", stockfish.get_best_move())
                            stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                            if checkformate() == True:
                                print("Black checkmates White!")
                                print(stockfish.get_board_visual())
                                break
                    else:
                        print("Please enter a valid input.")
            elif colorChoice == 2:
                print("White () plays the move -", stockfish.get_best_move())
                stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                while True:
                    print(stockfish.get_board_visual(perspective_white=False))
                    moveChoice = input("Please enter your move (or type 'help' if you dont know what to do) - ")
                    if str(moveChoice.lower()) == 'help':
                        print('''
                              Please enter moves in the format [present square of piece][future square of piece]. For example, to move a pawn to e4 from e2, enter 'e2e4'. Moves need not specify the piece being moved. Only the squares from where to where the piece is moving.
                              
                              To exit play, please enter 'exit'. To this help at any point during the game, type 'help'.''')
                    elif str(moveChoice.lower()) == 'exit':
                        break
                    elif stockfish.is_move_correct(moveChoice):
                            stockfish.make_moves_from_current_position([str(moveChoice)])
                            print("Black (user) plays the move -", moveChoice)
                            if checkformate() == True:
                                print("Black checkmates White!")
                                print(stockfish.get_board_visual(perspective_white=False))
                                break
                            print("White (Stockfish) plays the move -", stockfish.get_best_move())
                            stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                            if checkformate() == True:
                                print("White checkmates Black!")
                                print(stockfish.get_board_visual(perspective_white=False))
                                break
                    else:
                        print("Please enter a valid input.")
                print("White (Stockfish) plays the move -", stockfish.get_best_move())
                stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                while True:
                    print(stockfish.get_board_visual(perspective_white=False))
                    moveChoice = input("Please enter your move (or type 'help' if you dont know what to do) - ")
                    if str(moveChoice.lower()) == 'help':
                        print('''
                              Please enter moves in the format [present square of piece][future square of piece]. For example, to move a pawn to e4 from e2, enter 'e2e4'. Moves need not specify the piece being moved. Only the squares from where to where the piece is moving.
                              
                              To exit play, please enter 'exit'. To this help at any point during the game, type 'help'.''')
                    elif str(moveChoice.lower()) == 'exit':
                        break
                    elif stockfish.is_move_correct(moveChoice):
                            stockfish.make_moves_from_current_position([str(moveChoice)])
                            print("Black (user) plays the move -", moveChoice)
                            if checkformate() == True:
                                print("Black checkmates White!")
                                print(stockfish.get_board_visual(perspective_white=False))
                                break
                            print("White (Stockfish) plays the move -", stockfish.get_best_move())
                            stockfish.make_moves_from_current_position([str(stockfish.get_best_move())])
                            if checkformate() == True:
                                print("White checkmates Black!")
                                print(stockfish.get_board_visual(perspective_white=False))
                                break
                    else:
                        print("Please enter a valid input.")
            else:
                print("Not a valid input.")
                
                
                
                
    if appstate == 3:
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
            
        if inputChoice == 1:
            while True:
                moveChoice = input("Please enter your move (or type 'help' if you dont know what to do) - ")
                if str(moveChoice.lower()) == 'help':
                    print('''
                          Please enter moves in the format [present square of piece][future square of piece]. For example, to move a pawn to e4 from e2, enter 'e2e4'. Moves need not specify the piece being moved. Only the squares from where to where the piece is moving.
                          
                          To exit play, please enter 'exit'. To this help at any point during the game, type 'help'.''')
                elif str(moveChoice.lower()) == 'exit':
                    break
                elif stockfish.is_move_correct(moveChoice):
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
                        print("Evaluation -", str(stockfish.get_evaluation()['value'] / 100))
                        print("Best move -", str(stockfish.get_best_move()))
                    elif checkformate():
                        print("Checkmate!")
                        print(stockfish.get_board_visual())
                        if input("Please enter 1 if you would like to save the moves in this game as CSV - ") == "1":
                            moveFrame = pd.DataFrame(moveFrame, columns=["White", "Black"])
                            while True:
                                try:
                                    moveFrame.to_csv(str((input("Please enter a filename - ") + ".csv")))
                                    print("Saved successfully!")
                                    break
                                except:
                                    print("Please enter a valid input.")
                            break
                    elif stockfish.get_evaluation()['type'] == 'mate':
                        print("Evaluation - Mate in", str(stockfish.get_evaluation()['value']))
                        print("Best move -", str(stockfish.get_best_move()))
                    
                    print(stockfish.get_board_visual())
                
                
        
                
                
                
                
                
                
                
                
                