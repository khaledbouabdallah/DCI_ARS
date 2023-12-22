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
        
    

    #MAIN FUNCTIONS

    def VE_CO(this, E) -> bool:
        list_co = this.generate_all_cf()
        print(list_co)
        res = []
        for elem in list_co:                 #we check for each elem if is complete so that res is the list of all co
            if this.is_complete(elem):
                res.append(elem)         

        print(res)
        return True if set(E) in res else False      

    def DC_CO(this, a) -> bool:
        list_co = this.generate_all_cf()
        res = []
        for elem in list_co:                 #we check for each elem if is complete
            if this.VE_CO(elem):
                res.append(elem)         

        for elem in list_co:                 #we check if a is in one co
            if a in elem:
                return True
        return False                        

    def DS_CO(this, a) -> bool:
        list_co = this.generate_all_cf()
        res = []
        for elem in list_co:                 #we check for each elem if is complete
            if this.VE_CO(elem):
                res.append(elem)         

        for elem in list_co:                 #we check if a is in each co
            if a not in elem:
                return False
        return True                         

    

    def VE_ST(this, E) -> bool:
        list_co = this.generate_all_cf()
        print(list_co)
        res = []
        for elem in list_co:                 #we check for each elem if is stable so that res is the list of all st
            if this.is_stable(elem):
                res.append(elem)         

        print(res)
        return True if set(E) in res else False      
    
    def DC_ST(this, a) -> bool:
        list_co = this.generate_all_cf()
        res = []
        for elem in list_co:                 #we check for each elem if is Stable
            if this.VE_ST(elem):
                res.append(elem)            

        for elem in list_co:                 #we check if a is in one st
            if a in elem:
                return True
        return False                         

    def DS_ST(this, a) -> bool:
        list_co = this.generate_all_cf()
        res = []
        for elem in list_co:                 
            if this.VE_ST(elem):
                res.append(elem)            

        for elem in list_co:                 #we check if a is in each st
            if a not in elem:
                return False
        return True                         
    




    def is_admissible(this, E: list) -> bool:      #returns True if E is an admissable set
        for i in E:
            for j in E:
                if [i,j] in this.attacks:
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
        if not this.is_admissible(E):
            return False
        for a in E:                                       #for each a in E, we're looking if a is defended by E
            a_attacked_by_list = this.attacked_by(a)      #first we look into everything that attacks a
            for elem in a_attacked_by_list:               #then we check if each attacker is attacked by E
                if not this.is_defended(this.attacked_by(elem), E):         #we check if defended by E
                    return False
        return True
    
    def attacked_by(this, a) -> list:       #returns the list of everything that attacks a
        res = []
        for attack in this.attacks:
            if attack[1] == a:
                res.append(attack[0])
        return set(res)

    def is_defended(this, defensers_list, E) -> bool:  #returns True if at least one defenser is in E 
        for elem in defensers_list:
            if elem in E:
                return True
        return False 

    


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


    ## GENERATE ALL CF PART:

    def generate_all_cf(self) -> list:       #generate all cf sets for the AF
        res = [set([])]
        for elem in self.args:
            res_to_add = self.cf(elem)       #calculte all cfs induced by each element of the AF
            for elem in res_to_add:
                if isinstance(elem,str):     #if a single element add it as a set, else just append, we do this because we want a list of sets
                    res.append(set(elem))
                else:
                    res.append(elem)
        return res

    def cf(self, a) -> list:            # returns list of everything a defends, recusrive function
        if self.elem_defends(a) == []:  
            return a
        res = [set(a)]
        elems_defended_by_a = self.elem_defends(a)
        for elem in elems_defended_by_a:
            #print(a, elem, ":", [a] + elem)
            res.append(set([a] + elem))      #we do this because we want the complete list of args in the set, not just elem but also a
        return self.cf(res)
        
    
    def elem_defends(self, a) -> list:                  #return list of every args a defends
        a_attacks = self.elem_attacks(a)
        a_defends = []
        for elem in a_attacks:
            if self.elem_attacks(elem) != []:
                for elem_defends in flatten(self.elem_attacks(elem)):
                    if elem_defends != a and elem_defends not in a_attacks:
                        a_defends.append(self.elem_attacks(elem))
        #print(a, "attacks:", a_attacks, "and denfends: ", a_defends)
        return a_defends

    def elem_attacks(self, a) -> list:                  #return list of every args a attacks
        res = []
        for attack in self.attacks:
            if attack[0] == a:
                res.append(attack[1])
        return res



def majuscule(E):                    #uppers all character in E, usefull in main
        res = []
        for elem in E:
            res.append(elem.upper())
        return res

def flatten(xss):                    #flattens a list of list
    return [x for xs in xss for x in xs]

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
        print("YES") if af.VE_CO(majuscule(args.a.split(","))) else print("NO")

    elif args.p == "DC-CO":
        print("YES") if af.DC_CO(args.a.upper()) else print("NO")

    elif args.p == "DS-CO":
        print("YES") if af.DS_CO(args.a.upper()) else print("NO")

    elif args.p == "VE-ST":
        print("YES") if af.VE_ST(majuscule(args.a.split(","))) else print("NO")

    elif args.p == "DC-ST":
        print("YES") if af.DC_ST(args.a.upper()) else print("NO")

    elif args.p == "DS-ST":
        print("YES") if af.DS_ST(args.a.upper()) else print("NO")

if __name__ == "__main__":
    main()
    log_handler.close()
