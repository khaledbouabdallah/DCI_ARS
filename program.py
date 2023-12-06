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
    
    
    def VE_CO(self) -> bool:
        pass
    
    def DC_CO(self) -> bool:
        pass
    
    def DS_CO(self) -> bool:
        pass
    
    def VE_ST(self) -> bool:
        pass
    
    def DC_ST(self) -> bool:
        pass
    
    def DS_ST(self) -> bool:
        pass
    

    def is_admissible(this, E: list) -> bool:      #returns True if E is an admissable set
        for i in range(len(E)):                    #verify conflict-freeness
            for j in range(i+1, len(E)):
                if [E[i], E[j]] in this.attacks:
                    return False
        
        val = False
        for a in E:                                #verify defense
            for b in this.args:
                if [b,a] in this.attacks:
                    for c in E:
                        if [c,b] in this.attacks:  #looking for a defender for a
                            val = True
                    if val == False:
                        return False
        return True


"""   ça marche pas bien encore 
    def is_complete(this, S: list) -> bool:      #return True if E is a complete extension
        if not this.is_admissible(S):
            return False
        for a in this.args:
            attacking_a = []
            for elem1 in this.attacks:            
                if elem1[1] == a:                 #we list all the args that are attacking a
                    attacking_a.append(elem[0])
                    for elem_attacking_a in attacking_a:
                        for elem2 in this.attacks: #we check if all the elements attacking a are attacking by an element in S
                            if elem2[1] == elem_attacking_a and elem2[0] in S:
                                continue
                        return False
        return True
"""

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
    #print(af.is_admissible(['a','c','d']))          #a little test..
    
    if args.p == "VE-CO":
        print("YES") if af.VE_CO(args.a) else print("NO")

    elif args.p == "VE-ST":
        print("YES") if af.VE_ST(args.a) else print("NO")

    elif args.p == "DC-CO":
        print("YES") if af.DC_CO(args.a) else print("NO")

    elif args.p == "DS-CO":
        print("YES") if af.DS_CO(args.a) else print("NO")

    elif args.p == "DC-ST":
        print("YES") if af.DC_ST(args.a) else print("NO")

    elif args.p == "DS-ST":
        print("YES") if af.DS_ST(args.a) else print("NO")

if __name__ == "__main__":
    main()
