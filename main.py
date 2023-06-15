from td.TDParser import mainTD
from rbc.RBCParser import mainRBC

def main():
    print("Statements From Banks that Can be Converted:")
    print("1. TD")
    print("2. RBC")
    cont = True
    while(cont):
        str_state = input("Enter the statement's bank you want to convert (number): ")
        try:
            state = int(str_state)
            if state == 1 or state == 2:
                cont = False
            else:
                print("Error: input not valid, please try again")
        except:
            print("Error: input not valid, please try again")
    try:
        if state == 1:
            mainTD()
        else:
            mainRBC()
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()