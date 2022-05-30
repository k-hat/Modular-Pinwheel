import math
import pygame
pygame.init()
PI = math.pi
VERBOSE = False

# Define Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
ALPHA    = (   0, 120, 120)
LIGHT_BLUE = (  155,  205, 255)
 

RAINBOW = ( ( 255,   0,   0),
            ( 255, 127,   0),
            ( 255, 255,   0),
            (   0, 255,   0),
            (   0,   0, 255),
            (  75,   0, 130),
            ( 238, 130, 238) )

def main():
    drawPinwheel(450, 10, 2)
    
def drawPinwheel(in_arcSize, in_totalArc, in_rotateRate):      
            
    arcSize = in_arcSize
    rotateRate = in_rotateRate
    nextFrameArcs = in_totalArc
    
    runProgram = True
    pauseRotation = False
    pinwheelMode = False
    rainbowMode = False
    solidMode = False
    drawInstructions = True
    
    secondaryRotateRate = -3
    drawBgX = 0
    
    instructionsText = ("Number of Spokes:         Up arrow | Down Arrow",
                        "Rotation Speed:           Left Arrow | Right Arrow",
                        "Secondary Rotation Speed: j | k",
                        "Pause:                    Spacebar",
                        "Toggle Colors:            c",
                        "Toggle Pinwheel Mode:     p",
                        "Toggle Solid vs Outline:  s",
                        "Reset to default:         r",
                        "Toggle Help:              h",
                        "For interesting presets use 1-8")

    # Program loop
    while(runProgram):                
            
        size = (1440,900)
        fontSize = 16        
        screenFont = pygame.font.SysFont("Lucida Console", fontSize)

        totalArcs = nextFrameArcs        
        intervalAngle = 360/totalArcs
        
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Modular Pinwheel")
        
        # Keypress refresh rate
        pygame.key.set_repeat(0)        
        
        # Creates the moving background
        backgroundSurf1 = pygame.Surface(pygame.display.get_window_size())
        backgroundSurf1.fill(LIGHT_BLUE)
        bgArray = pygame.PixelArray(backgroundSurf1)
                
        for i in range(size[0]):
            
            if i >= 720:
                bgArray[i] = (150+2*(i/14.4%50), 205+(i/14.4%50), 255)
            else:
                bgArray[i] = (255-2*(i/14.4%50), 255-(i/14.4%50), 255)
                
        bgArray.close()
        backgroundSurf1.unlock()

        backgroundSurf2 = pygame.Surface.copy(backgroundSurf1)
        backgroundSurf2 = pygame.transform.rotate(backgroundSurf2, 180)

        
        # Creates text instructions 
        instructionsSurf = []
        totalInstructions = instructionsText.__len__()
        for i in range( totalInstructions ):
            instructionsSurf.append( screenFont.render(instructionsText[i], True, BLACK) )   
        textDrawX = size[0] - 508

        
        # Create ovals to be the pins of the pinwheel
        # Creates two copies of the list of ovals.  The first is our template 
        # and the second will be rotated and then drawn.   
        templateSurf = []    
        drawingList = []
        for i in range(totalArcs):
            templateSurf.append(pygame.Surface((arcSize,arcSize)))
            drawingList.append(pygame.Surface((arcSize,arcSize)))
            
        for i in range(totalArcs):
            templateSurf[i].fill(ALPHA)
            drawingList[i].fill(ALPHA)       
            templateSurf[i].set_colorkey(ALPHA)
            drawingList[i].set_colorkey(ALPHA)   
        
        rotateAngle = 0                
        offsets = [0]*totalArcs
        originalCenter = templateSurf[0].get_rect().center            
               
        arcWidth = arcSize/3.0
        arcRect = pygame.Rect(arcWidth,0,arcWidth,arcSize)            
        
        for i in range(totalArcs):
            if rainbowMode == True:
                drawColor = RAINBOW[i%7] 
            else:           
                drawColor = RED
                     
            if(solidMode):                
                pygame.draw.ellipse(templateSurf[i], drawColor, arcRect)
            else:
                pygame.draw.ellipse(templateSurf[i], drawColor, arcRect, 3)
            drawingList[i] = pygame.transform.rotate(templateSurf[i], -1*i*intervalAngle)                                
            
            newCenter = drawingList[i].get_rect().center
            offsets[i] = (newCenter[0] - originalCenter[0])

        
        # Keeps track of oval drawing angles with vectors
        pinVects = []
        for i in range(totalArcs):
            pinVects.append(pygame.math.Vector2(0,arcSize/2))
            pinVects[i] = pinVects[i].rotate(-1*i*intervalAngle)

        
        done = False
        clock = pygame.time.Clock()
        
        # Drawing loop
        while not done:
            
            # Handles user input
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    done = True
                    runProgram = False
                elif event.type == pygame.KEYDOWN:                      
                        
                    if event.key == pygame.K_ESCAPE:
                        done = True
                        runProgram = False                    
                    if event.key == pygame.K_SPACE:
                        pauseRotation = not pauseRotation
                    if event.key == pygame.K_UP and totalArcs < 20:
                        nextFrameArcs += 1
                        done = True
                    if event.key == pygame.K_DOWN and totalArcs > 1:
                        nextFrameArcs -= 1
                        done = True                        
                    if event.key == pygame.K_RIGHT:
                        rotateRate += .5
                    if event.key == pygame.K_LEFT:
                        rotateRate -= .5                                         
                    if event.key == pygame.K_c:
                        rainbowMode = not rainbowMode    
                        done = True             
                    if event.key == pygame.K_p:
                        pinwheelMode = not pinwheelMode
                    if event.key == pygame.K_h:
                        drawInstructions = not drawInstructions
                    if event.key == pygame.K_r:
                        nextFrameArcs = in_totalArc
                        rotateRate = in_rotateRate
                        secondaryRotateRate = -3
                        solidMode = False
                        rainbowMode = False  
                        done = True
                    if event.key == pygame.K_s:
                        solidMode = not solidMode
                        done = True                       
                    if event.key == pygame.K_j:
                        secondaryRotateRate -= .5
                    if event.key == pygame.K_k:
                        secondaryRotateRate += .5                
                    
                    # Preset configurations
                    if event.key == pygame.K_1:
                        nextFrameArcs = 7
                        rotateRate = -1
                        secondaryRotateRate = -2.5
                        solidMode = False
                        rainbowMode = False                        
                        done = True
                    if event.key == pygame.K_2:
                        nextFrameArcs = 15
                        rotateRate = .5
                        secondaryRotateRate = -6
                        solidMode = True
                        rainbowMode = True
                        done = True
                    if event.key == pygame.K_3:
                        nextFrameArcs = 14
                        rotateRate = .5
                        secondaryRotateRate = -6
                        solidMode = False
                        rainbowMode = False
                        done = True
                    if event.key == pygame.K_4:
                        nextFrameArcs = 2
                        rotateRate = -1
                        secondaryRotateRate = -44.5
                        solidMode = True
                        rainbowMode = True
                        done = True
                    if event.key == pygame.K_5:
                        nextFrameArcs = 12
                        rotateRate = 2.5
                        secondaryRotateRate = -.5
                        solidMode = True
                        rainbowMode = True
                        done = True   
                    if event.key == pygame.K_6:
                        nextFrameArcs = 12
                        rotateRate = -2.5
                        secondaryRotateRate = 1
                        solidMode = False
                        rainbowMode = True
                        done = True                                                                        
                    if event.key == pygame.K_7:
                        nextFrameArcs = 18
                        rotateRate = -.5
                        secondaryRotateRate = -10
                        solidMode = False
                        rainbowMode = False
                        done = True  
                    if event.key == pygame.K_8:
                        nextFrameArcs = 10
                        rotateRate = -.5
                        secondaryRotateRate = 7.5
                        solidMode = True
                        rainbowMode = False
                        done = True                            
                                                                
                    if(VERBOSE):
                        print("arcs " + str(totalArcs))
                        print("rotate: " + str(rotateRate))
                        print("rotation secondary: " + str(secondaryRotateRate))
                        print("solid:" + str(solidMode))
                        print("rainbow: " + str(rainbowMode) + "\n")

            
            # Calculates new angles and draws ovals                                    
            originalCenter = templateSurf[0].get_rect().center                
            
            if(not pauseRotation):      
                rotateAngle += rotateRate
                rotateAngle %= 360
            
            for i in range(totalArcs):
                
                testAngle = (rotateAngle + -1*i*intervalAngle)%360
                    
                if(pinwheelMode):
                    drawingList[i] = pygame.transform.rotate(templateSurf[i], rotateAngle + -1*i*intervalAngle)                        
                else:
                    drawingList[i] = pygame.transform.rotate(templateSurf[i], testAngle*secondaryRotateRate)
                
                newCenter = drawingList[i].get_rect().center
                offsets[i] = (newCenter[0] - originalCenter[0])
                
                if(not pauseRotation):  
                    pinVects[i] = pinVects[i].rotate(rotateRate)

            
            # Draws background and instructions
            drawBgX = (drawBgX + 1) % size[0]
            screen.blit(backgroundSurf1, (drawBgX,0))
            screen.blit(backgroundSurf2, (drawBgX - size[0],0))
            
            if(drawInstructions):
                for i in range( totalInstructions - 1):
                    screen.blit( instructionsSurf[i],  (textDrawX,i*(fontSize+5)+3) )
                screen.blit( instructionsSurf[totalInstructions - 1],  (3,3) )
            
            mousePos = pygame.mouse.get_pos() 

            
            # Posts all drawing to screen
            for i in range(totalArcs):
                screen.blit(drawingList[i], (mousePos[0] - arcSize/2 + pinVects[i].x - offsets[i],
                                             mousePos[1] - arcSize/2 - pinVects[i].y - offsets[i]))
            pygame.display.flip()
            
            # Sets frames per second    
            clock.tick(60)      
  
              


if __name__ == '__main__':
    main()
