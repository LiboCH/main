import time

class bcolors:
	CEND      = '\33[0m'
	CBOLD     = '\33[1m'
	CITALIC   = '\33[3m'
	CURL      = '\33[4m'
	CBLINK    = '\33[5m'
	CBLINK2   = '\33[6m'
	CSELECTED = '\33[7m'

	CBLACK  = '\33[30m'
	CRED    = '\33[31m'
	CGREEN  = '\33[32m'
	CYELLOW = '\33[33m'
	CBLUE   = '\33[34m'
	CVIOLET = '\33[35m'
	CBEIGE  = '\33[36m'
	CWHITE  = '\33[37m'

	CBLACKBG  = '\33[40m'
	CREDBG    = '\33[41m'
	CGREENBG  = '\33[42m'
	CYELLOWBG = '\33[43m'
	CBLUEBG   = '\33[44m'
	CVIOLETBG = '\33[45m'
	CBEIGEBG  = '\33[46m'
	CWHITEBG  = '\33[47m'

	CGREY    = '\33[90m'
	CRED2    = '\33[91m'
	CGREEN2  = '\33[92m'
	CYELLOW2 = '\33[93m'
	CBLUE2   = '\33[94m'
	CVIOLET2 = '\33[95m'
	CBEIGE2  = '\33[96m'
	CWHITE2  = '\33[97m'

def print_task(task_name,state,counter):
    exit_states={
        'success':"["+bcolors.CGREEN2+"SUCCESS"+bcolors.CEND+"]",
        'error':"["+bcolors.CRED2+" ERROR "+bcolors.CEND+"]",
        'warn':"["+bcolors.CYELLOW2+"WARNING"+bcolors.CEND+"]"
        }

    progress_bar=[
    "["+bcolors.CBLUE2+'       '+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+'■      '+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+'■■     '+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+' ■■    '+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+'  ■■   '+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+'   ■■  '+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+'    ■■ '+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+'     ■■'+bcolors.CEND+"]",
    "["+bcolors.CBLUE2+'      ■'+bcolors.CEND+"]"]
    print(f'\r',end='',flush=True);
    print(f'{task_name} '.ljust(50,'.'),end='',flush=True)
    if state=='running':
        print(f'{progress_bar[counter%9]}',end='',flush=True)
    else:
        if state != 'error':
            print(f'{exit_states[state]}',flush=True)
        else:
            print(f'{exit_states[state]} log: /some/log/path/file.log',flush=True)


if __name__ == '__main__':

    for i in range(30):
        print_task('Checking','running',i)
        time.sleep(0.1)
    print_task('Checking','warn',i)
    for i in range(30):
        print_task('Doing','running',i)
        time.sleep(0.1)
    print_task('Doing','error',i)


