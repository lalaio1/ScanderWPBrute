from pystyle import Colors, Colorate

def print_banner():
    with open('./banner/banner.txt', 'r') as file:
        banner = file.read()
    print(Colorate.Horizontal(Colors.rainbow, banner))