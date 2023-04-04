import threading
import tkinter as tk
import random
import secrets


class Memory:
    def __init__(self):
        self.blocks = {"000": 0,
                       "001": 0,
                       "010": 0,
                       "011": 0,
                       "100": 0,
                       "101": 0,
                       "110": 0,
                       "111": 0}

    def updateMemBlock(self,block, value):
        self.blocks[block] = value

    def getMemBlock(self,block):
        return self.blocks[block]

    def getMemBlocks(self):
        return self.blocks
class Processor:
    def __init__(self, number):
        self.logs = "" #registers every action the processor has done
        self.number = number
        self.currentOperation = []
        self.cache = {"000": 0,
                      "001": 0,
                      "010": 0,
                      "011": 0}
        self.cacheStates = {"000": 'I',
                            "001": 'I',
                            "010": 'I',
                            "011": 'I'}

    # assigns possible instructions to a processor
    def getRandomInstruction(self):
        def randomHex():  # return a random hex number of 16 bits or 4 bytes
            return secrets.token_hex(2)

        def randomBin():  # returns random binary of 3 digits
            random.seed()
            return bin(random.getrandbits(3))[2:].zfill(3)

        # random number to get probability
        randomNumber = random.uniform(0.1,1)

        # 30% chance of getting a write instruction
        if randomNumber < 0.3:
            # return the processor number, the block number in binary and the hex value to write
            self.currentOperation = ["P" + str(self.number),"WRITE",randomBin(),randomHex()]
            self.logs += "\n" + str(self.currentOperation)
            print(self.logs)
        # 40% chance of getting a read instruction
        elif randomNumber < 0.7:
            # return the processor number and the block that is going to read
            self.currentOperation = ["P" + str(self.number),"READ",randomBin()]
            self.logs += "\n" + str(self.currentOperation)
            print(self.logs)
        # 30% chance of getting a calc instruction
        else:
            self.currentOperation = ["P" + str(self.number),"CALC"]
            self.logs += "\n" + str(self.currentOperation)
            print(self.logs)


    def getlogs(self):
        return self.logs

    def getCurrentOperation(self):
        return self.currentOperation

    def updateCache(self,cacheBlock,value,state):
        self.cache[cacheBlock] = value
        self.cacheStates[cacheBlock] = state

    def getCache(self):
        return self.cache

    def getCacheBlock(self,cacheBlock):
        return self.cache[cacheBlock]

    def getCacheStates(self):
        return self.cacheStates

    def getCacheState(self,cacheBlock):
        return self.cacheStates[cacheBlock]

    def getNumber(self):
        return self.number

class Ventana:
    def __init__(self, master, modo):
        self.currentOperations = {1: "",
                                  2: "",
                                  3: "",
                                  4: ""}
        self.pause = False
        self.lock = threading.Lock() #lock pause asset

        self.master = master
        self.modoActual = modo

        # creates 4 text boxes for the processors
        self.text_box1 = tk.Text(self.master, height=11, width=30)
        self.text_box1.grid(row=0, column=0, padx=10, pady=10)

        self.text_box2 = tk.Text(self.master, height=11, width=30)
        self.text_box2.grid(row=0, column=1, padx=10, pady=10)

        self.text_box3 = tk.Text(self.master, height=11, width=30)
        self.text_box3.grid(row=1, column=0, padx=10, pady=10)

        self.text_box4 = tk.Text(self.master, height=11, width=30)
        self.text_box4.grid(row=1, column=1, padx=10, pady=10)

        # creates a text box to display the memory data
        self.text_box_memory = tk.Text(self.master, height=15, width=30)
        self.text_box_memory.grid(row=0, column=2, padx=10, pady=10)

        # creates a text box for information on processor states
        self.text_box_info = tk.Text(self.master, height=12, width=30)
        self.text_box_info.grid(row=1, column=2, padx=10, pady=10)

        # creates the buttons
        self.boton1 = tk.Button(self.master, text= "p1")
        self.boton1.grid(row=2, column=0, padx=10, pady=10)

        self.boton_pause = tk.Button(self.master, text="pausa", command=lambda: self.changePause())
        self.boton_pause.grid(row=2, column=1, padx=10, pady=10)

        self.boton3 = tk.Button(self.master, text="Boton 3")
        self.boton3.grid(row=2, column=2, padx=10, pady=10)

        self.boton4 = tk.Button(self.master, text="Boton 4")
        self.boton4.grid(row=2, column=3, padx=10, pady=10)

    def changePause(self):
        with self.lock: #adquire pause lock
            self.pause = not self.pause

    # updates the window information
    def actualizar(self, lista_procesadores, memoria):
        def newOperationRandProcessor(): # selects a random processor to give a random instruction
            pNumber = random.randint(0, 3)
            lista_procesadores[pNumber].getRandomInstruction()
            print(f"se asigna instruccion al procesador {pNumber+1}\n")

        with self.lock:
            if self.pause == False:
                newOperationRandProcessor()
                print("Se actualiza")
                #Iterates processors text boxes
                for i, procesador in enumerate(lista_procesadores):
                    if i == 0:
                        textBox = self.text_box1
                    elif i == 1:
                        textBox = self.text_box2
                    elif i == 2:
                        textBox = self.text_box3
                    elif i == 3:
                        textBox = self.text_box4

                    #Clean the text box
                    textBox.delete(1.0, tk.END)

                    #Updates cache data for each processor
                    textBox.tag_configure("center", justify="center",font=("Helvetica", 12, "bold"))
                    textBox.insert('end', f"Cache of processor {lista_procesadores[i].getNumber()}:\n","center")
                    for key,value in procesador.getCache().items(): #Cache values
                        textBox.insert('end', f"{key}: {value}\n")

                    textBox.tag_configure("center", justify="center",font=("Helvetica", 12, "bold"))
                    textBox.insert('end', f"State of the cache blocks:\n","center")
                    for key,value in lista_procesadores[i].getCacheStates().items(): #Cache states
                        textBox.insert('end', f"{key}: {value}\n")

                    #Keeps the operations done by the processors updated
                    self.currentOperations[i+1] = procesador.getCurrentOperation()

                #Writes the actions done by the processors
                self.text_box_info.delete(1.0,tk.END)
                for key, value in self.currentOperations.items():  #Cache values
                    self.text_box_info.insert(tk.END, f"Processor {key} action:\n{value}\n\n")

                #Updates the memory on screen
                self.text_box_memory.delete(1.0, tk.END)
                self.text_box_memory.tag_configure("center", justify="center", font=("Helvetica", 12, "bold"))
                self.text_box_memory.insert(tk.END, "Shared Memory Blocks:\n","center")
                for key, value in memoria.getMemBlocks().items():  # Cache values
                    self.text_box_memory.insert(tk.END, f"Block {key} value:{value}\n\n")
            else:
                print("Esta pausado")
                return


    def continuousUpdate(self, lista_procesadores, memoria,modo):
        # llama al método actualizar cada 2 segundos
        if modo == 1:
            lista_procesadores[0].getRandomInstruction()
            self.actualizar(lista_procesadores,memoria)
            self.master.after(2000, lambda: self.continuousUpdate(lista_procesadores, memoria,modo))
            # inicia el bucle de eventos
            self.master.mainloop()

        #agregar el cambio a paso a paso***************************************** con un else


def main():
    #validates execution mode
    """
    try:
        mode = int(input("Seleccion el modo de ejecucion inicial:\n1)Ejecucion continua\n2)Ejecucion paso a paso\n"))
    except ValueError:
        print("El valor ingresado no es un entero")
    """
    modo = 1
    #Creates a memory
    mem = Memory()

    #Create processors
    p1 = Processor(1)
    p2 = Processor(2)
    p3 = Processor(3)
    p4 = Processor(4)

    #Processors list
    processors = [p1,p2,p3,p4]

    #Creates display window
    root = tk.Tk()
    root.title("Protocolo MOESI para coherencia de cache en sistemas multiprocesador")
    ventana = Ventana(root,modo)


    #Updates display window
    if modo == 1:
        ventana.continuousUpdate(processors,mem,modo)

    elif modo == 2:
        #ventana.stepUpdate(processors,mem)
        print("modo step")


    # ejecuta la ventana
    root.mainloop()

if __name__ == "__main__":
    main()