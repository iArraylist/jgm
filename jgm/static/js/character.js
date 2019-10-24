var woe_fixable = document.getElementById("woe_fixable");
var woc_fixable = document.getElementById("woc_fixable");
var zone_fixable = document.getElementById("zone_fixable");

function cb_change(e){
    if (e.checked ) {
        console.log('check');
        img = document.getElementById(e.getAttribute('img_id')).setAttribute("class", "");
    }
    else {
        console.log('uncheck');
        img = document.getElementById(e.getAttribute('img_id')).setAttribute("class", "grayscale");
    }
    render_option(woe_fixable);
    render_option(woc_fixable);
    render_option(zone_fixable);
};

function render_option(fixable){
    var elem = document.getElementById(fixable.htmlFor);
    removeOptions(elem);
    var option_d = document.createElement("option");
    option_d.text = '-- Select --';
    option_d.selected = true;
    elem.add(option_d);
    var jobs = document.getElementsByName("jobs");
    var index;
    for (index = 0; index < jobs.length; index++){
        if (jobs[index].type == "checkbox") {
            if(jobs[index].checked){
                var model_img = document.getElementById(jobs[index].getAttribute('img_id'));
                var img = model_img.cloneNode(true);
                img.setAttribute("class", "");
                img.setAttribute("id", "");
                var option = document.createElement("option");
                option.text = jobs[index].getAttribute('text');
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