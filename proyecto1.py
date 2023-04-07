import threading
import tkinter as tk
from tkinter import ttk
import random
import secrets

class Memory:
    def __init__(self):
        self.blocks = {"000": "0xffff",
                       "001": "0xffff",
                       "010": "0xffff",
                       "011": "0xffff",
                       "100": "0xffff",
                       "101": "0xffff",
                       "110": "0xffff",
                       "111": "0xffff"}
        """
        self.blocks = {"000": "0x0000",
                       "001": "0x0045",
                       "010": "0x010a",
                       "011": "0x12af",
                       "100": "0x54ea",
                       "101": "0xe213",
                       "110": "0xffaa",
                       "111": "0xfeaa"}
        """
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
        self.cache = ["000","0x0000","I"],["010","0x0000","I"],["001","0x0000","I"], ["011","0x0000","I"]


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

            #checks the blocks of the specific set
            if set == 0:
                offset = 0
            else:
                offset = 2

            #Checks invalid blocks
            if "I" in self.cache[offset]:
                self.cache[offset][0] = address
                self.cache[offset][1] = value
                self.cache[offset][2] = state

            elif "I" in self.cache[offset+1]:
                self.cache[offset+1][0] = address
                self.cache[offset+1][1] = value
                self.cache[offset+1][2] = state

            # Checks shared blocks
            elif "S" in self.cache[offset]:
                self.cache[offset][0] = address
                self.cache[offset][1] = value
                self.cache[offset][2] = state

            elif "S" in self.cache[offset+1]:
                self.cache[offset+1][0] = address
                self.cache[offset+1][1] = value
                self.cache[offset+1][2] = state

            # Checks Owned blocks
            elif "O" in self.cache[offset]:
                self.cache[offset][0] = address
                self.cache[offset][1] = value
                self.cache[offset][2] = state

            elif "O" in self.cache[offset + 1]:
                self.cache[offset + 1][0] = address
                self.cache[offset + 1][1] = value
                self.cache[offset + 1][2] = state

            # Checks Exclusive blocks
            elif "E" in self.cache[offset]:
                self.cache[offset][0] = address
                self.cache[offset][1] = value
                self.cache[offset][2] = state

            elif "E" in self.cache[offset+1]:
                self.cache[offset+1][0] = address
                self.cache[offset+1][1] = value
                self.cache[offset+1][2] = state

            # Cheks Modified blocks
            elif "M" in self.cache[offset]:
                self.cache[offset][0] = address
                self.cache[offset][1] = value
                self.cache[offset][2] = state

            elif "M" in self.cache[offset+1]:
                self.cache[offset+1][0] = address
                self.cache[offset+1][1] = value
                self.cache[offset+1][2] = state

    def getCache(self):
        return self.cache

    def getCacheBlock(self,address):
        for block in self.cache:
            if address in block:
                return block


    def getNumber(self):
        return self.number

    def setHitMiss(self,state):
        self.hitMiss = state

    def getHitMiss(self):
        return self.hitMiss

    def invalidateCache(self,address):
        for block in self.cache:
            if address in block:
                block[2] = "I"

class Ventana:
    def __init__(self, master, modo):

        self.currentOperations = {1: "",
                                  2: "",
                                  3: "",
                                  4: ""}

        self.currentHitMiss = {1: "",
                               2: "",
                               3: "",
                               4: ""}

        self.inputOperation = ""

        self.pause = True
        self.lock = threading.Lock() #lock pause asset

        self.master = master
        self.modoActual = modo

        # establece el tamaño de la ventana
        self.master.geometry("900x550")

        # establece la posición de la ventana
        self.master.geometry("+{}+{}".format(350, 150))
        self.master.resizable(False, False)


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

        self.boton3 = tk.Button(self.master, text="new instruction", command = lambda: self.openInputWindow())
        self.boton3.grid(row=2, column=2, padx=10, pady=10)

        self.boton4 = tk.Button(self.master, text="Boton 4")
        self.boton4.grid(row=2, column=3, padx=10, pady=10)

    def openInputWindow(self):
        if self.pause == True:
            inputWindow = InputWindow()
            inputWindow.wait_window()

            print(f"Operacion desde la ventana {self.inputOperation}")

        else:
            print("No se puede ingresar una operacion si no esta pausada la ejecucion")

    def changePause(self):
        with self.lock: #adquire pause lock
            self.pause = not self.pause

    def updateProcessor(self,procesador):
        procesador.updateCache("100",str(secrets.token_hex(2)),random.choice(["M","S","O","I","E"]))

    # Determines what operation was done and applies MOESI
    def validateMOESI(self,instruction, processorList, memory):
        processorNumber = int(instruction[0][-1]) - 1
        request = instruction[1]
        print(f"Instruccion: {instruction}")
        try:
            address = instruction[2]

        except IndexError:
            address = ""
        try:
            value = instruction[3]
        except IndexError:
            value = ""

        print(instruction)
        if request == "READ":
            print(f"Se quiere hacer un read del P{processorNumber+1}")
            self.readMOESI(processorList,memory, processorNumber, address)

        elif request == "WRITE":
            print(f"Se quiere hacer un write del P{processorNumber + 1}")
            self.writeMOESI(processorList,memory,processorNumber,address,value)
        else:
            print(f"El P{processorNumber + 1} hace un calc")

    #checks if the data is in the processor cache
    def readMOESI(self, processorList, memory, processorNumber, address):
        if address in processorList[processorNumber].getCache():
            for block in processorList[processorNumber].getCache():
                # If it has a valid data value, reads it
                if block[0] == address:
                    if block[2] != "I":
                        processorList[processorNumber].setHitMiss("Hit")
                        processorList[processorNumber].addNewLog(f"Es un Hit y se lee {address} del mismo procesador y mantiene el valor {block[1]}")
                        return
                    else:
                        processorList[processorNumber].setHitMiss("Miss")
                        processorList[processorNumber].addNewLog(f"Es un Miss porque {address} es un dato invalido")
                        self.readMOESIProcessors(processorList, memory, processorNumber, address)
        else:
            processorList[processorNumber].setHitMiss("Miss")
            processorList[processorNumber].addNewLog(f"Es un Miss porque {address} no esta en cache")
            self.readMOESIProcessors(processorList, memory, processorNumber, address)

    def readMOESIProcessors(self,processorList,memory,processorNumber,address):
        for processor in processorList:
            if address in processor.getCache():
                for block in processor.getCache():
                    if block[0] == address:
                        # Read the cache of a processor with valid state
                        if block[2] != "I":
                            # Updates the cache of both processors
                            if block[2] == "S" or "O":
                                processorList[processorNumber].updateCache(block[0],block[1],"S")
                                processorList[processorNumber].addNewLog(f"El P{processor.getNumber()} tiene el dato y se lee {address} con un valor {block[1]}")
                                return

                            elif block[2] == "M":
                                processorList[processorNumber].updateCache(block[0], block[1], "S")
                                processor.updateCache(block[0],block[1],"O")
                                processorList[processorNumber].addNewLog(f"El P{processor.getNumber()} tiene el dato y se lee {address} con un valor {block[1]}")
                                processor.addNewLog(f"El P{processorNumber} leyo {address} con un valor {block[1]}, se cambia el estado de M a O")
                                return

                            elif block[2] == "E":
                                processorList[processorNumber].updateCache(block[0], block[1], "S")
                                processor.updateCache(block[0],block[1],"S")
                                processorList[processorNumber].addNewLog(f"El P{processor.getNumber()} tiene el dato y se lee {address} con un valor {block[1]}")
                                processor.addNewLog(f"El P{processorNumber} leyo {address} con un valor {block[1]}, se cambia el estado de E a S")
                                return

        processorList[processorNumber].setHitMiss("Miss")
        processorList[processorNumber].addNewLog(f"Es un Miss porque ningun procesador tiene el dato en un estado valido")
        self.readMOESIMemory(processorList, memory, processorNumber, address)
        print("Ningun procesador tiene el dato valido, se va a leer de memoria")

    def readMOESIMemory(self,processorList, memory, processorNumber, address):
        memoryReadData = memory.getMemBlock(address)
        processorList[processorNumber].updateCache(address,memoryReadData,"E")
        processorList[processorNumber].addNewLog(f"El P{processorNumber} leyo {address} de memoria con un valor de {memoryReadData}, se cambia el estado a E")
        print("Leyo memoria")

    def writeMOESI(self, processorList, memory, processorNumber, address, value):

        if address in processorList[processorNumber].getCache():
            #if its in cache the address is a hit
            processorList[processorNumber].setHitMiss("Hit")
            for block in processorList[processorNumber].getCache():
                # If it has the address, writes on it
                if block[0] == address:
                    # If its invalid
                    if block[2] == "I":
                        processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} reemplazando {block[1]} "
                                                                 f"y se cambia la I por una M")
                        # Invalidates the other caches with the same address
                        for processsor in processorList:
                            if processsor.getNumber() != processorNumber:
                                processsor.invalidateCache(address)

                    elif block[2] == "E":
                        # Only this processor had the old memory value
                        processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} reemplazando {block[1]}"
                                                                 f" y se cambia la E por una M")

                    elif block[2] == "S":
                        processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} reemplazando {block[1]} "
                                                                 f"y se cambia la S por una M")
                        # Invalidates the other caches with the same address
                        for processsor in processorList:
                            if processsor.getNumber() != processorNumber:
                                processsor.invalidateCache(address)
                        return

                    #if its modified or owned
                    elif block[2] == "M" or "O":
                        # old value to store in memory
                        cacheToStore = processorList[processorNumber].getCacheBlock(address)
                        memory.updateMemBlock(cacheToStore[0], cacheToStore[1])
                        processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} "
                                                                 f"y se guarda en memoria el valor anterior {cacheToStore[1]}")

                        # invalidates the rest of the processors with the same address
                        for processsor in processorList:
                            if processsor.getNumber() != processorNumber:
                                processsor.invalidateCache(address)

                    # Writes the value on the cache
                    processorList[processorNumber].updateCache(address, value, "M")
                    return
        # If the processor doesn't have the address
        else:
            for block in processorList[processorNumber].getCache():

                if block[2] == "I":
                    processorList[processorNumber].addNewLog(f"Se escribe en {block[0]} el valor {value} reemplazando {block} "
                        f"y se cambia la I por una M")
                    # Invalidates the other caches with the same address
                    for processsor in processorList:
                        if processsor.getNumber() != processorNumber:
                            processsor.invalidateCache(address)

                elif block[2] == "S":
                    processorList[processorNumber].addNewLog(f"Se escribe en {block[1]} el valor {value} reemplazando {block} "
                        f"y se cambia la S por una M")
                    # Invalidates the other caches with the same address
                    for processsor in processorList:
                        if processsor.getNumber() != processorNumber:
                            processsor.invalidateCache(address)

                elif block[2] == "E":
                    # Only this processor had the old memory value
                    processorList[processorNumber].addNewLog(f"Se escribe en {block[1]} el valor {value} reemplazando {block}"
                        f" y se cambia la E por una M")
                    # if its modified or owned

                elif block[2] == "M" or "O":
                    # old value to store in memory
                    cacheToStore = processorList[processorNumber].getCacheBlock(block[1])
                    memory.updateMemBlock(cacheToStore[0], cacheToStore[1])
                    processorList[processorNumber].addNewLog(f"Se escribe en {block[1]} el valor {value} "
                                                             f", se guarda en memoria el valor anterior {cacheToStore[1]} "
                                                             f"y se pone una M como estado")

                    # invalidates the rest of the processors with the same address
                    for processsor in processorList:
                        if processsor.getNumber() != processorNumber:
                            processsor.invalidateCache(address)
                #updates the cache
                processorList[processorNumber].updateCache(block[1], value, "M")

    # updates the window information
    def actualizar(self, lista_procesadores, memoria):
        def newOperationRandProcessor(): # selects a random processor to give a random instruction
            pNumber = random.randint(0, 3)
            print(f"se asigna instruccion al procesador {pNumber+1}\n")
            lista_procesadores[pNumber].getRandomInstruction()

            #calls the invalidation protocol
            self.validateMOESI(lista_procesadores[pNumber].getCurrentOperation(), lista_procesadores, memoria)


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
                    self.currentHitMiss[i+1] = procesador.getHitMiss()

                # Writes the actions done by the processors
                self.text_box_info.delete(1.0,tk.END)
                for key, value in self.currentOperations.items():  #Cache values
                    self.text_box_info.insert(tk.END, f"Processor {key} action:\n{value}\n{self.currentHitMiss[key]}\n")

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


class InputWindow(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.title("Instruction Input")
        self.geometry("275x175")
        self.resizable(False, False)

        self.result = ""

        self.processorNumber = tk.StringVar(self)
        self.operation = tk.StringVar(self)
        self.address = tk.StringVar(self)
        self.value = tk.StringVar(self)

        # Processor number input label
        first_label = ttk.Label(self, text="Processor Number:", padding=(5,5))
        first_label.grid(row=0, column=0)
        self.first_combobox = ttk.Combobox(self, values=["P1", "P2", "P3", "P4"], textvariable=self.processorNumber)
        self.first_combobox.grid(row=0, column=1)

        # Instruction input label
        second_label = ttk.Label(self, text="Instruction:",padding=(5,5))
        second_label.grid(row=1, column=0)
        self.second_combobox = ttk.Combobox(self, values=["READ", "WRITE", "CALC"], textvariable=self.operation)
        self.second_combobox.grid(row=1, column=1)
        self.second_combobox.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Address input label
        third_label = ttk.Label(self, text="address:", padding=(5,5))
        third_label.grid(row=2, column=0)
        self.third_combobox = ttk.Combobox(self, values=["000", "001", "010", "011", "100", "101", "110", "111"], textvariable=self.address)
        self.third_combobox.grid(row=2, column=1)

        # Value input label
        fourth_label = ttk.Label(self, text="Hex value:", padding=(5,5))
        fourth_label.grid(row=3, column=0)
        self.fourth_entry = ttk.Entry(self, textvariable=self.value)
        self.fourth_entry.grid(row=3, column=1)

        # Botón para guardar los datos ingresados y cerrar la ventana
        save_button = ttk.Button(self, text="Guardar", command=self.save_data, padding=(0,5))
        save_button.grid(row=4, column=0)

        # Botón para cancelar y cerrar la ventana
        cancel_button = ttk.Button(self, text="Cancelar", command=self.destroy, padding=(5,5))
        cancel_button.grid(row=4, column=1)

        # Centrar la ventana en la pantalla
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def save_data(self):
        # Returns input data
        number = self.processorNumber.get()
        instruction = self.operation.get()
        address = self.address.get()
        value = self.value.get()

        self.result = [number,instruction,address,value]

        if self.result[1] == "READ":
            self.result.pop()
        elif self.result[1] == "CALC":
            del self.result[-2:]

        self.master.inputOperation = self.result
        print(f"Resultado desde el input window {self.result}")
        self.destroy()

    def update_input_fields(self, event):
        # Si la opción "CALC" está seleccionada, desactiva los campos de entrada de dirección y valor
        if self.operation.get() == "CALC":
            self.third_combobox.state(["disabled"])
            self.fourth_entry.state(["disabled"])

        elif self.operation.get() == "READ":
            self.fourth_entry.state(["disabled"])
            self.third_combobox.state(["!disabled"])

        else:
            self.third_combobox.state(["!disabled"])
            self.fourth_entry.state(["!disabled"])

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

    p1.updateCache("001", "0x1fa2", "I")
    p1.updateCache("010", "0xfae2", "M")
    p1.updateCache("011", "0x1234", "E")
    p1.updateCache("100", "0xf2e3", "S")

    p2.updateCache("001", "0x1023", "S")
    p2.updateCache("010", "0xaaaa", "I")
    p2.updateCache("101", "0x4321", "E")
    p2.updateCache("100", "0xf2e3", "S")

    p3.updateCache("001", "0x1023", "S")
    p3.updateCache("010", "0xaaaa", "I")
    p3.updateCache("011", "0xef23", "M")
    p3.updateCache("100", "0xf2e3", "S")

    p4.updateCache("001", "0x1023", "O")
    p4.updateCache("110", "0xfae2", "S")
    p4.updateCache("101", "0x1023", "I")
    p4.updateCache("111", "0x1023", "I")

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