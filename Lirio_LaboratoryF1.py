def remainder():
    dividend: float = float(input("Enter the dividend: "))
    divisor: float = float(input("Enter the divisor: "))
    remainder = dividend % divisor
    print(f"The remainder when {dividend} is divided by {divisor} is {remainder}")

def Concatenate():
    num1: int = int(input("Enter an interger: "))
    num2: float = float(input("Enter a number with decimals: "))
    print("Here are the results: Integer = " + str(num1) + ", Float = " + str(num2))
    print(f"Here are the results: Integer = {num1}, Float = {num2}")

def Concatenate2():
    name: str = input("Enter your name: ")
    num: int = int(input("Enter a number: "))
    print("Hello, "+ name + " You entered "+ str(num) + ", and double that is " + str(num*2)+ ".")
    print(f"Hello, {name} You entered {num}, and double that is {num*2}.")
def main():
    Concatenate2()

if __name__ == '__main__':
    main()