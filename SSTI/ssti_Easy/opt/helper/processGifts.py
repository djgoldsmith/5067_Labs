"""
Hidden Function to Process Gifts.
Contains "Easter Egg"
"""

def boloRei(gifts):
    giftList = gifts.split("\n")
    #And add an easter egg
    askedForFlag = False
    askedNicely = False
    for item in giftList:
        if "flag" in item.lower():
            askedForFlag = True
        if "please" in item.lower():
            askedNicely = True

    #And if they asked for a flag
    if askedForFlag:
        #And they were good and asked nicely
        if askedNicely:
            giftList.append("As you asked nicely.  CUEH{If_Y0u_Ask_N1cely_You_Will_Rec1eve}")
        else:
            giftList.append("Polite people might get what they want")
    
    return giftList
