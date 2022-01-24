import ezdxf as ez  # Importar biblioteca ezdxf quando digitar ez
import math  # Importar biblioteca math
import numpy as np


# definição da função de Truncamento
def trunc(n, c):  # n = número a ser truncado; c = casas decimais desejadas
    a = 10 ** c
    b = int(n * a) / float(a)
    return b


dwg = ez.readfile('OUTFILE.dxf')  # Leitura do arquivo .dxf INFILE dentro da mesma pasta do .py
model = dwg.modelspace()  # indica que a busca sera feita no modelspace
# Busca e definição dos blocos pré definidos no AutoCAD
L14 = model.query('INSERT[name=="L14"]')
L14 = L14.query('*[color==4]')
L29 = model.query('INSERT[name=="L29"]')
L29 = L29.query('*[color==4]')
L44 = model.query('INSERT[name=="L44"]')
L44 = L44.query('*[color==4]')
BCL14 = model.query('INSERT[name=="BCL14"]')
BCL14 = BCL14.query('*[color==4]')
BCL29 = model.query('INSERT[name=="BCL29"]')
BCL29 = BCL29.query('*[color==4]')
BCL44 = model.query('INSERT[name=="BCL44"]')
BCL44 = BCL44.query('INSERT[color==4]')
# ----------------------------------------------- Blocos ---------------------------------------
y = model.query('INSERT[layer=="fiada2"]')
y = y[0].dxf.insert[1]
x = 200
y = (y - 450)
p1 = (x, y)
p2 = ((x + 120),(y))
p3 = ((x + 120),(y - 210))
p4 = ((x),(y - 210))
rec = (p1, p2, p3, p4)
model.add_lwpolyline(rec, format='xyb',
close=True, dxfattribs={'color': 3})
model.add_line([x,(y-15)], [(x+120),(y-15)], dxfattribs={'color': 3})
model.add_line([x,(y-30)], [(x+120),(y-30)], dxfattribs={'color': 3})
i = 30
for l in range(0,5):
    model.add_line([x,(y-30-i)], [(x+120),(y-30-i)], dxfattribs={'color': 3})
    i += 30
model.add_line([(x+60),(y-15)], [(x+60),(y-210)], dxfattribs={'color': 3})
model.add_text('TABELA DE BLOCOS', dxfattribs={'color': 3,
                                               'insert': ((x+15),(y-11)),
                                               'height': 7})
model.add_text('Blocos', dxfattribs={'color': 3,
                                               'insert': ((x+5),(y-25)),
                                               'height': 5})
model.add_text('Quantidade', dxfattribs={'color': 3,
                                               'insert': ((x+65),(y-25)),
                                               'height': 5})
bloco = ['L14', 'L29', 'L44', 'BCL14', 'BCL29', 'BCL44']
i = 60
n = 0
for b in range(0, 6):
    model.add_blockref(bloco[n], (x + 5, y-i+5 ), dxfattribs={'color': 3})
    if bloco[n] == 'L14':
        model.add_text(f'{len(L14)}', dxfattribs={'color': 3,
                                                  'insert': ((x+80),(y-i+10)),
                                                  'height': 5})
    if bloco[n] == 'L29':
        model.add_text(f'{len(L29)}', dxfattribs={'color': 3,
                                                  'insert': ((x + 80), (y - i + 10)),
                                                  'height': 5})
    if bloco[n] == 'L44':
        model.add_text(f'{len(L44)}', dxfattribs={'color': 3,
                                                  'insert': ((x + 80), (y - i + 10)),
                                                  'height': 5})
    if bloco[n] == 'BCL14':
        model.add_text(f'{len(BCL14)}', dxfattribs={'color': 3,
                                                  'insert': ((x + 80), (y - i + 10)),
                                                  'height': 5})
    if bloco[n] == 'BCL29':
        model.add_text(f'{len(BCL29)}', dxfattribs={'color': 3,
                                                  'insert': ((x + 80), (y - i + 10)),
                                                  'height': 5})
    if bloco[n] == 'BCL44':
        model.add_text(f'{len(BCL44)}', dxfattribs={'color': 3,
                                                  'insert': ((x + 80), (y - i + 10)),
                                                  'height': 5})
    n += 1
    i += 30
#--------------------------------------------- Armadura -----------------------------------
"""Realização de uma tabela com o total de aço a ser utilizado"""
phi5 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 5mm
phi63 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 6.3mm
phi8 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 8mm
phi10 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 10mm
phi125 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 12.5mm
phi16 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 16mm
phi20 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 20mm
phi25 = np.array([0])  # cria uma matriz de zeros para armazenar os ferros da bitola 25mm
ferro = model.query('INSERT[name=="ferro"]')  # Seleciona os blocos de ferro Verticais
for i in range(0,len(ferro)):  # Repete o processo para todos os ferros verticais encontrados
    x = ferro[i].dxf.insert[0]  # Busca a coordenada x do ferro
    y = ferro[i].dxf.insert[1]  # Busca a coordenada y do ferro
    point = (x,y)  # ponto onde o ferro esta em planta baixa
    """Seleciona os atributos do ferro"""
    barra = int(ferro[i].get_attrib_text('BARRA'))  # Número de baras
    bitola = float(ferro[i].get_attrib_text('BITOLA'))  # Bitola
    comprimento = float(ferro[i].get_attrib_text('COMPRIMENTO'))  # Comprimento
    quantitativo = (ferro[i].get_attrib_text('QUANTITATIVO'))  # Se deve ser incluido no quantitativo ou não
    if quantitativo == "s":  # Verificação se o ferro em questao deve ser incluido no quantitativo
        if bitola == 5:  # Verifica se a bitola do ferro selecionado é a de 5mm
            phi5 = np.append(phi5,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 6.3:  # Verifica se a bitola do ferro selecionado é a de 6.3mm
            phi63 = np.append(phi63,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 8:  # Verifica se a bitola do ferro selecionado é a de 8mm
            phi8 = np.append(phi8,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 10:  # Verifica se a bitola do ferro selecionado é a de 10mm
            phi10 = np.append(phi10,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 12.5:  # Verifica se a bitola do ferro selecionado é a de 12.5mm
            phi125 = np.append(phi125,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 16:  # Verifica se a bitola do ferro selecionado é a de 16mm
            phi16 = np.append(phi16,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 20:  # Verifica se a bitola do ferro selecionado é a de 20mm
            phi20 = np.append(phi20,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 25:  # Verifica se a bitola do ferro selecionado é a de 25mm
            phi25 = np.append(phi25,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
"""Procedimento Para as barras horizontais"""
ferro = model.query('INSERT[name=="ferroHorizontal"]')  # Seleciona as barras horizontais
for i in range(0,len(ferro)):  # Repete o procedimento para todas barras horizontais encontradas
    x = ferro[i].dxf.insert[0]  # Busca a coordenada x do ferro
    y = ferro[i].dxf.insert[1]  # Busca a coordenada y do ferro
    point = (x,y)  # ponto onde o ferro esta em planta baixa
    barra = int(ferro[i].get_attrib_text('BARRAS'))  # Número de baras
    bitola = float(ferro[i].get_attrib_text('BITOLA'))  # Bitola
    comprimento = float(ferro[i].get_attrib_text('COMPRIMENTO'))  # Comprimento
    quantitativo = (ferro[i].get_attrib_text('QUANTITATIVO'))  # Se deve ser incluido no quantitativo ou não
    if quantitativo == "s":  # Verificação se o ferro em questao deve ser incluido no quantitativo
        if bitola == 5:  # Verifica se a bitola do ferro selecionado é a de 5mm
            phi5 = np.append(phi5,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 6.3:  # Verifica se a bitola do ferro selecionado é a de 6.3mm
            phi63 = np.append(phi63,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 8:  # Verifica se a bitola do ferro selecionado é a de 8mm
            phi8 = np.append(phi8,[barra * comprimento])   # Adiciona o comprimento total da barra na matriz
        if bitola == 10:  # Verifica se a bitola do ferro selecionado é a de 10mm
            phi10 = np.append(phi10,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 12.5:  # Verifica se a bitola do ferro selecionado é a de 12.5mm
            phi125 = np.append(phi125,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 16:  # Verifica se a bitola do ferro selecionado é a de 16mm
            phi16 = np.append(phi16,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 20:  # Verifica se a bitola do ferro selecionado é a de 20mm
            phi20 = np.append(phi20,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
        if bitola == 25:  # Verifica se a bitola do ferro selecionado é a de 25mm
            phi25 = np.append(phi25,[barra * comprimento])  # Adiciona o comprimento total da barra na matriz
"""Soma todos os valores que compõe as matrizes"""
phi5 = round(np.sum(phi5),2)  # Qauntidade total de aço da bitola 5mm
phi63 = round(np.sum(phi63),2)  # Qauntidade total de aço da bitola 6.3mm
phi8 = round(np.sum(phi8),2)  # Qauntidade total de aço da bitola 8mm
phi10 = round(np.sum(phi10),2)  # Qauntidade total de aço da bitola 10mm
phi125 = round(np.sum(phi125),2)  # Qauntidade total de aço da bitola 12.5mm
phi16 = round(np.sum(phi16),2)  # Qauntidade total de aço da bitola 16mm
phi20 = round(np.sum(phi20),2)  # Qauntidade total de aço da bitola 20mm
phi25 = round(np.sum(phi25),2)  # Qauntidade total de aço da bitola 25mm
"""Desenho da Tabela de Aço"""
y = model.query('INSERT[layer=="fiada2"]')  # Localização da fiada par para que a tabela seja desenhada abaixo dela
y = y[0].dxf.insert[1]
x = 200
y = (y - 300)
p1 = (x, y)
p2 = ((x + 100),(y))
p3 = ((x + 100),(y - 110))
p4 = ((x),(y - 110))
rec = (p1, p2, p3, p4)
model.add_lwpolyline(rec, format='xyb',  # Retangulo externo da tabela
close=True, dxfattribs={'color': 3})
model.add_line([x,(y-20)], [(x+100),(y-20)], dxfattribs={'color': 3})
a = 10
for i in range(0, 8):
    model.add_line([x,(y-20-a)], [(x+100),(y-20-a)], dxfattribs={'color': 3})  # Linhas internas da tabela
    a += 10
model.add_line([(x+20),(y-20)], [(x+20),(y-110)], dxfattribs={'color': 3})  # Linhas Verticias
model.add_line([(x+70),(y-20)], [(x+70),(y-110)], dxfattribs={'color': 3})  # Linhas Verticias
model.add_text('TABELA DE FERROS', dxfattribs={'color': 3,  # Título da tabela
                                               'insert': ((x+2),(y-15)),
                                               'height': 7})

"""Coluna das Bitolas"""
c = 27  # Espacamento vertical
for i in range(0,9):
    if i == 0:
        a = 'Bitola'
    if i == 1:
        a = 'Φ 5'
    if i == 2:
        a = 'Φ 6.3'
    if i == 3:
        a = 'Φ 8'
    if i == 4:
        a = 'Φ 10'
    if i == 5:
        a = 'Φ 12.5'
    if i == 6:
        a = 'Φ 16'
    if i == 7:
        a = 'Φ 20'
    if i == 8:
        a = 'Φ 25'
    model.add_text(a, dxfattribs={'color': 3,  # Insere o texto conforme as condições acima
                                               'insert': ((x+2),(y-c)),
                                               'height': 4})
    c += 10

"""Coluna dos Comprimentos"""
c = 27  # Espaçamento Vertical
for i in range(0,9):
    if i == 0:
        a = 'Comprimento (m)'
        b = 22  # Coordenada de inscerção em x
    if i == 1:
        a = f' {phi5}'
        b = 38  # Coordenada de inscerção em x
    if i == 2:
        a = f' {phi63}'
        b = 38  # Coordenada de inscerção em x
    if i == 3:
        a = f' {phi8}'
        b = 38  # Coordenada de inscerção em x
    if i == 4:
        a = f' {phi10}'
        b = 38  # Coordenada de inscerção em x
    if i == 5:
        a = f' {phi125}'
        b = 38  # Coordenada de inscerção em x
    if i == 6:
        a = f' {phi16}'
        b = 38  # Coordenada de inscerção em x
    if i == 7:
        a = f' {phi20}'
        b = 38  # Coordenada de inscerção em x
    if i == 8:
        a = f' {phi25}'
        b = 38  # Coordenada de inscerção em x
    model.add_text(a, dxfattribs={'color': 3,
                                               'insert': ((x+b),(y-c)),
                                               'height': 4})
    c += 10
"""Coluna dos Pesos"""
c = 27  # Espaçamento Vertical
for i in range(0,9):
    if i == 0:
        a = 'Peso (kg)'
    if i == 1:
        a = f'{round(phi5*0.154,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    if i == 2:
        a = f'{round(phi63*0.245,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    if i == 3:
        a = f'{round(phi8*0.395,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    if i == 4:
        a = f'{round(phi10*0.617,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    if i == 5:
        a = f'{round(phi125*0.963,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    if i == 6:
        a = f'{round(phi16*1.578,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    if i == 7:
        a = f'{round(phi20*2.466,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    if i == 8:
        a = f'{round(phi25*3.853,2)}'  # Cálculo do peso total das barras atraves do peso por metro
    model.add_text(a, dxfattribs={'color': 3,
                                               'insert': ((x+72),(y-c)),
                                               'height': 4})
    c += 10
#---------------------------------------------Graute----------------------------------
graute = model.query('INSERT[name=="graute"]')  # definição dos blocos pre definidos de graute
graute = graute.query('INSERT[layer=="graute"]')  # seleciona os blocos de graute que estao no layer "graute"
pedireito = float(input('Altura da Parede em cm: '))  # Pergunta ao usuário a altura da Parede
y = model.query('INSERT[layer=="fiada2"]')
y = y[0].dxf.insert[1]
x = 200
y = (y - 700)
p1 = (x, y)
p2 = ((x + 120),(y))
p3 = ((x + 120),(y - 60))
p4 = ((x),(y - 60))
rec = (p1, p2, p3, p4)
model.add_lwpolyline(rec, format='xyb',
close=True, dxfattribs={'color': 3})
model.add_line([x,(y-15)], [(x+120),(y-15)], dxfattribs={'color': 3})
model.add_line([x,(y-30)], [(x+120),(y-30)], dxfattribs={'color': 3})
model.add_line([x+60,(y-15)], [(x+60),(y-60)], dxfattribs={'color': 3})
model.add_text('TABELA DE GRAUTE', dxfattribs={'color': 3,
                                               'insert': ((x+5),(y-11)),
                                               'height': 7})
model.add_text('Descrição', dxfattribs={'color': 3,
                                               'insert': ((x+10),(y-25)),
                                               'height': 5})
model.add_text('Volume(m³)', dxfattribs={'color': 3,
                                               'insert': ((x+70),(y-25)),
                                               'height': 5})
model.add_text('Vertical', dxfattribs={'color': 3,
                                               'insert': ((x+20),(y-37)),
                                               'height': 4})
model.add_text('Horizontal', dxfattribs={'color': 3,
                                               'insert': ((x+20),(y-47)),
                                               'height': 4})
model.add_text('Total', dxfattribs={'color': 3,
                                               'insert': ((x+20),(y-57)),
                                               'height': 4})
g = np.array([0])
for a in range(0,len(graute)):
    gr = graute[a].get_attrib_text('QUANTITATIVO')
    if gr == 's':
        g = np.append(g,1)
g = np.sum(g)
g = round((96.75*pedireito*g)/(1000000), 2)
b = round(((len(BCL14)*164*14)+(len(BCL29)*164*29)+(len(BCL44)*164*44))/(1000000), 2)
t = round(g + b, 2)
model.add_text(f'{g}', dxfattribs={'color': 3,
                                               'insert': ((x+80),(y-37)),
                                               'height': 4})
model.add_text(f'{b}', dxfattribs={'color': 3,
                                               'insert': ((x+80),(y-47)),
                                               'height': 4})
model.add_text(f'{t}', dxfattribs={'color': 3,
                                               'insert': ((x+80),(y-57)),
                                               'height': 4})



dwg.saveas('Quantitativo.dxf')