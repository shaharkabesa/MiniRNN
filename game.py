import pygame


pygame.init()

screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
box_shape = (80, 80, 100, 100)
box_color = (255,0,0)

running = True

player = [{
    "player_posX" : 50,
    "player_posY" : 50,
    "player_height" : 0,
    "player_width" : 0
}]


def createBox(left, top ,height, width, color):
    position = (left,top, height, width)
    color = color
    pygame.draw.rect(screen, color, position)

def createPlayer(left, top ,height, width, color):
    position = (left,top, height, width)
    color = color
    return pygame.draw.rect(screen, color, position)


def drawMap(map_matrix):
        for row in range(len(map_matrix)):
            for col in range(len(map_matrix[row])):
                cord = map_matrix[row][col]
                if cord == 1:
                    x = col * 50
                    y = row * 50
                
                    createBox(x,y, 40,40, (255,255,255))
                   
                     
                elif cord == 3:
                    x = col * 50
                    y = row * 50
                    createBox(x,y,40,40, (255,0,0)) 
                           
map = [[1,0,0,0,1],
       [1,0,1,0,1],
       [1,1,1,3,1],
       [1,1,1,1,1]]

drawMap(map)

def movementLogic(positionx,positiony, player):
    if positionx > 150 or positionx < 0:
        print("Trying to move out of bound")
        
    elif positiony > 150 or positiony < 0:
        print("Trying to move out of bound")
        
    
    positionx = int(positionx / 50)
    positiony = int(positiony / 50)
   
    if map[positiony][positionx] == 1:
        print(positionx,positiony)
        print("Hit a wall")
        return
    elif map[positiony][positionx] == 0:
        print("Can move")
        movement_vector = [positiony * 50, positionx *50]
        player[0]["player_posX"] = movement_vector[1]
        player[0]["player_posY"] = movement_vector[0]
    elif map[positiony][positionx] == 3:
        print("Ate food")
        movement_vector = [positiony * 50, positionx *50]
        player[0]["player_posX"] = movement_vector[1]
        player[0]["player_posY"] = movement_vector[0]
        map[positiony][positionx] = 0
    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
               past_x = player[0]["player_posX"]
               current_y = player[0]["player_posY"]
               future_x = past_x + 50
               movementLogic(future_x,current_y, player)
            elif event.key == pygame.K_UP:
                past_y = player[0]["player_posY"]
                current_x = player[0]["player_posX"]
                future_y = past_y - 50 
                movementLogic(current_x, future_y, player)
            elif event.key == pygame.K_DOWN:
                past_y = player[0]["player_posY"]
                current_x = player[0]["player_posX"]
                future_y = past_y + 50 
                movementLogic(current_x, future_y, player)
            elif event.key == pygame.K_LEFT:
               past_x = player[0]["player_posX"]
               current_y = player[0]["player_posY"]
               future_x = past_x - 50
               movementLogic(future_x,current_y, player)
            
    screen.fill("purple")
    drawMap(map)    
    createBox(player[0]["player_posX"],player[0]["player_posY"], 40,40, (0,0,255))
    pygame.display.flip()
    
    clock.tick(60)


pygame.quit()