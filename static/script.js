// //let sent_list_json;// = {{data}};|tojson 
// var parte1 = {{ result_parte1 }};
// var incorrect_loss = {{ result_incorrect_loss }};
// var incorrect_hazard = {{ result_incorrect_hazard }};
// var incorrect_constraint = {{ result_incorrect_constraint }};
// var list_sim_loss = {{ result_list_sim_loss }};
// var list_sim_hazard = {{ result_list_sim_hazard }};
// var list_sim_constraint = {{ result_list_sim_constraint }};
// //let list_erro_loss = {{result_list_erro_loss}};
// //let list_erro_hazard = {{result_list_erro_hazard}};
// //let list_erro_constraint = {{result_list_erro_constraint}};

var parte1;
var incorrect_loss;
var incorrect_hazard;
var incorrect_constraint;
var list_sim_loss;
var list_sim_hazard;
var list_sim_constraint;
var list_erro_loss;
var list_erro_hazard;
var list_erro_constraint;

let incorrect_ids = [];
let erro_classif_ids = [];

// let sub_loss_incorreto = ['accidentl', 'ambiguol', 'reescreverl', 'dueto', 'incompletol', 'notl', 'environment', 'during', 'eventl', 'hazardl'];
// let sub_hazard_incorreto = ['incompletoh', 'when', 'reescreverh', 'accidenth', 'ambiguoh', 'causes', 'fail', 'noth', 'eventh', 'while', 'lossh'];
// let sub_constraint_incorreto = ['recommendation', 'notc', 'incompletoc', 'reescreverc', 'ambiguoc'];

let sub_loss_incorreto = ['acidente', 'reescrever', 'condicional', 'not', 'ambiente']
let sub_hazard_incorreto = ['reescrever', 'acidente', 'fail', 'not', 'condicional']
let sub_constraint_incorreto = ['recomendacao', 'not', 'reescrever']

//let list_labels = ['loss', 'hazard', 'constraint'];

function addData(tupla,t_id) {

    let id = tupla['id'];
    let req = tupla['req'];
    let label = tupla['label'];
    let pred = tupla['pred'];
    
    let flag = 0;
    if(label!=pred){
        flag = 1;
    }


    //console.log(req)
    //console.log(label)

    // Get the table and insert a new row at the end
    let table = document.getElementById(t_id).getElementsByTagName('tbody')[0];
    let newRow = table.insertRow(table.rows.length);
    //table.innerHTML = '';

    for(let i = 0; i<incorrect_loss.length;i++){
        if(id==incorrect_loss[i]['id']){//pode ser ['id'][i]
            newRow.className = 'incorrect';
            incorrect_ids.push(id)
        }
    }
    for(let i = 0; i<incorrect_hazard.length;i++){
        if(id==incorrect_hazard[i]['id']){//pode ser ['id'][i]
            newRow.className = 'incorrect';
            incorrect_ids.push(id)
        }
    }
    for(let i = 0; i<incorrect_constraint.length;i++){
        if(id==incorrect_constraint[i]['id']){//pode ser ['id'][i]
            newRow.className = 'incorrect';
            incorrect_ids.push(id)
        }
    }

    if(label != pred){
        newRow.className = 'erro';
        erro_classif_ids.push(id);
    }

    newRow.insertCell(0).innerHTML = id;
    newRow.insertCell(1).innerHTML = req;

    newcell = newRow.insertCell(2);
    newcell.innerHTML = list_labels[label];
    newcell.className = "erro_classif";

    newcell = newRow.insertCell(3);
    newcell.innerHTML = list_labels[pred];
    newcell.className = "erro_classif";


    
    // Clear input fields
    //clearInputs();
}

function addData_correct(){
    data = parte1;
    document.getElementById("all_sent_table").getElementsByTagName('tbody')[0].innerHTML = '';
    for(let i = 0; i<data.length;i++){
        if(!incorrect_ids.includes(data[i]['id'])){
            addData(data[i],"all_sent_table");
        } 
    }
}

function addData_incorrect(){
        data = parte1;
        let aux = incorrect_ids;
        incorrect_ids = [];
        document.getElementById("all_sent_table").getElementsByTagName('tbody')[0].innerHTML = '';
        for(let i = 0; i<data.length;i++){
            if(aux.includes(data[i]['id'])){
                addData(data[i],"all_sent_table");
            } 
        }
}

function addData_erro(){
    data = parte1;
    let aux = erro_classif_ids;
    erro_classif_ids = [];
    document.getElementById("all_sent_table").getElementsByTagName('tbody')[0].innerHTML = '';
    for(let i = 0; i<data.length;i++){
        if(aux.includes(data[i]['id'])){
            addData(data[i],"all_sent_table");
        } 
    }
}

function addData2(tupla,t_id) {
    //alert("etnrou addData2");
    //let id = tupla[0];
    let prob = tupla[1];
    let req = tupla[2];

    

    // Get the table and insert a new row at the end
    let table = document.getElementById(t_id).getElementsByTagName('tbody')[0];
    let newRow = table.insertRow(table.rows.length);

    // Insert data into cells of the new row
    newRow.insertCell(0).innerHTML = (prob*100).toFixed(2)+'%';
    newRow.insertCell(1).innerHTML = req;


}

function addData3(tupla,p_id, label){
    let pred = tupla[2];
    let prob = tupla[3];
    let sugestao = 'Lorem Ipsum.'
    let sub;

    switch(pred){
        case 0:
            sugestao = 'Sugestao1';
            break;
        case 1:
        case 2:
            sugestao = 'Sugestao3';
            break;
        default:
            //console.log('entrou addData3');
            break;
    }


    switch(+label){
        case 0:
            sub = sub_loss_incorreto;
            //sugestao = 'Sugestao1';//lista de sugestao com base no pred let sug_loss = [(10 sugestoes)]
            break;
        case 1:
            sub = sub_hazard_incorreto;
            break;
        case 2:
            sub = sub_constraint_incorreto;
            break;
    }

    let paragrafo = document.getElementById(p_id);
    paragrafo.innerHTML = 'Erro detectado: '+sub[pred]+';<br />Sugestão de verificação: '+sugestao+';';//Probabilidade: ${prob};<br />
        
    // Get the table and insert a new row at the end

    let table = document.getElementById('erro_table').getElementsByTagName('tbody')[0];
    //table.innerHTML = '';
    
    
    for(let i=0 ;i<sub.length;i++){

        let newRow = table.insertRow(table.rows.length);

    // Insert data into cells of the new row
        
        newRow.insertCell(0).innerHTML = (prob[i]*100).toFixed(2)+'%';
        newRow.insertCell(1).innerHTML = sub[i];
    }
    
}

function update_table(){
    data = parte1;
    //console.log(data[0])
    document.getElementById("all_sent_table").getElementsByTagName('tbody')[0].innerHTML = '';
    for(let i = 0; i<data.length;i++){
        addData(data[i],"all_sent_table");
    }

}

function start(result_parte1,result_incorrect_loss,result_incorrect_hazard,result_incorrect_constraint,result_list_sim_loss,result_list_sim_hazard,result_list_sim_constraint,result_list_erro_loss,result_list_erro_hazard,result_list_erro_constraint){// window.onload = function()
parte1 = result_parte1;
incorrect_loss = result_incorrect_loss;
incorrect_hazard = result_incorrect_hazard;
incorrect_constraint = result_incorrect_constraint;
list_sim_loss = result_list_sim_loss;
list_sim_hazard = result_list_sim_hazard;
list_sim_constraint = result_list_sim_constraint;
list_erro_loss = result_list_erro_loss;
list_erro_hazard = result_list_erro_hazard;
list_erro_constraint = result_list_erro_constraint;
update_table();
}

function start2(label,id){
    //alert('entrou start2');
    //alert(label);
    //alert(id);
    let data;
    // var old_tbody = document.getElementById('similar_tbody');
    // var new_tbody = document.createElement('tbody');
    // populate_with_new_rows(new_tbody);
    // old_tbody.parentNode.replaceChild(new_tbody, old_tbody);
    document.getElementById('sim_sent_table').getElementsByTagName('tbody')[0].innerHTML = '';

if(label==0){
    data = list_sim_loss;
}
else if(label==1){
    data = list_sim_hazard;
}
else if(label==2){
    data = list_sim_constraint;
}
for(let i = 0; i<data.length;i++){
    
    if(id==data[i][0]){
        //alert(data[i][0])certo
        //alert(data[0][i])undefined
        //console.log(data[i])
        addData2(data[i],"sim_sent_table");
    }
    
}
}

function show_erro(label, id){
    let data;
    document.getElementById('erro_table').getElementsByTagName('tbody')[0].innerHTML = '';
    if(label==0){
        data = list_erro_loss;
    }
    else if(label==1){
        data = list_erro_hazard;
    }
    else if(label==2){
        data = list_erro_constraint;
    }
    for(let i = 0; i<data.length;i++){
    
        if(id==data[i][0]){
            //alert(data[i][0])certo
            //alert(data[0][i])undefined
            
            addData3(data[i],"p_erro",label);
        }
        
    }
}

