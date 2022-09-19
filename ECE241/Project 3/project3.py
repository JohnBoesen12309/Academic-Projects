import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class project3:
    def __init__(self):
        self.data={}
        self.header = ""
        self.weights = np.random.uniform(0,0.1,size=25)

    def loadData(self,filename):
        f = open(filename,'r',encoding='utf-8-sig')
        for i in f:
            line = i.strip("\n").split(",")
            if line[0] == "Id": #Setup header
                self.header = line
            else:
                count = 0
                for j in self.header: #Import data
                    try:
                        self.data[j].append(float(line[count]))
                    except:
                        self.data[j]=[float(line[count])]
                    count+=1
        self.data = pd.DataFrame(self.data) # Change self.data to a pandas Dataframe

    def pred(self,y):
        sums = []
        for i in range(len(y)):
            price = np.array(self.weights).dot(np.array(y[i]))
            sums.append(price)
        return np.array(sums)

    def loss(self,pred,actual):
        #return  1/len(pred)* sum(actual-pred)**2
        return  1/len(pred)* np.square(np.array(actual)-np.array(pred)).sum()

    def gradient(self,X,pred,actual):
        Xt = np.transpose(X)
        return 2/actual.size * Xt.dot((pred-actual))
        #return 2/len(actual) * Xt * (pred-actual)

    def update(self,grad,alpha):
        return self.weights - alpha * grad

    def q2_4(self):
        #Answers to question 2
        print("Total number of records:",len(self.data))
        print("Mean of Prices:",self.data["Price"].mean())
        print("Max Price:",self.data["Price"].max())
        print("Minimum Price:",self.data["Price"].min())
        print("Standard Deviation:",self.data["Price"].std())

        #Make the histogram for question 3
        bins = 50
        plt.hist(self.data["Price"],bins,facecolor='blue',alpha=0.6)
        plt.xlabel("Sales Price")
        plt.title("Frequency of Sales Prices")

        #Make the pair-plot for question 4
        newDict={}
        newDict['GrLivArea'] = self.data['GrLivArea']
        newDict['BedroomAbvGr'] = self.data['BedroomAbvGr']
        newDict['TotalBsmtSF'] = self.data['TotalBsmtSF']
        newDict['FullBath'] = self.data['FullBath']
        sns.pairplot(pd.DataFrame(newDict),diag_kws={'bins':bins})
        plt.show()





if __name__ == "__main__":
    i=500
    x = project3()
    print("--------------Loading Data-------------")
    x.loadData("train.csv")
    print("---------Answers to question 2---------")
    x.q2_4()
    print("---------------Running Sim-------------")
    alpha1 = 10**-9
    alpha2 = 10**-8
    MSE1 = []
    MSE2 = []
    row = x.data.loc[:, "LotFrontage":"MoSold"].to_numpy()
    actual = x.data.loc[:, "Price"].to_numpy()
    weights = x.weights

    #Train for alpha = 10**-9
    for j in range(i):
        pred = x.pred(row)
        MSE1.append(x.loss(pred,actual))
        grad = x.gradient(row,pred,actual)
        x.weights = x.update(grad,alpha1)
    x.weights = weights #Reset weights for next test using alpha2

    #Train for alpha = 10**-8
    for j in range(i):
        pred = x.pred(row)
        MSE2.append(x.loss(pred,actual))
        grad = x.gradient(row,pred,actual)
        x.weights = x.update(grad,alpha2)
    print("Alpha = %s converges to %s"%(alpha1,MSE1[499]))
    print("Alpha = %s converges to %s"%(alpha2,MSE2[499]))

    """Plot the MSEs"""

    plt.plot(MSE1, label = "MSE w/ alpha = %s"%alpha1)
    plt.plot(MSE2, label = "MSE w/ alpha = %s"%alpha2)
    plt.legend()
    plt.show()

    '''Use weights from training data to predict prices'''
    print("------------Testing Weights------------")
    y=project3()
    y.loadData('test.csv')
    y.weights = x.weights
    pred = y.pred(y.data.loc[:, "LotFrontage":"MoSold"].to_numpy())
    MSE = y.loss(pred,y.data.loc[:,"Price"].to_numpy())
    print("MSE using test data: %s"%MSE)


