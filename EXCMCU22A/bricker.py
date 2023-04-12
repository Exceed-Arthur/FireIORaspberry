currents = 0


def hashBrick(var: str):
    global currents
    limit = 10
    array, st, doe, due = list(var), "", list(["dal10ulqsAV", "mnrm", "dp6ti1vu", "D", "z", "1"]), list(["U5afPAFBvsj", "1llipf", "p21114", "Ak2", "1081Dvx5"])
    for i in range(len(array)-1):
        let = ord(array[i])
        if let % 2 == 0:
            j = len(doe)-1
            if i < (len(doe)):
                j = i
            array[i] = doe[j]
        elif let % 3 == 0:
            j = len(due)-1
            if i < (len(due)):
                j = i
            array[i] = due[j]
        else:
            array[i] = let
        st += str(array[i])
    currents += 1
    if currents < limit:
        return hashBrick(st)
    else:
        currents = 0
        counter = 0
        f = st[-len(var[-12:]):]
        for leg in f:
            if not str(leg).isdigit():
                counter += 1
        ind = int(len(var)/18)
        leeter = st[-(ind):]
        leajer = []
        for letter in leeter:
            leajer.append(letter)
        leeker = ""
        max = 21
        for i in range(len(leajer)-1):
            if i < max:
                leeker += leajer[i]
        if leeker:
            currents = 0
            return leeker
        else:
            currents = 0
            if len(st) > 25:
                return st[-25:]
            return st


print(hashBrick("Stfujb88#"))