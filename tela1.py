BRANCA = True
PRETA = False


class Casa():
    def __init__(self):
        self.peca = None
        
    def setPeca(self, peca, color):
        self.peca = peca(color)
        
    def __str__(self):
        if self.peca is None:
            return "x  "
        else:
            return self.peca.__str__() + " "
        


class Torre():
    def __init__(self, color):
        self.color = color
    
    def canMove(self, i1, j1, i2, j2):
        resultado = []
        pode = False
        if i1 == i2:
            pode = True
            if j2 < j1:
                j1, j2 = j2, j1
            for i in range(j1+1, j2):
                resultado.append((i1, i))
        if j1 == j2:
            pode = True
            if i2 < i1:
                i1, i2 = i2, i1
            for i in range(i1+1, i2):
                resultado.append((j1, i))
                
        return pode, resultado, []
                
    
    
    def __str__(self):
        return "T" + str(self.color)

class Cavalo():
    def __init__(self, color):
        self.color = color
    
    def canMove(self, i1, j1, i2, j2):
        if i1 + 2 == i2 or i1 - 2 == i2:
            if j1 + 1 == j2 or j1 - 1 == j2:
                return True, [], []
        if j1 + 2 == j2 or j1 - 2 == j2:
            if i1 + 1 == i2 or i1 - 1 == i2:
                return True, [], []
        return False, [], []
        
    def __str__(self):
        return "N" + str(self.color)
    
class Bispo():
    def __init__(self, color):
        self.color = color
    
    def __str__(self):
        return "B" + str(self.color)

class Rei():
    def __init__(self, color):
        self.color = color
        self.moveu = False
    
    def canMove(self, i1, j1, i2, j2):
        if abs(i1-i2) <= 1 and abs(j1-2) <= 1:
            return True, [], []
        return False, [], []
    
    def __str__(self):
        return "K" + str(self.color)
    
class Rainha():
    def __init__(self, color):
        self.color = color
    
    def __str__(self):
        return "Q" + str(self.color)
    
class Peao():
    def __init__(self, color):
        self.color = color
    
    def __str__(self):
        return "P" + str(self.color)
    
    
    
class Tabuleiro():
    def __init__(self):

        self.tabuleiro = []
        
        for i in range(0, 8):
            self.tabuleiro.append([])
            for j in range(0, 8):
                self.tabuleiro[i].append(Casa())

        
        self.tabuleiro[0][0].setPeca(Torre, BRANCA)
        self.tabuleiro[0][1].setPeca(Cavalo, BRANCA)
        self.tabuleiro[0][2].setPeca(Bispo, BRANCA)
        self.tabuleiro[0][3].setPeca(Rei, BRANCA)
        self.tabuleiro[0][4].setPeca(Rainha, BRANCA)
        self.tabuleiro[0][5].setPeca(Bispo, BRANCA)
        self.tabuleiro[0][6].setPeca(Cavalo, BRANCA)
        self.tabuleiro[0][7].setPeca(Torre, BRANCA)
        self.tabuleiro[1][0].setPeca(Peao, BRANCA)
        self.tabuleiro[1][1].setPeca(Peao, BRANCA)
        self.tabuleiro[1][2].setPeca(Peao, BRANCA)
        self.tabuleiro[1][3].setPeca(Peao, BRANCA)
        self.tabuleiro[1][4].setPeca(Peao, BRANCA)
        self.tabuleiro[1][5].setPeca(Peao, BRANCA)
        self.tabuleiro[1][6].setPeca(Peao, BRANCA)
        self.tabuleiro[1][7].setPeca(Peao, BRANCA)
        
        self.tabuleiro[6][0].setPeca(Peao, PRETA)
        self.tabuleiro[6][1].setPeca(Peao, PRETA)
        self.tabuleiro[6][2].setPeca(Peao, PRETA)
        self.tabuleiro[6][3].setPeca(Peao, PRETA)
        self.tabuleiro[6][4].setPeca(Peao, PRETA)
        self.tabuleiro[6][5].setPeca(Peao, PRETA)
        self.tabuleiro[6][6].setPeca(Peao, PRETA)
        self.tabuleiro[6][7].setPeca(Peao, PRETA)
        self.tabuleiro[7][0].setPeca(Torre, PRETA)
        self.tabuleiro[7][1].setPeca(Cavalo, PRETA)
        self.tabuleiro[7][2].setPeca(Bispo, PRETA)
        self.tabuleiro[7][3].setPeca(Rei, PRETA)
        self.tabuleiro[7][4].setPeca(Rainha, PRETA)
        self.tabuleiro[7][5].setPeca(Bispo, PRETA)
        self.tabuleiro[7][6].setPeca(Cavalo, PRETA)
        self.tabuleiro[7][7].setPeca(Torre, PRETA)
        
        self.turno = BRANCA

    def canMove(self, i1, j1, i2, j2):
        if i1 >= 8 or i2 >= 8 or j1 >= 8 or j2 >= 8:
            return False
        
        if i1 < 0 or i2 < 0 or j1 < 0 or j2 < 0:
            return False
        
        if self.tabuleiro[i1][j1].peca is None:
            return False
        
        if self.tabuleiro[i1][j1].peca.color is not self.turno:
            return False
        
        if i1 == i2 and j1 == j2:
            return False
        
        if self.tabuleiro[i1][j1].peca.color == self.tabuleiro[i2][j2].peca.color:
            return False
        
        pode, casasOcupadas, casasAtacadas = self.tabuleiro[i1][j1].peca.canMove(i1, j1, i2, j2)
        
        for casa in casasOcupadas:
            if self.tabuleiro[casa[0]][casa[1]].peca is not None:
                return False
        
        return True
        
    
    def move(self, i1, j1, i2, j2):
        if self.canMove(i1, j1, i2, j2):
            self.tabuleiro[i2][j2].peca = self.tabuleiro[i1][j1].peca 
            self.tabuleiro[i1][j1].peca = None
            self.turno = not self.turno
        

    def __str__(self):
        string = ""
        for i in range(0,8):
            for j in range(0,8):
                string += self.tabuleiro[i][j].__str__()
            string +=  "\n"
        return string


t = Tabuleiro()

print(t)

