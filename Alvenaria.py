import ezdxf as ez  # Importar biblioteca ezdxf quando digitar ez
import math  # Importar biblioteca math
import numpy as np # Importar biblioteca numpy
import PySimpleGUI as sg


# Criação da janela
sg.theme('DarkBrown5')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Software de Alvenaria Estrutural')],
            [sg.Text('Altura da Parede em cm: '), sg.Input()],
            [sg.Button('Ok', bind_return_key='65421'), sg.Button('Cancel', bind_return_key='65417')], 
            [sg.ProgressBar(100)]]

# Create the Window
window = sg.Window('Alvenaria', layout, icon='./images/tijolo.ico', location=(50,50))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Cancel': # if user closes window or clicks cancel
        pedireito = ''
        break     

    elif event == 'Ok':
        if values[0] == '' or values[0] == ' ' or values[0] == '0':
            layout2 = [[sg.Text('Por favor insira um valor!')],
                        [sg.Button('Voltar', bind_return_key='65307')]]
            window2 = sg.Window('Aviso', layout2, icon='./images/tijolo.ico', element_justification='center', size=(400, 100), location=(50, 50), keep_on_top=True,)

            while True:
                event, values = window2.read()
                if event == sg.WIN_CLOSED or event == 'Voltar':
                    window2.close()
                    break   



        else:
            pedireito = float(values[0]) # define a variavel da altura da Parede
            print('You entered ', values[0])
            window.close()


# definição da função de Truncamento
def trunc(n, c):  # n = número a ser truncado; c = casas decimais desejadas
    a = 10 ** c
    b = int(n * a) / float(a)
    return b

if pedireito == '':
    print('Por favor insira uma valor para funcionar adequadamente!')

else:
    fiadas = math.ceil(float(pedireito / 20.0))  # Cálculo do número de fiadas
    fiada1 = math.ceil(float(fiadas / 2))  # Cálculo do número de fiadas ímpares
    fiada2 = math.floor(float(fiadas / 2))  # Cálculo do número de fiadas pares
    print(fiada1, fiada2)  # Imprime números de fiadas

    dwg = ez.readfile('INFILE.dxf')  # Leitura do arquivo .dxf INFILE dentro da mesma pasta do .py
    model = dwg.modelspace()  # indica que a busca sera feita no modelspace
    # Busca e definição dos blocos pré definidos no AutoCAD
    B14 = model.query('INSERT[name=="B14"]')  # Busca e definição do bloco B14
    B29 = model.query('INSERT[name=="B29"]')  # Busca e definição do bloco B29
    B44 = model.query('INSERT[name=="B44"]')  # Busca e definição do bloco B44
    # Definião de Variáveis
    n = 0  # Variavel de contador de blocos
    i = 0  # Variavel de contador de blocos
    f = 200  # Variavel localização das fiadas (altura do inicio da representação das vistas acima da fiada1 - largura do bloco)
    m = model.query('INSERT[layer=="fiada1"]')  # Localizar todos os blocos no layer fiada1
    m = m.query('INSERT[name=="B29"]')  # Localizar e definir Blocos B29 no layer fiada1

    """Definição dos eixos dos blocos (cima, meio e baixo)
    esta definicão sera utilizada posteriormente para a verificação se o bloco pertence a fiada"""
    for a in range(0, (len(m))):  # repetir para todos os blocos B29 no layer fiada1
        if round(m[n].dxf.rotation) == 0:  # Selecionar blocos que estejam com a rotação = 0
            eixocima = round(float(m[n].dxf.insert[1] + 14), 3)  # Definição do eixocima atraves da cordenada y do bloco (como o ponto do bloco esta no canto inferior esquerdo, soma-se a largura do bloco para encontrar o eixo de cima)
            eixobaixo = round(float(m[n].dxf.insert[1]), 3)  # Definição do eixobaixo atraves da cordenada y do bloco
            eixomeio = round(float(m[n].dxf.insert[1] + 7), 3)  # Definição do eixocima atraves da cordenada y do bloco (como o ponto do bloco esta no canto inferior esquerdo, soma-se metade da largura do bloco para encontrar o eixo de cima)
            pontozero = eixobaixo + f  # Definição de onde começará a representação das vistas
            n += 1
        else:
            n += 1
    #------------------------------------------------------ FIADA IMPAR -----------------------------------------------
    """"Para a representação das vistas primeiro serão adicionados os blocos presentes nas fiadas impares"""
    for a in range(0, fiada1):  # Repetição para todas fiadas impares
        """É feita novamante a definição dos blocos B14, B29 e B44"""
        B14 = B14.query('*[layer=="fiada1"]')
        B29 = B29.query('*[layer=="fiada1"]')
        B44 = B44.query('INSERT[layer=="fiada1"]')
        if len(B14) == len(B29) == len(B44) == 0:  # Para evitar erro na excecução do software, se nao for encontrado nenhum bloco no layer fiada1 imprime:
            print('Fiada Ímpar nao encontrada.')
        else:
            while True:  # Repetição para número de blocos B14 da fiada1
                if len(B14) == 0:
                    i = 0
                else:
                    """Repreentação do bloco em vista conforme sua rotação
                    Blocos com a rotação igual a 0 e 180 serão representados em vista lateral
                    Blocos com a rotação igual a 90 e 270 serão representados em vista transversal"""
                    entity = B14[i] # Seleção de todos Blocos B14 no layer fiada1
                    if round(entity.dxf.rotation) == 0:  # Seleção dos blocos com rotação 0
                        x = (entity.dxf.insert[0])  # Definição do ponto de inserção em x
                        y = entity.dxf.insert[1] + f  # Definição do ponto de incerção em y
                        point = [x, y]  # Ponto de inserção do bloco
                        model.add_blockref('L14', point, dxfattribs={  # Inserir o Bloco L14 no ponto pré definido com os seguintes atributos:
                            'layer': "parede",  # Layer com nome parede
                            'color': 4,  # Cor do bloco ciano
                            'rotation': 0})  # Rotação do bloco igual a zero
                        i += 1  # Contador de número de blocos
                    elif round(entity.dxf.rotation) == 180:  # Seleção dos blocos com rotação 180
                        x = (entity.dxf.insert[0] - 14)  # Coordenada x do bloco
                        y = entity.dxf.insert[1] + f - 14
                        point = [x, y]
                        model.add_blockref('L14', point, dxfattribs={  # Inserir o Bloco L14 no ponto pré definido
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                        """Para os blocos transversais, é preciso verificar se eles pertencem ou nao as fiadas.
                        Isso é feito atraves da comparação dos eixos do bloco com os eixos da fiada, 
                        se algum deles for concidente é porque o bloco pertence a fiada."""
                    elif round(entity.dxf.rotation) == 270:  # Seleção dos blocos com rotação 270
                        eixo1 = round(entity.dxf.insert[1], 3)  # Eixo da parte de cima do Bloco
                        eixo2 = round((entity.dxf.insert[1] - 7), 3)  # Eixo do meio do Bloco
                        eixo3 = round((entity.dxf.insert[1] - 14), 3)  # Eixo da parte de Baixo do Bloco
                        if eixo1 == eixocima or eixo2 == eixomeio or eixo3 == eixobaixo:  # Comparação entre os eixos do bloco com os eixos da fiada
                            x = (entity.dxf.insert[0])  # Posição de incerção no eixo x
                            y = (eixo1 + f - 14)  # Posição de incerção no eixo y
                            point = [x, y]
                            model.add_blockref('T14', point, dxfattribs={  # Inserção do Bloco transversal com os atributos
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        else:
                            i += 1
                    elif round(entity.dxf.rotation) == 90:  # Seleção dos blocos com rotação 90
                        eixo1 = round((entity.dxf.insert[1] + 14), 3)  # Eixo da parte de cima do Bloco
                        eixo2 = round((entity.dxf.insert[1] + 7), 3)  # Eixo do meio do Bloco
                        eixo3 = round((entity.dxf.insert[1]), 3)  # Eixo da parte de Baixo do Bloco
                        if eixo1 == eixocima or eixo2 == eixomeio or eixo3 == eixobaixo: # Comparação entre os eixos do bloco com os eixos da fiada
                            x = (entity.dxf.insert[0] - 14)  # Posição de incerção no eixo x
                            y = eixo1 + f - 14  # Posição de incerção no eixo y
                            point = [x, y]
                            model.add_blockref('T14', point, dxfattribs={  # Inserção do Bloco transversal com os atributos
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        else:
                            i += 1
                    else:
                        i += 1
                if i == len(B14):
                    i = 0
                    break
            """Mesmo procedimento feito para o Bloco B29"""
            while True:
                if len(B29) == 0:
                    print('Não há B29 na fiada ímpar')
                    i = 0
                else:
                    entity = B29[i]
                    if round(entity.dxf.rotation) == 0:
                        x = (entity.dxf.insert[0])
                        y = entity.dxf.insert[1] + f
                        point = [x, y]
                        model.add_blockref('L29', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1

                    elif round(entity.dxf.rotation) == 180:
                        x = (entity.dxf.insert[0] - 29)
                        y = (entity.dxf.insert[1] + f - 14)
                        point = [x, y]
                        model.add_blockref('L29', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1

                    elif round(entity.dxf.rotation) == 270:
                        eixo1 = round(entity.dxf.insert[1], 3)
                        eixo2 = round((entity.dxf.insert[1] - 14.5), 3)
                        eixo3 = round((entity.dxf.insert[1] - 29), 3)
                        if eixo1 == eixocima:
                            x = (entity.dxf.insert[0])
                            y = eixo1 + f - 14
                            point = [x, y]
                            model.add_blockref('T29', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        elif eixo3 == eixobaixo:
                            x = (entity.dxf.insert[0])
                            y = eixo3 + f
                            point = [x, y]
                            model.add_blockref('T29', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        else:
                            print('Esse bloco não pertence a essa fiada.')
                            i += 1
                    elif round(entity.dxf.rotation) == 90:
                        eixo1 = round((entity.dxf.insert[1] + 29), 3)
                        eixo2 = round((entity.dxf.insert[1] + 14.5), 3)
                        eixo3 = round((entity.dxf.insert[1]), 3)
                        if eixo1 == eixocima:
                            x = entity.dxf.insert[0] - 14
                            y = eixo1 + f - 14
                            point = [x, y]
                            model.add_blockref('T29', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        elif eixo3 == eixobaixo:
                            x = (entity.dxf.insert[0] - 14)
                            y = eixo3 + f
                            point = [x, y]
                            model.add_blockref('T29', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        else:
                            print('Esse bloco não pertence a essa fiada.')
                            i += 1
                    else:
                        print('O bloco esta desalinhado!'), print(entity.dxf.rotation)
                        i += 1
                if i == len(B29):
                    i = 0
                    break
            """Mesmo procedimento para o Bloco B44"""
            while True:
                if len(B44) == 0:
                    print('Não há B44 na fiada ímpar')
                    i = 0
                else:
                    entity = B44[i]
                    if round(entity.dxf.rotation) == 0:
                        x = (entity.dxf.insert[0])
                        y = entity.dxf.insert[1] + f
                        point = [x, y]
                        model.add_blockref('L44', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    elif round(entity.dxf.rotation) == 180:
                        x = (entity.dxf.insert[0] - 44)
                        y = entity.dxf.insert[1] + f - 14
                        point = [x, y]
                        model.add_blockref('L44', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    elif round(entity.dxf.rotation) == 270:
                        eixo1 = round(entity.dxf.insert[1], 3)
                        eixo2 = round((entity.dxf.insert[1] - 22), 3)
                        eixo3 = round((entity.dxf.insert[1] - 44), 3)
                        if eixo1 == eixocima:
                            x = (entity.dxf.insert[0])
                            y = eixo1 + f - 14
                            point = [x, y]
                            model.add_blockref('T44', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        elif eixo2 == eixomeio:
                            x = (entity.dxf.insert[0])
                            y = eixo2 + f - 7
                            point = [x, y]
                            model.add_blockref('T44', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        elif eixo3 == eixobaixo:
                            x = (entity.dxf.insert[0])
                            y = eixo3 + f
                            point = [x, y]
                            model.add_blockref('T44', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        else:
                            print('Esse bloco não pertence a essa fiada.')
                            i += 1
                    elif round(entity.dxf.rotation) == 90:
                        eixo1 = round((entity.dxf.insert[1] + 44), 3)
                        eixo2 = round((entity.dxf.insert[1] + 22), 3)
                        eixo3 = round((entity.dxf.insert[1]), 3)
                        if eixo1 == eixocima:
                            x = entity.dxf.insert[0] - 14
                            y = eixo1 + f - 14
                            point = [x, y]
                            model.add_blockref('T44', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        elif eixo2 == eixomeio:
                            x = entity.dxf.insert[0] - 14
                            y = eixo2 + f - 7
                            point = [x, y]
                            model.add_blockref('T44', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        elif eixo3 == eixobaixo:
                            x = entity.dxf.insert[0] - 14
                            y = eixo3 + f
                            point = [x, y]
                            model.add_blockref('T44', point, dxfattribs={
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                            i += 1
                        else:
                            print('Esse bloco não pertence a essa fiada.')
                            i += 1
                    else:
                        print('O bloco esta desalinhado!')
                        i += 1
                if i == len(B44):
                    i = 0
                    break
            f += 40  # Contador de fiada para passar para proxima fiada impar
    #------------------------------------------------------FIADA PAR -------------------------------------------
    """Para as fiadas pares são seguidos os mesmos passos das fiadas impares, difenrenciando pela posição da colocação do ponto y """
    B14 = model.query('INSERT[name=="B14"]')
    B29 = model.query('INSERT[name=="B29"]')
    B44 = model.query('INSERT[name=="B44"]')
    m = model.query('INSERT[layer=="fiada2"]')
    n = 0
    # Determinação dos eixos da segunda fiada
    for a in range(0, (len(m) - 1)):
        if round(m[n].dxf.rotation) == 0:
            eixocima = round(float(m[n].dxf.insert[1] + 14), 3)
            eixomeio = round(float(m[n].dxf.insert[1] + 7), 3)
            eixobaixo = round(float(m[n].dxf.insert[1]), 3)
            n += 1
        else:
            n += 1
    f2 = (pontozero + 20)  # Ponto inicial de inserção das fiadas impares
    """Procediamento para incerção das fiadas impares"""
    for a in range(0, fiada2):  # repetir procedimento para número de fiadas impares
        """Localização e definição dos blocos estruturais"""
        B14 = B14.query('INSERT[layer=="fiada2"]')
        B29 = B29.query('*[layer=="fiada2"]')
        B44 = B44.query('*[layer=="fiada2"]')
        # Procedimento para Bloco B14
        while True:
            if len(B14) == 0:
                i = 0
            else:
                entity = B14[i]
                if round(entity.dxf.rotation) == 0:
                    x = (entity.dxf.insert[0])
                    y = f2
                    point = [x, y]
                    model.add_blockref('L14', point, dxfattribs={
                        'layer': "parede",
                        'color': 4,
                        'rotation': 0})
                    i += 1

                elif round(entity.dxf.rotation) == 180:
                    x = (entity.dxf.insert[0] - 14)
                    y = f2
                    point = [x, y]
                    model.add_blockref('L14', point, dxfattribs={
                        'layer': "parede",
                        'color': 4,
                        'rotation': 0})
                    i += 1

                elif round(entity.dxf.rotation) == 270:
                    eixo = round(entity.dxf.insert[1], 3)
                    if eixo == eixocima:
                        x = (entity.dxf.insert[0])
                        y = f2
                        point = [x, y]
                        model.add_blockref('T14', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    else:
                        i += 1

                elif round(entity.dxf.rotation) == 90:
                    eixo = round((entity.dxf.insert[1] + 14), 3)
                    if eixo == eixocima:
                        x = (entity.dxf.insert[0] - 14)
                        y = f2
                        point = [x, y]
                        model.add_blockref('T14', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    else:
                        i += 1
                else:
                    print('O bloco esta desalinhado!')
                    i += 1
            if i == len(B14):
                i = 0
                break
        # Procedimento para Bloco B29
        while True:
            if len(B29) == 0:
                print('Não há B29 na fiada par')
                i = 0
            else:
                entity = B29[i]
                if round(entity.dxf.rotation) == 0:
                    x = (entity.dxf.insert[0])
                    y = f2
                    point = [x, y]
                    model.add_blockref('L29', point, dxfattribs={
                        'layer': "parede",
                        'color': 4,
                        'rotation': 0})
                    i += 1

                elif round(entity.dxf.rotation) == 180:
                    x = (entity.dxf.insert[0] - 29)
                    y = f2
                    point = [x, y]
                    model.add_blockref('L29', point, dxfattribs={
                        'layer': "parede",
                        'color': 4,
                        'rotation': 0})
                    i += 1

                elif round(entity.dxf.rotation) == 270:
                    eixo1 = round(entity.dxf.insert[1], 3)
                    eixo2 = round((entity.dxf.insert[1] - 14.5), 3)
                    eixo3 = round((entity.dxf.insert[1] - 29), 3)
                    if eixo1 == eixocima or eixo3 == eixobaixo:
                        x = (entity.dxf.insert[0])
                        y = f2
                        point = [x, y]
                        model.add_blockref('T29', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    else:
                        print('Esse bloco não pertence a essa fiada.')
                        i += 1

                elif round(entity.dxf.rotation) == 90:
                    eixo1 = round((entity.dxf.insert[1] + 29), 3)
                    eixo2 = round((entity.dxf.insert[1] + 14.5), 3)
                    eixo3 = round((entity.dxf.insert[1]), 3)
                    if eixo1 == eixocima or eixo3 == eixobaixo:
                        x = entity.dxf.insert[0] - 14
                        y = f2
                        point = [x, y]
                        model.add_blockref('T29', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    else:
                        print('Esse bloco não pertence a essa fiada.')
                        i += 1
                else:
                    print('O bloco esta desalinhado!'), print(entity.dxf.rotation)
                    i += 1
            if i == len(B29):
                i = 0
                break
        # Procedimento para Bloco B44
        while True:
            if len(B44) == 0:
                print('Não há B44 na fiada par')
                i = 0
            else:
                entity = B44[i]
                if round(entity.dxf.rotation) == 0:
                    x = (entity.dxf.insert[0])
                    y = f2
                    point = [x, y]
                    model.add_blockref('L44', point, dxfattribs={
                        'layer': "parede",
                        'color': 4,
                        'rotation': 0})
                    i += 1

                elif round(entity.dxf.rotation) == 180:
                    x = (entity.dxf.insert[0] - 44)
                    y = f2
                    point = [x, y]
                    model.add_blockref('L44', point, dxfattribs={
                        'layer': "parede",
                        'color': 4,
                        'rotation': 0})
                    i += 1

                elif round(entity.dxf.rotation) == 270:
                    eixo1 = round(entity.dxf.insert[1], 3)
                    eixo2 = round((entity.dxf.insert[1] - 22), 3)
                    eixo3 = round((entity.dxf.insert[1] - 44), 3)
                    if eixo1 == eixocima or eixo2 == eixomeio or eixo3 == eixobaixo:
                        x = (entity.dxf.insert[0])
                        y = f2
                        point = [x, y]
                        model.add_blockref('T44', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    else:
                        print('Esse bloco não pertence a essa fiada.')
                        i += 1

                elif round(entity.dxf.rotation) == 90:
                    eixo1 = round((entity.dxf.insert[1] + 44), 3)
                    eixo2 = round((entity.dxf.insert[1] + 22), 3)
                    eixo3 = round((entity.dxf.insert[1]), 3)
                    if eixo1 == eixocima or eixo2 == eixomeio or eixo3 == eixobaixo:
                        x = entity.dxf.insert[0] - 14
                        y = f2
                        point = [x, y]
                        model.add_blockref('T29', point, dxfattribs={
                            'layer': "parede",
                            'color': 4,
                            'rotation': 0})
                        i += 1
                    else:
                        print('Esse bloco não pertence a essa fiada.')

                        i += 1
                else:
                    print('O bloco esta desalinhado!')
                    i += 1
            if i == len(B44):
                i = 0
                break
        f2 += 40
    #---------------------------------------------------- PORTA ----------------------------------------------
    """Exclusão de blocos que estao no vão da porta e acrecimo de blocos B14 para acabamento"""
    parede = model.query('INSERT[layer=="parede"]')  # Seleção de blocos que estao no layer "parede"
    """Como os blocos inseridos anteriormente tem o atributo layer = parede, todos os blocos são selecionados."""
    i = 0  # Contador de blocos
    porta = model.query('INSERT[layer=="porta"]')  # Seleção de blocos que estao no layer "porta"
    if len(porta) != 0:  # Condição para verificar a presença de portas
        for f in range(0, len(porta)):  # Repete o prcedimento para o numero total de portas encontradas.
            parede = model.query('INSERT[layer=="parede"]')  # Seleção de blocos que estao no layer "parede"
            porta = model.query('INSERT[layer=="porta"]')  # Seleção de blocos que estao no layer "porta"
            largurap = float(porta[f].get_attrib_text('LARGURA'))  # Leitura da largura da porta, Atraves do atributo largura do bloco dinâmico "porta"
            alturap = float(porta[f].get_attrib_text('ALTURA'))  # Leitura da altura da porta, Atraves do atributo altura do bloco dinâmico "porta"
            portax = trunc(float(porta[f].dxf.insert[0]), 2)  # Coordenada x da porta truncado com 2 casas após a vírgula
            portay = trunc(pontozero, 2)   # Coordenada y da porta truncado com 2 casas após a vírgula
            """Determinação do vão da porta"""
            m1 = int((portax - 15) * 1000)  # ponto de inicio da porta em x
            n1 = int((portax + largurap) * 1000)  # ponto final da porta em x
            m2 = int(portay * 1000)  # ponto de inicio da porta em y
            n2 = int((alturap + portay) * 1000)  # ponto final da porta em y
            """Determinação de quais os blocos estão no vão da porta"""
            for i in range(0, len(parede)):  # Repetir procedimento para numero de blocos no layer parede
                px = trunc((parede[i].dxf.insert[0]), 2)  # Coordenada x dos blocos que compõe a parede
                py = trunc(parede[i].dxf.insert[1], 2)  # # Coordenada y dos blocos que compõe a parede
                if (px * 1000) in range(m1, n1):  # Comparação de cada bloco para ver se ele esta no vão da porta no eixo x
                    if (py * 1000) in range(m2, n2):  # Comparação de cada bloco para ver se ele esta no vão da porta no eixo y
                        model.delete_entity(parede[i])  # deleta os blocos que estao no vão da porta
                        if (px * 1000) in range(m1, (m1 + 15000)):  # blocos deletados da ponta direita
                            model.add_blockref('L14', (px, py), dxfattribs={  # adição do bloco L14
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                        if (px * 1000) in range((n1 - 15000), n1):  # blocos deletados da ponta esquerda
                            model.add_blockref('L14', ((px + 15), py), dxfattribs={  # adição do bloco L14
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                        i += 1
                    else:
                        i += 1
                else:
                    i += 1
            f += 1
    #------------------------------------------------------- JANELA -------------------------------------------
    parede = model.query('INSERT[layer=="parede"]')  # Seleção de blocos que estao no layer "parede"
    janela = model.query('INSERT[name=="Janela"]')  # Seleção de blocos que estao no layer "Janela"
    if len(janela) != 0:  # Verificando se há janelas na parede
        for f in range(0, len(janela)):  # Repetir procedimento para todas janelas
            parede = model.query('INSERT[layer=="parede"]')  # Seleção de blocos que estao no layer "parede"
            janela = model.query('INSERT[name=="Janela"]')  # Seleção de blocos que estao no layer "Janela"
            larguraj = float(janela[f].get_attrib_text('LARGURA'))  # Define atravez dos atributos do bloco dinamico a largura da janela
            alturaj = float(janela[f].get_attrib_text('ALTURA'))  # Define atravez dos atributos do bloco dinamico a altura da janela
            peitoril = float(janela[f].get_attrib_text('PEITORIL'))  # Define atravez dos atributos do bloco dinamico o peitoril da janela
            janelax = trunc(float(janela[f].dxf.insert[0]), 2)  # Localização do vão janela no eixo x
            janelay = trunc(pontozero, 2)  # Armazena a coordenada do pontozero
            """Manipulações para determinar o inicio e o fim do vão da janela no eixo x e y"""
            x1 = int((janelax - 15) * 1000)  # Coordenada de inicio da janela no eixo x
            x2 = int((janelax + larguraj) * 1000)  # Coordenada final da janela no eixo x
            y1 = int((peitoril + janelay) * 1000)  # Coordenada de inicio da janela no eixo y consifderando a altura do peitoril
            y2 = int((janelay + peitoril + alturaj) * 1000)  # Coordenada final da janela no eixo y
            for i in range(0, len(parede)):  # verificação de todos os blocos inseridos anteriormente
                px = trunc((parede[i].dxf.insert[0]), 2)  # coordenada em x do bloco de alvenaria
                py = trunc(parede[i].dxf.insert[1], 2)  # coordenada em y do bloco de alvenaria
                if (px * 1000) in range(x1, x2):  # verificação se o bloco estao no vão da janela no eixo x
                    if (py * 1000) in range(y1, y2):  # verificação se o bloco estao no vão da janela no eixo y
                        model.delete_entity(parede[i])  # exclusão do bloco
                        """Além da exclusão do bloco é feita a inserção do bloco L14 para o acabamento"""
                        if (px * 1000) in range(x1, (x1 + 15000)):  # verificação se o bloco esta no canto esquerdo da janela
                            model.add_blockref('L14', (px, py), dxfattribs={  # adição do bloco L14
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                        if (px * 1000) in range((x2 - 15000), x2):  # verificação se o bloco esta no canto direito da janela
                            model.add_blockref('L14', ((px + 15), py), dxfattribs={  # adição do bloco L14
                                'layer': "parede",
                                'color': 4,
                                'rotation': 0})
                        i += 1
                    else:
                        i += 1
                else:
                    i += 1
            f += 1
    # ------------------------------------------------------------ CINTAS DE AMARRAÇÃO ------------------------------------------------------------------------
    """Realização das cintas de amarração das paredes. Procedimento de localizar a ultima fiada,
    excluir e colocar blocos calha com graute."""
    hparede = (fiadas - 1) * 20
    hparede = trunc((pontozero + hparede - 1),2)
    parede = model.query('INSERT[layer=="parede"]')  # localiza os blocos no layer parede
    for i in range(0,len(parede)):  # Repetir procedimento para todos blocos da vista
        nome = parede[i].dxf.name  # nome do bloco
        bloco = trunc(parede[i].dxf.insert[1],2)  # Coordenada y do bloco
        x = parede[i].dxf.insert[0]  # definição da coordenada x de inserção
        y = parede[i].dxf.insert[1]  # definição da coordenada y de inserção
        point = (x,y)  # definição do ponto de inserção
        if bloco > hparede:  # Se a Coordenada y do bloco for maior que a penultima fiada
            model.delete_entity(parede[i])  # deleta blocos da ultima fiada
            "insere o bloco referente ao bloco deletado. com layer 'cinta' e cor ciano "
            if nome == 'L14':
                model.add_blockref('BCL14', (point), dxfattribs={  # bloco 14 lateral
                    'layer' : "cinta",
                    'color' : 4,
                })
            if nome == 'L29':
                model.add_blockref('BCL29', (point), dxfattribs={  # bloco 29 lateral
                    'layer' : "cinta",
                    'color' : 4,
                })
            if nome == 'L44':
                model.add_blockref('BCL44', (point), dxfattribs={  # bloco 44 lateral
                    'layer': "cinta",
                    'color': 4,
                })
            if nome == 'T14':
                model.add_blockref('BCT14', (point), dxfattribs={  # bloco 14 transversal
                    'layer' : "cinta",
                    'color' : 4,
                })
            if nome == 'T29':
                model.add_blockref('BCT29', (point), dxfattribs={  # bloco 29 transversal
                    'layer' : "cinta",
                    'color' : 4,
                })
            if nome == 'T44':
                model.add_blockref('BCT44', (point), dxfattribs={  # bloco 44 transversal
                    'layer' : "cinta",
                    'color' : 4,
                })
        i += 1  # Contador de número de blocos
    # ---------------------------------------- VERGA PORTA -----------------------------------
    """A verga da porta será realizada atravez da localização dos blocos que
    ficam logo acima da porta e até 30cm do seu vão. Depois da localização será
    realizada a exclusão dos mesmos e a inserção dos blocos pré definidos do tipo calha"""
    porta = model.query('INSERT[layer=="porta"]')  # localização  dos blocos de porta
    for i in range(0, len(porta)):  # realização da função para todas as portas
        parede = model.query('INSERT[layer=="parede"]')  # localização dos blocos que compõe a parede
        largurap = float(porta[i].get_attrib_text('LARGURA'))  # Pega o atributo de largura da porta do bloco dinamico pré definido
        alturap = float(porta[i].get_attrib_text('ALTURA'))  # Pega o atributo de altura da porta do bloco dinamico pré definido
        """Manipulações de coordenadas para limite de exclusão e inserção dos blocos"""
        x1 = int(trunc((porta[i].dxf.insert[0] - 30), 2) * 1000)    # limite inicial na coordenada x# limite inicial na coordenada x
        x2 = int(trunc((porta[i].dxf.insert[0] + largurap + 15), 2) * 1000)    # limite final na coordenada x# limite final na coordenada x
        y1 = int(trunc((pontozero + alturap), 2) * 1000)    # limite inicial na coordenada y# limite inicial na coordenada y
        y2 = int(trunc((pontozero + alturap + 19), 2) * 1000)     # limite final na coordenada y# limite final na coordenada y
        for a in range(0, len(parede)):  # realização da função para todos blocos da parede
            nome = parede[a].dxf.name  # identifica o nome do bloco para correlacionar seu tamanho
            x = int(parede[a].dxf.insert[0] * 1000)  # posição em x do bloco
            y = int(parede[a].dxf.insert[1] * 1000)  # posição em y do bloco
            point = ((x / 1000), (y / 1000))  # ponto de inserção do bloco calha
            if x in range(x1, x2):  # verica se o bloco esta entre os limites pré definidos
                if y in range(y1, y2):  # verica se o bloco esta entre os limites pré definidos
                    model.delete_entity(parede[a])  # deleta o bloco
                    if nome == 'L14':  # identifica se o bloco é o L14
                        model.add_blockref('BCL14', (point), dxfattribs={  # inseção do bloco calha lateral 14
                            'layer': "verga",
                            'color': 4,
                        })
                    if nome == 'L29':  # identifica se o bloco é o L29
                        model.add_blockref('BCL29', (point), dxfattribs={  # inseção do bloco calha lateral 29
                            'layer': "verga",
                            'color': 4,
                        })
                    if nome == 'L44':  # identifica se o bloco é o L44
                        model.add_blockref('BCL44', (point), dxfattribs={  # inseção do bloco calha lateral 44
                            'layer': "verga",
                            'color': 4,
                        })
    #---------------------------------------- VERGA JANELA -----------------------------------
    """A verga da janela será realizada atravez da localização dos blocos que 
    ficam logo acima da janela e até 30cm do seu vão. Depois da localização 
    será realizada a exclusão dos mesmos e a inserção dos blocos pré definidos do tipo calha"""
    janela = model.query('INSERT[name=="Janela"]')   # localização  dos blocos da janela
    for i in range(0, len(janela)):  # realização da função para todas as janelas
        parede = model.query('INSERT[layer=="parede"]')  # localização dos blocos que compõe a parede
        larguraj = float(janela[i].get_attrib_text('LARGURA'))  # Pega o atributo de largura da janela do bloco dinâmico pré definido
        alturaj = float(janela[i].get_attrib_text('ALTURA'))  # Pega o atributo de altura da janela do bloco dinâmico pré definido
        peitoril = float(janela[i].get_attrib_text('PEITORIL'))  # Pega o atributo de peitoril da janela do bloco dinâmico pré definido
        """Manipulações de coordenadas para limite de exclusão e inserção dos blocos"""
        x1 = int(trunc((janela[i].dxf.insert[0] - 30), 2) * 1000)  # limite inicial na coordenada x
        x2 = int(trunc((janela[i].dxf.insert[0] + larguraj + 15), 2) * 1000)  # limite final na coordenada x
        y1 = int(trunc((pontozero + alturaj + peitoril), 2) * 1000)  # limite inicial na coordenada y
        y2 = int(trunc((pontozero + alturaj + peitoril + 19), 2) * 1000)  # limite final na coordenada y
        for a in range(0, len(parede)):  # realização da função para todos blocos da janela
            nome = parede[a].dxf.name  # identifica o nome do bloco para correlacionar seu tamanho
            x = int(parede[a].dxf.insert[0] * 1000)  # posição em x do bloco
            y = int(parede[a].dxf.insert[1] * 1000)  # posição em y do bloco
            point = ((x/1000), (y/1000))  # ponto de incerção do bloco calha
            if x in range(x1, x2):  # verica se o bloco esta entre os limites pré definidos
                if y in range(y1, y2):  # verica se o bloco esta entre os limites pré definidos
                    model.delete_entity(parede[a])  # deleta o bloco
                    if nome == 'L14':  # identifica se o bloco é o L14
                        model.add_blockref('BCL14', (point), dxfattribs={  # inseção do bloco calha lateral 14
                            'layer': "verga",
                            'color': 4,
                        })
                    if nome == 'L29':  # identifica se o bloco é o L29
                        model.add_blockref('BCL29', (point), dxfattribs={   # inseção do bloco calha lateral 29
                            'layer': "verga",
                            'color': 4,
                        })
                    if nome == 'L44':  # identifica se o bloco é o L44
                        model.add_blockref('BCL44', (point), dxfattribs={  # inseção do bloco calha lateral 44
                            'layer': "verga",
                            'color': 4,
                        })
    #---------------------------------------- CONTRA VERGA JANELA -----------------------------------
    """A contra verga da janela será realizada atravez da localização dos blocos que
    ficam logo abaixo da janela e até 30cm do seu vão. Depois da localização será 
    realizada a exclusão dos mesmos e a inserção dos blocos pré definidos do tipo calha"""
    janela = model.query('INSERT[name=="Janela"]')
    for i in range(0, len(janela)):
        parede = model.query('INSERT[layer=="parede"]')
        larguraj = float(janela[i].get_attrib_text('LARGURA'))
        alturaj = float(janela[i].get_attrib_text('ALTURA'))
        peitoril = float(janela[i].get_attrib_text('PEITORIL'))
        "Manipulações de coordenadas"
        x1 = int(trunc((janela[i].dxf.insert[0] - 30), 2) * 1000)
        x2 = int(trunc((janela[i].dxf.insert[0] + larguraj + 15), 2) * 1000)
        y1 = int(trunc((pontozero + (peitoril - 20)), 2) * 1000)
        y2 = int(trunc((pontozero + (peitoril - 20) + 19), 2) * 1000)
        for a in range(0, len(parede)):
            nome = parede[a].dxf.name
            x = int(parede[a].dxf.insert[0] * 1000)
            y = int(parede[a].dxf.insert[1] * 1000)
            point = ((x/1000), (y/1000))
            if x in range(x1, x2):
                if y in range(y1, y2):
                    model.delete_entity(parede[a])
                    if nome == 'L14':
                        model.add_blockref('BCL14', (point), dxfattribs={  # bloco 14 lateral
                            'layer': "verga",
                            'color': 4,
                        })
                    if nome == 'L29':
                        model.add_blockref('BCL29', (point), dxfattribs={  # bloco 29 lateral
                            'layer': "verga",
                            'color': 4,
                        })
                    if nome == 'L44':
                        model.add_blockref('BCL44', (point), dxfattribs={  # bloco 44 lateral
                            'layer': "verga",
                            'color': 4,
                        })
    #----------------------------------------------- GRAUTE ----------------------------------------
    """"O graute deve ser localizado atrevez de um bloco e layer pre definidos e inserido na 
    forma de hachura. A Localização e inserção são realizados atravez de coordenadas."""
    graute = model.query('INSERT[name=="graute"]')  # definição dos blocos pre definidos de graute
    graute = graute.query('INSERT[layer=="graute"]')  # seleciona os blocos de graute que estao no layer "graute"
    for i in range(0, len(graute)):  # repetir procedimento para todos grautes encontrados
        p1 = ((graute[i].dxf.insert[0]),(pontozero))  # ponto de inseção da hachura do graute em vista lateral
        p2 = ((p1[0] + 10.75),(pontozero))  # ponto de inseção da hachura do graute em vista lateral
        p3 = ((graute[i].dxf.insert[0]),(pontozero+pedireito))  # ponto de inseção da hachura do graute em vista lateral
        p4 = ((p1[0] + 10.75),(pontozero+pedireito))  # ponto de inseção da hachura do graute em vista lateral
        point = (p2, p1, p3, p4)  # pontos de limite da area da hachura do graute
        hatch = model.add_hatch(color=1, dxfattribs={'layer': "graute"})  # definições da hachura, layer pre definido
        hatch.paths.add_polyline_path(point, is_closed=True)  # adiciona a hachura do graute na area pre definida
    #----------------------------------------------- FERRO VERTICAIS ------------------------------------
    """Os ferros verticais devem ser inseridos em planta com bloco pre definido "ferro" e juntamente
    indicada as propriedades como bitola, numero de barras e comprimento do ferro. Apartir dai é feita
    a localização identificação dos atributos do bloco pre definido e inserido o ferro conforme as 
    propriedades, atraves de uma linha vertical e texto de linha unica"""
    ferro = model.query('INSERT[name=="ferro"]')  # localiza e identifica os blocos com nome ferro
    for i in range(0,len(ferro)):  # repete o procedimento para todos os ferros encontrados
        x = ferro[i].dxf.insert[0]  # define a coordenada x do ferro que é a mesma do ferro representado em planta
        y = pontozero  # define a coordenada y do ponto inicial do ferro, que é o mesmo ponto onde começam as representações dos blocos
        point = (x,y)  # ponto inial de inserção da barra
        barra = int(ferro[i].get_attrib_text('BARRA'))  # Define o numero de barras através dos atributos fornecidos anteriormente
        bitola = float(ferro[i].get_attrib_text('BITOLA'))  # Define a bitola barras através dos atributos fornecidos anteriormente
        comprimento = float(ferro[i].get_attrib_text('COMPRIMENTO'))  # Define o comprimento das barras através dos atributos fornecidos anteriormente
        x1 = x  #  Coordenada x do "pont1"
        y1 = y + comprimento  # Coordenada y do "point1"
        point1 = (x1, y1)  # ponto final de inserção da barra
        model.add_line(point,point1, dxfattribs={  # Adiciona uma linha com os pontos pré definidos no layer ferro, representando a barra
            'layer': "ferro"
        })
        model.add_line([x,(y+pedireito+49)],[x,((y+pedireito+49)+comprimento)], dxfattribs={'layer': "ferroNcontado",  # Adiciona uma linha representando as barras, porem esta linha sera localizada acima da parede junto com o restante das informações e os cortes
                                                                                        'color': 2,
                                                                                        })
        model.add_text(f'N{i+1} {barra} Φ{bitola} - C={comprimento}', dxfattribs={'layer': "ferro",  # Adiciona informações (Numero da barra, numero de barras, bitola e comprimento) da barra inserida anteriormente
                                                                                    'rotation': 90,
                                                                                    'height': 5,
                                                                                    'insert': (x-1,(((y+pedireito+49)+(y+pedireito+49)+pedireito))/2),
                                                                                })
        ultimoFerro = i
    #--------------------------------------------------------- FERRO HORIZONTAIS-------------------------------------------
    """Os ferros horizontais devem ser inseridos em planta com bloco pre definido "ferroHorizontal" e juntamente indicada as propriedades como
    bitola, numero de barras e comprimento do ferro. Apartir dai é feita a localização identificação dos atributos do bloco pré
    definido e inserido o ferro conforme as propriedades, atraves de uma linha vertical e texto de linha unica"""
    ferroH = model.query('INSERT[name=="ferroHorizontal"]')  # localiza e identifica os blocos com nome ferroHorizontal
    for i in range(0, len(ferroH)):  # repete o procedimento para todos os ferros horizontais encontrados
        alturaF = float(ferroH[i].get_attrib_text('ALTURA'))  # Define atravez dos atributos do bloco dinamico a altura do ferro Horizontal.
        barra = int(ferroH[i].get_attrib_text('BARRAS'))  # Define atravez dos atributos do bloco dinamico o número de barras.
        bitola = float(ferroH[i].get_attrib_text('BITOLA'))  # Define atravez dos atributos do bloco dinamico a bitola do ferro Horizontal.
        comprimento = float(ferroH[i].get_attrib_text('COMPRIMENTO'))  # Define atravez dos atributos do bloco dinamico o comprimento do ferro Horizontal.
        x = ferroH[i].dxf.insert[0]  # define a coordenada x do ponto "point"
        y = pontozero + alturaF # define a coordenada y do ponto "point"
        point = (x,y)  # ponto inicial de inseção da barra
        point1 = ((x+comprimento), y)  # ponto final de inserção da barra
        model.add_line(point, point1, dxfattribs={
            'layer': "ferro"})
        point2 = (x, (pontozero-(i+1)*10))
        point3 = (x+comprimento, (pontozero-(i+1)*10))
        model.add_line(point2, point3,  # Adiciona uma linha representando as barras, porem esta linha sera localizada abaixo da parede junto com o restante das informações da barra
                    dxfattribs={'layer': "ferroNcontado",
                                'color': 2,
                                })
        model.add_text(f'N{ultimoFerro + i + 2} {barra} Φ{bitola} - C={comprimento}', dxfattribs={'layer': "ferro",  # Adiciona um texto com as informações da barra
            'rotation': 0,
            'height': 5,
            'insert': (x,pontozero-(i+1)*10)})
    #----------------------------------------------------------- Corte Parede ---------------------------------------------
    """Esta parte do software desenha o um corte transversal da parede na posição indicada em planta"""
    corte = model.query('INSERT[name=="corte"]')  # Pesquisa blocos de nome "corte" no arquivo .dxf
    x = 0
    for i in range(0,len(corte)):  # Repete o procedimento para o numero de cortes encontrados
        xCorte = round(corte[i].dxf.insert[0], 2)  # Localiza a posição x que foi inserido o corte
        x1 = int((xCorte - 30) * 1000)  # Indicação inicial do intervalo do corte
        x2 = int(xCorte * 1000)  # Indicação final do intervalo do corte
        nomeCorte = corte[i].get_attrib_text('CORTE')  # Estabelece o nome do bloco definido anteriormente
        parede = model.query('INSERT[layer=="parede"]')  # Seleciona os blocos no layer parede (Blocos de alvenaria)
        cinta = model.query('INSERT[layer=="cinta"]')  # Seleciona os blocos no layer cinta (Blocos de cinta)
        verga = model.query('INSERT[layer=="verga"]')  # Seleciona os blocos no layer verga (Blocos de verga e contraverga)
        for a in range(0, len(parede)):  # Repete o procedimento para todos blocos de alvenaria no layer parede
            nome = parede[a].dxf.name  # Seleciona o nome do bloco, para identificar o seu tamanho
            x = int(parede[a].dxf.insert[0] * 1000)  # Define a coordenada x do selecionado, para verificar de esta no intervalo do corte
            y = (parede[a].dxf.insert[1]) + pedireito + 50  # Define a coordenada y de inserção dos blocos
            point = ((xCorte), (y)) #  ponto de inserção do bloco
            if x in range(x1, x2):  # Verifica se o bloco seleciona esta no intervalo do corte
                if nome == 'L14':  # Verifica se o bloco selecionado é o L14
                    model.add_blockref('Bcorte', (point), dxfattribs={  # inseção do bloco lateral 14
                        'layer': "corte",
                        'color': 4,
                    })
                if nome == 'L29':  # identifica se o bloco é o L29
                    model.add_blockref('Bcorte', (point), dxfattribs={  # inseção do bloco lateral 29
                        'layer': "corte",
                        'color': 4,
                    })
                if nome == 'L44':  # identifica se o bloco é o L44
                    model.add_blockref('Bcorte', (point), dxfattribs={  # inseção do bloco lateral 44
                        'layer': "corte",
                        'color': 4,
                    })
        for a in range(0, len(cinta)):  # Repete o procedimento para todos blocos de alvenaria no layer cinta
            nome = cinta[a].dxf.name  # Seleciona o nome do bloco, para identificar o seu tamanho
            x = int(cinta[a].dxf.insert[0] * 1000)  # Define a coordenada x do selecionado, para verificar de esta no intervalo do corte
            y = (cinta[a].dxf.insert[1]) + pedireito + 50  # Define a coordenada y de inserção dos blocos
            point = ((xCorte), (y))  # ponto de inserção do bloco
            if x in range(x1, x2):  # Verifica se o bloco seleciona esta no intervalo do corte
                if nome == 'BCL14':  # identifica se o bloco é o L14
                    model.add_blockref('BCT14', (point), dxfattribs={  # inseção do bloco calha lateral 14
                        'layer': "corte",
                        'color': 4,
                    })
                if nome == 'BCL29':  # identifica se o bloco é o L29
                    model.add_blockref('BCT29', (point), dxfattribs={  # inseção do bloco calha lateral 29
                        'layer': "corte",
                        'color': 4,
                    })
                if nome == 'BCL44':  # identifica se o bloco é o L44
                    model.add_blockref('BCT44', (point), dxfattribs={  # inseção do bloco calha lateral 44
                        'layer': "corte",
                        'color': 4,
                    })
        for a in range(0, len(verga)):  # Repete o procedimento para todos blocos de alvenaria no layer verga
            nome = verga[a].dxf.name  # Seleciona o nome do bloco, para identificar o seu tamanho
            x = int(verga[a].dxf.insert[0] * 1000)  # Define a coordenada x do selecionado, para verificar de esta no intervalo do corte
            y = (verga[a].dxf.insert[1]) + pedireito + 50  # Define a coordenada y de inserção dos blocos
            point = ((xCorte), (y))  # ponto de inserção do bloco
            if x in range(x1, x2):  # Verifica se o bloco seleciona esta no intervalo do corte
                if nome == 'BCL14':  # identifica se o bloco é o L14
                    model.add_blockref('BCT14', (point), dxfattribs={  # inseção do bloco calha lateral 14
                        'layer': "corte",
                        'color': 4,
                    })
                if nome == 'BCL29':  # identifica se o bloco é o L29
                    model.add_blockref('BCT29', (point), dxfattribs={  # inseção do bloco calha lateral 29
                        'layer': "corte",
                        'color': 4,
                    })
                if nome == 'BCL44':  # identifica se o bloco é o L44
                    model.add_blockref('BCT44', (point), dxfattribs={  # inseção do bloco calha lateral 44
                        'layer': "corte",
                        'color': 4,
                    })
        posicaoLaje = corte[i].get_attrib_text('LAJE')  # Seleciona a posição que a laje deve ser representada
        if posicaoLaje == 'd':  # Laje para a direita
            model.add_blockref('LajeDir', ((xCorte), (pedireito+pontozero+49+pedireito)), dxfattribs={'layer': "laje"})  # Posiciona o bloco o qual representa o corte da laje para a direita
        if posicaoLaje == 'e':  # Laje para a esquerda
            model.add_blockref('LajeEsq', ((xCorte), (pedireito+pontozero+49+pedireito)), dxfattribs={'layer': "laje"})  # Posiciona o bloco o qual representa o corte da laje para a esquerda
        if posicaoLaje == '2':  # Laje para ambos os lados
            model.add_blockref('Laje', ((xCorte), (pedireito+pontozero+49+pedireito)), dxfattribs={'layer': "laje"})  # Posiciona o bloco o qual representa o corte da laje para ambos lados
        """Pontos para representação das linha das paredes em vista"""
        p1 = ((xCorte),(pedireito+pontozero+49))
        p2 = ((xCorte),(pedireito+pontozero+49+pedireito))
        p3 = ((xCorte+14),(pedireito+pontozero+49))
        p4 = ((xCorte+14),(pedireito+pontozero+49+pedireito))
        """Linhas das paredes"""
        model.add_line(p1,p2, dxfattribs={'layer': "corte",
                                        'color': 2,})
        model.add_line(p3,p4, dxfattribs={'layer': "corte",
                                        'color': 2,})
        model.add_line(p1, p3, dxfattribs={'layer': "corte",
                                        'color': 2, })

        model.add_text(f'{nomeCorte}', dxfattribs={'color': 3,
                                                    'insert': ((xCorte), (pedireito+pontozero+70+pedireito)),
                                                    'height': 10})

    #---------------------------------------------------------- TABELA AÇO --------------------------------------
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
    for i in range(1,len(ferro)):  # Repete o procedimento para todas barras horizontais encontradas
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
    x = 0
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

    #---------------------------------------------------- Quantitativo Blocos -----------------------------------
    """Tabela de quantitativo de blocos"""
    y = model.query('INSERT[layer=="fiada2"]')
    y = y[0].dxf.insert[1]
    x = 0
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
    L14 = model.query('INSERT[name=="L14"]')
    L29 = model.query('INSERT[name=="L29"]')
    L44 = model.query('INSERT[name=="L44"]')
    BCL14 = model.query('INSERT[name=="BCL14"]')
    BCL29 = model.query('INSERT[name=="BCL29"]')
    BCL44 = model.query('INSERT[name=="BCL44"]')

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

    #-------------------------------------------- Quantitativo volume de graute ------------------------
    y = model.query('INSERT[layer=="fiada2"]')
    y = y[0].dxf.insert[1]
    x = 0
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


    dwg.saveas('OUTFILE.dxf')  # salvamento do arquivo modificado no arquivo "OUTFILE.DXF"

window.close()