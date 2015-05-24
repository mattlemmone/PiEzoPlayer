import RPi.GPIO as GPIO 
import collections, time

class Song:
    'Store tempo, notes'
    melody, timing = [], []

    def __init__(self, title):
      self.title = title

    def transpose(self, halfSteps):
        nbSz = len(noteBank) #notebank size
        
        for i, note in enumerate(self.melody): 
            oldOct = note[-1] 
            oldNote = note[:-1]
            oldInd = noteBank.index(oldNote)
            
            newInd = oldInd + halfSteps            
            newOct = int(oldOct) + newInd/nbSz
              
            newNote = noteBank[(newInd)%nbSz]
            newNO = newNote + str(newOct) #new note + octave
            
            print oldNote + oldOct + '->' + newNO
            
            self.melody[i] = newNote + str(newOct) #transpose
        return self

    def tempoMult(self, multiplier):
        nbSz = len(noteBank) #notebank size
        
        for i, t in enumerate(self.timing): 
            oldT = t
            newT = t / abs(multiplier)
            
            print str(oldT) + 's ->' + str(newT) +'s'
            
            self.timing[i] = newT
            
        return self
             
    def play(self):    
        
        time.sleep(1) #Prevent back-to-back chaining
        GPIO.cleanup() #Can never be too safe!
    
        print "Now Playing: " + self.title
        
        #Check for unsupported notes before playing
        for note in Song.melody:
            try:
                noteFrequency[note] #fix
            except KeyError:
                print "Unsupported note outside of octave range: " + note
                print "Permitted range: " + noteBank[0]+str(baseOctave) +":" +noteBank[0]+str(loopSize-1)
                print "Song exited."
                return
        
        #GPIO prep
        GPIO.setmode(GPIO.BOARD) #Because nobody likes .BCM
        GPIO.setup(15, GPIO.OUT) #PWM pin = 15
        p = GPIO.PWM(15, 90) #Set up pin
        GPIO.output(15, True) #Start producing sound
        p.start(80) #duty cycle @ 80%
        
        for i in range(len(self.melody)):  
            note = self.melody[i]
            freq = noteFrequency[note]
            duration = self.timing[i]
            
            print note +" @ "+str(duration) + 's'
            p.ChangeFrequency(freq) 
            time.sleep(duration)
        
        GPIO.cleanup()
        print "Song Fin."

#Global vars (calm down, its just a script)
noteFrequency = collections.OrderedDict() #note frequencies
noteBank = ["C", "C#","D","D#","E","F","F#","G", "G#", "A","A#","B"]
baseOctave, octaveRange = 2, 5
loopSize = octaveRange + baseOctave + 1
fMult =  1.059463
noteFrequency.update({"C2": 65.41}) #Lowest Note Supported

#Instantiate dictionary of frequencies starting with C(baseOctave) -> C(loopSize)
#Ex: baseOctave = 2, octaveRange = 4 -> C(2) -> C(6)
for j in range(baseOctave, loopSize):
    for i in range(0, len(noteBank)):
        if (j == 2 and i == 0): continue #Skip C(baseOctave)
        if (j == loopSize - 1 and i == 1): break #Exit after C(loopSize)
        
        if i == 0: curOctave = j - 1 #When thisNote = C and examining the last note from the previous octave
        else: curOctave = j #thisNote != C, don't look at previous octave
        
        lastNote = noteBank[i-1] + str(curOctave)
        thisNote = noteBank[i] + str(j)
        thisFreq = noteFrequency[lastNote] * fMult
        
        noteFrequency.update({thisNote: thisFreq}) #update list
    
bubBob = Song("Bubble Bobble")
bubBob.melody = [
    "E4", "F#4", "G#4", 
    "A4", "G#4", "F#4", 
    "E4", 
    "G#4", "F#4", "E4", "D4", 
    "F#4", "E4", "D4", "C#4", "E4"
    ]
bubBob.timing = [
    .23, .23, .23,
    .23, .23, .3,
    .17, 
    .23, .23, .2, .3,
    .23, .23, .13, .17, .4
    ]
    
rimShot = Song("I'm Not Funny")
rimShot.melody = [
    "A4", "A4", "A4", 
    "E4", "F#4", 
    "D4", 
    "D#5"
    ]
rimShot.timing = [
    .22, .22, .3,
    .15, .25, 
    .55,
    .4, 
    ]  
    
ff7 = Song("FF7 Victory")
ff7.melody = [
    "D4","D4","D4","D4",
    "A#3","C4",
    "D4","C4","D4",
    ]
ff7.timing = [
    .18, .18, .18, .4,
    .40, .40,
    .30, .15, .30
    ]  
    
zot = Song("Zelda - Owl Theme")
zot.melody = [
    "C4",
    "B3", "C4",
    "B3", "C4", "D4", "D#4", "F4", "G4", 
    "C4", 
    "G4", "C5",
    "A#4", "G#4", "G4", "F4", 
    "D#4", "D4", "C4", "B3", 
    "G3",
    
    "C4",
    "B3", "C4",
    "B3", "C4", "D4", "D#4", "F4", "G4", 
    "C4", 
    "F4", "G#4", "G4", "F4", "D#4", "D4", "D4", "C4", "C4"
]
zot.timing = [
    .35,
    .16, .4,
    .14, .14, .14, .14, .14, .2, 
    .32,
    .25, .25,
    .17, .14, .14, .14,
    .3, .14, .14, .3,
    .35,
    
    .35,
    .16, .4,
    .16, .14, .14, .14, .14, .23, 
    .33,
    .25, .23, .14, .14, .14, .14, .4, .14, .3
]

zot.play()
#bubBob.transpose(5).tempoMult(1.3).play()
#rimShot.play()
#ff7.transpose(3).play()
#ff7.transpose(5).tempoMult(1.6).play()