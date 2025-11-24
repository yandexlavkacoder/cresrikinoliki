import random
import os

class krestikinoliki:
    def __init__(self):
        self.razmer_polya = 3
        self.pole = []
        self.kto_hodit = 'X'
        self.kak_igraem = 1
        self.papka_dlya_zapisi = "statistika_igr"
        
    def ochistit_pole(self):
        self.pole = [['.' for _ in range(self.razmer_polya)] for _ in range(self.razmer_polya)]
    
    def nachalo_novoy_igry(self):
        os.makedirs(self.papka_dlya_zapisi, exist_ok=True)
        
        while True:
            try:
                vvedenny_razmer = input("Введите размер поля (3-9): ")
                chislo = int(vvedenny_razmer)
                if 3 <= chislo <= 9:
                    self.razmer_polya = chislo
                    break
                else:
                    print("Неверный размер, пожалуйста, введите снова")
            except ValueError:
                print("Неверный размер, пожалуйста, введите снова")
        
        while True:
            try:
                rezhim = input("Выберите режим (1 - два игрока, 2 - против бота): ")
                if rezhim in ['1', '2']:
                    self.kak_igraem = int(rezhim)
                    break
                else:
                    print("Неверный режим, выберите 1 или 2")
            except ValueError:
                print("Неверный режим, выберите 1 или 2")
        
        self.kto_hodit = random.choice(['X', 'O'])
        print(f"Первым ходит: {self.kto_hodit}")
        
        self.ochistit_pole()
    
    def pokazat_pole(self):
        print("   " + " ".join(str(i + 1) for i in range(self.razmer_polya)))
        
        for nomer_stroki in range(self.razmer_polya):
            print(f"{nomer_stroki + 1}  " + " ".join(self.pole[nomer_stroki]))
        print()
    
    def postavit_krestik_ili_nolik(self, stroka, stolbec):
        if 0 <= stroka < self.razmer_polya and 0 <= stolbec < self.razmer_polya:
            if self.pole[stroka][stolbec] == '.':
                self.pole[stroka][stolbec] = self.kto_hodit
                return True
        return False
    
    def proverka_pobedy(self):
        for i in range(self.razmer_polya):
            if all(self.pole[i][j] == self.kto_hodit for j in range(self.razmer_polya)):
                return True
        
        for j in range(self.razmer_polya):
            if all(self.pole[i][j] == self.kto_hodit for i in range(self.razmer_polya)):
                return True
        
        if all(self.pole[i][i] == self.kto_hodit for i in range(self.razmer_polya)):
            return True
        
        if all(self.pole[i][self.razmer_polya - 1 - i] == self.kto_hodit for i in range(self.razmer_polya)):
            return True
        
        return False
    
    def net_pustyh_kletok(self):
        for i in range(self.razmer_polya):
            for j in range(self.razmer_polya):
                if self.pole[i][j] == '.':
                    return False
        return True
    
    def zapisat_v_fayl(self, pobeditel):
        imya_fayla = os.path.join(self.papka_dlya_zapisi, f"statistika_{self.razmer_polya}x{self.razmer_polya}.txt")
        with open(imya_fayla, 'a', encoding='utf-8') as f:
            f.write(f"Победитель: {pobeditel}, Размер поля: {self.razmer_polya}x{self.razmer_polya}\n")
    
    def chelovek_hodit(self):
        while True:
            try:
                vvod = input(f"Ход {self.kto_hodit}. Введите строку и столбец (например, 1 2): ")
                chasti = vvod.split()
                if len(chasti) != 2:
                    print("Неверный ввод. Введите два числа через пробел.")
                    continue
                
                stroka = int(chasti[0]) - 1
                stolbec = int(chasti[1]) - 1
                
                if self.postavit_krestik_ili_nolik(stroka, stolbec):
                    break
                else:
                    print("Неверный ход. Попробуйте снова.")
            except ValueError:
                print("Неверный ввод. Введите числа.")
            except IndexError:
                print("Неверный ввод. Числа должны быть в пределах поля.")
    
    def bot_hodit(self):
        svobodnye_kletki = []
        for i in range(self.razmer_polya):
            for j in range(self.razmer_polya):
                if self.pole[i][j] == '.':
                    svobodnye_kletki.append((i, j))
        
        if svobodnye_kletki:
            stroka, stolbec = random.choice(svobodnye_kletki)
            self.pole[stroka][stolbec] = self.kto_hodit
            print(f"Бот походил: {stroka + 1} {stolbec + 1}")
    
    def odin_krug_igry(self):
        self.nachalo_novoy_igry()
        
        while True:
            self.pokazat_pole()
            
            if self.kak_igraem == 2 and self.kto_hodit == 'O':
                self.bot_hodit()
            else:
                self.chelovek_hodit()
            
            if self.proverka_pobedy():
                self.pokazat_pole()
                print(f"{self.kto_hodit} выиграл!")
                self.zapisat_v_fayl(self.kto_hodit)
                break
            elif self.net_pustyh_kletok():
                self.pokazat_pole()
                print("Ничья!")
                self.zapisat_v_fayl("Ничья")
                break
            
            self.kto_hodit = 'O' if self.kto_hodit == 'X' else 'X'
    
    def start(self):
        print("Добро пожаловать в Крестики-нолики!")
        
        while True:
            self.odin_krug_igry()
            
            prodolzhit = input("Хотите сыграть еще раз? (y/n): ").lower()
            if prodolzhit != 'y':
                print("Спасибо за игру!")
                break

if __name__ == "__main__":
    moja_igra = krestikinoliki()
    moja_igra.start()