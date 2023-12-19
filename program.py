import argparse
import logging
import numpy as np
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
        
    
    
    def VE_CO(this, E) -> bool:
        list_co = this.generate_possible_complete()

        for elem in list_co:                 #we check for each elem if is complete
            if not this.is_complete(elem):
                list_co.remove(elem)         #if not we remove it from the list

        return True if set(E) in list_co else False      #return True if E in the list of complete extensions
    

    def DC_CO(this, a) -> bool:
        list_co = this.generate_possible_complete()

        for elem in list_co:                 #we check for each elem if is complete
            if not this.VE_CO(elem):
                list_co.remove(elem)         #if not we remove it from the list

        for elem in list_co:                 #we check if a is in one co
            if a in elem:
                return True
        return False                         #if not we return False
    

    def DS_CO(this, a) -> bool:
        list_co = this.generate_possible_complete()

        for elem in list_co:                 #we check for each elem if is complete
            if not this.VE_CO(elem):
                list_co.remove(elem)         #if not we remove it from the list

        for elem in list_co:                 #we check if a is in each co
            if a not in elem:
                return False
        return True                          #if not we return True

    
    def VE_ST(this, E) -> bool:
        list_co = this.generate_possible_complete()

        for elem in list_co:                 #we check for each elem if is stable
            if not this.is_stable(elem):
                list_co.remove(elem)         #if not we remove it from the list

        return True if set(E) in list_co else False   #return True if E in the list of stable extensions
    

    def DC_ST(this, a) -> bool:
        list_co = this.generate_possible_complete()

        for elem in list_co:                 #we check for each elem if is complete
            if not this.VE_ST(elem):
                list_co.remove(elem)         #if not we remove it from the list

        for elem in list_co:                 #we check if a is in one co
            if a in elem:
                return True
        return False                         #if not we return False

    
    def DS_ST(this, a) -> bool:
        list_co = this.generate_possible_complete()

        for elem in list_co:                 #we check for each elem if is complete
            if not this.VE_ST(elem):
                list_co.remove(elem)         #if not we remove it from the list

        for elem in list_co:                 #we check if a is in each co
            if a not in elem:
                return False
        return True                          #if not we return True
    


    def _get_attacks_by_(self,s) -> set: # get list of attacks done by set s (list of lists)
        attacks = [] 
        for attack in self.attacks:
            if attack[0] in s:
                attacks.append(attack)
        return attacks
    
    def _is_attacked_by_(self,s,z) -> bool: # return True if set 's' is attacked by set 'z'
        attacks = self._get_attacks_by_(z)
        for a in s:   
            for attack in attacks :
                if attack[1] == a:
                    return True
        return False
    
    def _get_attacked_by_(self,s,z) -> set: # get subset of 's' which is attacked by set 'z'
        attacked = set()
        for a in s:
            if self._is_attacked_by_([a],z):
                attacked.add(a)
        return attacked
    
    def _get_not_attacked_by(self,s,z) -> set: # get subset of 's' which are not attacked by set 'z'
        arguments = set(self.args)
        return arguments.difference(self._get_attacked_by_(s,z))
    
 
    
  
    def generate_possible_complete(self) -> list:
        result = []
        # find nodes that are not attacked by anyone
        not_attacked =  self._get_not_attacked_by(self.args,self.args)
        result.append(not_attacked)
            
        if not_attacked: # we found something 
            logger.info(f"not attacked at all (grounded): {not_attacked}")     
            while True:
                new_attackers = self._get_not_attacked_by(self.args,result[-1]) # original set - set which are attacked by the grounded (first iteration example) #1
                new_not_attacked = self._get_not_attacked_by(self.args,new_attackers) # set which are not attacked by #1 (defended by grounded (first iteration))
                logger.info(f"new possible complete: {new_not_attacked}")
                if new_not_attacked in result:
                    return result
                result.append(new_not_attacked)
        else: # we only have the empty set 
            logger.info(f"not attacked at all (grounded): empty set")            
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

    def is_complete(this, E:list) -> bool:
        for a in E:                                
            for b in this.args:                         #we check everything that a is attacking
                if [a,b] in this.attacks:
                    for set_attack in this.attacks:            #we check everything attacked by b, and so defended by a
                        if [b,set_attack[1]] in this.attacks:  
                            if set_attack[1] not in E:         #if that element is not in E, then E is not a CO
                                return False
        return True 
    
    def is_stable(this, E:list) -> bool:
        not_E = set(this.args) - set(E)      # A \ E
        
        val = False
        for a in not_E:                      #we check for each a € A\E if an element from E attacks a
            for set_attack in this.attacks:
                if set_attack[0] in E and set_attack[1] == a:
                    val = True
            if not val:                      #if there's none we return False directly
                return False
            else:                            #if there's one we put val back to False for the next loop
                val = False
        return True

def main():
    parser = argparse.ArgumentParser()
    # Add script arguments
    parser.add_argument('-p', type=str) # Function
    parser.add_argument('-f', type=str) # File
    parser.add_argument('-a', type=str) # Arguments
    # Parse the command-line arguments
    args = parser.parse_args()
    af = AF(path=args.f)


    if args.p == "VE-CO":
        print("YES") if af.VE_CO(args.a.split(",")) else print("NO")

    elif args.p == "DC-CO":
        print("YES") if af.DC_CO(args.a) else print("NO")

    elif args.p == "DS-CO":
        print("YES") if af.DS_CO(args.a) else print("NO")

    elif args.p == "VE-ST":
        print("YES") if af.VE_ST(args.a.split(",")) else print("NO")

    elif args.p == "DC-ST":
        print("YES") if af.DC_ST(args.a) else print("NO")

    elif args.p == "DS-ST":
        print("YES") if af.DS_ST(args.a) else print("NO")

if __name__ == "__main__":
    main()
    log_handler.close()
