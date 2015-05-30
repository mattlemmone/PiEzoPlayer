# PiEzoPlayer
Using a Raspberry Pi, create songs in a tedious format that reflect pre-polyphonic ringtones and 8-bit bliss.

Frequency calculations are approximated. 

Formula as provided by my EEL4523 Audio Engineering class, and can be found on the web.
![](http://puu.sh/hZf6a/0f1ff08f3a.png)

### Circuit
![](http://puu.sh/i6lOj/cfded08350.png)

The circuit is simply using BOARD pin 15 (not BCM) as a square wave generator through pulse width modulation (PWM). The wave varies between HIGH and LOW, 3.3V & 0V.

### Example
A good example of usage is included. The 'zot' song object.

Keep melodies and timings with spacings that are easy to follow along with to facilitate song creation.

```
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
```

To play the song: 
>zot.play()

To transpose the song:
>zot.transpose(n)
Where n is an integer. n>0 will transpose your song n halfsteps sharper.

Change the tempo:
>zot.tempoMultiplier(n)
Where n is a float. n>0 will make all notes play n times faster.

These methods can be chained as well:
>zot.tempoMultiplier(m).transpose(n).play()

### To do
* ~~Correct Frequency Calculation~~
* Port to Arduino for analog functionality and manipulation of multiple waveform types.
* Analyze freq. peaks from microphone to determine timing and/or notes. This would allow for mic -> piezo song creation.
