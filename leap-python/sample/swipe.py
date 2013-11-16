import Leap, sys, pygame, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

SIZEX = 640
SIZEY = 480
backgroundColor = (0,0,0)

offsetX = -100
offsetY = 100
leapSizeX = 200
leapSizeY = 200
leapScaleX = (SIZEX/leapSizeX)
leapScaleY = (SIZEY/leapSizeY)

palmPosition = [offsetX + leapSizeX/2, offsetY + leapSizeY/2]
oldTime = None

def convertCoords(leapPos):
    return (
        (leapPos[0] - offsetX)*leapScaleX,
        SIZEY - (leapPos[1] - offsetY)*leapScaleY
        )
        
def getDeltaTime():
    currentTime = time.time()
    global oldTime
    if oldTime == None:
        oldTime = currentTime
    deltaTime = currentTime - oldTime
    oldTime = currentTime
    return deltaTime
        
def drawCircle(pos):
    window.fill(backgroundColor)
    pygame.draw.circle(window, (255, 255, 255), pos, 10)
    pygame.display.flip()

class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        
        global palmPosition
        print palmPosition
        
        if not frame.hands.is_empty:
            # Gestures
            for gesture in frame.gestures():
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    
                    print swipe.direction
                    
                    velx = swipe.direction[0]*swipe.speed
                    vely = swipe.direction[1]*swipe.speed
                    dt = .001
                    
                    palmPosition[0] += velx*dt
                    palmPosition[1] += vely*dt
                    
                    print "b"
                    circlePosition = convertCoords(palmPosition)
                    circlePosition = (int(circlePosition[0]), int(circlePosition[1]))
                    
                    drawCircle(circlePosition)
def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    #input handling (somewhat boilerplate code):
    while True: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                break
            else: 
                print event 
        else:
            continue
        break
    
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    window = pygame.display.set_mode((SIZEX, SIZEY))
    
    circlePosition = convertCoords(palmPosition)
    circlePosition = (int(circlePosition[0]), int(circlePosition[1]))
    drawCircle(circlePosition)
    
    main()
