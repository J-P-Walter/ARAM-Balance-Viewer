import tkinter as tk
import time
class GUI():
    def __init__(self, name, damageDealt, damageReceived, otherEffects):

        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.minsize(200,400)

        for i in range(4):
            self.window.grid_rowconfigure(i, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.nameLabel = tk.Label(text=name)
        self.damageDealtLabel = tk.Label(text=damageDealt)
        self.damageReceivedLabel = tk.Label(text=damageReceived)
        self.otherEffectsLabel = tk.Label(text=otherEffects, justify='center', wraplength=100)

        self.nameLabel.grid(row=0, column=0)
        self.damageDealtLabel.grid(row=1, column=0)
        self.damageReceivedLabel.grid(row=2, column=0)
        self.otherEffectsLabel.grid(row=3, column=0)
        
    
    def updateData(self, name, damageDealt, damageReceived, otherEffects):
        self.nameLabel.config(text=name)
        self.window.update()
        # self.damageDealtLabel.config(text=damageDealt)
        # self.damageReceivedLabel.config(text=damageReceived)
        # self.otherEffectsLabel.config(text=otherEffects)
    
    # def startGUI(self):
    #     self.window.mainloop()
        return
    # def stopGUI(self):
    #     self.window.destroy()

test = GUI("", "", "", "")
# test.startGUI()
test.updateData("Aatrox", "5%", "-5%", "Tenacity increased by 20%.")
# test.stopGUI()
time.sleep(1)
# test.startGUI()
# time.sleep(2)
# test.stopGUI()
# window = tk.Tk()
# # window.geometry('200x200')
# window.resizable(False, False)
# window.minsize(200,400)
# # window.maxsize(200,400)
# # window.columnconfigure(0, minsize=100)
# # window.rowconfigure([0, 4], weight=1, minsize=500)
# for i in range(4):
#     window.grid_rowconfigure(i, weight=1)
# window.grid_columnconfigure(0, weight=1)

# name = tk.Label(text="Aatrox")
# damageDealt = tk.Label(text="+5%")
# damageReceived = tk.Label(text="+5%")
# otherEffects = tk.Label(text="Ability haste increased by 20. \nTotal attack speed increased by 2.5%. \n Arise!\n\nAzir will start the game with one point already ranked in Arise!, allowing him to allocate the other two to his other abilities.", justify='center', wraplength=100)

# name.grid(row=0, column=0)
# damageDealt.grid(row=1, column=0)
# damageReceived.grid(row=2, column=0)
# otherEffects.grid(row=3, column=0)

# def moveWindow(event):
#     window.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

# window.bind('<B1-Motion>', moveWindow)

# window.mainloop()

