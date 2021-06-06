import random
import chess
import numpy as np

from evaluation import evaluation
from Minimax import Minimax


class TDleaf():
  def __init__(self):
    # parameters of training


    # the weight matrix and bias vector to be calculated
    self.eval=evaluation()
    self.minimax=Minimax()


  
  
  def tdleaf(self, training_sample, alpha, gamma, lmda, W, depth):
    
    #Training parameters 
    self.alpha = alpha
    self.gamma = gamma
    self.lmda = lmda
    self.W = W
    self.depth = depth

    training_sample  #secuence of borads

    

    
    features = self.get_leaf_features(training_sample)
    d = self.get_td(features)

    sum2 = 0 # Sumatorio de los TD ponderados por lambda
    sum1 = 0 # gradiente de V(s(l), w)): basaso en V(s(l)): Partial derivate of V inrespects to w. --> in practic this = W in our case

    
    for t in range (0, len(training_sample) - 1):
      sum2 = 0 # Sumatorio de los TD ponderados por lambda

      for i in range (t, len(training_sample) - 1):
      
        # Sumatorio de los TD ponderados por lambda
        sum2 += pow(self.lmda, i-t) * d[i]
      
      #Calculate gradient and multiply by lmabda wighted TDs.
      gradient = features[i+1] - features[i]
      
      # We add 1-lambda as a normalizatio factor
      sum1 += gradient * (1-self.lmda)*sum2

    # update weights
    self.W+= self.alpha*sum1
  
    return self.W







  def get_leaf_features(self, training_sample): 
      
    features_list =[]
    for b in training_sample:
      features, _ = self.minimax.minimax_train(self.depth, b, b.turn)
      features_list.append(np.array(features))
    
    return features_list
        
  def get_td(self, features):
    d =[] #almacenamos las td calculadas en base a bestleaf 
    grad=0
    for i in range(len(features)-1):
      grad = features[i+1] - features[i]
      d.append(grad)
    
    return d
