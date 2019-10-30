var party_card_body = document.getElementById('party_card_body');
var party_btn_edit = document.getElementById('party_btn_edit');

function party_edit(e){
console.log('edit');
};

function party_save(e){
console.log('save');
};

function party_back(e){
console.log('back');
};

function party_remove(e){
console.log('remove');
console.log(e.dataset.party_name);
confirm("Delete party " + e.dataset.party_name + "?");
};