from yaspin import yaspin
from time import sleep


def start_spiner(message:str, time:float=0.5): # Starts the spiner and send a message for a time
    print("")
    spiner = yaspin(text=message)
    spiner.start()
    if(time):
        sleep(time)
    spiner.stop()

def success_message(message:str, time:float=0.5): # Uses the start_spiner function and send a marked text
    start_spiner(message=message, time=time)
    text_marker(message)


def fail_message(message:str, time:float=0.5): # Uses the start_spiner function and send a marked text
    start_spiner(message=message, time=time)
    text_marker(message, icon="-")


def text_marker(text:str, icon:str="="): # Makes a marker for a text
    text_lenght = len(text)+(len(text)//2)

    print("")
    print(f"{icon}"*text_lenght)
    print(text.center(text_lenght))
    print(f"{icon}"*text_lenght)
    print("")
