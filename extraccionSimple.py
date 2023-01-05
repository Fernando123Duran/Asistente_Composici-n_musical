import music21 as m21
import json
import numpy as np
import time
import os
from tqdm import tqdm
def extraccionSimple():
    song = m21.converter.parse("datos/t1.xml")
    
    
    ele=song.flatten().elements
    print(+song.analyze('key') )
    for e in ele :
        try:
            if e.isRest:
                    # print("Silencio: " + str(e.duration.quarterLength))
                    print("Silencio: " + str(e.duration.quarterLength)) 
            # e.analyze()
            elif  isinstance(e, m21.note.Note):
                # print("Nota : "+str(e.name))
                 
                if e.pitch.accidental is None:
                    print("Nota : "+str(e.pitch.midi) +"/"+str(e.name)+" duracion: "+str(e.duration.quarterLength))    
                else:
                    print("Nota : "+str(e.pitch.midi) +"/"+str(e.pitch.accidental.unicode)+" duracion: "+str(e.name))    
            
            if  isinstance(e.classes[0],m21.bar.Barline):
                print("Barra " + str(e))
            if isinstance(e, m21.clef.TrebleClef):
                print("Clave : " + str(e.sign)+" en linea : "+ str(e.line))                
            
            if isinstance(e, m21.meter.TimeSignature):
                print("Compas : " + str(e.ratioString))
            
        except:
            print(" Exepcion: " + str(e.classes))
           
    # a=song.getKeySignatures()
    # print(a)
    # print(type(song))
    # print(song.show("text"))


def extracto_dos():
    # song = m21.converter.parse("datos/pru_trios.xml")
    song = m21.converter.parse("datos/t1.xml")
    
    ele=song.flatten().elements
    for e in ele :
        try:
            if isinstance(e,m21.clef.TrebleClef):
                print("entro clave: "+ e.sign+" en linea : "+ str(e.line))
            elif  isinstance(e, m21.instrument.Instrument):
                print("es trompeta"+str(e))
            elif  isinstance(e, m21.note.Note):
                print("Nota: "+str(e.pitch.midi)+" "+e.pitch.unicodeNameWithOctave +" "+str(e.transpose(-2).pitch.unicodeNameWithOctave)+" "+str(e.transpose(-2).pitch.midi)+ " duracion: "+str(e.duration.quarterLength))
            elif isinstance(e,m21.note.Rest):
                print("Silencio: " + str(e.duration.quarterLength)) 
            elif isinstance(e,m21.key.KeySignature):
                print("Tono: " + str(e.name))   
                print("Tono2: " + str(e.sharps)+" "+str(e.mode))                        
            elif  isinstance(e,m21.bar.Barline):
                if isinstance(e,m21.bar.Repeat):
                    print("Barra Repeticion " + str(e.direction))
                else:
                    print("Barra  " + str(e.type))
            elif isinstance(e, m21.meter.TimeSignature):
                print("Compas : " + str(e.ratioString))
            elif isinstance(e, m21.spanner.RepeatBracket):
                print("Casillas de repeticion: " + str(e))
            else:
                print("Ninguno: " + str(e))
        except:
            print(" Exepcion: " + str(e.classes))


def extracto_tres():
    # song = m21.converter.parse("datos/Tinkuy_proyecto.xml")
    song = m21.converter.parse("datos/t1.xml")
    song.show('text')
    song.show('musicxml.png')
    # ele=song.flatten().elements
    # for e in ele :
    #     print(e)
        
        
def cargarVocabulario(pathVocabulario):
    with open(pathVocabulario, "r") as fp:
        mappings = json.load(fp)
    return mappings
    
class GenArchivosNumpy:
    
    def __init__(self,pathPartitura, pathVocabulario,numero_de_part):
        self.pathPartitura = pathPartitura
        self.pathVocabulario = pathVocabulario  
        self.dicVocabulario= cargarVocabulario(pathVocabulario)
        self.song = m21.converter.parse(pathPartitura)
        self.ele=self.song.flatten().elements
        self.llavesRepeticionList= self.listaLlavesRepeticion(self.ele)
        self.llaveSelect=None
        self.llaveNumberMeasure=[]
        self.partituraTokens=[self.dicVocabulario["<start>"]]
        self.allParteTokens={}
        self.numero_de_part=numero_de_part
        self.numeroCorcheteAnterior="0"
        self.trompeta=False
        self.infParte={
            'llave':0,
            'compas':0,
            'tono':0
        }
        
    
    def asignarTokensDePartituras(self):
        notasAddLlave=[]
        e=self.recolectar_ligas_slur(self.ele)
        # e=self.ele
        for i in range(0,len(self.ele)):
            if not isinstance(e[i],m21.layout.SystemLayout):
                if isinstance(e, m21.instrument.Instrument):
                    if isinstance(e, m21.instrument.Trumpet):
                        self.trompeta=True
                    else:
                        self.trompeta=False
                        
                if self.llaveSelect is None:
                    if(e[i].measureNumber!=None):
                        self.seleccionarLlavesRepet(e[i].measureNumber)
                if len(self.llaveNumberMeasure)==1:
                    if self.llaveNumberMeasure[0]==e[i].measureNumber:
                        notasAddLlave.append(e[i])
                        if len(e)<i+1:
                            if e[i+1].measureNumber!=self.llaveNumberMeasure[0] and len(notasAddLlave)>0 and not isinstance(e[i+1],m21.layout.SystemLayout):
                                self.guardarNotasAcumuladas(notasAddLlave)
                                notasAddLlave.clear()
                        if len(e)==i+1:
                            self.guardarNotasAcumuladas(notasAddLlave)
                            notasAddLlave.clear()     
                    else:
                        if len(notasAddLlave)>0:
                            self.guardarNotasAcumuladas(notasAddLlave)
                            notasAddLlave.clear()
                        self.addToListTokens(e[i])
                elif len(self.llaveNumberMeasure)==2:
                    if e[i].measureNumber in range(self.llaveNumberMeasure[0],self.llaveNumberMeasure[1]+1):
                        notasAddLlave.append(e[i])
                        if len(e)<i+1:
                            if e[i+1].measureNumber not in  range(self.llaveNumberMeasure[0],self.llaveNumberMeasure[1]+1) and len(notasAddLlave)>0 and not isinstance(e[i+1],m21.layout.SystemLayout):
                                self.guardarNotasAcumuladas(notasAddLlave)
                                notasAddLlave.clear() 
                        if len(e)==i+1:
                            self.guardarNotasAcumuladas(notasAddLlave)
                            notasAddLlave.clear()    
                    else:
                        if len(notasAddLlave)>0:
                            self.guardarNotasAcumuladas(notasAddLlave)
                            notasAddLlave.clear()
                        self.addToListTokens(e[i])
                else:
                    if len(notasAddLlave)>0:
                        self.guardarNotasAcumuladas(notasAddLlave)
                        notasAddLlave.clear()
                    self.addToListTokens(e[i]) 
        # print(self.allParteTokens)
        return self.allParteTokens
        # np.save(self.pathArchNumpy,self.allParteTokens)   
    
    def guardarNotasAcumuladas(self,notasAcumuladas):
        if len(notasAcumuladas)>0:
            numeroCorchete=self.llaveSelect.number
            numCorLin=str(numeroCorchete)
            
            if numCorLin=="":
                if self.numeroCorcheteAnterior=="1":
                    numCorLin="2"
                elif self.numeroCorcheteAnterior=="2":
                    numCorLin="1"
            if numCorLin!="1" and numCorLin!="2" :
                numCorLin=numCorLin[-1]
            self.numeroCorcheteAnterior=numCorLin
            simboloCorche="corchetRep"+numCorLin
            self.partituraTokens.append(self.dicVocabulario[simboloCorche+"_start"])
            for no in notasAcumuladas:
                if self.ver_barra_final(no):                  
                    if  isinstance(no,m21.bar.Barline):
                        if not isinstance(no,m21.bar.Repeat):                           
                            simbolo="b_"+ str(no.type)
                            self.partituraTokens.append(self.dicVocabulario[simbolo])
                            numeroCorchete=self.llaveSelect.number
                            numCorLin=str(numeroCorchete)
                            if numCorLin=="":
                                if self.numeroCorcheteAnterior=="1":
                                    numCorLin="2"
                                elif self.numeroCorcheteAnterior=="2":
                                    numCorLin="1"
                            if numCorLin!="1" and numCorLin!="2" :
                                numCorLin=numCorLin[-1]
                            self.numeroCorcheteAnterior=numCorLin
                            simboloCorche="corchetRep"+numCorLin
                            self.partituraTokens.append(self.dicVocabulario[simboloCorche+"_stop"]) 
                            if str(no.type)=="final":
                                self.partituraTokens.append(self.dicVocabulario["<stop>"])
                                self.allParteTokens[str(self.numero_de_part)]= self.partituraTokens
                                self.numero_de_part+=1
                                self.partituraTokens=[]
                                self.partituraTokens.append(self.dicVocabulario["<start>"]) 
                else:    
                    self.addToListTokens(no)
            if not self.ver_barra_final(no):
                numeroCorchete=self.llaveSelect.number
                numCorLin=str(numeroCorchete)
                if numCorLin=="":
                    if self.numeroCorcheteAnterior=="1":
                        numCorLin="2"
                    elif self.numeroCorcheteAnterior=="2":
                        numCorLin="1"
                if numCorLin!="1" and numCorLin!="2" :
                    numCorLin=numCorLin[-1]
                self.numeroCorcheteAnterior=numCorLin
                simboloCorche="corchetRep"+numCorLin
                self.partituraTokens.append(self.dicVocabulario[simboloCorche+"_stop"])
            self.llaveSelect=None
            self.llaveNumberMeasure.clear()
                
    
    def addToListTokens(self,e):
        if isinstance(e,m21.clef.TrebleClef):           
            simbolo="clave_"+str(e.sign)+"_"+str(e.line)
            # self.partituraTokens.append(self.dicVocabulario[simbolo])
            self.infParte['llave']=self.dicVocabulario[simbolo]
        elif  isinstance(e, m21.note.Note):
            if len(self.partituraTokens)==1:
                for infPa in self.infParte:
                    self.partituraTokens.append(self.infParte[infPa])   
            if self.trompeta:
                self.partituraTokens.append(self.dicVocabulario[str(e.transpose(-2).pitch.midi)])
            else:
                self.partituraTokens.append(self.dicVocabulario[str(e.pitch.midi)])
            
            self.partituraTokens.append(self.dicVocabulario[str(e.duration.quarterLength)])
            if e.tie != None:
                if e.tie.type =="start":
                    self.partituraTokens.append(self.dicVocabulario["liga_start"])
                if e.tie.type=="continue":
                    self.partituraTokens.append(self.dicVocabulario["liga_continue"])
                if e.tie.type=="stop":
                    self.partituraTokens.append(self.dicVocabulario["liga_stop"])
        elif isinstance(e,m21.note.Rest):
            self.partituraTokens.append(self.dicVocabulario["silencio"])
            self.partituraTokens.append(self.dicVocabulario[str(e.duration.quarterLength)])
        elif isinstance(e,m21.key.KeySignature):
            simbolo=str(e.sharps)
            # self.partituraTokens.append(self.dicVocabulario[simbolo])   
            self.infParte['tono']=self.dicVocabulario[simbolo] 
        elif isinstance(e, m21.meter.TimeSignature):      
            # self.partituraTokens.append(self.dicVocabulario[str(e.ratioString)])  
            self.infParte['compas']=self.dicVocabulario[str(e.ratioString)]
        elif  isinstance(e,m21.bar.Barline):
            if isinstance(e,m21.bar.Repeat):
                simbolo="b_repeticion_"+str(e.direction)
                self.partituraTokens.append(self.dicVocabulario[simbolo]) 
            else:
                if str(e.type)=="double":
                    tipobar="regular"
                else:
                    tipobar=str(e.type)
                simbolo="b_"+ tipobar
                self.partituraTokens.append(self.dicVocabulario[simbolo]) 
                if str(e.type)=="final":
                    self.partituraTokens.append(self.dicVocabulario["<stop>"])
                    self.allParteTokens[str(self.numero_de_part)]= self.partituraTokens
                    self.numero_de_part+=1
                    self.partituraTokens=[]
                    self.partituraTokens.append(self.dicVocabulario["<start>"])    
            
    def ver_barra_final(self,e):
        if  isinstance(e,m21.bar.Barline):
            if not isinstance(e,m21.bar.Repeat):
                if str(e.type)=="final":
                    return True
        return False
    
    
    def seleccionarLlavesRepet(self,measureNumero):
        for llave in self.llavesRepeticionList:
            if len(llave.getSpannedElements())==1:
                if llave.getSpannedElements()[0].measureNumber == measureNumero:
                    self.llaveSelect=llave
                    self.llaveNumberMeasure.append(llave.getSpannedElements()[0].measureNumber)              
            else:
                datos=llave.getSpannedElements()
                if measureNumero in range(datos[0].measureNumber,datos[1].measureNumber+1):  
                    self.llaveSelect=llave
                    self.llaveNumberMeasure.append(datos[0].measureNumber)
                    self.llaveNumberMeasure.append(datos[1].measureNumber)
                
                        
    def listaLlavesRepeticion(self,partFlat):
        corchetesRepeticion=[]
        for e in partFlat:
            try:
                if isinstance(e, m21.spanner.RepeatBracket): 
                    corchetesRepeticion.append(e)
            except:
                print(" Exepcion: " + str(e))   
        return corchetesRepeticion 
    
    
    def recolectar_ligas_slur(self,partFlat):
        listaLigaSlur=[]
        for e in partFlat:
            try:
                if isinstance(e, m21.spanner.Slur): 
                    listaLigaSlur.append(e)
            except:
                print(" Exepcion: " + str(e))   
        
        for li in partFlat:
            if isinstance(li, m21.note.Note):
                for slu in listaLigaSlur:
                    if li in slu:
                        elementsSlur=slu.getSpannedElements()
                        index=elementsSlur.index(li)
                        if index==0:
                            li.tie=m21.tie.Tie('start')
                            break
                        elif index+1 ==len(elementsSlur):
                            li.tie=m21.tie.Tie('stop')
                            break
                        else:
                            li.tie=m21.tie.Tie('continue')
                            break 
        
        return partFlat       
                    
        
    def cargarVocabulario(self,pathVocabulario):
        with open(pathVocabulario, "r") as fp:
            mappings = json.load(fp)
        return mappings
    

def juntarPartituras(pathPartEntrena):
    dataset={}
    for path, subdirs, files in os.walk(pathPartEntrena,topdown=False):
        print(path)
        
        for file_name in tqdm(files):
            claIn= GenArchivosNumpy(pathPartitura=os.path.join(path, file_name),pathVocabulario="datos/vocabulario/vocabulario2022.json",numero_de_part=len(dataset))
            nuevaPart= claIn.asignarTokensDePartituras()
            dataset={**dataset,**nuevaPart}   
    
        print(len(dataset)) 
        np.save("datos/archivos_numpy/dataSetCompleto.npy",dataset)     
                

def leerDesdeVariasCarpetas(pathPartEntrena):
    dataset={}
    for path, subdirs, files in os.walk(pathPartEntrena,topdown=False):
        nombreCarpeta = os.path.split(path)
        print("nombreCarpeta: "+str(nombreCarpeta[-1]))
        for file_name in tqdm(files):
            claIn= GenArchivosNumpy(pathPartitura=os.path.join(path, file_name),pathVocabulario="datos/vocabulario/vocabulario2022.json",numero_de_part=len(dataset))
            nuevaPart= claIn.asignarTokensDePartituras()
            dataset={**dataset,**nuevaPart} 
        print(len(dataset)) 
        np.save("datos/archivos_numpy/"+str(nombreCarpeta[-1])+".npy",dataset)
        dataset={}   
     
if __name__ == "__main__":
    # ejecutar para configurar las vista de imagenes de music21 con musescore
    # us = m21.environment.Environment()    
    # us['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'
    # us['musicxmlPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'
    # extracto_dos() vista rapida de la partitura
    #///////////////////////////////////////
    # saca una muestra de estraccion de una partitura
    # claIn= GenArchivosNumpy(pathPartitura="datos/t1.xml",pathVocabulario="datos/vocabulario/vocabulario2022.json",numero_de_part=0)
    # parte= claIn.asignarTokensDePartituras()
    # print(parte)
    
    # genera un archivo numpy con todas las partituras en la carpeta
    juntarPartituras("datos/partiturasEntrenamiento")
    #genera varios archivos numpy segun el genero divididos en carpetas
    # leerDesdeVariasCarpetas("datos/rutacarpeta")
    
   