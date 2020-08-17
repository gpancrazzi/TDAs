#!/usr/bin/python3
from grafo import Grafo
from biblioteca import camino_minimo_bfs, vertices_rango_n, ciclo_largo_n, diametro_grafo, componente_fuertemente_conexa
import sys
import constantes

def construir_grafo(archivo):
    """Recibe un archivo, con formato tsv, abierto para lectura.
    Retorna un grafo con las conexiones especificadas en el archivo."""
    grafo = Grafo(True)
    for linea in archivo:
        linea_limpia = linea.strip()
        titulos = linea_limpia.split('\t')
        articulo = titulos.pop(0)
        link1 = None
        if titulos:
            link1 = titulos.pop(0)
            grafo.agregar_vertice(link1)
        if grafo.pertenece_vertice(articulo): grafo.actualizar_dato(articulo, link1)
        else: grafo.agregar_vertice(articulo, link1)
        if link1: grafo.agregar_arista(articulo, link1)
        for link in titulos:
            grafo.agregar_vertice(link)
            grafo.agregar_arista(articulo, link)
    return grafo

def listar_operaciones():
    """"""
    operaciones = ["camino", "mas_importantes", "conectados", "ciclo", "lectura", 
    "diametro", "rango", "comunidad", "navegacion", "clustering"]
    for operacion in operaciones:
        print(operacion)

def reconstruir_camino(padres, origen, destino):
    """"""
    fin = destino
    recorrido = []
    while fin != origen:
        recorrido.append(fin)
        fin = padres.get(fin)
    recorrido.append(origen)
    recorrido.reverse()
    camino = constantes.FLECHA.join(recorrido)
    return camino

def camino_mas_corto(grafo, parametros):
    """"""
    origen = parametros.pop(0)
    destino = parametros.pop(0)
    if ((not grafo.pertenece_vertice(origen)) or 
    (not grafo.pertenece_vertice(destino))): 
        print(constantes.SIN_CAMINO)
        return 
    (padres, orden) = camino_minimo_bfs(grafo, origen, destino)
    if not destino in orden:
        print(constantes.SIN_CAMINO)
        return
    camino = reconstruir_camino(padres, origen, destino)
    print(camino)
    print(constantes.COSTO_CAMINO %orden[destino])

def todos_en_rango(grafo, parametros):
    """"""
    origen = parametros.pop(0)
    n = int(parametros.pop(0))
    en_rango = vertices_rango_n(grafo, origen, n)
    print(en_rango)

def navegacion_primer_link(grafo, parametros):
    """"""
    v = parametros.pop(0)
    camino = []
    camino.append(v)
    while v:
        if len(camino) == 21: break
        v = grafo.ver_dato_vertice(v)
        if not v: break
        camino.append(v)
    recorrido = constantes.FLECHA.join(camino)
    print(recorrido)

def ciclo_n_articulos(grafo, parametros):
    """"""
    origen = parametros.pop(0)
    n = int(parametros.pop(0))
    ciclo = ciclo_largo_n(grafo, origen, n)
    if not ciclo:
        print(constantes.SIN_CAMINO)
        return
    ciclo.append(origen)
    recorrido = constantes.FLECHA.join(ciclo)
    print(recorrido)

def calcular_diametro(grafo):
    """"""
    (padres, origen, destino, orden) = diametro_grafo(grafo)
    diametro = reconstruir_camino(padres, origen, destino)
    print(diametro)
    print(constantes.COSTO_CAMINO %orden)

def calcular_conectividad(grafo, parametros):
    """"""
    origen = parametros.pop(0)
    componente = componente_fuertemente_conexa(grafo, origen)
    print(componente)

def limpiar_parametros(linea):
    """"""
    parametros = linea.split(',')
    parametros_limpios = []
    for parametro in parametros:
        parametro = parametro.lstrip()
        parametro = parametro.rstrip()
        parametros_limpios.append(parametro)
    return parametros_limpios

def identificar_comando(linea):
    """"""
    comandos = linea.split(' ', 1)
    comando = comandos.pop(0)
    if not comandos: return comando, None
    linea = "".join(comandos)
    parametros = limpiar_parametros(linea)
    return comando, parametros

def procesar_entrada(grafo):
    """"""
    comando = constantes.LISTAR_OPERACIONES
    #cfc = {}
    while comando:
        try: linea = input()
        except EOFError: break
        (comando, parametros) = identificar_comando(linea)
        if comando == constantes.LISTAR_OPERACIONES: listar_operaciones()
        elif comando == constantes.CAMINO: camino_mas_corto(grafo, parametros)
        elif comando == constantes.RANGO: todos_en_rango(grafo, parametros)
        elif comando == constantes.NAVEGACION: navegacion_primer_link(grafo, parametros)
        elif comando == constantes.CICLO: ciclo_n_articulos(grafo, parametros)
        elif comando == constantes.DIAMETRO: calcular_diametro(grafo)
        elif comando == constantes.CONECTADOS: calcular_conectividad(grafo, parametros)

archivo = open(sys.argv[1], 'r')
red = construir_grafo(archivo)
print("OK")
archivo.close()
procesar_entrada(red)