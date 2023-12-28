# import required module
from playsound import playsound
import threading
 
# play a sound file asyncrously
def play_async(filename):
    threading.Thread(target=playsound, args=(filename,)).start()

play_async("Meow.wav")
print('playing sound using  playsound')
