import numpy as np

class rnnml:
    def __init__(self, learning_rate):
        self.weight_matrix = np.array([])
        self.input_matrix = np.array([])
        self.target_matrix = np.array([])
        self.memory_weight = np.array([])
        self.output_weight = np.array([])
        self.previous_memory = np.array([])
        self.probabilty_matrix = np.array([])
        self.previous_memory_cache = np.array([])
        self.loss = np.array([])
        self.error = np.array([])
        self.learning_rate = learning_rate
        self.mode = "research"

    def createWeight(self, doors):
        size = self.input_matrix.shape
        self.weight_matrix = np.random.uniform(-0.001, 0.001, (size[1], doors))
        self.memory_weight = np.random.uniform(-0.001, 0.001, (size[1], doors))
        self.output_weight = np.random.uniform(-0.001, 0.001, (size[1], doors))
        self.previous_memory = np.random.uniform(0,0, (size[1], doors))

    def forwardpass(self):
        h = np.tanh((self.input_matrix @ self.weight_matrix) + (self.previous_memory @ self.memory_weight))
        self.previous_memory_cache = self.previous_memory
        self.previous_memory = h
        self.probabilty_matrix = h @ self.output_weight
        self.sigmoid()

    def sigmoid(self):
        output_matrix = 1 / (1 + np.exp(-self.probabilty_matrix))
        self.probabilty_matrix = output_matrix
        if self.mode == "research":
            self.lossfunction()
        elif self.mode == "recognize":
            print(self.probabilty_matrix)

    def lossfunction(self):
        self.loss = -np.log((self.probabilty_matrix @ self.target_matrix[0]) + 1e-8)
        print(f"Loss: {self.loss[0]}")
        self.errorCalculation()

    def errorCalculation(self):
        error = self.probabilty_matrix - self.target_matrix 
        self.error = error
        
        self.gradientCalculation()

    def gradientCalculation(self):
        outputGradient = self.previous_memory.T @ self.error
        hidden_error_raw = self.error @ self.output_weight.T
        true_hidden_error = self.tanhDerivative(self.previous_memory, hidden_error_raw)
        weightGradient = self.input_matrix.T @ true_hidden_error
        memoryGradient = self.previous_memory_cache.T @ true_hidden_error
        self.calculateWeights(outputGradient, weightGradient, memoryGradient)

    def calculateWeights(self, outputGradient, weightGradient, memoryGradient):
        self.output_weight = self.output_weight - (outputGradient * self.learning_rate)
        self.weight_matrix = self.weight_matrix - (weightGradient * self.learning_rate)
        self.memory_weight = self.memory_weight - (memoryGradient * self.learning_rate)

    def tanhDerivative(self, previous_memory, error):
        tanhDerivative = (1 - previous_memory ** 2)
        trueDerivative = error * tanhDerivative
        return trueDerivative
    
    
    def addTarget(self, target_matrix):
        self.target_matrix = target_matrix         
        
    def addInput(self, input_matrix):
        self.input_matrix = input_matrix        

    def saveData(self):
        np.save("models/np1.npy", [self.weight_matrix,self.memory_weight, self.output_weight, self.previous_memory, self.previous_memory_cache])
        print("Data saved succesfully")
    def loadData(self):
       self.weight_matrix = np.load("models/np1.npy")[0]
       self.memory_weight = np.load("models/np1.npy")[1]
       self.output_weight = np.load("models/np1.npy")[2]
       self.previous_memory = np.load("models/np1.npy")[3]
       self.previous_memory_cache = np.load("models/np1.npy")[4]
       print("Data loaded succesfully")
    
    
    def startResearch(self,amount):

        for i in range(amount):
            self.forwardpass()
        self.saveData()
    def recognize(self):

        self.mode = "recognize"
        self.input_matrix = np.array([[int(input("Enter a number: "))]])
        self.forwardpass()