def DetectChanges(name, listA, listB):
    smallListA = [i[0] for i in listA]
    smallListB = [i[0] for i in listB]

    answer = ""

    for i in range(len(smallListA)):
        if smallListA[i] in smallListB:
            tempB = listB[smallListB.index(smallListA[i])]
            if (float(listA[i][1] ) < float(tempB[1])) and (listA[i][2] == "Long"): answer += f"{name} just increased size {smallListA[i]} from {listA[i][1]} to {tempB[1]} \n \n"
            elif (float(listA[i][1]  ) > float (tempB[1])) and (listA[i][2] == "Short") : answer += f"{name} just increased size {smallListA[i]} from {listA[i][1]} to {tempB[1]}  \n \n" 
    
            elif (float(listA[i][1]) > float(tempB[1])): answer += f"{name} just reduced size {smallListA[i]} from {listA[i][1]} to {tempB[1]}\n \n"
            if(listA[i][2]!=tempB[2]):
                answer += f"{name} flipped {smallListA[i]} position from {listA[i][2]} to {tempB[2]} with {tempB[1]}\n \n"
            if(listA[i][-1]!=tempB[-1]):
                answer += f"{name} changed leverage on {smallListA[i]} \n position from {listA[i][-1]} >>>>>>>>>>  {tempB[-1]}\n \n"
        else:
            answer += f"{name} just closed {smallListA[i]} position at {listA[i][4]} \n \n"
    smallListB = [i for i in smallListB if i not in smallListA]
    for i in smallListB:
        new = ""
        new = [pair for pair in listB if pair not in listA]
        filter_obj = filter(lambda s: s[0] == i,new)
        print("***filter_obj***")
        print(list(filter_obj))
        DisptachToTelegram2(list(filter_obj))
        answer += f"{name} just opened new {i} position\n {new}"
    answer = answer[:-1]
    return answer
