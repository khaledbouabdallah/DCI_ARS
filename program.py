import sys
import os.path
import argparse

def load_AF(path):
    pass

class AF():
    
    args = []
    attacks = []
    
    def __init__(self,path) -> None:
        with open(path) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("arg"): 
                    self.args.append(line[4:].split(")")[0])
                elif line.startswith("att"):
                    attack = [line[4:].split(",")[0],line[4:].split(",")[1].split(")")[0]]
                    self.attacks.append(attack)
    
    
    def VE_CO(self) -> None:
        pass
    
    def DC_CO(self) -> None:
        pass
    
    def DS_CO(self) -> None:
        pass
    
    def VE_ST(self) -> None:
        pass
    
    def DC_ST(self) -> None:
        pass
    
    def DS_ST(self) -> None:
        pass
    
def main():
    parser = argparse.ArgumentParser()
    # Add script arguments
    parser.add_argument('-p', type=str) # Function
    parser.add_argument('-f', type=str) # File
    parser.add_argument('-a', type=str) # Arguments
    # Parse the command-line arguments
    args = parser.parse_args()
    # ##
    af = AF(path=args.f)
    print(af.args)
    print(af.attacks)
    
    if args.p == "":
        pass
    elif args.p == "":
        pass
    elif args.p == "":
        pass
    
    

if __name__ == "__main__":
    main()
