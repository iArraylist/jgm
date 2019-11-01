var party_card_body = document.getElementById('party_card_body');
var party_btn_add = document.getElementById('party_btn_add');

function party_remove(e){
confirm('Delete party ' + e.dataset.party_name + '?');
};

function job_sl_change(e){
    lb = document.getElementById(e.dataset.lb);
    while (lb.hasChildNodes()) {
        lb.removeChild(lb.firstChild);
    };
    if (e.value != 'None'){
        var model_img = document.getElementById('job_model_img_' + e.value);
        var img = model_img.cloneNode(true);
        img.removeAttribute('id');
        img.removeAttribute('class');
        img.setAttribute('width', 24);
        img.setAttribute('height', 24);
        img.removeAttribute('hidden');
        lb.appendChild(img);
    }
};

var WidgetPartySelectCharacter = Class.extend({
    init: function(url_reloadData, url_pushPMCData){
        this.url_reloadData = url_reloadData;
        this.url_pushPMCData = url_pushPMCData;
        var e_pmc_select_list = document.getElementsByName('pmc_select');
        var i;
        for (i = 0; i < e_pmc_select_list.length; i++) {
            if (e_pmc_select_list[i].type == 'select-one') {
                var pmc_select = e_pmc_select_list[i];
                var pmj_select = document.getElementById(e_pmc_select_list[i].dataset.pmj_select);
                if (pmj_select.value != 'None'){
                    this.reloadData(pmj_select, pmc_select);
                };
                $(pmj_select).data('widget', this);
                pmj_select.addEventListener('change', function(){
                    widget = $(this).data('widget');
                    pmc_select = document.getElementById(this.dataset.pmc_select);
                    pmc_select.dataset.war_job_id = 'None';
                    widget.reloadData(this, pmc_select);
                });
                $(pmc_select).data('widget', this);
                pmc_select.addEventListener('focus', function(){
                    widget = $(this).data('widget');
                    pmj_select = document.getElementById(this.dataset.pmj_select);
                    widget.reloadData(pmj_select, this);
                });
                pmc_select.addEventListener('change', function(){
                    widget = $(this).data('widget');
                    pmj_select = document.getElementById(this.dataset.pmj_select);
                    widget.pushPMCData(pmj_select, this);
                });
            };
        };
    },
    genPMCSelect: function(pmc_select, war_job_list){
        this.resetPMC(pmc_select);
        var war_job;
        for (war_job of war_job_list) {
            var option = document.createElement('option');
            option.text = war_job[1];
            option.value = war_job[0];
            if (pmc_select.dataset.war_job_id == war_job[0]){
                option.selected = true;
            }
            pmc_select.add(option);
        };
    },
    reloadData: function(pmj_select, pmc_select){
        var pass_data = {};
        var parent = this;
        var pmc_select = pmc_select;
        pass_data['p_id'] = pmj_select.dataset.p_id;
        pass_data['pm_id'] = pmj_select.dataset.pm_id;
        pass_data['job_id'] = pmj_select.value;
        pass_data['war_job_id_selected'] = pmc_select.dataset.war_job_id;
        $.ajax({
            dataType: 'json',
            url: this.url_reloadData,
            type: 'GET',
            data: pass_data,
            async: false
        }).done(function (response) {
            parent.genPMCSelect(pmc_select, response.result);
        });
    },
    resetPMC: function(pmc_select){
        this.removeOptions(pmc_select);
        var option = document.createElement('option');
        option.text = '-- Select --';
        option.value = 'None';
        option.selected = true;
        pmc_select.add(option);
    },
    removeOptions: function(elem){
        var i;
        for(i = elem.options.length - 1 ; i >= 0 ; i--){
            elem.remove(i);
        }
    },
    pushPMCData: function(pmj_select, pmc_select){
        var pass_data = {};
        var parent = this;
        var pmj_select = pmj_select;
        var pmc_select = pmc_select;
        pass_data['p_id'] = pmj_select.dataset.p_id;
        pass_data['pm_id'] = pmj_select.dataset.pm_id;
        pass_data['war_job_id'] = pmc_select.value;
        $.ajax({
            dataType: 'json',
            url: this.url_pushPMCData,
            type: 'GET',
            data: pass_data
        }).done(function (response) {
            if (response.error_code == 0) {
                pmc_select.dataset.war_job_id = pmc_select.value
            } else {
                alert('Something wrong!!. Pls,Contact Jaelynn');
            }
        });
    },
});