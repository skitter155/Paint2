# Simple input parsers

def parseInt(inputString, upperBound, lowerBound = 0, allowZero = True):
    try:
        intOutput = int(inputString)
    except ValueError:
        print("Enter plain integer: [eg 1, 2, etc]" + '\n')
        return 'invalid'
    if intOutput > upperBound:
        print("Input too large. Maximum: " + str(upperBound) + '\n')
        return 'invalid'
    if (intOutput == 0 and allowZero == False):
        print("Zero is not allowed" + '\n')
        return 'invalid'
    if intOutput < lowerBound:
        print("Input too small. Minimum: " + str(lowerBound) + '\n')
        return 'invalid'
    return intOutput

def parseFloat(inputString, upperBound, lowerBound = 0.0, allowZero = True):
    try:
        floatOutput = float(inputString)
    except ValueError:
        print("Enter plain decimal number: [eg 1.0, 2.0, etc]")
        return 'invalid'
    if floatOutput >= upperBound:
        print("Input too large. Maximum: " + str(upperBound))
        return 'invalid'
    if (floatOutput == 0 and allowZero == False):
        print("Zero is not allowed")
        return 'invalid'
    if floatOutput < lowerBound:
        print("Input too small. Minimum: " + str(lowerBound))
        return 'invalid'
    return floatOutput