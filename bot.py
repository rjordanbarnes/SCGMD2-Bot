import os
import time
import autopy
import ImageGrab
import win32api, win32con


def initialSetup():
    ''' Finds the game and returns a tuple containing the screen position of the game.'''
    raw_input("\nTo detect the game, select a song and press Enter. ")
    
    readyButton = autopy.bitmap.Bitmap.open('readyButton.png')
    screen = autopy.bitmap.capture_screen()
    #autopy.bitmap.capture_screen().save('screengrab.png')
    buttonPos = screen.find_bitmap(readyButton)
    
    if buttonPos:
        pos = (buttonPos[0] - 421, buttonPos[1] - 184)
        print "\nGame successfully detected at %s" % str(pos)
        print "You may now start the song."
        return pos
    else:
        raw_input("Couldn't detect the game. ")

def startSong():
    ''' Presses the "Ready?" button. Not necessary.'''
    autopy.mouse.move(OFFSET[0] + 500, OFFSET[1] + 200)
    autopy.mouse.click()

def grabGameArea():
    gameArea = (OFFSET[0] + 79, OFFSET[1] + 25, OFFSET[0] + 120, OFFSET[1] + 174)
    im = ImageGrab.grab(gameArea)
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
    
def checkArrowSpaces():
    for i in range(40):
        # Temporary variables to aid in resetting keypresses.
        exit = False
        up = False
        left = False
        right = False
        down = False
        
        topArrowSpace = currentGameArea[i, 43]
        if topArrowSpace == (153, 0, 0) or topArrowSpace == (177, 1, 60):
            win32api.keybd_event(win32con.VK_UP, 0, 0, 0)
            print "Tap Up"
            exit = True
            up = True
        elif topArrowSpace == (0, 51, 102) or topArrowSpace == (102, 153, 204):
            win32api.keybd_event(win32con.VK_RIGHT, 0, 0, 0)
            print "Tap Right"
            exit = True
            right = True
            
        bottomArrowSpace = currentGameArea[i, 107]
        if bottomArrowSpace == (255, 204, 0) or bottomArrowSpace == (166, 133, 0):
            win32api.keybd_event(win32con.VK_LEFT, 0, 0, 0)
            print "Tap Left"
            exit = True
            left = True
        elif bottomArrowSpace == (153, 51, 153) or bottomArrowSpace == (95, 31, 95):
            win32api.keybd_event(win32con.VK_DOWN, 0, 0, 0)
            print "Tap Down"
            exit = True
            down = True
            
        if exit is True:
            time.sleep(.05)
            if up:
                win32api.keybd_event(win32con.VK_UP, 0, win32con.KEYEVENTF_KEYUP, 0);
            if right:
                win32api.keybd_event(win32con.VK_RIGHT, 0, win32con.KEYEVENTF_KEYUP, 0);
            if down:
                win32api.keybd_event(win32con.VK_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0);
            if left:
                win32api.keybd_event(win32con.VK_LEFT, 0, win32con.KEYEVENTF_KEYUP, 0);
            break
           
def checkLetterSpaces():
    global aPressed
    global sPressed
    global dPressed
    
    if aPressed:
        if currentGameArea[0, 7] == (153, 153, 51) and currentGameArea[20, 14] == (153, 153, 51):
            win32api.keybd_event(win32api.VkKeyScan('A'), 0, win32con.KEYEVENTF_KEYUP, 0);
            print "Let Go of A"
            aPressed = False
    elif sPressed:
        if currentGameArea[0, 70] == (153, 153, 51) and currentGameArea[21, 68] == (153, 153, 51):
            win32api.keybd_event(win32api.VkKeyScan('S'), 0, win32con.KEYEVENTF_KEYUP, 0);
            print "Let Go of S"
            sPressed = False
    elif dPressed:       
        if currentGameArea[0, 146] == (153, 153, 51) and currentGameArea[21, 141] == (153, 153, 51):
            win32api.keybd_event(win32api.VkKeyScan('D'), 0, win32con.KEYEVENTF_KEYUP, 0);
            print "Let Go of D"
            dPressed = False
    
    for i in range(40):
        if aPressed is False:
            if currentGameArea[i, 1] == (217, 236, 160):
                win32api.keybd_event(win32api.VkKeyScan('A'), 0, 0, 0)
                print "Hold A"
                aPressed = True
            
        if sPressed is False:
            if currentGameArea[i, 75] == (217, 236, 160):
                win32api.keybd_event(win32api.VkKeyScan('S'), 0, 0, 0)
                print "Hold S"
                sPressed = True
         
        if dPressed is False:         
            if currentGameArea[i, 148] == (217, 236, 160):
                win32api.keybd_event(win32api.VkKeyScan('D'), 0, 0, 0)
                print "Hold D"
                dPressed = True

def checkExit():
    if currentGameArea[31, 30] == (177, 101, 60) and currentGameArea[8, 116] == (255, 255, 255):
        print "\nSong complete."
        return False
    else:
        return True

# Program Loop
while 1:
    OFFSET = initialSetup()
    
    aPressed = False
    sPressed = False
    dPressed = False
    
    currentGameArea = grabGameArea().load()

    # Song Loop
    while checkExit():
        currentGameArea = grabGameArea().load()
        
        checkLetterSpaces()
        checkArrowSpaces()