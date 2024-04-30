import shutil

class ProgBar:
    def __init__(self, total: int):
        self.total = total
        self.width = shutil.get_terminal_size().columns - 4 - len(str(self.total))*2
        self.cnt = 1
        
    def increment(self, print_flg: bool = True):
        prog_bar = '{bar:{length}}'.format(bar='=' * int(self.cnt / self.total * self.width), length=self.width)
        if print_flg:
            print('\r[{0}] {1:>{3}}/{2}'.format(prog_bar, self.cnt, self.total, len(str(self.total))), end='')
        self.cnt += 1