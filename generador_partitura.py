
import json
from music21 import *
import music21 as m21
from IPython.display import Image, Audio,display
partitura=[   51, 47, 40, 112, 4, 116, 6, 116, 4, 19, 116, 4, 21, 116, 6, 114, 4, 116, 6, 114, 6, 116, 4, 114, 4, 116,
           4, 118, 4, 119, 9, 26, 6, 111, 4, 114, 6, 114, 4, 19, 114, 4, 21, 114, 6, 116, 4, 114, 7, 109, 4, 111, 4, 109, 
           4, 108, 4, 111, 4, 109, 8, 26, 8, 30, 29, 109, 4, 112, 6, 112, 4, 19, 112, 4, 21, 112, 6, 111, 4, 112, 6, 111,
           6, 112, 4, 111, 4, 112, 4, 114, 4, 116, 9, 26, 6, 111, 4, 114, 6, 114, 4, 19, 114, 4, 21, 114, 6, 116, 4, 114, 
           7, 111, 4, 111, 4, 109, 4, 108, 4, 111, 4, 22, 27, 109, 9, 26, 6, 30, 23, 27, 24, 109, 7, 116, 4, 19, 116, 4, 21,
           116, 6, 114, 4, 29, 116, 4, 116, 6, 114, 4, 116, 7, 114, 4, 116, 9, 26, 6, 27, 25, 111, 4, 114, 6, 114, 4, 19, 114,
           4, 21, 114, 6, 116, 4, 114, 7, 111, 4, 111, 4, 109, 4, 108, 4, 111, 4, 22, 27, 109, 7, 116, 4, 19, 116, 4, 21, 116, 
           6, 114, 4, 30, 23, 27, 24, 109, 6, 109, 6, 109, 4, 107, 4, 104, 6, 27, 25, 29, 26, 8, 116, 4, 116, 4, 114, 4, 116, 4,
           119, 9, 26, 6, 114, 4, 116, 4, 119, 4, 114, 4, 116, 4, 119, 4, 114, 4, 112, 4, 109, 9, 26, 6, 109, 4, 112, 6, 112, 4, 
           19, 112, 4, 21, 112, 6, 111, 4, 112, 6, 111, 6, 112, 4, 111, 4, 112, 4, 114, 4, 116, 9, 26, 6, 111, 4, 114, 6, 114, 4, 
           19, 114, 4, 21, 114, 6, 116, 4, 114, 7, 111, 4, 111, 4, 109, 4, 108, 4, 111, 4, 22, 27, 109, 9, 26, 6, 30, 23, 27, 24, 
           109, 6, 109, 6, 109, 4, 107, 4, 104, 6, 28, 25, ]

partitura1=[51,47,42,110,4,114,6,114,4,19,114,4,21,114,6,112,4,114,6,112,6,114,4,112,4,114,4,116,4,117,9,26,6,109,4,112,6,112,4
            ,19,112,4,21,112,6,114,4,112,7,107,4,109,4,107,4,106,4,109,4,107,8,26,8,30,29,107,4,110,6,110,4,19,110,4,21,110,6,109,4
            ,110,6,109,6,110,4,109,4,110,4,112,4,114,9,26,6,109,4,112,6,112,4,19,112,4,21,112,6,114,4,112,7,109,4,109,4,107,4,106,4
            ,109,4,22,27,107,9,26,6,30,23,27,24,107,7,114,4,19,114,4,21,114,6,112,4,29,114,4,114,6,112,4,114,7,112,4,114,9,26,6,27,
            25,109,4,112,6,112,4,19,112,4,21,112,6,114,4,112,7,109,4,109,4,107,4,106,4,109,4,22,27,107,7,114,4,19,114,4,21,114,6,112
            ,4,30,23,27,24,107,6,107,6,107,4,105,4,102,6,27,25,29,26,8,114,4,114,4,112,4,114,4,117,9,26,6,112,4,114,4,117,4,112,4,114,
            4,117,4,112,4,110,4,107,9,26,6,107,4,110,6,110,4,19,110,4,21,110,6,109,4,110,6,109,6,110,4,109,4,110,4,112,4,114,9,26,6,109
            ,4,112,6,112,4,19,112,4,21,112,6,114,4,112,7,109,4,109,4,107,4,106,4,109,4,22,27,107,9,26,6,30,23,27,24,107,6,107,6,107,4,105,4,102,6,28,25, ]


def show(music):
    display(Image(str(music.write('lily.png'))))



def cargarVocabulario(pathVocabulario):
    with open(pathVocabulario, "r") as fp:
        mappings = json.load(fp)
    return mappings


def cargarVocabularioInverso(pathVocabulario):
    with open(pathVocabulario, "r") as fp:
        mappings = json.load(fp)
    return mappings



  
def graficarPartitura2(notas,titulo,vocabReves):
  score = stream.Score()
  partStream = stream.Part()
  score.insert(0, metadata.Metadata())
  listaLLaves={}
  acumLlaves=[]
  acumulador=[]
  for i in range(0,len(notas)):
    acumNotas=None
    notaNumero=int(notas[i])
    notaLetra=str(notas[i])
    if notaNumero in range(31,45+1):
      song_key = key.Key(key.sharpsToPitch(int(vocabReves[notaLetra]))) #asigna el numero de # o bemol
      partStream.insert(0, song_key)
      # song_key.octave = 4 # moverse hasta la 4ta octava alrededor del C central
      score.metadata.title = titulo+" %s" % song_key.name
    if notaNumero in range(46,50+1):
      partStream.append(meter.TimeSignature(vocabReves[notaLetra]))#asigna el compas 2/4
    if notaNumero in range(58,145+1):
      if int(notas[i+1])in range(3,18+1) or int(notas[i+1])in range(53,56+1):
        
        if i+2<len(notas) and  int(notas[i+2]) in [19,20,21] :
          if int(notas[i+1])in range(53,56+1):
            nota=vocabReves[str(notas[i+1])]
            numerador=int(nota[0])
            denominador=int(nota[-1])
            acumNotas=note.Note(int(vocabReves[notaLetra]),quarterLength=numerador/denominador)
          else:
            acumNotas=note.Note(int(vocabReves[notaLetra]),quarterLength=float(vocabReves[str(notas[i+1])]))
          if int(notas[i+2]) ==19:
            acumNotas.tie=tie.Tie('start')
          elif int(notas[i+2]) ==20:
            acumNotas.tie=tie.Tie('continue')
          if int(notas[i+2]) ==21:
            acumNotas.tie=tie.Tie('stop')
          
        else:
          if int(notas[i+1])in range(53,56+1):
            nota=vocabReves[str(notas[i+1])]
            numerador=int(nota[0])
            denominador=int(nota[-1])
            acumNotas=note.Note(int(vocabReves[notaLetra]),quarterLength=numerador/denominador)
          else:
            acumNotas=note.Note(int(vocabReves[notaLetra]),quarterLength=float(vocabReves[str(notas[i+1])]))
          
    if notaNumero==26:
      if int(notas[i+1]) in range(3,18+1):
        acumNotas=note.Rest(quarterLength=float(vocabReves[str(notas[i+1])]))
   
    if acumNotas != None:
      # measure.append(acumNotas)
      acumulador.append(acumNotas)
    
    
    

    if notas[i]==27:
      acumulador.append(bar.Barline(type='regular'))
    if notas[i]==28:
      acumulador.append(bar.Barline(type='final'))
    if notas[i]==29:
      acumulador.append(bar.Repeat(direction='start'))
    if notas[i]==30:
      acumulador.append(bar.Repeat(direction='end'))
   
    if notas[i-1] ==22:       
      acumLlaves.append(acumulador[-1]) 
    elif notas[i] ==23:
      acumLlaves.append(acumulador[-1])
      listaLLaves["llave_"+str(len(listaLLaves))+"_1"]=acumLlaves
      acumLlaves=[]
    if notas[i-1] ==24:       
      acumLlaves.append(acumulador[-1])
    elif notas[i] ==25:
      acumLlaves.append(acumulador[-1])
      listaLLaves["llave_"+str(len(listaLLaves))+"_2"]=acumLlaves
      acumLlaves=[]
      
  barras=[]
  partStream.append(acumulador)
  # partStream.show('text')
  for  e in partStream:
    if isinstance(e,m21.bar.Barline):
      barras.append(e)
                  
  partStream.makeMeasures(inPlace=True)

  part2=partStream.elements
  for compas in part2:
    # print(compas)
    # print(compas.offset)
    for bara in barras:
      if compas.offset ==bara.offset:
        if isinstance(bara,m21.bar.Repeat):
          if "start"== bara.direction:
            compas.leftBarline=bara
          else:
            num=compas.measureNumber
            for i in part2:
              if i.measureNumber == num-1:
                i.rightBarline=bara
        else:
          compas.append(bara)
  recComp=[]
  listaBrakets=[]        
  for compas in part2:
    for lave in listaLLaves:
      if listaLLaves[lave][0] in compas:
        recComp.append(compas)
        break
      if listaLLaves[lave][1] in compas:
        recComp.append(compas)
        if lave[-1]=="1":
          listaBrakets.append(spanner.RepeatBracket(recComp, number=1))
        else:
          listaBrakets.append(spanner.RepeatBracket(recComp, number=2))
        recComp=[]
        break
      elif isinstance(listaLLaves[lave][1],m21.bar.Barline)and isinstance(compas[-1],m21.bar.Barline) and len(recComp)>0:  
        if lave[-1]=="2":
          recComp.append(compas)
          listaBrakets.append(spanner.RepeatBracket(recComp, number=2))
          recComp=[]
          break
          
  for lis in listaBrakets:
    part2[0].insert(0.0, lis)
      
  score.append(part2)
  
  # score.show('text')
  score.show('musicxml.png')
 


if __name__ == "__main__":
    user_settings = m21.environment.UserSettings()
     # ejecutar para configurar las vista de imagenes de music21 con musescore
    # user_settings["lilypondPath"] = "C:/Program Files (x86)/LilyPond/usr/bin/lilypond.exe"
    # user_settings['showFormat'] = "lilypond" 
    # user_settings["musescoreDirectPNGPath"] = "C:/Program Files/MuseScore 3/bin/MuseScore3.exe"
    # music21.environment.set("musescoreDirectPNGPath", "C:/Program Files/MuseScore 3/bin/MuseScore3.exe")
    # user_settings.create()
    vocabReves= cargarVocabularioInverso('datos/vocabulario/vocabulario_inverso_2022.json')
    # introducionedo una lista de tokens de partituras genera una imagen de partitura
    graficarPartitura2(partitura,"Tono Actual",vocabReves)
    graficarPartitura2(partitura1,"Nuevo Tono",vocabReves)