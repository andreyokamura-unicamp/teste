
from flask import render_template, request, redirect
from app import app
from fileinput import filename
import pandas as pd
from functions import *
import json
#{% autoescape off %}#codigo dentro executa html
#{% endautoescape %}
#https://jsfiddle.net/onury/kBQdS/ cromo criar lista js


        #definicao de variaveis
device = 'cuda' if cuda.is_available() else 'cpu'
torch.manual_seed(0)

#parte 2: classificar correto, incorreto
# sub_loss = ['loss', 'accidentl', 'ambiguol', 'reescreverl', 'dueto', 'incompletol', 'notl', 'environment', 'during', 'eventl', 'hazardl']
# sub_hazard = ['hazard', 'incompletoh', 'when', 'reescreverh', 'accidenth', 'ambiguoh', 'causes', 'fail', 'noth', 'eventh', 'while', 'lossh']
# sub_constraint = ['prevent', 'recommendation', 'mitigate', 'detect', 'notc', 'incompletoc', 'reescreverc', 'ambiguoc']

sub_loss = ['loss', 'newaccidentl', 'newreescreverl', 'newcondl', 'newnotl', 'environment'] #10->5
sub_hazard = ['hazard', 'newreescreverh', 'newaccidenth', 'fail', 'newnoth', 'newcondh'] #11->5
sub_constraint = ['prevent', 'recommendation', 'mitigate', 'detect', 'newnotc', 'newreescreverc'] #5->3

sub_loss_incorreto = sub_loss.copy()
sub_loss_incorreto.remove('loss')

sub_hazard_incorreto = sub_hazard.copy()
sub_hazard_incorreto.remove('hazard')

sub_constraint_incorreto = sub_constraint.copy()
for item in ['prevent', 'detect', 'mitigate']:
    sub_constraint_incorreto.remove(item)

#path = './models/8020/'
#path = './models/7030/experimental/menos_erros1/'
path = 'andreyunic23/'
#carregar modelos

#modelo 1
num_label1 = 3
model_path1 = path+'parte_1'
tokenizer = AutoTokenizer.from_pretrained(model_path1)
model_classif = AutoModelForSequenceClassification.from_pretrained(model_path1, num_labels=num_label1).to(device)

#modelos 2
num_label2 = 2
model_path2l = path+'parte_2l'
model_path2h = path+'parte_2h'
model_path2c = path+'parte_2c'
tokenizer_loss = AutoTokenizer.from_pretrained(model_path2l)
tokenizer_hazard = AutoTokenizer.from_pretrained(model_path2h)
tokenizer_constraint = AutoTokenizer.from_pretrained(model_path2c)
model_classif_loss = AutoModelForSequenceClassification.from_pretrained(model_path2l, num_labels=num_label2).to(device)
model_classif_hazard = AutoModelForSequenceClassification.from_pretrained(model_path2h, num_labels=num_label2).to(device)
model_classif_constraint = AutoModelForSequenceClassification.from_pretrained(model_path2c, num_labels=num_label2).to(device)

labels_corretos = ['loss', 'hazard', 'prevent', 'detect', 'mitigate']

#modelo 3
model_path_s = path+'parte_3'
s_model = SentenceTransformer(model_path_s)

########era x_loss_correto!!!!!! errei

correct_example_path = "./datasets/"

correct_loss_df = pd.read_csv(correct_example_path+'correct_loss.csv')
correct_hazard_df = pd.read_csv(correct_example_path+'correct_hazard.csv')
correct_constraint_df = pd.read_csv(correct_example_path+'correct_constraint.csv')

examples_correct_loss = format_examples(correct_loss_df['req'].to_list())
examples_correct_hazard = format_examples(correct_hazard_df['req'].to_list())
examples_correct_constraint = format_examples(correct_constraint_df['req'].to_list())

# #modelo 4

# #num_label = x
model_path4l = path+'parte_4l'
model_path4h = path+'parte_4h'
model_path4c = path+'parte_4c'
tokenizer_loss_incorreto = AutoTokenizer.from_pretrained(model_path4l)
tokenizer_hazard_incorreto = AutoTokenizer.from_pretrained(model_path4h)
tokenizer_constraint_incorreto = AutoTokenizer.from_pretrained(model_path4c)
model_classif_loss_incorreto = AutoModelForSequenceClassification.from_pretrained(model_path4l, num_labels=len(sub_loss_incorreto)).to(device)
model_classif_hazard_incorreto = AutoModelForSequenceClassification.from_pretrained(model_path4h, num_labels=len(sub_hazard_incorreto)).to(device)
model_classif_constraint_incorreto = AutoModelForSequenceClassification.from_pretrained(model_path4c, num_labels=len(sub_constraint_incorreto)).to(device)

def inferencia(df):

    result_parte1 = []
    result_incorrect_loss = []
    result_incorrect_hazard = []
    result_incorrect_constraint = []
    result_list_sim_loss = []
    result_list_sim_hazard = []
    result_list_sim_constraint= []
    result_list_erro_loss = []
    result_list_erro_hazard = []
    result_list_erro_constraint = []
    
    x_test = df['req'].to_list()
    y_test = convert_label(df['label'])

    #teste parte 1
    with torch.no_grad():
        test_encodings = tokenizer(x_test, truncation=True, padding='max_length', max_length=512,return_tensors="pt")
        results = model_classif(test_encodings['input_ids'].to(device),test_encodings['attention_mask'].to(device))
        predictions = np.argmax(results.logits.cpu(), axis=-1)

    ####em vez de printar, guardar as predicoes numa lista [id, sent, orig, pred]
    ### nao sei se eu coloco probabilidade. quando a probabilidade do top é menor que 70%, seja um "bom" mal sinal que deve ser levantado. por enquanto
    df_parte1 = df_with_pred(y_test,results,df)
    result_parte1 = df_parte1.to_json(orient="records", default_handler=str)


    
    #carregar modelo 2

    #organize predictions: em vez de df, apenas lista de sentencas
    ##posso fazer ver. com rotulo e sem rotulo
    list_classif_loss, list_classif_hazard, list_classif_constraint = organize_predictions_list(predictions, df_parte1) #return df[id, req]

    #teste parte 2 loss
    x_loss = list_classif_loss['req'].to_list()
    #print('x_loss=',x_loss)

    if x_loss:

        with torch.no_grad():
            test_loss = tokenizer_loss(x_loss, truncation=True, padding='max_length', max_length=512,return_tensors="pt")
            results_loss = model_classif_loss(test_loss['input_ids'].to(device),test_loss['attention_mask'].to(device))
            predictions_loss = np.argmax(results_loss.logits.cpu(), axis=-1)

        incorrect_loss = get_incorrect(predictions_loss, list_classif_loss) #return df:[id,req]
        result_incorrect_loss = incorrect_loss.to_json(orient='records', default_handler=str)

        list_sim_loss = check_similarity_return2(incorrect_loss, examples_correct_loss, s_model)
        result_list_sim_loss = json.dumps(list_sim_loss, default=int)


        # #teste parte 4 loss
        x_loss2 = incorrect_loss['req'].to_list()

        if x_loss2:

            with torch.no_grad():
                test_loss_incorrect = tokenizer_loss_incorreto(x_loss2, truncation=True, padding='max_length', max_length=512,return_tensors="pt")
                results_loss_incorrect = model_classif_loss_incorreto(test_loss_incorrect['input_ids'].to(device),test_loss_incorrect['attention_mask'].to(device))



            list_erro_loss = list_erro_with_pred(results_loss_incorrect, incorrect_loss, sub_loss_incorreto)
            result_list_erro_loss = json.dumps(list_erro_loss, default=int)

    #teste parte 2 hazard
    x_hazard = list_classif_hazard['req'].to_list()

    if x_hazard:

        with torch.no_grad():
            test_hazard = tokenizer_hazard(x_hazard, truncation=True, padding='max_length', max_length=512,return_tensors="pt")
            results_hazard = model_classif_hazard(test_hazard['input_ids'].to(device),test_hazard['attention_mask'].to(device))
            predictions_hazard = np.argmax(results_hazard.logits.cpu(), axis=-1)

        incorrect_hazard = get_incorrect(predictions_hazard, list_classif_hazard)
        result_incorrect_hazard = incorrect_hazard.to_json(orient='records', default_handler=str)

        list_sim_hazard = check_similarity_return2(incorrect_hazard, examples_correct_hazard, s_model)
        result_list_sim_hazard = json.dumps(list_sim_hazard, default=int)


        #teste parte 4 hazard
        x_hazard2 = incorrect_hazard['req'].to_list()

        if x_hazard2:

            with torch.no_grad():
                test_hazard_incorrect = tokenizer_hazard_incorreto(x_hazard2, truncation=True, padding='max_length', max_length=512,return_tensors="pt")
                results_hazard_incorrect = model_classif_hazard_incorreto(test_hazard_incorrect['input_ids'].to(device),test_hazard_incorrect['attention_mask'].to(device))



            list_erro_hazard = list_erro_with_pred(results_hazard_incorrect, incorrect_hazard, sub_hazard_incorreto)
            result_list_erro_hazard = json.dumps(list_erro_hazard, default=int)


    #teste parte 2 constraint
    x_constraint = list_classif_constraint['req'].to_list()

    if x_constraint:

        with torch.no_grad():
            test_constraint = tokenizer_constraint(x_constraint, truncation=True, padding='max_length', max_length=512,return_tensors="pt")
            results_constraint = model_classif_constraint(test_constraint['input_ids'].to(device),test_constraint['attention_mask'].to(device))
            predictions_constraint = np.argmax(results_constraint.logits.cpu(), axis=-1)

        incorrect_constraint = get_incorrect(predictions_constraint, list_classif_constraint)
        result_incorrect_constraint = incorrect_constraint.to_json(orient='records', default_handler=str)


        list_sim_constraint = check_similarity_return2(incorrect_constraint, examples_correct_constraint, s_model)
        result_list_sim_constraint = json.dumps(list_sim_constraint, default=int)
    
        #teste parte 4 constraint
        x_constraint2 = incorrect_constraint['req'].to_list()

        if x_constraint2:
        
            with torch.no_grad():
                test_constraint_incorrect = tokenizer_constraint_incorreto(x_constraint2, truncation=True, padding='max_length', max_length=512,return_tensors="pt")
                results_constraint_incorrect = model_classif_constraint_incorreto(test_constraint_incorrect['input_ids'].to(device),test_constraint_incorrect['attention_mask'].to(device))



            list_erro_constraint = list_erro_with_pred(results_constraint_incorrect, incorrect_constraint, sub_constraint_incorreto)
            result_list_erro_constraint = json.dumps(list_erro_constraint, default=int)
    
    #parte 4


    

    return render_template("interface.html",
                            #data = result,
                            result_parte1 = result_parte1,
                            result_incorrect_loss = result_incorrect_loss,
                            result_incorrect_hazard = result_incorrect_hazard,
                            result_incorrect_constraint = result_incorrect_constraint,
                            result_list_sim_loss = result_list_sim_loss,
                            result_list_sim_hazard = result_list_sim_hazard,
                            result_list_sim_constraint= result_list_sim_constraint,
                            result_list_erro_loss = result_list_erro_loss,
                            result_list_erro_hazard = result_list_erro_hazard,
                            result_list_erro_constraint = result_list_erro_constraint
                            )

@app.route('/')
def homepage():
    return render_template('index.html', name='', file = None)

@app.route('/interface3', methods = ['POST'])#para teste da hp
def teste():
    return render_template('interface.html', name='', file = None)

@app.route('/interface', methods = ['POST'])#/success   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        df = pd.read_csv(f, names=['req','label'])
        df.insert(0, 'id', range(0, 0 + len(df)))
        #result = df.to_json(orient="records")

############################################# FIM
        #f.save(f.filename)
        
    return inferencia(df)

def parse_text(text):
    sentences = []
    split = text.split('\n')
    for item in split:
        item = item.replace('\r','')
        if item!= '':
            sentences.append(item)
    return sentences

@app.route('/interface2', methods = ['POST'])
def success2():
    if request.method == 'POST':   
        form_loss = request.form['text_loss']
        form_loss = parse_text(form_loss)
        form_hazard = request.form['text_hazard']
        form_hazard = parse_text(form_hazard)
        form_constraint = request.form['text_constraint']
        form_constraint = parse_text(form_constraint)

        #fill_loss = ['loss' for x in range(len(form_loss))]
        fill_loss = ['loss'] * len(form_loss)
        fill_hazard = ['hazard'] * len(form_hazard)
        fill_constraint = ['constraint'] * len(form_constraint)

        dict_loss = {'req': form_loss, 'label': fill_loss}
        dict_hazard = {'req': form_hazard, 'label': fill_hazard}
        dict_constraint = {'req': form_constraint, 'label': fill_constraint}

        df = pd.DataFrame(dict_loss)  
        df = pd.concat([df, pd.DataFrame(dict_hazard)])
        df = pd.concat([df, pd.DataFrame(dict_constraint)])
        df.insert(0, 'id', range(0, 0 + len(df)))
        df.reset_index(drop=True, inplace=True)


    return inferencia(df)
        #return render_template("interface.html", name='', file = None)