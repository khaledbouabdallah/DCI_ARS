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
    
    args = set()
    attacks = []
    
    def __init__(self,path) -> None:
        with open(path) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("arg"): 
                    self.args.add(line[4:].split(")")[0])
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
    
    def _set_is_in_list(self,s,l) -> bool: #check if a set is in a list of sets (somehow set in L does not work directly)
        for x in l:
            if x == s:
                return True
        return False
    
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
      
    def _generate_possible_complete_(self) -> list:
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
            for argument in self.args:
                    if self._set_is_in_list(set(argument),result):
                        continue
                    logger.info(f"picked start: {argument}")
                    new_attackers = self._get_not_attacked_by(self.args,argument) # original set - set which are attacked by the grounded (first iteration example) 
                    new_not_attacked = self._get_not_attacked_by(self.args,new_attackers) # set which are not attacked by #1 (defended by grounded (first iteration))
        
                    if not new_not_attacked: # pass current iteration
                        logger.info(f"new possible complete: 'empty set'")
                        continue 
                    logger.info(f"new possible complete: {new_not_attacked}")
                    if not self._set_is_in_list(new_not_attacked,result): 
                            result.append(new_not_attacked)
                    while True: # same logic as the other case
                        new_attackers = self._get_not_attacked_by(self.args,result[-1]) 
                        new_not_attacked = self._get_not_attacked_by(self.args,new_attackers)      
                        if self._set_is_in_list(new_not_attacked,result): 
                            break
                        logger.info(f"new possible complete: {new_not_attacked}")
                        result.append(new_not_attacked)
            logger.info(f"list of possible complete extensions: {result}")
            return result
                
            



def main():
    parser = argparse.ArgumentParser()
    # Add script arguments
    parser.add_argument('-p', type=str) # Function
    parser.add_argument('-f', type=str) # File
    parser.add_argument('-a', type=str) # Arguments
    # Parse the command-line arguments
    args = parser.parse_args()
    af = AF(path=args.f)
    af._generate_possible_complete_()

    
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
