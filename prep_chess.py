import pandas as pd
import chess

board = chess.Board()

def gen(move):

    over = 0
    isCastle = 0
    isCheck = 0
    suffix = ""
    ans = ""
    if move[len(move)-1] == '+':
        suffix = " and gives check"
        move = move[:-1]
        isCheck = 1
    elif move[len(move)-1] == '#':
        suffix = " and this is a mate"
        move = move[:-1]
        isCheck = 1
        over = 1

    board.push_san(move)
    move_string = str(board.pop())
    board.push_san(move)
    source = move_string[:2]
    dest = move_string[2:5]

    
    if move == "O-O" or move == "O-O-O":
        ans = "king castled from "+source+" to "+dest
        isCastle = 1
    elif len(move) == 2:
        ans = "pawn moved from "+source+" to "+move
    elif len(move) == 3:
        if move[0] == 'N':
            ans = "knight moved from " +source+ " to "+ dest
        elif move[0] == 'B':
            ans = "bishop moved from " +source+ " to "+ dest
        elif move[0] == 'R':
            ans = "rook moved from "+source+" to "+ dest
        elif move[0] == 'K':
            ans = "king moved from " +source+" to "+ dest
        elif move[0] == 'Q':
            ans = "queen moved from " +source+ " to "+ dest
    elif len(move) == 4:
        if move[1] == 'x':
            if move[0] == 'N':
                ans = "knight moved from "+source+" to capture piece at " + dest
            elif move[0] == 'B':
                ans = "bishop moved from " +source+ " to capture piece at "+ dest
            elif move[0] == 'R':
                ans = "rook moved from "+source+" to capture piece at "+ dest
            elif move[0] == 'K':
                ans = "king moved from " +source+" to capture piece at "+ dest
            elif move[0] == 'Q':
                ans = "queen moved from " +source+ " to capture piece at "+ dest
            else:
                ans = "pawn moved from "+ source + " to capture piece at "+dest
        else:
            if move[0] == 'N':
                ans = "knight moved from "+source+" to " + dest
            elif move[0] == 'B':
                ans = "bishop moved from " +source+ " to "+ dest
            elif move[0] == 'R':
                ans = "rook moved from "+source+" to "+ dest
            elif move[0] == 'K':
                ans = "king moved from " +source+" to "+ dest
            elif move[0] == 'Q':
                ans = "queen moved from " +source+ " to "+ dest
            else:
                ans = "pawn moved from "+ source + " to "+dest
    ans += suffix    
    return ans, over, isCastle, isCheck



if __name__ == "__main__":
    f = open('ficsgamesdb_2019_standard2000_nomovetimes_129012.pgn', 'r')
    # f = open('game.pgn', 'r')
    # fw = open('comments.en','w')
    # tw = open('train.txt', 'w')

    flag = 0
    all_comments = []
    all_moves = []
    all_len = []
    ctr = 0
    cc = 0

    for lines in f:
        ctr += 1
        if lines == "\n" and flag == 0:
            flag = 1
        elif lines == "\n" and flag == 1:
            flag = 0
        elif flag:
            #CODE HERE
            try:
                cc += 1
                # if ctr > 50000:
                #     break
                board = chess.Board()
                line = lines.split()
                curr = 1
                skip = 0
                line = lines.split()
                comment_str = ""
                move_str = ""
                for xx in range(5):
                    
                    if line[0][0] == '{':
                        skip = 1
                        break
                    

                    #white moves
                    move = line[curr]
                    move_str += str(move) + " "
                    comm1, over, isCastle, isCheck = gen(move)


                    #write
                    comment_str += "the white " + comm1 + ". "
                    if over:
                        break

                    if line[curr+1][0] == '{':
                        # fw.write("Black resigns. ")
                        break

                    #black moves
                    move = line[curr + 1]
                    move_str += str(move) + " "
                    comm2, over, isCastle, isCheck = gen(move)

                    comment_str += "the black " + comm2 + ". "

                    if line[curr+2][0] == '{':
                        # fw.write("White resigns. ")
                        break


                    curr += 3

                    if over:
                        break
                    if board.is_stalemate() or board.is_game_over():
                        break
                if skip == 0:
                    all_comments.append(comment_str)
                    all_moves.append(move_str)
                    all_len.append(len(move_str.split()))
            except Exception as e:
                print(cc)
                print(ctr)
                break
    # print(all_comments)
    # print(all_moves)
    # print(all_len)

    # data = list(zip(all_moves, all_comments, all_len))
    df = pd.DataFrame({'moves': all_moves, 'opening_name': all_comments, 'opening_ply': all_len})
    df.to_csv("./game.csv",sep=",")

f.close()
