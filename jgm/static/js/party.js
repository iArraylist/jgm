var party_card_body = document.getElementById('party_card_body');
var party_btn_add = document.getElementById('party_btn_add');

function party_remove(e){
confirm('Delete party ' + e.dataset.party_name + '?');
};

function job_sl_change(e){
    lb = document.getElementById(e.dataset.lb);
    var model_img = document.getElementById('job_model_img_' + e.value);
    var img = model_img.cloneNode(true);
    img.removeAttribute('id');
    img.removeAttribute('class');
    img.setAttribute('width', 24);
    img.setAttribute('height', 24);
    img.removeAttribute('hidden');
    while (lb.hasChildNodes()) {
        lb.removeChild(lb.firstChild);
    };
    lb.appendChild(img);
};

var WidgetPartySelectCharacter = Class.extend({
    init: function(url){
        console.log(url);
        this.url = url;
        var e_pmc_select_list = document.getElementsByName('pmc_select');
        console.log(e_pmc_select_list);
        var i;
        for (i = 0; i < e_pmc_select_list.length; i++) {
            console.log(e_pmc_select_list[i].type);
            if (e_pmc_select_list[i].type == 'select-one') {
                pmc_select = e_pmc_select_list[i];
                pmj_select = document.getElementById(e_pmc_select_list[i].dataset.pmj_select);
                if (pmj_select.value != 'none'){
                    this.reloadData(pmj_select, pmc_select);
                };

                pmj_select.addEventListener("change", function(){
                    this.reloadData(pmj_select, pmc_select);
                });
                pmc_select.addEventListener("click", function(){

                });
                pmc_select.addEventListener("change", function(){

                });
            };
        };
    },
    genPMCSelect: function(pmc_select, war_job_list){
        var war_job_id_select = pmc_select.dataset.war_job_id;
        console.log(war_job_list);
        this.removeOptions(pmc_select);

        var war_job;
        for (war_job of war_job_list) {
            var option = document.createElement('option');
            option.text = war_job[1];
            option.value = war_job[0];
            if (war_job_id_select == war_job[0]){
                option.selected = true;
            }
            pmc_select.add(option);
        };

    },
    reloadData: function(pmj_select, pmc_select){
        var pass_data = {};
        var parent = this;
        var pmc_select = pmc_select;
        pass_data['pm_id'] = pmj_select.dataset.pm_id;
        pass_data['job_id'] = pmj_select.value;
        $.ajax({
            dataType: 'json',
            url: this.url,
            type: 'GET',
            data: pass_data
        }).done(function (response) {
            if (response.error_code == 0) {
                parent.genPMCSelect(pmc_select, response.result);
            } else {
                alert('Something wrong!!');
            }
        });
    },
    resetPMC: function(pmc_select){
        this.removeOptions(pmc_select);
        var option = document.createElement('option');
        option.text = '-- Select --';
        option.value = 'none';
        pmc_select.add(option);
    },
    removeOptions: function(elem){
        var i;
        for(i = elem.options.length - 1 ; i >= 0 ; i--){
            elem.remove(i);
        }
    }
});