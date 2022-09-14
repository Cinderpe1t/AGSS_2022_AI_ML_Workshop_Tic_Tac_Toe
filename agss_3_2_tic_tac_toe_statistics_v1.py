import time
import tkinter as tk
import random
import numpy as np
import math
import copy

def checkWinner(board, player):
    #
    player=1
    for i in range(3):
        if board[i][0]==player and board[i][1]==player and board[i][2]==player:
            return player
        if board[0][i]==player and board[1][i]==player and board[2][i]==player:
            return player
    if board[0][0]==player and board[1][1]==player and board[2][2]==player:
        return player
    if board[0][2]==player and board[1][1]==player and board[2][0]==player:
        return player
    player=2
    for i in range(3):
        if board[i][0]==player and board[i][1]==player and board[i][2]==player:
            return player
        if board[0][i]==player and board[1][i]==player and board[2][i]==player:
            return player
    if board[0][0]==player and board[1][1]==player and board[2][2]==player:
        return player
    if board[0][2]==player and board[1][1]==player and board[2][0]==player:
        return player
    return 0

def cAnimFaster():
    global stepDelay
    if stepDelay>0:
        stepDelay=round(10*(stepDelay-0.1))/10
        inputSpeed.delete('1.0', tk.END)
        inputSpeed.insert(tk.END, stepDelay)
        
def cAnimSlower():
    global stepDelay
    stepDelay=round(10*(stepDelay+0.1))/10
    inputSpeed.delete('1.0', tk.END)
    inputSpeed.insert(tk.END, stepDelay)

def cAnimationDelay():
    global stepDelay
    inp = inputSpeed.get(1.0, "end-1c")
    stepDelay = float(inp)


def updateScore():
    global tGameStat, lGameStat
    tD=tGameStat
    lGameStat.config(text = ' / '.join(str(x) for x in tD))

def viewSelected():
    global tPlayOrder, tUserMark, tAI1Style, tAI2Style
    tPlayOrder = rbPlayOrder.get()
    tUserMark = rbUserMark.get()
    tAI1Style = rbAI1style.get()
    tAI2Style = rbAI2style.get()

def setMountOrigin(eventorigin):
    global mouseXY
    mouseXY=[eventorigin.x, eventorigin.y]
    #print(mouseXY)

def cNoSample():
    global tNoGames
    inp = inputText.get(1.0, "end-1c")
    tNoGames = int(inp)
    
def aiCount(tBoard):
    count=0
    for i in range(3):
        for j in range(3):
            if tBoard[i][j]>0:
                count+=1
    return count

def aiEmptyPairs(tBoard):
    emptyPairs=[]
    for i in range(3):
        for j in range(3):
            if tBoard[i][j]==0:
                emptyPairs.append([i, j])
    return emptyPairs

def aiEmptyCorner(tBoard):
    emptyPairs=[]
    for i in [0, 2]:
        for j in [0, 2]:
            if tBoard[i][j]==0:
                emptyPairs.append([i, j])
    return emptyPairs

def aiFindTwo(tBoard, player):
    #find two in a row cases
    #print(tBoard)
    #print('empty')
    emptyXY=aiEmptyPairs(tBoard)
    #print(emptyXY)
    placeXY=[]
    tempBoard=[]
    for k in range(len(emptyXY)):
        #print('check', emptyXY[k])
        tempBoard=copy.deepcopy(tBoard)
        tempBoard[emptyXY[k][0]][emptyXY[k][1]]=player
        #print('temp board', tempBoard)
        #check X
        #print('check X')
        count2=0
        count1=0
        for m in range(3):
            if tempBoard[m][emptyXY[k][1]]==player:
                count2+=1
            if tempBoard[m][emptyXY[k][1]]==3-player:
                count1+=1
        if count2==2 and count1==0:
            placeXY.append(emptyXY[k])
            #print(emptyXY[k])
        #check Y
        #print('check Y')
        count2=0
        count1=0
        for m in range(3):
            if tempBoard[emptyXY[k][0]][m]==player:
                count2+=1
            if tempBoard[emptyXY[k][0]][m]==3-player:
                count1+=1
        if count2==2 and count1==0:
            placeXY.append(emptyXY[k])
            #print(emptyXY[k])
        #check diagonal 1
        if emptyXY[k][0]==emptyXY[k][1]:
            count2=0
            count1=0
            #print('diagonal 1')
            for m in range(3):
                if tempBoard[m][m]==player:
                    count2+=1
                if tempBoard[m][m]==3-player:
                    count1+=1
            if count2==2 and count1==0:
                placeXY.append(emptyXY[k])
                #print(emptyXY[k])

        #check diagonal 2
        if emptyXY[k][0]+emptyXY[k][1]==2:
            #print('diagonal 2')
            count2=0
            count1=0
            for m in range(3):
                if tempBoard[m][2-m]==player:
                    count2+=1
                if tempBoard[m][2-m]==3-player:
                    count1+=1
            if count2==2 and count1==0:
                placeXY.append(emptyXY[k])
                #print(emptyXY[k])
    #print(placeXY)
    return placeXY

def aiRandom(tBoard, player):
    x=np.random.randint(0,3)
    y=np.random.randint(0,3)
    while tBoard[x][y] > 0:
        x=np.random.randint(0,3)
        y=np.random.randint(0,3)
    tBoard[x][y]=player
    return [x,y]

def aiDefense(tBoard, player):
    if player==1:
        tLastMove=tP1LastMove
    else:
        tLastMove=tP2LastMove        
    count=aiCount(tBoard)
    #if first, random
    if count==0:
        x=np.random.randint(0,3)
        y=np.random.randint(0,3)
        while tBoard[x][y] > 0:
            x=np.random.randint(0,3)
            y=np.random.randint(0,3)
        tBoard[x][y]=player
        return [x,y]
    elif count==1:
        #place next to the first. Find empty around the tLastMove
        possibleXY=[]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                tX=i+tLastMove[0]
                tY=j+tLastMove[1]
                if tX>=0 and tX<=2 and tY>=0 and tY<=2:
                    if tBoard[tX][tY]==0:
                        possibleXY.append([tX,tY])
        #print(possibleXY)
        tI=np.random.randint(0,len(possibleXY))
        #print(tI)
        tBoard[possibleXY[tI][0]][possibleXY[tI][1]]=player
        return possibleXY[tI]
    else: #find out defense cases
        emptyXY=aiEmptyPairs(tBoard)
        #print(emptyXY)
        placeXY=[]
        tempBoard=[]
        for k in range(len(emptyXY)):
            tempBoard=copy.deepcopy(tBoard)
            tempBoard[emptyXY[k][0]][emptyXY[k][1]]=3-player
            tempWin=checkWinner(tempBoard, 3-player)
            if tempWin>0:
                placeXY=emptyXY[k]
        #print(placeXY)
        if len(placeXY)>0:
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY
        else: #place next to opponent
            possibleXY=[]
            for i in [-1,1]:
                for j in [-1,1]:
                    tX=i+tLastMove[0]
                    tY=j+tLastMove[1]
                    if tX>=0 and tX<=2 and tY>=0 and tY<=2:
                        if tBoard[tX][tY]==0:
                            possibleXY.append([tX,tY])
            if len(possibleXY)>0:
                tI=np.random.randint(0,len(possibleXY))
                tBoard[possibleXY[tI][0]][possibleXY[tI][1]]=player
                return possibleXY[tI]
            else:
                tI=np.random.randint(0,len(emptyXY))
                tBoard[emptyXY[tI][0]][emptyXY[tI][1]]=player
                return emptyXY[tI]

def aiOffense(tBoard, player):
    count=aiCount(tBoard)
    #if first, random
    if count==0: #place it at center
        tBoard[1][1]=player
        return [1,1]
    elif count==1:
        if tBoard[1][1]==0: #center if empty
            tBoard[1][1]=player
            return [1,1]
        else: #center was taken, place at corners
            emptyXY=aiEmptyCorner(tBoard)
            tI=np.random.randint(0,len(emptyXY))
            tBoard[emptyXY[tI][0]][emptyXY[tI][1]]=player
            return emptyXY[tI]            
    elif count==2:
        #avoid ineffective directions and set preferred direction
        pXY=aiFindTwo(tBoard,player)
        tI=np.random.randint(0,len(pXY))
        tBoard[pXY[tI][0]][pXY[tI][1]]=player
        return pXY[tI]                    
    else:
        #find any winning positions
        emptyXY=aiEmptyPairs(tBoard)
        placeXY=[]
        tempBoard=[]
        for k in range(len(emptyXY)):
            tempBoard=copy.deepcopy(tBoard)
            tempBoard[emptyXY[k][0]][emptyXY[k][1]]=player
            tempWin=checkWinner(tempBoard, player)
            if tempWin>0:
                placeXY=emptyXY[k]
        if len(placeXY)>0:
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY
        #if not, find positions for two in a row without opponent
        pXY=aiFindTwo(tBoard,player)
        if len(pXY)>0:
            tI=np.random.randint(0,len(pXY))
            tBoard[pXY[tI][0]][pXY[tI][1]]=player
            return pXY[tI]                    
        #if not random
        tI=np.random.randint(0,len(emptyXY))
        tBoard[emptyXY[tI][0]][emptyXY[tI][1]]=player
        return emptyXY[tI]                    

def aiShallow(tBoard, player):
    count=aiCount(tBoard)
    #if first, random
    if count==0: #place it at center
        tBoard[1][1]=player
        return [1,1]
    elif count==1:
        if tBoard[1][1]==0: #center if empty
            tBoard[1][1]=player
            return [1,1]
        else: #center was taken, place at corners
            emptyXY=aiEmptyCorner(tBoard)
            tI=np.random.randint(0,len(emptyXY))
            tBoard[emptyXY[tI][0]][emptyXY[tI][1]]=player
            return emptyXY[tI]            
    elif count==2:
        #avoid ineffective directions and set preferred direction
        pXY=aiFindTwo(tBoard,player)
        tI=np.random.randint(0,len(pXY))
        tBoard[pXY[tI][0]][pXY[tI][1]]=player
        return pXY[tI]                    
    else: #count>2
        #find any winning positions
        emptyXY=aiEmptyPairs(tBoard)
        placeXY=[]
        tempBoard=[]
        for k in range(len(emptyXY)):
            tempBoard=copy.deepcopy(tBoard)
            tempBoard[emptyXY[k][0]][emptyXY[k][1]]=player
            tempWin=checkWinner(tempBoard, player)
            if tempWin>0:
                placeXY=emptyXY[k]
        if len(placeXY)>0:
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY
        #find any defensive positions
        emptyXY=aiEmptyPairs(tBoard)
        placeXY=[]
        tempBoard=[]
        for k in range(len(emptyXY)):
            tempBoard=copy.deepcopy(tBoard)
            tempBoard[emptyXY[k][0]][emptyXY[k][1]]=3-player
            tempWin=checkWinner(tempBoard, 3-player)
            if tempWin>0:
                placeXY=emptyXY[k]
        if len(placeXY)>0:
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY

        #if not, find positions for two in a row without opponent
        pXY=aiFindTwo(tBoard,player)
        if len(pXY)>0:
            tI=np.random.randint(0,len(pXY))
            tBoard[pXY[tI][0]][pXY[tI][1]]=player
            return pXY[tI]                    
        #if not random
        tI=np.random.randint(0,len(emptyXY))
        tBoard[emptyXY[tI][0]][emptyXY[tI][1]]=player
        return emptyXY[tI]                    

def aiSearch(tBoard, player):
    count=aiCount(tBoard)
    #if first, random
    if count==0: #place it at center
        tBoard[1][1]=player
        return [1,1]
    elif count==1:
        if tBoard[1][1]==0: #center if empty
            tBoard[1][1]=player
            return [1,1]
        else: #center was taken, place at corners
            emptyXY=aiEmptyCorner(tBoard)
            tI=np.random.randint(0,len(emptyXY))
            tBoard[emptyXY[tI][0]][emptyXY[tI][1]]=player
            return emptyXY[tI]            
    elif count==2:
        #avoid ineffective directions and set preferred direction
        pXY=aiFindTwo(tBoard,player)
        tI=np.random.randint(0,len(pXY))
        tBoard[pXY[tI][0]][pXY[tI][1]]=player
        return pXY[tI]                    
    else: #count>2
        #find any winning positions
        emptyXY=aiEmptyPairs(tBoard)
        placeXY=[]
        tempBoard=[]
        for k in range(len(emptyXY)):
            tempBoard=copy.deepcopy(tBoard)
            tempBoard[emptyXY[k][0]][emptyXY[k][1]]=player
            tempWin=checkWinner(tempBoard, player)
            if tempWin>0:
                placeXY=emptyXY[k]
        if len(placeXY)>0:
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY
        
        #find any defensive positions
        emptyXY=aiEmptyPairs(tBoard)
        placeXY=[]
        tempBoard=[]
        for k in range(len(emptyXY)):
            tempBoard=copy.deepcopy(tBoard)
            tempBoard[emptyXY[k][0]][emptyXY[k][1]]=3-player
            tempWin=checkWinner(tempBoard, 3-player)
            if tempWin>0:
                placeXY=emptyXY[k]
        if len(placeXY)>0:
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY

        #find preemptive defensive positions
        [winPath1, winPath2]=searchNext(tBoard,player)
        if len(winPath1)>0 and player==2:
            tI=np.random.randint(0,len(winPath1))
            placeXY=winPath1[tI][1] #preemptive 2nd node place
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY
        if len(winPath2)>0 and player==1:
            tI=np.random.randint(0,len(winPath2))
            placeXY=winPath2[tI][1] #preemptive 2nd node place
            tBoard[placeXY[0]][placeXY[1]]=player
            return placeXY

        
        #if not, find positions for two in a row without opponent
        pXY=aiFindTwo(tBoard,player)
        if len(pXY)>0:
            tI=np.random.randint(0,len(pXY))
            tBoard[pXY[tI][0]][pXY[tI][1]]=player
            return pXY[tI]                    
        #if not random
        tI=np.random.randint(0,len(emptyXY))
        tBoard[emptyXY[tI][0]][emptyXY[tI][1]]=player
        return emptyXY[tI]                    



def searchNext(board, player):
    searchWeight=1
    emptyXY=aiEmptyPairs(board)
    #print(board)
    #winPath0=[]
    winPath1=[]
    winPath2=[]
    if len(emptyXY)==0: #draw
        return [winPath1, winPath2]

    #winning cases
    for k in range(len(emptyXY)):
        tempBoard=copy.deepcopy(board)
        tempBoard[emptyXY[k][0]][emptyXY[k][1]]=player
        tempWin=checkWinner(tempBoard, player)
        if tempWin>0:
            if tempWin==1:
                winPath1.append([emptyXY[k]])
            if tempWin==2:
                winPath2.append([emptyXY[k]])
    if len(winPath1)>0 or len(winPath2)>0:
        return [winPath1, winPath2]     

    else: #if there is no win, search for next step

        #find any defensive positions
        emptyXY=aiEmptyPairs(board)
        placeXY=[]
        tempBoard=[]
        for k in range(len(emptyXY)):
            tempBoard=copy.deepcopy(board)
            tempBoard[emptyXY[k][0]][emptyXY[k][1]]=3-player
            tempWin=checkWinner(tempBoard, 3-player)
            if tempWin>0:
                placeXY.append(emptyXY[k])
        if len(placeXY)>0:
            for k in range(len(placeXY)):
                tempBoard=copy.deepcopy(board)
                tempBoard[placeXY[k][0]][placeXY[k][1]]=player
                [tWinPath1, tWinPath2]=searchNext(tempBoard,3-player)
                for i in range(len(tWinPath1)):
                    if player==1:
                        tList=[placeXY[k]]
                    else:
                        tList=[]
                    for j in range(len(tWinPath1[i])):
                        tList.append(tWinPath1[i][j])
                    winPath1.append(tList)
                for i in range(len(tWinPath2)):
                    if player==1:
                        tList=[]
                    else:
                        tList=[placeXY[k]]
                    for j in range(len(tWinPath2[i])):
                        tList.append(tWinPath2[i][j])
                    winPath2.append(tList)
            return [winPath1, winPath2]    
        
        else: #if there is no defensive positions
            
            for k in range(len(emptyXY)):
                tempBoard=copy.deepcopy(board)
                tempBoard[emptyXY[k][0]][emptyXY[k][1]]=player
                [tWinPath1, tWinPath2]=searchNext(tempBoard,3-player)
                for i in range(len(tWinPath1)):
                    if player==1:
                        tList=[emptyXY[k]]
                    else:
                        tList=[]
                    for j in range(len(tWinPath1[i])):
                        tList.append(tWinPath1[i][j])
                    winPath1.append(tList)
                for i in range(len(tWinPath2)):
                    if player==1:
                        tList=[]
                    else:
                        tList=[emptyXY[k]]
                    for j in range(len(tWinPath2[i])):
                        tList.append(tWinPath2[i][j])
                    winPath2.append(tList)
            #if len(winPath1)==1:
            return [winPath1, winPath2]

def cPlayMatch():
    global tObj, mouseXY, tCoord, tGameStat, tLastMove, tBoard, tNoGames, tP1LastMove, tP2LastMove
    tGameStat=[0,0,0,0]
    tPlayTurn=0
    for g in range(tNoGames):
        #start match
        mBoard=[]
        tBoard=[[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        lGameOver.config(text="")
        #1 for player, and 2 for AI always
        if len(tObj)>0:
            for i in range(len(tObj)):
                canv.delete(tObj[i])
        tObj=[]
        tCount=0
        tWin=0
        mouseXY=[0,0]
        win.update()
        #Set starting player
        if tPlayOrder == 1:
            tPlayTurn=1
        elif tPlayOrder == 2:
            tPlayTurn=2
        elif tPlayOrder == 3:
            tPlayTurn=(g % 2) + 1
        while tCount<9 and tWin==0:
            #player order
            if tPlayTurn == 1:
                #wait for mouse click
                if tAI1Style==1:
                    #random player
                    xy=aiRandom(tBoard, 1)                
                elif tAI1Style==2:
                    #defense player
                    xy=aiDefense(tBoard, 1)
                elif tAI1Style==3:
                    #offense player
                    xy=aiOffense(tBoard, 1)
                elif tAI1Style==4:
                    #shallow search
                    xy=aiShallow(tBoard, 1)
                elif tAI1Style==5:
                    #complete search
                    xy=aiSearch(tBoard, 1)
                #display AI mark
                tX=tCoord[xy[0]]
                tY=tCoord[xy[1]]
                if tUserMark==1:
                    tL1=canv.create_line(tX-30,tY-30,tX+30,tY+30, width = tLineWidth, fill='green')
                    tL2=canv.create_line(tX+30,tY-30,tX-30,tY+30, width = tLineWidth, fill='green')
                    tObj.append(tL1)
                    tObj.append(tL2)
                else:
                    tL1=canv.create_oval(tX-30,tY-30,tX+30,tY+30, width = tLineWidth, outline='green')
                    tObj.append(tL1)
                #tWin=checkWinner(tBoard, 1)
                tP1LastMove = xy
                tPlayTurn = 2
                mBoard.append(copy.deepcopy(tBoard))
            else: #call AI player
                if tAI2Style==1:
                    #random player
                    xy=aiRandom(tBoard, 2)                
                elif tAI2Style==2:
                    #defense player
                    xy=aiDefense(tBoard, 2)
                elif tAI2Style==3:
                    #offense player
                    xy=aiOffense(tBoard, 2)
                elif tAI2Style==4:
                    #shallow search
                    xy=aiShallow(tBoard, 2)
                elif tAI2Style==5:
                    #complete search
                    xy=aiSearch(tBoard, 2)
                #display AI mark
                tX=tCoord[xy[0]]
                tY=tCoord[xy[1]]
                if tUserMark==2:
                    tL1=canv.create_line(tX-30,tY-30,tX+30,tY+30, width = tLineWidth, fill='orange')
                    tL2=canv.create_line(tX+30,tY-30,tX-30,tY+30, width = tLineWidth, fill='orange')
                    tObj.append(tL1)
                    tObj.append(tL2)
                else:
                    tL1=canv.create_oval(tX-30,tY-30,tX+30,tY+30, width = tLineWidth, outline='orange')
                    tObj.append(tL1)
                #check winner for player 2
                #print('AI placed:',tBoard)
                
                #print('AI wins:',tWin)
                tP2LastMove = xy
                tPlayTurn = 1
                mBoard.append(copy.deepcopy(tBoard))
            if stepDelay>0:
                time.sleep(stepDelay)
            win.update()
            tWin=checkWinner(tBoard, 1)
            tCount+=1
            #print(tBoard)
        #announce results - win or draw    
        tGameStat[3]+=1
        if tWin==0:
            lGameOver.config(text="Draw")
            tGameStat[1]+=1
        elif tWin==1:
            lGameOver.config(text="Toothless won!")
            tGameStat[0]+=1
        elif tWin==2:
            lGameOver.config(text="Pouncer won!")
            tGameStat[2]+=1
            #for k in range(len(mBoard)):
                #printBoard(mBoard[k])
        updateScore()
        win.update()
        if stepDelay>0:
            time.sleep(stepDelay*2)

xWinSize=1024
yWinSize=768
noSample=100
stepDelay=0
winFontSize=20
listFontSize=12
yLineUp=0.5
yCompare=0.6

tSize=300
tOffset=3
tLineWidth=5

tPlayOrder=1
tUserMark=1
tAI1Style=1
tAI2Style=1
tNoGames=100

tP1LastMove=[]
tP2LastMove=[]
tObj=[]
tGameStat=[0,0,0,0]
mouseXY=[0,0]

#noArray=[]
#widgetList=[]
#noList=[]
#dispListIn=[]
#dispListOut=[]

#Create an instance of tkinter frame
win=tk.Tk()
win.title("Tic-Tac-Toe AI Statistics Play")
rbAI1style = tk.IntVar()
rbAI1style.set(tAI1Style)
rbAI2style = tk.IntVar()
rbAI2style.set(tAI2Style)
rbUserMark = tk.IntVar()
rbUserMark.set(tUserMark)
rbPlayOrder = tk.IntVar()
rbPlayOrder.set(tPlayOrder)
#Define the geometry of window
win.geometry("1024x768")

canv=tk.Canvas(win, width=tSize, height=tSize)
canv.place(relx=0.5, rely=0.55, anchor='n')

xP1=(tSize-tOffset*2)/3+tOffset
xP2=(tSize-tOffset*2)/3*2+tOffset
tCoord=[0.5*(tSize-tOffset*2)/3+tOffset, 1.5*(tSize-tOffset*2)/3+tOffset, 2.5*(tSize-tOffset*2)/3+tOffset]

#tic-tac-toe board
canv.create_line(xP1,tOffset,xP1,tSize-tOffset, width = tLineWidth, fill='black')
canv.create_line(xP2,tOffset,xP2,tSize-tOffset, width = tLineWidth, fill='black')
canv.create_line(tOffset,xP1,tSize-tOffset,xP1, width = tLineWidth, fill='black')
canv.create_line(tOffset,xP2,tSize-tOffset,xP2, width = tLineWidth, fill='black')
tttRect1=canv.create_rectangle(tOffset,tOffset,tSize-tOffset,tSize-tOffset,outline="gray")
#canv.delete(tttRect1)
#
canv.bind("<Button 1>",setMountOrigin)

#start match button
bPlay = tk.Button(win, text = "Play a match",  command = cPlayMatch, font=("Arial", winFontSize))
bPlay.place(relx=0.5, rely=0.40, anchor='n')

#play order radio button
lPlayOrder = tk.Label(win, text = "Play order", font=("Arial", winFontSize))
lPlayOrder.place(relx=0.1, rely=0.05, anchor=tk.W)
bPlayOrderUser=tk.Radiobutton(win, text="Toothless plays first", variable=rbPlayOrder, value=1, command=viewSelected, font=("Arial", winFontSize))
bPlayOrderUser.place(relx=0.1, rely=0.10, anchor=tk.W)
bPlayOrderAI=tk.Radiobutton(win, text="Pouncer plays first", variable=rbPlayOrder, value=2, command=viewSelected, font=("Arial", winFontSize))
bPlayOrderAI.place(relx=0.1, rely=0.15, anchor=tk.W)
bPlayOrderAI=tk.Radiobutton(win, text="Alternating", variable=rbPlayOrder, value=3, command=viewSelected, font=("Arial", winFontSize))
bPlayOrderAI.place(relx=0.1, rely=0.20, anchor=tk.W)

    
#player shape radio button
lPlayMark= tk.Label(win, text = "Player mark", font=("Arial", winFontSize))
lPlayMark.place(relx=0.1, rely=0.25, anchor=tk.W)
bStyleX=tk.Radiobutton(win, text="Toothless uses X", variable=rbUserMark, value=1, command=viewSelected, font=("Arial", winFontSize))
bStyleX.place(relx=0.1, rely=0.30, anchor=tk.W)
bStyleO=tk.Radiobutton(win, text="Toothless uses O", variable=rbUserMark, value=2, command=viewSelected, font=("Arial", winFontSize))
bStyleO.place(relx=0.1, rely=0.35, anchor=tk.W)


#AI player type selection
lAIType= tk.Label(win, text = "Toothless AI player style", font=("Arial", winFontSize))
lAIType.place(relx=0.35, rely=0.05, anchor=tk.W)

b1Random=tk.Radiobutton(win, text="Random", variable=rbAI1style, value=1, command=viewSelected, font=("Arial", winFontSize))
b1Random.place(relx=0.35, rely=0.10, anchor=tk.W)
b1Defense=tk.Radiobutton(win, text="Defensive", variable=rbAI1style, value=2, command=viewSelected, font=("Arial", winFontSize))
b1Defense.place(relx=0.35, rely=0.15, anchor=tk.W)
b1Attack=tk.Radiobutton(win, text="Offensive", variable=rbAI1style, value=3, command=viewSelected, font=("Arial", winFontSize))
b1Attack.place(relx=0.35, rely=0.20, anchor=tk.W)
b1SearchShallow=tk.Radiobutton(win, text="Defense and offense", variable=rbAI1style, value=4, command=viewSelected, font=("Arial", winFontSize))
b1SearchShallow.place(relx=0.35, rely=0.25, anchor=tk.W)
b1SearchComplete=tk.Radiobutton(win, text="Search", variable=rbAI1style, value=5, command=viewSelected, font=("Arial", winFontSize))
b1SearchComplete.place(relx=0.35, rely=0.30, anchor=tk.W)

#AI player type selection
lAIType= tk.Label(win, text = "Pouncer AI player style", font=("Arial", winFontSize))
lAIType.place(relx=0.6, rely=0.05, anchor=tk.W)

b2Random=tk.Radiobutton(win, text="Random", variable=rbAI2style, value=1, command=viewSelected, font=("Arial", winFontSize))
b2Random.place(relx=0.6, rely=0.10, anchor=tk.W)
b2Defense=tk.Radiobutton(win, text="Defensive", variable=rbAI2style, value=2, command=viewSelected, font=("Arial", winFontSize))
b2Defense.place(relx=0.6, rely=0.15, anchor=tk.W)
b2Attack=tk.Radiobutton(win, text="Offensive", variable=rbAI2style, value=3, command=viewSelected, font=("Arial", winFontSize))
b2Attack.place(relx=0.6, rely=0.20, anchor=tk.W)
b2SearchShallow=tk.Radiobutton(win, text="Defense and offense", variable=rbAI2style, value=4, command=viewSelected, font=("Arial", winFontSize))
b2SearchShallow.place(relx=0.6, rely=0.25, anchor=tk.W)
b2SearchComplete=tk.Radiobutton(win, text="Search", variable=rbAI2style, value=5, command=viewSelected, font=("Arial", winFontSize))
b2SearchComplete.place(relx=0.6, rely=0.30, anchor=tk.W)

#input
inputText = tk.Text(win, height = 1, width = 5, bg = "light yellow", font=("Arial", winFontSize))
inputText.place(relx=0.05, rely=0.4, anchor=tk.W)
inputText.insert(tk.END, noSample)

bNoSample = tk.Button(win, text = "Number of games",  command = cNoSample, font=("Arial", winFontSize))
bNoSample.place(relx=0.15, rely=0.4, anchor=tk.W)

#
inputSpeed = tk.Text(win, height = 1, width = 5, bg = "light yellow", font=("Arial", winFontSize))
inputSpeed.place(relx=0.05, rely=0.5, anchor=tk.W)
inputSpeed.insert(tk.END, stepDelay)

bDelay = tk.Button(win, text = "Game delay",  command = cAnimationDelay, font=("Arial", winFontSize))
bDelay.place(relx=0.15, rely=0.50, anchor=tk.W)

bFaster = tk.Button(win, text = "Faster",  command = cAnimFaster, font=("Arial", winFontSize))
bFaster.place(relx=0.15, rely=0.45, anchor=tk.W)

bSlower = tk.Button(win, text = "Slower",  command = cAnimSlower, font=("Arial", winFontSize))
bSlower.place(relx=0.15, rely=0.55, anchor=tk.W)

lGameOver= tk.Label(win, text = "", font=("Arial", winFontSize))
lGameOver.place(relx=0.8, rely=0.40, anchor='n')


lGameCount=tk.Label(win, text = "W / D / L / Total", font=("Arial", winFontSize))
lGameCount.place(relx=0.8, rely=0.45, anchor='n')

#lGameStat=[]
#tGameStat
#need to display game statistics
#for i in range(len(tGameStat)):
#    tD=tGameStat[i]
#    tL=tk.Label(win, text = ' / '.join(str(x) for x in tD), font=("Arial", winFontSize))
lGameStat=tk.Label(win, text = ' / '.join(str(x) for x in tGameStat), font=("Arial", winFontSize))
lGameStat.place(relx=0.8, rely=0.50, anchor='n')

win.mainloop()