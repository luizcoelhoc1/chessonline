BRANCA = True
PRETA = False
switcher = {
    BRANCA: "B",
    PRETA: "P"
}


import PySimpleGUI as sg

class Casa():
    def __init__(self, row, column):
        self.peca = None
        self.color = ("white", "#FFFFFF") if (row + column) % 2 == 0 else ("black", "#333333")

        self.btn = sg.ReadFormButton('', 
                                     button_color=self.color, 
                                     image_filename="pieces/none.png",
                                     image_size=(50, 50), 
                                     image_subsample=2, 
                                     border_width=0,
                                     size=(3,3)
                                     )
    def setPeca(self, peca, color):
        self.peca = peca(color)
        self.btn = sg.ReadFormButton('', 
                                     button_color=self.color, 
                                     image_filename=self.peca.imagefile(),
                                     image_size=(50, 50), 
                                     image_subsample=2, 
                                     border_width=0,
                                     size=(3,3)
                                     )
        
    def __str__(self):
        if self.peca is None:
            return "x  "
        else:
            return self.peca.__str__() + " "
        
class Peca():
    def __init__(self, color):
        self.color = color
        self.moveu = False
    def imagefile(self):
        return ("white" if self.color is BRANCA else "black") + ".png" 
        
class Torre(Peca):
    def __init__(self, color):
        super().__init__(color)
    
    def imagefile(self):
        return "pieces/rook_" + super().imagefile()
    
    def canMove(self, i1, j1, i2, j2, atk):
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
        return "T" + switcher.get(self.color)

class Cavalo(Peca):
    def __init__(self, color):
        super().__init__(color)
    
    def canMove(self, i1, j1, i2, j2, atk):
        if abs(i1-i2) is 2:
            if abs(j1-j2) is 1:
                return True, [], []
        if abs(j1-j2) is 2:
            if abs(i1-i2) is 1:
                return True, [], []
        return False, [], []

    def imagefile(self):
        return "pieces/knight_" + super().imagefile()

    def __str__(self):
        return "N" + switcher.get(self.color)
    
class Bispo(Peca):
    def __init__(self, color):
        super().__init__(color)
    
    def canMove(self, i1, j1, i2, j2, atk):
        if abs(i1-i2) == abs(j1-j2):
            casasOcupadas= []
            if i1 < i2:
                i1, i2 = i2, i1
                j1, j2 = j2, j1
            for i in range(1, abs(i1-i2)):
                casasocupadas.append((i1+i,j1+i))
        return False, [], []
    
    def imagefile(self):
        return "pieces/bishop_" + super().imagefile()
    
    def __str__(self):
        return "B" + switcher.get(self.color)

class Rei(Peca):
    def __init__(self, color):
        super().__init__(color)
    
    def canMove(self, i1, j1, i2, j2, atk):
        if abs(i1-i2) <= 1 and abs(j1-j2) <= 1:
            return True, [], []
        return False, [], []
    
    def imagefile(self):
        return "pieces/king_" + super().imagefile()
    
    def __str__(self):
        return "K" + switcher.get(self.color)
    
class Rainha(Peca):
    def __init__(self, color):
        super().__init__(color)
        self.torre = Torre(color)
        self.bispo = Bispo(color)
    
    def canMove(self, i1, j1, i2, j2, atk):
        podeT, ocupT, atkT = self.torre.canMove(i1, j1, i2, j2, atk)
        podeB, ocupB, atkB = self.bispo.canMove(i1, j1, i2, j2, atk)
        return podeT and podeB, ocupT + ocupB, atkT + atkB

    def imagefile(self):
        return "pieces/rook_" + super().imagefile()

    def __str__(self):
        return "Q" + switcher.get(self.color)
    
class Peao(Peca):
    def __init__(self, color):
        super().__init__(color)
        
    def canMove(self, i1, j1, i2, j2, atk):

        cor = -1 if self.color is PRETA else 1
        if atk:
            if abs(j1-j2) is 1:
                if i1 + cor == i2:
                    return True, [], []                    
        else:
            if j1 == j2:
                for move in [1, 2] if not self.moveu else [1]:
                    if i1 + (move*cor) == i2:
                        return True, [], []

        return False, [], []


    def imagefile(self):
        return "pieces/pawn_" + super().imagefile()

    def __str__(self):
        return "P" + switcher.get(self.color)
    
    
    
class Tabuleiro():
    def __init__(self):
        #set tabuleiro
        self.tabuleiro = []
        for i in range(0, 8):
            self.tabuleiro.append([])
            for j in range(0, 8):
                self.tabuleiro[i].append(Casa(i, j))
        self.setInitState()
        
        #set configs do jogo
        self.turno = BRANCA
        self.historico = []
        
    def setInitState(self):
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
        
        
        if self.tabuleiro[i2][j2].peca is not None:
            if self.tabuleiro[i1][j1].peca.color is self.tabuleiro[i2][j2].peca.color:
                return False
            atk = True
        else: 
            atk = False
        
        
        pode, casasOcupadas, casasAtacadas = self.tabuleiro[i1][j1].peca.canMove(i1, j1, i2, j2, atk)
    
        if not pode:
            return False
        
        for casa in casasOcupadas:
            if self.tabuleiro[casa[0]][casa[1]].peca is not None:
                return False
        return True
        
    
    def move(self, i1, j1, i2, j2):
        if self.canMove(i1, j1, i2, j2):
            #mover peça
            self.tabuleiro[i2][j2].peca = self.tabuleiro[i1][j1].peca 
            self.tabuleiro[i1][j1].peca = None
            self.tabuleiro[i2][j2].peca.moveu = True
            #mudar turno
            self.turno = not self.turno
            
            self.historico.append((i1,j1,i2,j2))
        

    def __str__(self):
        string = "   1  2  3  4  5  6  7  8\n"
        for i in range(0,8):
            string += str(i+1) + "  "
            for j in range(0,8):
                string +=  self.tabuleiro[i][j].__str__()
            string +=  "\n"
        return string


t = Tabuleiro()




