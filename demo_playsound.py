#!!!!!!!!!!!
# non-block call not working
# use winsound instead

# import required module
from playsound import playsound
import threading
 
# play a sound file asyncrously
def play_async(filename):
    threading.Thread(target=playsound, args=(filename,)).start()


# second call not working:(
play_async("Meow.wav")

# non-blocking not working:(
playsound("Meow.wav", False)

print('playing sound using  playsound')
