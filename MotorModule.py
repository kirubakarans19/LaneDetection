from gpiozero import Motor, PWMOutputDevice
from time import sleep

class MotorController:
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        # Initialize motors using gpiozero Motor and PWMOutputDevice
        self.left_motor = Motor(In1A, In2A)
        self.right_motor = Motor(In1B, In2B)
        self.pwmA = PWMOutputDevice(EnaA)
        self.pwmB = PWMOutputDevice(EnaB)
        
    def set_speed(self, speed, turn=0):
        # Calculate speed for each motor
        left_speed = speed - turn
        right_speed = speed + turn

        # Clamp speed between -1.0 and 1.0
        left_speed = max(min(left_speed, 0.25), -0.25)
        right_speed = max(min(right_speed, 0.25), -0.25)

        # Set PWM duty cycle to control speed
        self.pwmA.value = abs(left_speed)
        self.pwmB.value = abs(right_speed)

        # Set motor directions
        if left_speed > 0:
            self.left_motor.forward(left_speed)
        elif left_speed < 0:
            self.left_motor.backward(-left_speed)
        else:
            self.left_motor.stop()

        if right_speed > 0:
            self.right_motor.forward(right_speed)
        elif right_speed < 0:
            self.right_motor.backward(-right_speed)
        else:
            self.right_motor.stop()

    def move(self, speed=0.25, turn=0, t=0):
        self.set_speed(speed, turn)
        sleep(t)
        self.stop()

    def stop(self, t=0):
        self.left_motor.stop()
        self.right_motor.stop()
        sleep(t)

def main():
    motor = MotorController(EnaA=2, In1A=3, In2A=4, EnaB=17, In1B=27, In2B=22)
    
    motor.move(0.25, 0, 2)
    motor.stop(2)
    motor.move(-0.25, 0, 2)
    motor.stop(2)
    motor.move(0, 0.5, 2)
    motor.stop(2)
    motor.move(0, -0.5, 2)
    motor.stop(2)

if __name__ == '__main__':
    main()
