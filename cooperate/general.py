def getNextCoordsByDirection(degrees, speed):
    def reverse(deg):
        if deg > 90: return 180 - deg
        if deg < -90: return -180 - deg

    d = degrees
    movementX = 0
    movementY = 0
    if d <= 90 and d >= -90:
        movementX = speed * -d / 90
    else:
        movementX = speed * -reverse(d) / 90
    if d >= 0:
        movementY = speed * (90 - d) / 90
    elif d < 0:
        movementY = speed * (90 + d) / 90
    return (movementX, movementY)