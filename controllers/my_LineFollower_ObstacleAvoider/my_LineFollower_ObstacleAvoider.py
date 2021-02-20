from controller import Robot


def run_robot(robot):
    time_step = 128
    max_speed = 6.28
    isLeftObstacle = False
    isRightObstacle = False
    counter = 0
    afterLeftObstacle = False
    afterRightObstacle = False
    #print(robot.getSFRotation)

    
   # initialize devices
    ps = []
    psNames = [
        'ps0', 'ps1', 'ps2', 'ps3',
        'ps4', 'ps5', 'ps6', 'ps7'
    ]

    for i in range(8):
        ps.append(robot.getDevice(psNames[i]))
        ps[i].enable(time_step)
    
    
    #Motors 
    left_motor = robot.getMotor('left wheel motor')
    right_motor = robot.getMotor('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    
    left_ir = robot.getDistanceSensor('ir0')
    left_ir.enable(time_step)
    
    
    right_ir = robot.getDistanceSensor('ir1')
    right_ir.enable(time_step)
    
    
    
    
    while robot.step(time_step) != -1:
        left_ir_value = left_ir.getValue()
        right_ir_value = right_ir.getValue()
        
        #print("left: {} right: {}".format(left_ir_value, right_ir_value))
         
        left_speed = max_speed
        right_speed = max_speed
        if (left_ir_value > right_ir_value) and (6 < left_ir_value < 15):
            #print("GoLeft")
            left_speed = -max_speed
        elif (right_ir_value > left_ir_value) and (6 < right_ir_value < 15):
            #print("Go Right")
            right_speed = -max_speed
        
        
        
        # read sensors outputs
        psValues = []
        for i in range(8):
            psValues.append(ps[i].getValue())

        # detect obstacles
        right_obstacle = psValues[0] > 80.0 or psValues[1] > 80.0 or psValues[2] > 80.0
        left_obstacle = psValues[5] > 80.0 or psValues[6] > 80.0 or psValues[7] > 80.0
        
      
        
        if (counter < 10) and (isLeftObstacle or isRightObstacle):
            counter = counter + 1
            print(counter)
        if isRightObstacle and counter > 5:
           left_speed  = 0 * max_speed
           right_speed = 0 * max_speed
           isRightObstacle = False
           counter = 0
         
           afterLeftObstacle = True
           
        if isLeftObstacle and counter > 5:
           left_speed  = 0 * max_speed
           right_speed =  0 * max_speed
           isLeftObstacle = False
           counter = 0
           afterRightObstacle = True
           
           
        # modify speeds according to obstacles
        if left_obstacle:
           # turn right
           left_speed  = 0.5 * max_speed
           right_speed = -0.5 * max_speed
           isLeftObstacle = True
         
         
           
        elif right_obstacle:
            # turn left
            left_speed  = -0.5 * max_speed
            right_speed = 0.5 * max_speed
            isRightObstacle = True
          
        if afterLeftObstacle:
            left_speed  = -0.5 * max_speed
            right_speed = 0.5 * max_speed
            counter = counter +1
            if counter > 6:
                left_speed = 0.6*max_speed
                right_speed = 0.6*max_speed
                afterLeftObstacle = False
                counter = 0
            #afterLeftObstacle = False
        if afterRightObstacle:
            left_speed  = 0.5 * max_speed
            right_speed =  -0.5 * max_speed
            counter = counter + 1
            if counter > 6: 
                left_speed = 0.6*max_speed
                right_speed = 0.6*max_speed 
                afterRightObstacle = False
                counter = 0
                
            #afterRightObstacle = False   
        
               
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
        
        
if __name__ == "__main__":
    my_Robot = Robot()
    run_robot(my_Robot)
        
    
    