import numpy as np  
  
def markovCluster(adjacencyMat, dimension, numIter, power = 2, inflation = 2):  
    columnSum = np.sum(adjacencyMat, axis = 0)  
    probabilityMat = adjacencyMat / columnSum  
      
    #Expand by taking the e^th power of the matrix.  
    def _expand(probabilityMat, power):  
        expandMat = probabilityMat  
        for i in range(power - 1):  
            expandMat = np.dot(expandMat, probabilityMat)  
        return expandMat  
    expandMat = _expand(probabilityMat, power)  
      
    #Inflate by taking inflation of the resulting   
    #matrix with parameter inflation.   
    def _inflate(expandMat, inflation):  
        powerMat = expandMat  
        for i in range(inflation - 1):  
            powerMat = powerMat * expandMat  
        inflateColumnSum = np.sum(powerMat, axis = 0)  
        inflateMat = powerMat / inflateColumnSum  
        return inflateMat  
    inflateMat = _inflate(expandMat, inflation)  
      
    for i in range(numIter):  
        expand = _expand(inflateMat, power)  
        inflateMat = _inflate(expand, inflation)  
    print(inflateMat)  
      
      
if __name__ == "__main__":  
    dimension = 4  
    numIter = 2  
    adjacencyMat = np.array([[1, 1, 1, 1],  
                             [1, 1, 0, 1],  
                             [1, 0, 1, 0],  
                             [1, 1, 0, 1]])  
    markovCluster(adjacencyMat, dimension, numIter)  
