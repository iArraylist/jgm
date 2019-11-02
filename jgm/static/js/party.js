var WidgetURL = Class.extend({
    init: function(){
        this.loadURL();
    },
    loadURL: function(){
        var url_list = document.getElementById('url_list');
        this.url_reloadData = url_list.dataset.url_reload_data;
        this.url_pushPMCData = url_list.dataset.url_push_pmc_data;
        this.url_pushLeader = url_list.dataset.url_push_leader;
        this.url_pushPartyData = url_list.dataset.url_push_party_data;
    }
});

var WidgetParty = WidgetURL.extend({
    init: function(){
        this.loadURL();
        this.addelstn('leader_cb', 'checkbox', 'change',this.leader_cb_change, this.url_pushLeader);
        this.addelstn('job_select', 'select-one', 'change', this.job_sl_change);
        this.addelstn('party_data_edit_btn', 'button', 'click', this.party_data_edit);
        this.addelstn('party_data_back_btn', 'button', 'click', this.party_data_back);
        this.addelstn('party_data_save_btn', 'button', 'click', this.party_data_save, this.url_pushPartyData);
        this.addelstn('party_del_btn', 'button', 'click', this.party_del);
        this.addelstn('color_select', 'select-one', 'change', this.color_sl_change);
    },
    addelstn:function(e_name, e_type, event, func, url){
        var e_list = document.getElementsByName(e_name);
        var i;
        for (i = 0; i < e_list.length; i++) {
            if (e_list[i].type == e_type) {
                var e = e_list[i];
                e.addEventListener(event, function(){
                    func(this, url)
                });
            };
        };
    },
    party_data_edit: function(e){
        var party_name_div = document.getElementById(e.dataset.party_name_div);
        while (party_name_div.hasChildNodes()) {
            party_name_div.removeChild(party_name_div.firstChild);
        };
        var name_input = document.createElement('input');
        name_input.setAttribute('id', 'party_name_input_' + party_name_div.dataset.p_id);
        name_input.setAttribute('type', 'text');
        name_input.setAttribute('class', 'form-control form-control-sm form-custom-sm');
        name_input.setAttribute('placeholder', 'Party name');
        name_input.setAttribute('maxlength', 255);
        name_input.value = party_name_div.dataset.party_name;
        party_name_div.appendChild(name_input);
        party_name_div.dataset.party_name_input = name_input.getAttribute('id');

        var party_remark_div = document.getElementById(e.dataset.party_remark_div);
        while (party_remark_div.hasChildNodes()) {
            party_remark_div.removeChild(party_remark_div.firstChild);
        };
        var remark_input = document.createElement('input');
        remark_input.setAttribute('id', 'party_remark_input_' + party_name_div.dataset.p_id);
        remark_input.setAttribute('type', 'text');
        remark_input.setAttribute('class', 'form-control form-control-sm form-custom-sm');
        remark_input.value = party_remark_div.dataset.party_remark;
        party_remark_div.appendChild(remark_input);
        party_remark_div.dataset.party_remark_input = remark_input.getAttribute('id');

        document.getElementById(party_name_div.dataset.party_c_tool).hidden = false;
        document.getElementById(party_name_div.dataset.party_b_tool).hidden = false;
        document.getElementById(party_name_div.dataset.party_a_tool).hidden = true;
    },
    party_data_back: function(e){
        var party_name_div = document.getElementById(e.dataset.party_name_div);
        while (party_name_div.hasChildNodes()) {
            party_name_div.removeChild(party_name_div.firstChild);
        };
        party_name_div.innerHTML = party_name_div.dataset.party_name;

        var party_remark_div = document.getElementById(e.dataset.party_remark_div);
        while (party_remark_div.hasChildNodes()) {
            party_remark_div.removeChild(party_remark_div.firstChild);
        };
        party_remark_div.innerHTML = party_remark_div.dataset.party_remark;

        var party_color_select = document.getElementById(e.dataset.party_color_select);
        party_color_select.value = party_color_select.dataset.color;
        var party_header = document.getElementById(party_color_select.dataset.party_header);
        var party_footer = document.getElementById(party_color_select.dataset.party_footer);
        party_header.setAttribute('class', 'card-header ' + party_color_select.dataset.color +' p-1 px-2');
        party_footer.setAttribute('class', 'card-footer ' + party_color_select.dataset.color +' p-1 px-2');

        document.getElementById(party_name_div.dataset.party_c_tool).hidden = true;
        document.getElementById(party_name_div.dataset.party_b_tool).hidden = true;
        document.getElementById(party_name_div.dataset.party_a_tool).hidden = false;
    },
    party_data_save: function(e, url){
        var party_name_div = document.getElementById(e.dataset.party_name_div);
        var party_name = document.getElementById(party_name_div.dataset.party_name_input).value;
        var party_remark_div = document.getElementById(e.dataset.party_remark_div);
        var party_remark = document.getElementById(party_remark_div.dataset.party_remark_input).value;
        var party_color_select = document.getElementById(e.dataset.party_color_select);
        var party_color = party_color_select.value;
        if (party_name != ''){
            var pass_data = {};
            pass_data['p_id'] = party_name_div.dataset.p_id;
            pass_data['party_name'] = party_name;
            pass_data['party_remark'] = party_remark;
            pass_data['party_color'] = party_color
            $.ajax({
                dataType: 'json',
                url: url,
                type: 'GET',
                data: pass_data
            });
            party_name_div.dataset.party_name = party_name;
            while (party_name_div.hasChildNodes()) {
                party_name_div.removeChild(party_name_div.firstChild);
            };
            party_name_div.innerHTML = party_name_div.dataset.party_name;

            party_remark_div.dataset.party_remark = party_remark;
            while (party_remark_div.hasChildNodes()) {
                party_remark_div.removeChild(party_remark_div.firstChild);
            };
            party_remark_div.innerHTML = party_remark_div.dataset.party_remark;

            party_color_select.dataset.color = party_color;

            document.getElementById(party_name_div.dataset.party_c_tool).hidden = true;
            document.getElementById(party_name_div.dataset.party_b_tool).hidden = true;
            document.getElementById(party_name_div.dataset.party_a_tool).hidden = false;
        } else {
            alert('Pls enter party name')
        };
    },
    party_del: function(e){
        var con = confirm('Delete party ' + e.dataset.party_name + '?');
        if (con == true) {
            location.replace(e.dataset.go);
        }
    },
    leader_cb_change: function(e, url){
        var pass_data = {};
        pass_data['p_id'] = e.dataset.p_id;
        pass_data['pm_id'] = e.dataset.pm_id;
        if (e.checked) { pass_data['check'] = true }
        else { pass_data['check'] = false };
        $.ajax({
            dataType: 'json',
            url: url,
            type: 'GET',
            data: pass_data
        });
    },
    job_sl_change: function(e){
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
    },
    color_sl_change: function(e){
        var color = e.value
        var party_header = document.getElementById(e.dataset.party_header);
        var party_footer = document.getElementById(e.dataset.party_footer);
        party_header.setAttribute('class', 'card-header ' + color +' p-1 px-2');
        party_footer.setAttribute('class', 'card-footer ' + color +' p-1 px-2');
    }
});

var WidgetPartySelectCharacter = WidgetURL.extend({
    init: function(){
        this.loadURL();
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
                alert('Something wrong!!. Pls contact Jaelynn');
            }
        });
    }
});