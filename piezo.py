import RPi.GPIO as GPIO 
import collections, time

class Song:
   'Store tempo, notes'
   melody = []
   timing = []

   def __init__(self, title):
      self.title = title
    
def playSong(Song):
    GPIO.cleanup()
    print "Now Playing: " + Song.title
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15, GPIO.OUT) 
    p = GPIO.PWM(15, 100)
    GPIO.output(15, True)  
    time.sleep(1)
    p.start(100)
    p.ChangeDutyCycle(90)
    for i in range(len(Song.melody)):  
        note = noteFrequency[Song.melody[i]]
        p.ChangeFrequency(note) 
        print Song.melody[i] +" @ "+str(Song.timing[i]) + 's'
        time.sleep(Song.timing[i])
    
    GPIO.cleanup()
    print "Song Fin."

#Global vars (calm down, its just a script)
noteFrequency = collections.OrderedDict() #note frequencies
notesNotRoot = ["C", "C#","D","D#","E","F","F#","G", "G#", "A","A#","B"]
octaveRange = 4
baseOctave = 2
loopSize = octaveRange + baseOctave + 1

noteFrequency.update({"C2": 65.41}) #Lowest Note

#Instantiate dictionary of frequencies starting with C(baseOctave) -> C(loopSize)
#Ex: baseOctave = 2, octaveRange = 4 -> C(2) -> C(6)
for j in range(baseOctave, loopSize):
    for i in range(0, len(notesNotRoot)):
        if (j == 2 and i == 0): continue #Skip C(baseOctave)
        if (j == loopSize - 1 and i == 1): break #Exit after C(loopSize)
        
        if i == 0: curOctave = j - 1 #When thisNote = C and examining the last note from the previous octave
        else: curOctave = j #thisNote != C, don't look at previous octave
        
        lastNote = notesNotRoot[i-1] + str(curOctave)
        thisNote = notesNotRoot[i] + str(j)
        thisFreq = noteFrequency[lastNote] * pow(2, 1.0/12.0)
        
        noteFrequency.update({thisNote: thisFreq}) #update list
    
bubBob = Song("Bubble Bobble")
bubBob.melody = [
    "E4", "F#4", "G#4", 
    "A4", "G#4", "F#4", 
    "E4", 
    "G#4", "F#4", "E4", "D4", 
    "F#4", "E4", "D4", "C#4", "E4"]
bubBob.timing = [
    .3, .3, .3,
    .3, .3, .4,
    .2, 
    .3, .3, .3, .4,
    .3, .3, .2, .25, .5
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
     
playSong(bubBob)
playSong(rimShot)