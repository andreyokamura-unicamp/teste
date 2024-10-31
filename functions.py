#bibliotecas
import pandas as pd
import numpy as np
import torch
from torch import cuda
from torch.nn import functional as F
from sklearn.model_selection import train_test_split
import transformers
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
from sentence_transformers import SentenceTransformer


#classes e funcs

#parte 1 ###########################################################################################################
#parte 1 ###########################################################################################################

def convert_label(lista):
  for x in range(len(lista)):
    curr = lista[x]
    lista[x] = 0 if curr =='loss' else 1 if curr == 'hazard' else 2# if curr == 'constraint' else 3
  return lista

def df_with_pred(labels, results, data):
    lista = []
    cont = 0
    predicted = np.argmax(results.logits.cpu(), axis=-1)
    for test,pred in zip(labels, predicted):
        lista.append([data.id.iloc[cont],data.req.iloc[cont],test,pred.item()])
        cont += 1
    return pd.DataFrame(lista, columns=['id','req', 'label', 'pred'])

#parte 2 ###########################################################################################################
#parte 2 ###########################################################################################################

def organize_predictions_list(predicted, data):#data : ['id','req', 'label', 'pred']
  list_loss = []
  list_hazard = []
  list_constraint = []
  for x in range(len(predicted)):
    if(predicted[x] == 0):
      list_loss.append([data.id.iloc[x], data.req.iloc[x]])
    elif(predicted[x] == 1):
      list_hazard.append([data.id.iloc[x], data.req.iloc[x]])
    elif(predicted[x] == 2):
      list_constraint.append([data.id.iloc[x], data.req.iloc[x]])
  return  pd.DataFrame(list_loss, columns=['id','req']),  pd.DataFrame(list_hazard, columns=['id','req']),  pd.DataFrame(list_constraint, columns=['id','req'])


def get_incorrect(predicted, data): #data : [id, req]
  list_incorrect = []
  for x in range(len(predicted)):
    if predicted[x] == 1:
      list_incorrect.append([data.id.iloc[x],data.req.iloc[x]])
  return pd.DataFrame(list_incorrect,columns=['id','req'])


#parte 3 ###########################################################################################################
#parte 3 ###########################################################################################################

def format_examples(df):
  examples = []
  for sentence in df:
    examples.append([sentence,sentence])
  return examples

def check_similarity_return(list_incorrect, list_correct, model):
  embeddings = model.encode(list_correct)
  for x in range(len(list_incorrect)):
    id = list_incorrect.id.iloc[x]
    sentence = list_incorrect.req.iloc[x]
    sentence = model.encode(sentence)
    similarity = model.similarity(sentence, embeddings)
    sim_pair = []

    for sim,correct in zip(similarity[0].tolist(), list_correct):
      sim_pair.append([id, sim, correct[0]])

    sim_pair.sort(key=lambda x: x[0])
    sim_pair.reverse()

  return sim_pair[:10]

def check_similarity_return2(list_incorrect, list_correct, model):
  sim_pair = []
  embeddings = model.encode(list_correct)

  for x in range(len(list_incorrect)):
    id = list_incorrect.id.iloc[x]
    sentence = list_incorrect.req.iloc[x]
    sentence = model.encode(sentence)
    similarity = model.similarity(sentence, embeddings)
    temp_list = []
    for sim,correct in zip(similarity[0].tolist(), list_correct):
      temp_list.append([id, sim, correct[0]])

    temp_list.sort(key=lambda x: x[1])
    temp_list.reverse()

    sim_pair.extend(temp_list[:10])
  # print(sim_pair)
  return sim_pair
#parte 4 ###########################################################################################################
#parte 4 ###########################################################################################################


def list_erro_with_pred(results, data, sub):
    diff_label = []
    cont = 0
    predicted = np.argmax(results.logits.cpu(), axis=-1)
    probabilidade = F.softmax(results.logits.cpu(), dim=-1)
    for id,req,pred,prob in zip(data.id, data.req, predicted, probabilidade):
        # print(pred)
        # print(sub[pred.item()])
        # print(prob.tolist())
        #diff_label.append([id,req,sub[pred.item()],prob.tolist()])
        diff_label.append([id,req,pred.item(),prob.tolist()])
        cont+=1
    return diff_label

########################################################################
########################################################################
########################################################################
########################################################################




###########################################



