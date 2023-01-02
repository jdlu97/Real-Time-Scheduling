'''!    @file       task_motor_controller.py
        @brief      Runs the motor and controller tasks together.  
        @details    Implements closed-loop position control on a motor
                    using a task defined as a generator.

        @author     Juan Luna
        @date       2022-02-10 Original file
        @date       2022-12-30 Modified for portfolio update
'''
import controller
import motor
import utime
import print_task
import array

class Task_Motor_Controller:
    '''! @brief     Task motor controller class.
    '''
     def __init__(self, encoder_share, gain_share, set_point_share, ENA_pin, In1_pin, In2_pin, Timer):
        '''! @brief    Instantiates objects of the Task_Motor_Controller class.
             @param  encoder_share  Passes the present value from the encoder
             @param  gain_share    Share variable for proportional gain value.
             @param  set_point_share   Share variable for setpoint value.
             @param  ENA_pin            Enable pin object for the motor.
             @param  In1_pin       Control pin 1 associated with motor.
             @param  In2_pin       Control pin 2 associated with motor.
             @param  Timer          Timer object for motor.
        '''
        # Define shares for motor and encoder 1

        ## @brief   Passes the present value from the encoder
        self.encoder_share = encoder_share
        ## @brief   Share variable for proportional gain value.
        self.gain_share = gain_share
        ## @brief   Share variable for setpoint value.
        self.set_point_share = set_point_share
        
        # Define motor-related pin objects

        ## @brief   Enable pin object for the motor.
        self.ENA = ENA_pin
        ## @brief   Control pin 1 associated with motor.
        self.IN1A_pin = In1_pin
        ## @brief   Control pin 2 associated with motor.
        self.IN2A_pin = In2_pin
        ## @brief   Timer object for motor.
        self.tim_MOT_A = Timer
        
        ## @brief  Motor object
        self.motor = motor.MotorDriver(self.ENA, self.IN1A_pin, self.IN2A_pin, self.tim_MOT_A)
         
        ## @brief  Timing variable for tracking starting time.
        self.start_time = utime.ticks_ms()
        ## @brief  Timing variable for recording time.
        self.record_time = self.start_time
        ## @brief  Timing variabe for recording period.
        self.record_period = 20
        ## @brief  Array of time data point values for plotting.
        self.time_list = array.array('i', [1000]*0)
        ## @brief  Array of position values for plotting.
        self.position_list = array.array('f', [1000]*0)
        
     def run(self):
         '''! @brief Runs the controller task and sets new duty cycle 
         '''
         ## @brief  Controller object
         self.controller = controller.controller(self.set_point_share.get(), self.gain_share.get())
         
         while True:
             
             ## @brief  Encoder position reading, accounting for 
             true_position = float(self.encoder_share.get())
             ## @brief  Difference between measured and setpoint values
             self.calc_error = self.controller.run(true_position)
             self.motor.set_duty_cycle(float(self.calc_error))
             
             ## @brief  Timing variable for tracking the current time.
             self.current_time = utime.ticks_diff(utime.ticks_ms(), self.start_time)
             
             #if utime.ticks_diff(self.current_time,self.record_time) >=0: 
             self.time_list.append(self.current_time)
             self.position_list.append(true_position)
             #print(position_list)
               #self.record_time = utime.ticks_add(self.current_time, self.record_period)

             print_task.put(str(true_position))
            
             yield (0)
             
     def prints(self):
         '''! @brief    Prints time and position data for plotting.
         '''
         for k in range(len(self.time_list)):
             
             ## @brief  Time stamps for plotting
             self.time = utime.ticks_diff(self.time_list[k], self.time_list[0])
             print(self.time  ,',', self.position_list[k])

         self.motor.set_duty_cycle(0)     
         self.time_list = array.array('i', [1000]*0)
         self.position_list = array.array('f', [1000]*0)