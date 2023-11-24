#Actividad 07
#Diego Maldonado

def compresion():
    # Pedir el nombre del archivo. Por si no está, validar error
    archivo = open('ArchivoEjemplo.txt', encoding='utf-8')
    palabras = []
    for palabra in archivo:
        palabras.append(palabra)
    archivo.close()

    # Determinación de la frecuencia de palabras utilizando un diccionario
    frecuencias = {}
    simbolos = []

    for palabra in palabras:
        if palabra in frecuencias:
            frecuencias[palabra] += 1
        else:
            frecuencias[palabra] = 1
            simbolos.append(palabra)

    # Creación del árbol
    #La lista recorre cada elemento de mi lista simbolos,
    #EL primer elemento es la frecuencia, ya que busco representar cuantas veces se muestra
    #cada simbolo
    nodos = [[frecuencias[simbolo], simbolo] for simbolo in simbolos]
    #Con los nodos busco la creacion de mi arbol de huffman
    arbol = [nodos]
    #Arbol es una lista que contiene una lista. Se inicializa asi ya que, por el momento,
    #solo tiene un nivel. Con la siguiente funcion se organizan los niveles

    # Creación de los niveles
    def determinarNiveles(nodos):
        #donde la lista de nodos son los elementos iniciales del arbol
        #ES importante recordar que cada nodo tiene el dato de la frecuencia y simbolos
        posicion = 0
        nuevoNodo = []

        #Si hay mas de 1 nodos, debe haber una determinacion de niveles
        if len(nodos) > 1:
            #Ordenar los elementos de menor a mayor frecuencia
            nodos.sort()
            #Se le asigna 0 y 1 a los elementos mas bajos
            #Recordando que 0 para el de la izquierda y 1 al de la derecha
            nodos[posicion].append("0")
            nodos[posicion+1].append("1")

            #Se crean niveles que mezclan los nodos anteriores, tanto en la frecuencia como en los simbolos
            primerNivel = (nodos[posicion][0]+nodos[posicion+1][0])
            segundoNivel = (nodos[posicion][1]+nodos[posicion+1][1])
            
            #Los niveles creados se consideran como nuevos nodos
            nuevoNodo.append(primerNivel)
            nuevoNodo.append(segundoNivel)
            nuevosNodos = []
            nuevosNodos.append(nuevoNodo)

            #Se unen los niveles creados con el nivel anterior, pero sin considerar los
            #dos nodos inicialmente combinados, ya que ya estan considerados
            nuevosNodos = nuevosNodos + nodos[2:]
            nodos = nuevosNodos
            arbol.append(nodos)
            #Se utiliza recursividad hasta la existencia de un solo nodo
            determinarNiveles(nodos)
        #Se retorna el arbol construido
        return arbol
    
    #Se establece en funcion para la recursividad
    determinarNiveles(nodos)

    #Por la teoria de los arboles de huffman, estos se muestran 
    #de menor a mayor frecuencia, o de abajo hacia arriba
    arbol.sort(reverse=True)

    mostrar = []
    for nivel in arbol:
        for nodo in nivel:
            #Verificamos si el nodo actual no esta siendo mostrado
            if nodo not in mostrar:
                mostrar.append(nodo)
            else:
                nivel.remove(nodo)

    print("Arbol obtenido: ")
    for nivel in arbol:
        print(nivel)

#Creacion del codigo binario para cada segmento
    caracteresEnBinario = []
    #SI solo hay un simbolo, el texto es de una palabra, por lo que su codigo sera 0
    if len(simbolos) == 1:
        codigo = [simbolos[0], "0"]
        caracteresEnBinario.append(codigo*len(palabras))
    else:
        #Se recorren todas las palabras del texto
        for simbolo in simbolos:
            #cada iteracion se inicializa la variable codigo, que sera el codigo huffman del texto
            codigo = ""
            for nodo in mostrar:
                #Condicional que se usa para saber si son nodos hijos o madres
                #y si el simbolo esta presente en la seccion del nodo que guarda los simbolos
                if len(nodo) > 2 and simbolo in nodo[1]:
                    #se agrega el 3er elemento del nodo, que es simplemente un 1 o 0 que indica el camino
                    codigo = codigo + nodo[2] #Bifurcacion que muestra el camino
            #union del codigo de las palabras, con las palabras mismas
            codigo = [simbolo, codigo]
            caracteresEnBinario.append(codigo)

    codigoBinario = ""
    #Se recorre el texto original
    for i in palabras:
        #Recorre los codigos de las palabras
        for j in caracteresEnBinario:
            if i in j:
                #Adquiere el codigo de la palabra "i"
                codigoBinario += j[1]
    
    #Convierte mi string a numero binario
    codigoBinario = bin(int(codigoBinario, base=2))
    print("Generando archivo comprimido...")

    #Creacion del nuevo archivo
    with open("ArchivoComprimido.bin", 'w') as archivo:
        archivo.write(codigoBinario)
    
    return caracteresEnBinario
    
def descompresion(caracteresEnBinario):
    #Invocamos al archivo comprimido
    archivo = open('ArchivoComprimido.bin', 'r')
    codigoBinario = ""
    for digito in archivo:
        codigoBinario+=digito
    archivo.close()
    #El bin coloca un 0b al inicio de la cadena. Con la siguiente linea eso no pasa
    codigoBinario = codigoBinario[2:]
    #Almaceno el texto descomprimido
    palabras = ""
    #codigo particular de las palabras, necesario para la comparacion
    codigo = ""
    #Se recorren todos los 0's y 1's
    for numero in codigoBinario:
        #Se agrega ese 0 o 1 al codigo
        codigo += numero
        posicion = 0
        #Se utiliza los codigos creados en mi funcion de compresion
        for i in caracteresEnBinario:
            if codigo == i[1]:
                #Si coincide el codigo con el codigo de las palabras, se añade dicha palabra a la descompresion
                palabras += caracteresEnBinario[posicion][0] + " "
                codigo = ""
            posicion += 1
    print("Decodificando...")
    with open('ArchivoDescomprimido.txt', 'w') as archivo:
        archivo.write(palabras)

#Menu ciclico
def menu():
    while(True):
        print("Seleccione la opcion deseada:")
        print("1: Comprimir archivo")
        print("2: Descromprimir archivo")
        print("3: Salir")
        try:
            option = int(input("Ingrese el numero: "))
        except:
            print("Ingrese un valor correcto...")
        
        if(option == 1):
            #Inicializo la variable para pasarla como parametro en la descompresion
            caracteresEnBinario = compresion();
        elif(option == 2):
            descompresion(caracteresEnBinario)
        elif(option == 3):
            print("Saliendo del programa: ")
            break
        else:
            print("Ingrese una opcion valida...")

menu()
