# TODO
# Use different color walls for each generated room
# Speed

from tkinter import *
from Generator import Generator
from Raycast import *

WORLD_WIDTH = 40
WORLD_HEIGHT = 20

if __name__ == '__main__':
    print('Generating level...')
    gen = Generator()
    gen.Initialise(WORLD_WIDTH, WORLD_HEIGHT)
    gen.Run()
    gen.Draw()

    world = gen.getWorld();

    window = Tk()
    window.title('Raycast')
    window.resizable(0, 0)

    canvas = Canvas(window, width=Raycast.SCREEN_WIDTH, height = Raycast.SCREEN_HEIGHT, background = 'black')
    canvas.pack()

    raycast = Raycast(world, canvas)

    window.after(0, raycast.render())
    window.bind('<Key>', lambda x: raycast.keypress(x))
    
    # sustain
    window.mainloop()