import serial

class Joystick:

    def __init__(self, connection_port = "COM5", baud_rate : int = 9600) -> None:
        # Conenction parameters
        self.port = connection_port
        self.baud_rate = baud_rate
        self.timeout = 1
        # Creating the connection
        self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        
        # Fucntional variables
        self.last_read = (0, 0, 0)
        

    def get_joystick(self):
        result = self.serial_connection.readline()
        # Remove control characters (carriage return and newline \r\n) 
        result = result[:-2]
        result = result.decode()

        # Creates a list with the output values
        out = result.split(";")
 
        if len(out) == 3:
            # Convert to int
            out = [int(value) for value in out]

            # Normalize x,y ranges [0, 1024] to [-1, 1]
            out[0] = out[0] / 1024 * 2 - 1
            out[1] = out[1] / 1024 * 2 - 1
            # Invert button default value to 0
            out[2] ^= 1
            return tuple(out)

        return self.last_read