import threading
import tkinter as tk
from tkinter import ttk
import random
import secrets
import re
import tkinter.messagebox as messagebox

class Memory:
    def __init__(self):
        self.blocks = {"000": 0x0000,
                        "001": 0x1234,
                        "010": 0x8732,
                        "011": 0xabcd,
                        "100": 0xffaa,
                        "101": 0xacfa,
                        "110": 0x1045,
                        "111": 0x5682}
        """
        self.blocks = {
                        "000": 0x0000,
                        "001": 0x1234,
                        "010": 0x8732,
                        "011": 0xabcd,
                        "100": 0xffaa,
                        "101": 0xacfa,
                        "110": 0x1045,
                        "111": 0x5682
                        
                        "000": 0x0000,
                       "001": 0x0000,
                       "010": 0x0000,
                       "011": 0x0000,
                       "100": 0x0000,
                       "101": 0x0000,
                       "110": 0x0000,
                       "111": 0x0000
                       
                       }
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
        self.cache = ["000",0x0000,"I"],["010",0x0000,"I"],["001",0x0000,"I"], ["011",0x0000,"I"]


    # assigns possible instructions to a processor
    def getRandomInstruction(self):
        def randomHex():  # return a random hex number of 16 bits or 4 bytes
            return secrets.token_hex(2)

        def randomBin():  # returns random binary of 3 digits
            random.seed()
            return bin(random.getrandbits(3))[2:].zfill(3)

        # random number to get probability
        randomNumber = random.uniform(0,1)

        # 33% chance of getting a write instruction
        if randomNumber <= 0.3:
            # return the processor number, the block number in binary and the hex value to write
            self.currentOperation = ["P" + str(self.number),"WRITE",randomBin(),randomHex()]
            self.logs += "\n" + str(self.currentOperation)
        # 33% chance of getting a read instruction
        elif randomNumber > 0.3 and randomNumber <= 0.6:
            # return the processor number and the block that is going to read
            self.currentOperation = ["P" + str(self.number),"READ",randomBin()]
            self.logs += "\n" + str(self.currentOperation)
        # 33% chance of getting a calc instruction
        elif randomNumber > 0.6 and randomNumber <= 1:
            self.currentOperation = ["P" + str(self.number),"CALC"]
            self.logs += "\n" + str(self.currentOperation)



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

            #checks the blocks of the specific set
            if set == 0:
                offset = 0
            else:
                offset = 2
            #["E","I","S","M","O"]
            #Checks invalid blocks
            # Checks Exclusive blocks
            if "E" in self.cache[offset]:
                self.cache[offset][0] = address
                self.cache[offset][1] = value
                self.cache[offset][2] = state

            elif "E" in self.cache[offset+1]:
                self.cache[offset+1][0] = address
                self.cache[offset+1][1] = value
                self.cache[offset+1][2] = state

            elif "I" in self.cache[offset]:
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

            # Cheks Modified blocks
            elif "M" in self.cache[offset]:
                self.cache[offset][0] = address
                self.cache[offset][1] = value
                self.cache[offset][2] = state

            elif "M" in self.cache[offset+1]:
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

class Ventana:
    def __init__(self, master, modo):
        self.currentOperations = {1: "", 2: "", 3: "", 4: ""}
        self.currentHitMiss = {1: "", 2: "", 3: "", 4: ""}

        # input window attributes
        self.inputOperation = ""
        self.processorNumber = tk.StringVar()
        self.operation = tk.StringVar()
        self.address = tk.StringVar()
        self.value = tk.StringVar()

        # pause attributes
        self.pause = True
        self.lock = threading.Lock() #lock pause asset

        # window settings
        self.master = master
        self.modoActual = modo
        self.master.geometry("1100x550+200+150")
        self.master.resizable(False, False)

        # creates 4 text boxes for the processors
        self.text_box1 = tk.Text(self.master, height=11, width=25)
        self.text_box1.grid(row=0, column=0, padx=10, pady=10)

        self.text_box2 = tk.Text(self.master, height=11, width=25)
        self.text_box2.grid(row=0, column=1, padx=10, pady=10)

        self.text_box3 = tk.Text(self.master, height=11, width=25)
        self.text_box3.grid(row=1, column=0, padx=10, pady=10)

        self.text_box4 = tk.Text(self.master, height=11, width=25)
        self.text_box4.grid(row=1, column=1, padx=10, pady=10)

        # creates a text box to display the memory data
        self.text_box_memory = tk.Text(self.master, height=17, width=30)
        self.text_box_memory.grid(row=0, column=2, padx=10, pady=10)

        # creates a text box for information on processor states
        self.text_box_info = tk.Text(self.master, height=12, width=30)
        self.text_box_info.grid(row=1, column=2, padx=10, pady=10)

        # creates a text box for processors last logs
        self.processorsLogs = tk.Text(self.master, height=15, width=45)
        self.processorsLogs.place(x = 715, y = 275)

        # creates the buttons
        self.boton_pause = tk.Button(self.master, text="pausa", command=lambda: self.changePause())
        self.boton_pause.place(x = 900, y = 205)


        # Processor number input label and option box
        self.pNumberLabel = ttk.Label(self.master, text="Processor Number:", padding=(5, 5))
        self.pNumberLabel.place(x=800, y=10)
        self.pNumber_combobox = ttk.Combobox(self.master, values=["P1", "P2", "P3", "P4"], textvariable=self.processorNumber, state = 'disabled')
        self.pNumber_combobox.place(x = 925, y =15)

        # Instruction input label and option box
        self.instructionLabel = ttk.Label(self.master, text="Instruction:", padding=(5, 5))
        self.instructionLabel.place(x= 840, y=60)
        self.instruction_combobox = ttk.Combobox(self.master, values=["READ", "WRITE", "CALC"], textvariable=self.operation, state = 'disabled')
        self.instruction_combobox.place(x = 925, y = 65)
        self.instruction_combobox.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Address input label and option box
        self.addressLabel = ttk.Label(self.master, text="Address:", padding=(5, 5))
        self.addressLabel.place(x = 853, y = 110)
        self.address_combobox = ttk.Combobox(self.master, values=["000", "001", "010", "011", "100", "101", "110", "111"],
                                           textvariable=self.address, state = 'disabled')
        self.address_combobox.place(x = 925, y = 115)

        # Value input label
        self.hex_label = ttk.Label(self.master, text="Hex value:", padding=(5, 5))
        self.hex_label.place(x = 842, y = 160)
        self.hex_entry = ttk.Entry(self.master, textvariable=self.value, state = 'disabled')
        self.hex_entry.place(x=932, y=165)

        # button to store values and call the instruction
        self.save_button = ttk.Button(self.master, text="Guardar", command=self.save_data, padding=(0, 5), state = 'disabled')
        self.save_button.place(x = 955, y = 200)


    def save_data(self):
        # Returns input data
        number = self.processorNumber.get()
        instruction = self.operation.get()
        address = self.address.get()
        value = self.value.get()

        if instruction == "WRITE":
            if not re.match(r'^[0-9a-fA-F]+$', value, re.IGNORECASE):
                tk.messagebox.showerror("Error", "El valor introducido no es hexadecimal")
                return

        self.inputOperation = [number, instruction, address, value]

        if self.inputOperation[1] == "READ":
            self.inputOperation.pop()
        elif self.inputOperation[1] == "CALC":
            del self.inputOperation[-2:]


    def update_input_fields(self, event):
        # Si la opción "CALC" está seleccionada, desactiva los campos de entrada de dirección y valor
        selected_instruction = self.instruction_combobox.get()
        if selected_instruction == "CALC":
            self.address_combobox.state(["disabled"])
            self.hex_entry.state(["disabled"])

        elif selected_instruction == "READ":
            self.hex_entry.state(["disabled"])
            self.address_combobox.state(["!disabled"])

        else:
            self.address_combobox.state(["!disabled"])
            self.hex_entry.state(["!disabled"])

    def changePause(self):
        with self.lock: #adquire pause lock
            self.pause = not self.pause
        if self.pause == True:
            self.save_button.configure(state = 'normal')
            self.pNumber_combobox.configure(state='normal')
            self.instruction_combobox.configure(state='normal')
            self.address_combobox.configure(state='normal')
            self.save_button.configure(state='normal')
            self.hex_entry.configure(state='normal')
            self.modoActual = 2
        else:
            self.save_button.configure(state='disabled')
            self.pNumber_combobox.configure(state='disabled')
            self.instruction_combobox.configure(state='disabled')
            self.address_combobox.configure(state='disabled')
            self.save_button.configure(state='disabled')
            self.hex_entry.configure(state='disabled')
            self.modoActual = 1

    def validateSet(self, address):
        set = int(address) % 2
        if set == 0:
            return 0
        else:
            return 2

    # Determines what operation was done and applies MOESI
    def validateMOESI(self,instruction, processorList, memory):
        processorNumber = int(instruction[0][-1]) - 1
        request = instruction[1]
        processorList[processorNumber].currentOperation = instruction
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
            self.master.after(3000, print(f"Se quiere hacer un read del P{processorNumber+1}"))
            self.readMOESI(processorList,memory, processorNumber, address)

        elif request == "WRITE":
            self.master.after(5000,print(f"Se quiere hacer un write del P{processorNumber + 1}") )
            self.writeMOESI(processorList,memory,processorNumber,address,value)

        else:
            self.calcMOESI(processorList, processorNumber)

    def calcMOESI(self, processorList, processorNumber):
        simulatedTime = random.choice([3000, 2000, 1000])
        self.master.after(simulatedTime, print(f"El P{processorNumber + 1} va a realizar un CALC"), processorList, processorNumber)
        processorList[processorNumber].addNewLog(f"El P{processorNumber + 1} realizo un CALC durante {str(simulatedTime)[0]} segundos")

    #checks if the data is in the processor cache
    def readMOESI(self, processorList, memory, processorNumber, address):
        processorCache = processorList[processorNumber].getCache()

        for block in processorCache:
            # If it has a valid data value, reads it
            if block[0] == address:
                if block[2] != "I":
                    processorList[processorNumber].setHitMiss("Cache Read Hit")
                    processorList[processorNumber].addNewLog(f"Es un Hit y se lee {address} del mismo procesador y mantiene el valor {hex(block[1])}")
                    return
                else:
                    processorList[processorNumber].setHitMiss("Cahe Read Miss (invalid)")
                    processorList[processorNumber].addNewLog(f"Es un Miss porque {address} es un dato invalido")
                    self.readMOESIProcessors(processorList, memory, processorNumber, address)
                    return
        else:
            processorList[processorNumber].setHitMiss("Cahe Read Miss (not in cache)")
            processorList[processorNumber].addNewLog(f"Es un Miss porque {address} no esta en cache")
            print((f"Es un Miss porque {address} no esta en cache"))
            self.readMOESIProcessors(processorList, memory, processorNumber, address)

    def readMOESIProcessors(self,processorList,memory,processorNumber,address):
        for processor in processorList:
            processorCache = processor.getCache()
            for block in processorCache:
                if block[0] == address:
                    # Read the cache of a processor with valid state
                    if block[2] != "I":
                        # Updates the cache of both processors
                        if block[2] == "S":
                            processorList[processorNumber].updateCache(block[0],block[1],"S")
                            processorList[processorNumber].addNewLog(f"El P{processor.getNumber()} tiene el dato y se lee {address} con un valor {hex(block[1])}")
                            processor.addNewLog(f"El P{processorNumber + 1} leyo {address} con un valor {hex(block[1])}, se mantiene el estado en S")
                            return

                        elif block[2] == "O":
                            processorList[processorNumber].updateCache(block[0],block[1],"S")
                            processorList[processorNumber].addNewLog(f"El P{processor.getNumber()} tiene el dato y se lee {address} con un valor {hex(block[1])}")
                            processor.updateCache(block[0],block[1],"S")
                            processor.addNewLog(f"El P{processorNumber + 1} leyo {address} con un valor {hex(block[1])}, se cambia el estado de O a S")
                            return

                        elif block[2] == "M":
                            processorList[processorNumber].updateCache(block[0], block[1], "S")
                            processor.updateCache(block[0],block[1],"O")
                            processorList[processorNumber].addNewLog(f"El P{processor.getNumber()} tiene el dato y se lee {address} con un valor {hex(block[1])}")
                            processor.addNewLog(f"El P{processorNumber + 1} leyo {address} con un valor {hex(block[1])}, se cambia el estado de M a O")
                            return

                        elif block[2] == "E":
                            processorList[processorNumber].updateCache(block[0], block[1], "S")
                            processor.updateCache(block[0],block[1],"S")
                            processorList[processorNumber].addNewLog(f"El P{processor.getNumber()} tiene el dato y se lee {address} con un valor {hex(block[1])}")
                            processor.addNewLog(f"El P{processorNumber + 1} leyo {address} con un valor {hex(block[1])}, se cambia el estado de E a S")
                            return

        processorList[processorNumber].addNewLog("Ningun procesador tiene el dato en un estado valido de lectura")
        self.readMOESIMemory(processorList, memory, processorNumber, address)
        print("Es un Miss porque ningun procesador tiene el dato en un estado valido de lectura")

    def readMOESIMemory(self,processorList, memory, processorNumber, address):
        memoryReadData = memory.getMemBlock(address)
        processorList[processorNumber].updateCache(address,memoryReadData,"E")
        processorList[processorNumber].addNewLog(f"El P{processorNumber + 1} leyo {address} de memoria con un valor de {hex(memoryReadData)}, se cambia el estado a E")


    def writeMOESI(self, processorList, memory, processorNumber, address, value):

        # Processor that is going to be invalidated, address to invalidate and the processor that caused the invalidation
        def invalidateCache(processorToInvalidate, address, processorModified):
            pNumberInvalidates = processorModified.getNumber()

            for block in processorToInvalidate.getCache():
                # In case the invalidation has to be done in the cache of the processor that called it
                if address in block:
                    oldValue = processorToInvalidate.getCacheBlock(address)[1]
                    if block[2] == "E":
                        processorToInvalidate.addNewLog(f"Se cambia el estado en {address} de E a I porque P{pNumberInvalidates}"
                                                        f" lo modifico")

                    elif block[2] == "I":
                        processorToInvalidate.addNewLog(f"Se mantiene el estado en {address} en I porque P{pNumberInvalidates}"
                                                        f" lo modifico")

                    elif block[2] == "S":
                        processorToInvalidate.addNewLog(f"Se cambia el estado de en {address} de S a I porque P{pNumberInvalidates}"
                                                        f" lo modifico")

                    # Invalidates the cache and stores the old value on memory if the old staste was Modified
                    elif block[2] == "M":
                        processorToInvalidate.addNewLog(f"Se cambia el estado en {address} de M a I porque P{pNumberInvalidates}"
                                                        f" lo modifico, pero antes se guarda {oldValue} en memoria")
                        memory.updateMemBlock(block[0], block[1])


                    # Invalidates the cache and stores the old value on memory if the old staste was Owned
                    elif block[2] == "O":
                        processorToInvalidate.addNewLog(f"Se cambia el estado en {address} de O a I porque P{pNumberInvalidates}"
                                                        f" lo modifico, pero antes se guarda {oldValue} en memoria")
                        memory.updateMemBlock(block[0], block[1])

                    block[2] = "I"



        processorCache = processorList[processorNumber].getCache()

        # If it has the address, writes on it and sets a Hit
        for block in processorCache:
            if block[0] == address:
                processorList[processorNumber].setHitMiss("Write Hit")
                # If its invalid
                if block[2] == "I":
                    processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} reemplazando {hex(block[1])} "
                                                             f"y se cambia la I por una M")
                    # Invalidates the other caches with the same address
                    for processor in processorList:
                        if processor.getNumber() != processorNumber + 1:
                            invalidateCache(processor, address, processorList[processorNumber])

                elif block[2] == "E":
                    # Only this processor had the old memory value
                    processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} reemplazando {hex(block[1])}"
                                                             f" y se cambia la E por una M")

                elif block[2] == "S":
                    processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} reemplazando {hex(block[1])} "
                                                             f"y se cambia la S por una M")
                    # Invalidates the other caches with the same address
                    for processor in processorList:
                        if processor.getNumber() != processorNumber + 1:
                            invalidateCache(processor, address, processorList[processorNumber])

                # if its modified
                elif block[2] == "M":
                    processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} y se guarda en memoria el valor anterior {hex(block[1])}")
                    # invalidates the rest of the processors with the same address
                    memory.updateMemBlock(block[0],block[1])
                    for processor in processorList:
                        if processor.getNumber() != processorNumber + 1:
                            invalidateCache(processor, address, processorList[processorNumber])

                # if its owned
                elif block[2] == "O":
                    processorList[processorNumber].addNewLog(f"Se escribe en {address} el valor {value} y se guarda en memoria el valor anterior {hex(block[1])}")
                    # invalidates the rest of the processors with the same address
                    memory.updateMemBlock(block[0], block[1])
                    for processor in processorList:
                        if processor.getNumber() != processorNumber + 1:
                            invalidateCache(processor, address, processorList[processorNumber])

                # Writes the value on the cache
                processorList[processorNumber].updateCache(address, value, "M")
                return

        # If the processor doesn't have the address
        else:
            processorList[processorNumber].setHitMiss("Write Miss")
            set = self.validateSet(address)
            priorityOrder = ["E","I","S","M","O"]
            for letter in priorityOrder:
                for block in processorList[processorNumber].getCache()[set:set+2]:
                    if letter in block:
                        if letter == "E":
                            processorList[processorNumber].addNewLog(f"Se escribe en {block[0]} el valor {value} reemplazando {block}, se cambia E por M")
                            for processor in processorList:
                                if processor.getNumber() != processorNumber:
                                    invalidateCache(processor, address, processorList[processorNumber])
                            break
                        elif letter == "I" or "S":
                            processorList[processorNumber].addNewLog(f"Se escribe en {block[0]} el valor {value} reemplazando {block}, se cambia {letter} por M")
                            for processor in processorList:
                                if processor.getNumber() == processorNumber:
                                    invalidateCache(processor, address, processorList[processorNumber])
                            break
                        elif letter == "O" or "M":
                            processorList[processorNumber].addNewLog(f"Se escribe en {block[0]} el valor {value} reemplazando {block}, "
                                                                     f"se cambia {letter} por M y se guarda en memoria {hex(block[1])}")
                            for processor in processorList:
                                invalidateCache(processor, address, processorList[processorNumber])
                            break

                    break
            processorList[processorNumber].updateCache(address, value, "M")
            return

    # updates the window information
    def actualizar(self, lista_procesadores, memoria):
        def newOperationRandProcessor(): # selects a random processor to give a random instruction
            pNumber = random.randint(0, 3)
            print(f"se asigna instruccion al procesador {pNumber+1}\n")
            lista_procesadores[pNumber].getRandomInstruction()

            #calls the invalidation protocol
            self.validateMOESI(lista_procesadores[pNumber].getCurrentOperation(), lista_procesadores, memoria)

        def updateWindow():
            # Iterates processors text boxes
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
                textBox.tag_configure("center", justify="center", font=("Helvetica", 12, "bold"))
                textBox.insert('end', f"Cache of processor {lista_procesadores[i].getNumber()}:\n", "center")

                for bloque in procesador.getCache():  # Cache values
                    try:
                        value = int(bloque[1],16)
                        hexValue = hex(value)
                        textBox.insert('end', f"{bloque[0]}: {hexValue} \n")
                    except:
                        textBox.insert('end', f"{bloque[0]}: {hex(bloque[1])} \n")

                # Updates cache states for each processor
                textBox.tag_configure("center", justify="center", font=("Helvetica", 12, "bold"))
                textBox.insert('end', f"State of the cache blocks:\n", "center")

                for bloque in procesador.getCache():  # Cache states
                    textBox.insert('end', f"{bloque[0]}: {bloque[2]}\n")

                # Keeps the operations done by the processors updated
                self.currentOperations[i + 1] = procesador.getCurrentOperation()
                self.currentHitMiss[i + 1] = procesador.getHitMiss()

                # Writes the actions done by the processors
                self.text_box_info.delete(1.0, tk.END)
                for key, value in self.currentOperations.items():  # Cache values
                    self.text_box_info.insert(tk.END, f"Processor {key} action:\n{value}\n{self.currentHitMiss[key]}\n")

                # Updates the memory on screen
                self.text_box_memory.delete(1.0, tk.END)
                self.text_box_memory.tag_configure("center", justify="center", font=("Helvetica", 12, "bold"))
                self.text_box_memory.insert(tk.END, "Shared Memory Blocks:\n", "center")
                for key, value in memoria.getMemBlocks().items():  # Cache values
                    self.text_box_memory.insert(tk.END, f"Block {key} value:{hex(value)}\n\n")

                # Updates last processors logs on screen
                self.processorsLogs.delete(1.0, tk.END)
                self.processorsLogs.tag_configure("center", justify="center", font=("Helvetica", 12, "bold"))
                self.processorsLogs.insert(tk.END, "Processors Logs:\n", "center")
                for processor in lista_procesadores:
                    logs = processor.getlogs().split('\n')
                    lastLog = str(logs[-1])
                    self.processorsLogs.insert(tk.END, f"P{processor.getNumber()}:{lastLog}\n\n")

        with self.lock:
            if self.pause == False:
                newOperationRandProcessor()
                updateWindow()
                return

            else:
                if self.inputOperation != "":
                    self.validateMOESI(self.inputOperation, lista_procesadores, memoria)
                    self.inputOperation = ""
                    updateWindow()
                    return

    def continuousUpdate(self, lista_procesadores, memoria,modo):
        # llama al método actualizar cada 2 segundos
        if modo == 1:
            self.actualizar(lista_procesadores,memoria)
            self.master.after(3000, lambda: self.continuousUpdate(lista_procesadores, memoria,modo))

def main():
    modo = 1
    #Creates a memory
    mem = Memory()

    #Create processors
    p1 = Processor(1)
    p2 = Processor(2)
    p3 = Processor(3)
    p4 = Processor(4)

    p1.updateCache("000", 0x1fa2, "I")
    p1.updateCache("010", 0xfae2, "M")
    p1.updateCache("001", 0x1234, "E")
    p1.updateCache("011", 0xf2e3, "I")

    p2.updateCache("000", 0x1023, "S")
    p2.updateCache("110", 0xaaaa, "M")
    p2.updateCache("101", 0x4321, "O")
    p2.updateCache("111", 0xef23, "S")

    p3.updateCache("000", 0x1023, "S")
    p3.updateCache("100", 0xaaaa, "I")
    p3.updateCache("111", 0xef23, "O")
    p3.updateCache("101", 0x4321, "S")

    p4.updateCache("000", 0x1023, "O")
    p4.updateCache("010", 0x12ab, "I")
    p4.updateCache("111", 0xef23, "S")
    p4.updateCache("101", 0xbbb, "I")


    #Processors list
    processors = [p1,p2,p3,p4]

    #Creates display window
    root = tk.Tk()
    root.title("Protocolo MOESI para coherencia de cache en sistemas multiprocesador")
    ventana = Ventana(root,modo)

    # Updates display window
    if ventana.modoActual == 1:
        ventana.continuousUpdate(processors,mem,modo)


    # ejecuta la ventana
    root.mainloop()

if __name__ == "__main__":
    main()

