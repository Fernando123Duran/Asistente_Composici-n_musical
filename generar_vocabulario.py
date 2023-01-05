import json
def crear_vocabulario():
    otrosSignos=["<pad>","<start>","<stop>","0.125","0.25","0.375","0.5","0.75","1.0","1.5","2.0",
                 "2.25","2.5","2.75","3.0","3.25","3.5","3.75","4.0","liga_start","liga_continue","liga_stop",
                 "corchetRep1_start","corchetRep1_stop","corchetRep2_start","corchetRep2_stop",
                 "silencio","b_regular","b_final","b_repeticion_start","b_repeticion_end",
                 "1","2","3","4","5","6","7","-1","-2","-3","-4","-5","-6","-7","0",
                 "2/2","2/4","2/8","6/8","3/4","clave_G_2","clave_F_4","1/3","2/3","1/12","1/6","4/4"]
    mappings={}
    for i,te in enumerate(otrosSignos):
        mappings[te] = i
        
    midi=21
    
    for index in range(len(mappings),len(mappings)+88):
        mappings[midi]=index
        midi+=1
    
    with open("datos/vocabulario/vocabulario2022.json", "w") as fp:
        json.dump(mappings, fp, indent=4)
    
    vocaRev = { i:str(ch) for i,ch in enumerate(mappings) }
    with open("datos/vocabulario/vocabulario_inverso_2022.json", "w") as fp:
        json.dump(vocaRev, fp, indent=4)
        
def generarVocabularioMIDI():
    nombres=["DO","DO#_LAb","RE","RE#_MIb","MI","FA","FA#_SOLb","SOL","SOL#_LAb","LA","LA#_SIb","SI"]
    octava=0
    nombresIndex=0
    controlOctava=24
    midi={}
    for i in range(12,127+1):
        if i <controlOctava:
            midi[i]=nombres[nombresIndex]+" "+str(octava)
            nombresIndex+=1
            if len(nombres)==nombresIndex:
                nombresIndex=0
        elif i==controlOctava:
            octava=octava+1
            midi[i]=nombres[nombresIndex]+" "+str(octava)
            nombresIndex+=1
            if len(nombres)==nombresIndex:
                nombresIndex=0
            controlOctava=controlOctava+12
    with open("datos/vocabulario/vocabularioMIDI.json", "w") as fp:
        json.dump(midi, fp, indent=4)
if __name__ == "__main__":
    # crear_vocabulario()
    # genera un vocabulario con las notaciones necesarias para la extraccion de caracteristicas de las partituras
    generarVocabularioMIDI()