import threading
import tkinter as tk
import random
import secrets

class Memory:
    def __init__(self):
        self.blocks = {"000": "0x0000",
                       "001": "0x0000",
                       "010": "0x0000",
                       "011": "0x0000",
                       "100": "0x0000",
                       "101": "0x0000",
                       "110": "0x0000",
                       "111": "0x0000"}

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
        #address, value, state
        self.cache = ["000","0x0000","I"],["001","0x0000","I"],["010","0x0000","I"], ["011","0x0000","I"]


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

    def addNewLog(self,log):
        self.logs += "\n"+log

    def getCurrentOperation(self):
        return self.currentOperation



    def updateCache(self,address,value,state): #validates the 2 way set in case a block needs to be changed
        #If the block is in the cache, just overwrite it
        for i, block in enumerate(self.cache):
            if self.cache[i][0] == address:
                self.cache[i][1] = value
                self.cache[i][2] = state
                return

        #determines in which block it should be writen in case there is no invalid block
        else:
            set = int(address) % 2 #gets the set with a 2 way set logic
            # gets the address of the blocks in set 0
            print(f"Cache viejo: {self.cache}")

            #checks the blocks of the specific set
            if set == 0:
                offset = 0
            else:
                offset = 2

            for i in range(0+offset,2+offset):
                # Checks invalid blocks
                if "I" in self.cache[i]:
                    self.cache[i] = [address,value,state]
                    return
                # Checks shared blocks
                elif "S" in self.cache[i]:
                    self.cache[i] = [address,value,state]
                    return
                # Checks Exclusive blocks
                elif "E" in self.cache[i]:
                    self.cache[i] = [address, value, state]
                    return
                # Checks Owned blocks
                elif "O" in self.cache[i]:
                    self.cache[i] = [address,value,state]
                    return
                #C CHeks Modified blocks
                elif "M" in self.cache[i]:
                    self.cache[i] = [address,value,state]
                    return


    def getCache(self):
        return self.cache

    def getCacheBlockValue(self,cacheBlock):
        return self.cache[cacheBlock]

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

    """def validateMOESI(self,instruction, listaProcesadores, memoria):
        processorNumber = int(instruction[0][-1])-1
        request = instruction[1]
        processorCache = listaProcesadores[processorNumber].getCache()
        print(f"Cache del procesador: {processorCache}")

        #handles exceptions for instructions that are not a write
        try:
            address = instruction[2]
            value = instruction[3]
        except IndexError:
            address = ''
            value = ''

        def readMOESI():
            for bloque in processorCache:  # checks the cache states to see if it has to go to memory
                print(f"Revisando bloque de cache: {bloque}")

                #checks is the address is in the cache of the processor
                if address in bloque:
                    if bloque[2] == "M" or "S" or "E":
                        listaProcesadores[processorNumber].setHitMiss("Hit")
                        listaProcesadores[processorNumber].addNewLog(f"El valor de {bloque[0]} estaba en cache y se volvio a leer")
                        print("Se hace un read en cache")

        if request == "READ":
            for bloque in processorCache:  # checks the cache states to see if it has to go to memory
                print(f"Revisando bloque de cache: {bloque}")

                #checks is the address is in the cache of the processor
                if address in bloque:
                    if bloque[2] == "M" or "S" or "E":
                        listaProcesadores[processorNumber].setHitMiss("Hit")
                        listaProcesadores[processorNumber].addNewLog(f"El valor de {bloque[0]} estaba en cache y se volvio a leer")
                        print("Se hace un read en cache")


                else:
                    listaProcesadores[processorNumber].setHitMiss("Miss")
                    listaProcesadores[processorNumber].addNewLog(f"Hubo Miss, no se encontro el valor en el cache de P{processorNumber}")
                    print("Hay que leer los demas caches")

                    #Checks if the value is valid in other processors
                    for procesador in listaProcesadores:
                        if address in procesador.getCacheStates() and procesador.getCacheState(address) != "I":
                            if procesador.getCacheState(address) == "E":
                                # Updates state of the processor to S
                                listaProcesadores[processorNumber].updateCache(address,procesador.getCacheBlockValue(address),"S")
                                print(f"El procesador {processorNumber} tenia el dato que buscaba y estaba en E")

                                #Updates E state to S of the processor that was read
                                procesador.updateCache(address,procesador.getCacheBlockValue(address), "S")
                                procesador.addNewLog(f"El P{processorNumber} leyo la direccion {address} de "
                                                     f"P{procesador.getNumber()}y se cambio de E a S")


                            elif procesador.getCacheState(address) == "M":
                                # Updates state of the processor to S
                                listaProcesadores[processorNumber].updateCache(address,procesador.getCacheBlockValue(address),"S")
                                print(f"El procesador {processorNumber} tenia el dato que buscaba y estaba en M")

                                # Updates M state to O of the processor that was read
                                procesador.updateCache(address, procesador.getCacheBlockValue(address), "M")
                                procesador.addNewLog(f"El P{processorNumber} leyo la direccion {address} de "
                                                     f"P {procesador.getNumber()}y se cambio de M a O")


                            else: # Case where the state was S or O stays the same
                                listaProcesadores[processorNumber].updateCache(address,procesador.getCacheBlockValue(address),"S")
                                listaProcesadores[processorNumber].addNewLog(f"Se leyo el dato del P{procesador.getNumber()}")

                        else:
                            print(f"El procesador {processorNumber} no tiene la direccion que quiere leer o es Invalida")
                    #Buscar en memoria el dato***************************
                    print("No esta en cache el dato hay que ir a buscarlo a memoria")

        #elif request == "WRITE":

        #else: #Calc request"""
    # updates the window information
    def actualizar(self, lista_procesadores, memoria):
        def newOperationRandProcessor(): # selects a random processor to give a random instruction
            pNumber = random.randint(0, 3)
            print(f"se asigna instruccion al procesador {pNumber+1}\n")
            lista_procesadores[pNumber].getRandomInstruction()

            #calls the invalidation protocol
            #self.validateMOESI(lista_procesadores[pNumber].getCurrentOperation(),lista_procesadores,memoria)


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

                    # Clean the text box
                    textBox.delete(1.0, tk.END)

                    # Updates cache values for each processor
                    textBox.tag_configure("center", justify="center",font=("Helvetica", 12, "bold"))
                    textBox.insert('end', f"Cache of processor {lista_procesadores[i].getNumber()}:\n","center")

                    for bloque in procesador.getCache(): #Cache values
                        textBox.insert('end', f"{bloque[0]}: {bloque[1]} \n")

                    # Updates cache states for each processor
                    textBox.tag_configure("center", justify="center",font=("Helvetica", 12, "bold"))
                    textBox.insert('end', f"State of the cache blocks:\n","center")

                    for bloque in procesador.getCache(): #Cache states
                        textBox.insert('end', f"{bloque[0]}: {bloque[2]}\n")

                    # Keeps the operations done by the processors updated
                    self.currentOperations[i+1] = procesador.getCurrentOperation()

                # Writes the actions done by the processors
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

    p1.updateCache("000","0x0123","M")
    p2.updateCache("000","0x1abc","I")
    p3.updateCache("000","0x2ca4","S")
    p4.updateCache("000","0xf102","O")

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