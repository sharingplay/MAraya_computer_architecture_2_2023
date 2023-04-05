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
        self.hitMiss = ""
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


    def updateCache(self,block,value,state): #validates the 2 way set in case a block needs to be changed
        #If the block is in the cache, just overwrite it
        if block in self.cache:
            self.cache[block] = value
            self.cacheStates[block] = state

        #determines in which block it should be writen in case there is no invalid block ******************
        else:
            set = int(block) % 2 #gets the set with a 2 way set logic
            if set == 0:
                block1 = self.getCacheStates()[0]
                block2 = self.getCacheStates()[1]
                if "I" in block1:


                for key, value in self.cacheStates.items():

                if block1 == "I":
                    self.cache[block] = self.cache.pop(block1)
                elif block1 == "S":

            else:
                block3 = self.getCacheStates()[2]
                block4 = self.getCacheStates()[3]


    def getCache(self):
        return self.cache

    def getCacheBlockValue(self,cacheBlock):
        return self.cache[cacheBlock]

    def getCacheStates(self):
        return self.cacheStates

    def getCacheState(self,cacheBlock):
        return self.cacheStates[cacheBlock]

    def getNumber(self):
        return self.number

    def setHitMiss(self,state):
        self.hitMiss = state

    def getHitMiss(self):
        return self.hitMiss

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
        self.boton1 = tk.Button(self.master, text= "boton1")
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

    def validateMOESI(self,instruction, listaProcesadores, memoria):
        processorNumber = int(instruction[0][-1])-1
        request = instruction[1]
        processorCacheValues = listaProcesadores[processorNumber].getCache()
        processorCacheStates = listaProcesadores[processorNumber].getCacheStates()

        #handles exceptions for instructions that are not a write
        try:
            address = instruction[2]
            value = instruction[3]
        except IndexError:
            address = ''
            value = ''

        if request == "READ":
            for key, value in processorCacheStates.items():  # checks the cache states to see if it has to go to memory
                print(f"Key {key} address: {address}")

                #checks is the address is in the cache of the processor
                if address == key:
                    if value == "M" or "S" or "E":
                        listaProcesadores[processorNumber].setHitMiss("Hit")
                        print("Se hace un read en cache")
                        print(f"valores cache: {processorCacheValues}")
                        print(f"estados cache: {processorCacheStates}")
                else:
                    listaProcesadores[processorNumber].setHitMiss("Miss")
                    print("Hay que leer los demas caches")

                    #Checks if the value is valid in other processors
                    for procesador in listaProcesadores:
                        if address in procesador.getCacheStates() and procesador.getCacheState(address) != "I":
                            #VALIDAR AQUI LOS DEMAS ESTADOS Y ACTUALIZAR EL CACHE **************
                            print(f"El procesador {processorNumber} tenia el dato que buscaba")
                        else:
                            print(f"El procesador {processorNumber} no tiene la direccion que quiere leer o es Invalida")

        #elif request == "WRITE":

        #else: #Calc request

        print("Validar MOESI")
        print(f"instruccion: {instruction}")
        print(f"procesadores: {listaProcesadores[0].getCache()}")
        print(f"memoria: {memoria}")


    # updates the window information
    def actualizar(self, lista_procesadores, memoria):
        def newOperationRandProcessor(): # selects a random processor to give a random instruction
            pNumber = random.randint(0, 3)
            print(f"se asigna instruccion al procesador {pNumber+1}\n")
            lista_procesadores[pNumber].getRandomInstruction()

            #calls the invalidation protocol
            self.validateMOESI(lista_procesadores[pNumber].getCurrentOperation(),lista_procesadores,memoria)


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