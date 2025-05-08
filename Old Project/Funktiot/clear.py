from os import system, name

# HUOM tämä on kopioitu stackoverflowsta suoraan koska oli sen verran hyvä ja tekee juuri mitä toivottiin
# define our clear function
def clear():
    # for windows the name is 'nt'
    if name == 'nt':
        _ = system('cls')

    # and for mac and linux, the os.name is 'posix'
    else:
        _ = system('clear')
    return
# Then, whenever you want to clear the screen, just use this clear function as:
