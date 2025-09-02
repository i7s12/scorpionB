from colorama import Fore as F
import os

os.system('clear')

__version__ = '0.3'
__author__ = "iraq_Team"

print(f'''
{F.BLUE}
.___                       
|   |___________    ______ 
|   \_  __ \__  \  / ____/ 
|   ||  | \// __ \< <_|  | 
|___||__|  (____  /\__   |
                \/    |__|


                {F.CYAN} ScorpionB V{F.GREEN} {__version__}{F.RESET}

''')
print(F.WHITE+'_'*40)

def listMethod():

    print(f'''
{F.GREEN}1- {F.RESET}HTTP-PROXIES. 
{F.GREEN}2- {F.RESET}UDP. (Coming Soon)
{F.GREEN}3- {F.RESET}DNS. (Coming Soon)
{F.GREEN}4- {F.RESET}SLOWLORIS. (Coming Soon)
''')

    choiceMethod = int(input(f'''{F.CYAN}┌─({F.GREEN}ScorpionB{F.CYAN})─({F.YELLOW}~ Method{F.CYAN})
└──╼ {F.YELLOW}~#{F.GREEN} '''))

    if choiceMethod == 1:
        os.system('python3 tools/scorpion_http.py')
    elif choiceMethod in [2, 3, 4]:
        print(f'\n{F.YELLOW}This method is {F.RED}Coming Soon{F.RESET}\n')
    else:
        print(f'{F.RED}( !!! ) {F.RESET}Error! Choose between {F.CYAN}1-4{F.RESET}!')

if __name__ == "__main__":
    listMethod()
