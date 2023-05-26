#-------------------------------------------
# USCC Headquarter's Instruction Set Architecture
#  System Design:
#   - Four function calculator
#   - Can only operate on numbers stored in registers
#   - Processor receives binary data as 32-bit strings
#   - Returns results to the terminal
#   - Can operate on 10-bit numbers (0 thru 1023)
#   - Results can be negative (5 - 10 = -5)
#  Instruction format:
#   - 32 bit's in length
#   - Binary data will come to the CPU as a string
#   - Registers (32 total on CPU, 0-indexed)
#      - 0 thru 21:  Available for number storage
#        - 0: Constant 0
#      - 22 thru 31: Available for history storage
# +=======+=======+=======+=======+=======+=======+=======+=======+
# | 0: 0  | 1:    | 2:    | 3:    | 4:    | 5:    | 6:    | 7:    |
# +-------+-------+-------+-------+-------+-------+-------+-------+
# | 8:    | 9:    |10:    |11:    |12:    |13:    |14:    |15:    |
# +-------+-------+-------+-------+-------+-------+-------+-------+
# |16:    |17:    |18:    |19:    |20:    |21:    |22: H0 |23: H1 |
# +-------+-------+-------+-------+-------+-------+-------+-------+
# |24: H2 |25: H3 |26: H4 |27: H5 |28: H6 |29: H7 |30: H8 |31: H9 |
# +=======+=======+=======+=======+=======+=======+=======+=======+
#   - Bits 0-5 are OPCODEs
#     - use variable 'opcode' in program
#   - Bits 6-10 & 11-15 are source register locations
#     - use variables 'source_one' and 'source_two' in program
#   - Bits 16-25 are reserved for adding a new value to the registers
#     - use variable 'store' in program
#   - Bits 26-31 are functions
#     - use variable 'function_code' in program
# +--------+----------+-------------------------------------+
# | OPCODE | FUNCTION | Definition                          |
# | 000000 |  100000  | Add two numbers from registers      |
# | 000000 |  100010  | Subtract two numbers from registers |
# | 000000 |  011000  | Multiply two numbers from registers |
# | 000000 |  011010  | Divide two numbers from registers   |
# | 000001 |  000000  | Store value to next register        |
# | 100001 |  000000  | Return previous calculation         |
# +--------+----------+-------------------------------------+

#######################################################
# Class: UltraSuperCalculator
#######################################################
class UltraSuperCalculator:
  def __init__(self, name) -> None:
    self.name = name
    
    # These lists simulate empty registers when calculator first turned on
    self.number_registers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.history_registers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # ISA documentation specifies that number_registers[0] is always 0
    # So, numbers_index starts at 1
    self.numbers_index = 1
    self.history_index = 0
    self.temp_history_index = 0

    # Data that will be returned to user
    self.user_display = ''

    self.update_display(f"Hello {self.name}! Welcome to the USCC.")
  
  #######################################################
  # Function: update_display
  # Change the user_display and print to the console
  #######################################################
  def update_display(self, to_update):
    self.user_display = to_update

    print(self.user_display)
  
  #######################################################
  # Function: store_value_to_register
  # Stores values to the numbers register
  #######################################################  
  def store_value_to_register(self, value_to_store):
    # If all registers are full, start overwriting oldest registers
    if(self.numbers_index > 21):
      self.numbers_index = 1
    
    # Convert binary value to integer and store in numbers register
    self.number_registers[self.numbers_index] = int(value_to_store, 2)

    print(f"The number {self.number_registers[self.numbers_index]} was stored to register {self.numbers_index}")

    self.numbers_index += 1

  #######################################################
  # Function: load_value_from_register
  # Loads a value from the register
  # For use with actual calculation methods
  #######################################################  
  def load_value_from_register(self, register_address):
    # Convert register address binary to int
    index = int(register_address)

    # Retrieve the number at the specified address
    int_value = int(self.number_registers[index])

    return int_value

  #######################################################
  # Function: store_to_history_register
  # Stores result in history register
  #######################################################  
  def store_to_history_register(self, result_to_store):
    # If all history registers are full, start overwriting oldest registers
    if(self.history_index > 9):
      self.history_index = 0

    # Convert result to a binary and store in history register
    self.history_registers[self.history_index] = bin(result_to_store)

    self.history_index += 1
    # Ensure that after each calculation, history starts at right location
    self.temp_history_index = self.history_index

  #######################################################
  # Function: add
  # Adds numbers stored in registers
  #######################################################  
  def add(self, address_num1, address_num2):
    # Load values
    num1 = self.load_value_from_register(address_num1)
    num2 = self.load_value_from_register(address_num2)

    # Perform calculation
    calculated_value = num1 + num2

    return calculated_value

  #######################################################
  # Function: subtract
  # Subtracts numbers stored in registers
  ####################################################### 
  def subtract(self, address_num1, address_num2):
    # Load values
    num1 = self.load_value_from_register(address_num1)
    num2 = self.load_value_from_register(address_num2)

    # Perform calculation
    calculated_value = num1 - num2

    return calculated_value

  #######################################################
  # Function: multiply
  # Multiplies numbers stored in registers
  ####################################################### 
  def multiply(self, address_num1, address_num2):
    # Load values
    num1 = self.load_value_from_register(address_num1)
    num2 = self.load_value_from_register(address_num2)

    # Perform calculation
    calculated_value = num1 * num2

    return calculated_value

  #######################################################
  # Function: multiply
  # Divides numbers stored in registers
  ####################################################### 
  def divide(self, address_num1, address_num2):
    # Load values
    num1 = self.load_value_from_register(address_num1)
    num2 = self.load_value_from_register(address_num2)

    calculated_value = 0

    # Check for division by 0
    if(num2 != 0):
      calculated_value = int(num1 / num2)
    else:
      print(f"Division by 0 error: {num1}/{num2}.")

    # Returns 0 if dividing by zero
    return calculated_value

  #######################################################
  # Function: get_last_calculation
  # Returns the last calculated value
  ####################################################### 
  def get_last_calculation(self):
    # Look backwards
    self.temp_history_index -= 1

    # Formulate message with last calculated value in history register
    last_value = f"Last Calculated Value: {int(self.history_registers[self.temp_history_index], 2)}"

    self.update_display(last_value)

  #######################################################
  # Function: binary_reader
  # Process binary data coming in from user
  ####################################################### 
  def binary_reader(self, instruction):
    # Check if valid instruction length
    if(len(instruction) != 32):
      self.update_display("Invalid Instruction Length")
      return

    # Break up instruction into its separate parts
    opcode = instruction[0 : 6]
    source_one = instruction[6 : 11]
    source_two = instruction[11 : 16]
    store = instruction[16 : 26]
    function_code = instruction[26:]

    # Process opcode
    if(opcode == '000001'):
      self.store_value_to_register(store)
      return
    elif(opcode == '100001'):
      self.get_last_calculation()
      return
    elif(opcode != '000000'):
      self.update_display("Invalid OPCODE")
      return

    result = 0

    if(function_code == '100000'):
      result = self.add(source_one, source_two)
    elif(function_code == '100010'):
      result = self.subtract(source_one, source_two)
    elif(function_code == '011000'):
      result = self.multiply(source_one, source_two)
    elif(function_code == '011010'):
      result = self.divide(source_one, source_two)
    else:
      self.update_display("Invalid Function Code")
      return

    # Store result to history register
    self.store_to_history_register(result)

    # Display calculated result
    self.update_display(f"Calculated Result: {result}")
    

#######################################################
####################################################### 

new_calculator = UltraSuperCalculator("Nick")

# Adds 5 and 10 to number registers
new_calculator.binary_reader("00000100000000000000000101000000")
new_calculator.binary_reader("00000100000000000000001010000000")
 
# Adds/Subtracts/Multiplies/Divides 5 and 10 from registers
new_calculator.binary_reader("00000000001000100000000000100000")
new_calculator.binary_reader("00000000001000100000000000100010")
new_calculator.binary_reader("00000000001000100000000000011000")
new_calculator.binary_reader("00000000001000100000000000011010")
 
# Gets the last three calculations
new_calculator.binary_reader("10000100000000000000000000000000")
new_calculator.binary_reader("10000100000000000000000000000000")
new_calculator.binary_reader("10000100000000000000000000000000")