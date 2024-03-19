import Postion as ps

CENTERMOVENUM = 10
CENTERMOVE = [[CENTERMOVENUM,CENTERMOVENUM], [CENTERMOVENUM,-CENTERMOVENUM], [-CENTERMOVENUM,-CENTERMOVENUM], [-CENTERMOVENUM,CENTERMOVENUM]]
MOVE = [[5,5], [5,-5], [-5,-5], [-5,5]]
MOVEMAX = 15
REPEAT = 3
APEX = 4

centerPostion = [0,0]

def Move_Append(Send):
    for i in range(REPEAT):
        Send.append(ps.Postion(MOVE[0][0] + centerPostion[0], MOVE[0][1] + + centerPostion[1], 15))
        Send.append(ps.Postion(MOVE[1][0] + centerPostion[0], MOVE[1][1] + + centerPostion[1], 15))
        Send.append(ps.Postion(MOVE[2][0] + centerPostion[0], MOVE[2][1] + + centerPostion[1], 15))
        Send.append(ps.Postion(MOVE[3][0] + centerPostion[0], MOVE[3][1] + + centerPostion[1], 15))

def nextPostionMoveCheck(Send, index, check, now):
    return check == 1 and abs(Send[index].x - now.x) < 2 and abs(Send[index].y - now.y) < 2 and abs(Send[index].z - now.z) < 2 

def apexAverage(list):
    d = []
    for i in range(APEX):
        sum = 0
        for j in range(i, len(list), APEX):
            sum += list[j]
        d.append(sum/REPEAT)
    return d

def dataMax(Environment_Average):
    index = 0
    average = apexAverage(Environment_Average)
    max = average[0]
    for i in range(1,len(average)):
        if(max < average[i]):
            max = average[i]
            index = i
    return index

def nextCenterMove(Environment_Average, Send):
    if((centerPostion[0] + CENTERMOVENUM < MOVEMAX) and (centerPostion[0] - CENTERMOVENUM > -MOVEMAX)) and ((centerPostion[1] + CENTERMOVENUM < MOVEMAX) and (centerPostion[1] - CENTERMOVENUM > -MOVEMAX)):
        key = dataMax(Environment_Average)
        centerPostion[0] += CENTERMOVE[key][0]
        centerPostion[1] += CENTERMOVE[key][1]
        Move_Append(Send)
        return False
    else:
        return True

