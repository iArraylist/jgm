var woe_fixable = document.getElementById('woe_fixable');
var woc_fixable = document.getElementById('woc_fixable');
var zone_fixable = document.getElementById('zone_fixable');
var img_woe_job = document.getElementById('img_woe_job');
var img_woc_job = document.getElementById('img_woc_job');
var img_zone_job = document.getElementById('img_zone_job');

function sl_change(e){
    lb = document.getElementById(e.dataset.lb);
    var jobs = document.getElementsByName('jobs');
    var index;
    for (index = 0; index < jobs.length; index++){
        if (jobs[index].type == 'checkbox') {
            if(jobs[index].value == e.value){
                var model_img = document.getElementById(jobs[index].dataset.img_id);
                var img = model_img.cloneNode(true);
                img.removeAttribute('id');
                img.removeAttribute('class');
                img.setAttribute('width', 24);
                img.setAttribute('height', 24);
                while (lb.hasChildNodes()) {
                  lb.removeChild(lb.firstChild);
                }
                lb.appendChild(img);
            }
        }
    }
};

function cb_change(e){
    if (e.checked) {
        img = document.getElementById(e.dataset.img_id).setAttribute('class', '');
    }
    else {
        img = document.getElementById(e.dataset.img_id).setAttribute('class', 'grayscale');
    }
    render_option(woe_fixable, img_woe_job);
    render_option(woc_fixable, img_woc_job);
    render_option(zone_fixable, img_zone_job);
};

function render_option(fixable, img_job){
    var elem = document.getElementById(fixable.htmlFor);
    removeOptions(elem);
    var option_d = document.createElement('option');
    option_d.text = '-- Select --';
    option_d.selected = true;
    elem.add(option_d);
    var jobs = document.getElementsByName('jobs');
    var index;
    for (index = 0; index < jobs.length; index++){
        if (jobs[index].type == 'checkbox') {
            if(jobs[index].checked){
                img_job.innerHTML = '';
                var option = document.createElement('option');
                option.text = jobs[index].dataset.text;
                option.value = jobs[index].getAttribute('value');
                elem.add(option);
            }
        }
    }
};

function removeOptions(elem){
    var i;
    for(i = elem.options.length - 1 ; i >= 0 ; i--){
        elem.remove(i);
    }
};