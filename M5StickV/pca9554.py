from machine import I2C

# define command byte registers
IN_REG   = 0x00 # Input register
OUT_REG  = 0x01 # Output register
POL_REG  = 0x02 # Polarity inversion register
CONF_REG = 0x03 # Config register (0=output, 1=input)


class PCA9554(object):
    def __init__(self, i2c_bus=I2C.I2C1, address=0x27, scl=34, sda=35, freq=400000):
        try:
            print("i2c_address:" + str(address))
            self.PORTS_COUNT = 8   # number of GPIO ports
            self.i2c_address = address
            self.i2c = I2C(i2c_bus, mode=I2C.MODE_MASTER, scl=scl, sda=sda, freq=freq)
            devices = self.i2c.scan()
            print(devices)

            if self.read_input_register() is None:
                raise ValueError

        except ValueError:
            print("No device found")
            self.i2c = None

    def i2c_read_byte(self, register):
        return self.i2c.readfrom_mem(self.i2c_address, register, 1, mem_size=8)

    def i2c_write_byte(self, register, value):
        print(value)
        if value < 0x00 or value > 0xff:
           print("write value is invalid"+ str(value))
           raise ValueError
        self.i2c.writeto_mem(self.i2c_address, register, value, mem_size = 8)

    def read_input_register(self):
        return self.i2c_read_byte(IN_REG)

    def read_output_register(self):
        return self.i2c_read_byte(OUT_REG)
        
    def read_polarity_inversion_register(self):
        return self.i2c_read_byte(POL_REG)

    def read_config_resister(self):
        return self.i2c_read_byte(CONF_REG)

    def read_port(self, port_num):
        """Read port bit value (high=1 or low=0)."""
        if port_num < 0 or port_num >= self.PORTS_COUNT:
            return None
        line_value = self.i2c_read_byte(IN_REG)
#        print(line_value)
#        print(port_num)
        ret = ((line_value[0] >> port_num) & 1)
#        print(ret)
        return ret

    def write_port(self, port_num, state):
        """Write port bit specified in port_num to state value: 0=low, 1=high. Return True if successful."""
        if port_num < 0 or port_num >= self.PORTS_COUNT:
            return False
        if state < 0 or state > 1:
            return False
        current_value = self.i2c_read_byte(OUT_REG)
        if state:
            new_value = current_value[0] | 1 << port_num
        else:
            new_value = current_value[0] & (255 - (1 << port_num))

        self.i2c_write_byte(OUT_REG, new_value)
        return True

    def write_output_register(self, value):
        """Write all ports to states specified in byte value(each pin bit: 0=low, 1=high)."""
        self.i2c_write_byte(OUT_REG, value)

    def write_polarity_inversion_register(self, value):
        """Write polarity (1=inverted, 0=retained) for each input register port data (value has all ports polarities)."""
        self.i2c_write_byte(POL_REG, value)

    def write_config_register(self, value):
        """Write all ports to desired configuration (1=input or 0=output), parameter: value(type: byte)."""
        self.i2c_write_byte(CONF_REG, value)

    def write_config_port(self, port_num, state):
        """Write port configuration (specified by port_num) to desired state: 1=input or 0=output."""
        if port_num < 0 or port_num >= self.PORTS_COUNT:
            print("PORT_NUM error" + str(port_num))
            raise ValueError
        if state < 0 or state > 1:
            print("state error" + str(state))
            raise ValueError
        current_value = self.i2c_read_byte(CONF_REG)
        if state:
            new_value = current_value[0] | 1 << port_num
        else:
            new_value = current_value[0] & (255 - (1 << port_num))
        self.i2c_write_byte(CONF_REG, new_value)

    def __del__(self):
        """Driver destructor."""
        self.i2c = None
