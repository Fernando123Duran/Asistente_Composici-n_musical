import numpy as np
def cargarArchivosNPY(path):
    with open(path, 'rb') as f:
        datos = np.load(f,allow_pickle=True)
        datosCompletos=[]
        datos=datos.tolist()
        for da in datos:
          datosCompletos.append(np.array(datos[da]))
        # print(len(datosCompletos))
    return datosCompletos

armadura={
    "1": 31,
    "2": 32,
    "3": 33,
    "4": 34,
    "5": 35,
    "6": 36,
    "7": 37,
    "-1": 38,
    "-2": 39,
    "-3": 40,
    "-4": 41,
    "-5": 42,
    "-6": 43,
    "-7": 44,
    "0": 45,
}
armaduraInv={
    "31":1,
    "32":2,
    "33":3,
    "34":4,
    "35":5,
    "36":6,
    "37":7,
    "38":-1,
    "39":-2,
    "40":-3,
    "41":-4,
    "42":-5,
    "43":-6,
    "44":-7,
    "45":0,
}
def transposePartituras(part,cambioTono):
    partNuevoTono=[]
    modificador=cambioTono*2
    # print(part)
    for note in part:
        if note in range(31,45+1):
            tono = armaduraInv[str(note)]                
            nuevoTono=tono+modificador
            if nuevoTono>=8 :
                nuevoTono=nuevoTono-7
                nuevoTono=-5+nuevoTono
            elif nuevoTono<=-8:
                nuevoTono=nuevoTono+7
                nuevoTono=5+nuevoTono
            nuevoTono =armadura[str(nuevoTono)]
            partNuevoTono.append(nuevoTono)
        elif note in range(58,145+1):
            nuevaNota=note+modificador
            partNuevoTono.append(nuevaNota)
        else:
            partNuevoTono.append(note)
    return np.array(partNuevoTono)
    
def generarNuevasPartituras(datos):
    nuevoTOTAL = {}
    print(len(datos)) 
    for n in range(0,len(datos)):
        t1= transposePartituras(part=datos[n],cambioTono=1)
        t2= transposePartituras(part=datos[n],cambioTono=2)
        b1= transposePartituras(part=datos[n],cambioTono=-1)
        b2= transposePartituras(part=datos[n],cambioTono=-2)
        nuevoTOTAL["_"+str(n)]=datos[n]
        nuevoTOTAL["t1_"+str(n)]=t1
        nuevoTOTAL["t2_"+str(n)]=t2
        nuevoTOTAL["b1_"+str(n)]=b1
        nuevoTOTAL["b2_"+str(n)]=b2
    print(len(nuevoTOTAL)) 
    np.save("datos/archivos_numpy/dataAumentation_tobas.npy",nuevoTOTAL) 
        
    
                
def sacaMuestra(part):
    muestra="["
    for n in part:
        muestra = muestra+","+str(n)
    muestra=muestra+"]"
    return muestra
if __name__ == "__main__":
    datos=cargarArchivosNPY("datos/archivos_numpy/dataSetCompleto.npy")
    datos=cargarArchivosNPY("datos/archivos_numpy/tobas.npy")
    #las siguientes lineas comentadas sacan una muestra de como transpone la partitura 'dat'
    # dat=[1, 51, 47, 40, 112, 4, 116, 6, 116, 4, 19, 116, 4, 21, 116, 6, 114, 4, 116, 6, 114, 6, 116, 4, 114, 4, 116, 
    #      4, 118, 4, 119, 9, 26, 6, 111, 4, 114, 6, 114, 4, 19, 114, 4, 21, 114, 6, 116, 4, 114, 7, 109, 4, 111, 4, 109, 4, 108, 4, 
    #      111, 4, 109, 8, 26, 8, 30, 29, 109, 4, 112, 6, 112, 4, 19, 112, 4, 21, 112, 6, 111, 4, 112, 6, 111, 6, 112, 4, 111, 4, 112, 4, 114,
    #      4, 116, 9, 26, 6, 111, 4, 114, 6, 114, 4, 19, 114, 4, 21, 114, 6, 116, 4, 114, 7, 111, 4, 111, 4, 109, 4, 108, 4, 111, 4, 22, 27, 109, 
    #      9, 26, 6, 30, 23, 27, 24, 109, 7, 116, 4, 19, 116, 4, 21, 116, 6, 114, 4, 29, 116, 4, 116, 6, 114, 4, 116, 7, 114, 4, 116, 9, 26, 6, 27,
    #      25, 111, 4, 114, 6, 114, 4, 19, 114, 4, 21, 114, 6, 116, 4, 114, 7, 111, 4, 111, 4, 109, 4, 108, 4, 111, 4, 22, 27, 109, 7, 116, 4, 19, 116, 
    #      4, 21, 116, 6, 114, 4, 30, 23, 27, 24, 109, 6, 109, 6, 109, 4, 107, 4, 104, 6, 27, 25, 29, 26, 8, 116, 4, 116, 4, 114, 4, 116, 4, 119, 9, 26, 
    #      6, 114, 4, 116, 4, 119, 4, 114, 4, 116, 4, 119, 4, 114, 4, 112, 4, 109, 9, 26, 6, 109, 4, 112, 6, 112, 4, 19, 112, 4, 21, 112, 6, 111, 4, 112, 
    #      6, 111, 6, 112, 4, 111, 4, 112, 4, 114, 4, 116, 9, 26, 6, 111, 4, 114, 6, 114, 4, 19, 114, 4, 21, 114, 6, 116, 4, 114, 7, 111, 4, 111, 4, 109, 
    #      4, 108, 4, 111, 4, 22, 27, 109, 9, 26, 6, 30, 23, 27, 24, 109, 6, 109, 6, 109, 4, 107, 4, 104, 6, 28, 25, 2]
    # salida=np.array(dat)
    # print(sacaMuestra(salida))
    # print("//////")
    # nuevoPart=transposePartituras(dat,-1)
    # print(sacaMuestra(nuevoPart))
    generarNuevasPartituras(datos)
   