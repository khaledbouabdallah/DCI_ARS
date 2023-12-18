import argparse
import logging
import datetime


# Set up the logging configuration with a FileHandler
#log_filename = f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
log_filename = "log.txt"
log_handler = logging.FileHandler(log_filename, mode='w')
log_handler.setLevel(logging.DEBUG)  # Set the level to the lowest (DEBUG)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# Create a logger and add the FileHandler to it
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)  # Set the logger level to the lowest (DEBUG)


# Example usage

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
        logger.info(f'list of arguments: {self.args}') 
        logger.info(f'list of attacks: {self.attacks}')             
        
    
    
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
    
    def _get_attacks_by_(self,s) -> list: # get list of attacks done by set s (list of lists)
        attacks = []    
        for attack in self.attacks:
            if attack[0] in s:
                attacks.append(attack)
        return attacks
    
    def _is_attacked_by_(self,s,z) -> bool: # return True if set 's' attack is attacked by set 'z'
        attacks = self._get_attacks_by_(z)
        for a in s:   
            for attack in attacks :
                if attack[1] == a:
                    return True
        return False
    
    def _get_attacked_by_(self,s,z) -> list: # get subset of s which is attacked by set z
        attacked = []
        for a in s:
            if self._is_attacked_by_([a],z):
                attacked.append(a)
        return attacked
    
 
    
  
    def generate_possible_complete(self) -> list:
        result = []
        # find nodes that are not attacked 
        attacked = self._get_attacked_by_(self.args,self.args)
        not_attacked = set(self.args).difference(set(attacked))
        result.append(not_attacked)
        logger.info(f"not attacked at all: {not_attacked}")         
        if not_attacked: # we found something 
            while True:
                new_attacked = self._get_attacked_by_(self.args,result[-1]) # argument that are attacked with our initial "grounded"
                new_attackers = set(self.args).difference(set(new_attacked)) # remove their attacks 
                new_attacked = self._get_attacked_by_(self.args,new_attackers) # find elements that are attacked
                new_not_attacked = set(self.args).difference(set(new_attacked)) # find new set that are not attacked after 
                logger.info(f"new possible complete: {new_not_attacked}")
                if new_not_attacked in result:
                    return result
                result.append(new_not_attacked)
        else: # we only have the empty set 
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
    af.generate_possible_complete()
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
    log_handler.close()
