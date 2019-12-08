if(document.getElementById("fab").innerText === "add"){

} else{
    // Form 개수
    var form_num = document.getElementById("id_proj-TOTAL_FORMS").value;
    var crtf_num = document.getElementById("id_crtf-TOTAL_FORMS").value;

    // 양식 제거 버튼 기능 추가
    for(var i=0; i < form_num; i++){
        var btn_id = "del_project_"+i;

        document.getElementById(btn_id).addEventListener("click", function (e) {
            var id = this.id.split("_")[2];
            var del_id = "id_proj-"+id+"-DELETE";
            document.getElementById(del_id).checked = true;
            this.parentElement.style.display = 'none';
        })
    }

    for(i=0; i < crtf_num; i++){
        btn_id = "del_crtf_"+i;

        document.getElementById(btn_id).addEventListener("click", function (e) {
            var id = this.id.split("_")[2];
            var del_id = "id_crtf-"+id+"-DELETE";
            document.getElementById(del_id).checked = true;
            this.parentElement.style.display = 'none';
        })
    }
}


// 양식 추가시, 양식 제거 버튼 기능 추가
document.getElementById("add_project").addEventListener("click", function () {
    var form_idx = document.getElementById("id_proj-TOTAL_FORMS").value;
    // add Project Form
    var newNode = document.createElement("div");
    newNode.className = "project_container";
    newNode.innerHTML = document.getElementById("empty_form").innerHTML.replace(/__prefix__/g, form_idx);
    document.getElementById("form_set").appendChild(newNode);

    document.getElementById("id_proj-TOTAL_FORMS").value = parseInt(form_idx) + 1;

    document.getElementById("del_project_").id = "del_project_"+(parseInt(form_idx)+1);
    document.getElementById("del_project_"+(parseInt(form_idx)+1)).addEventListener("click", function () {
        console.log("clicked");
        this.parentElement.remove();
    })
});

document.getElementById("add_crtf").addEventListener("click", function () {
    var form_idx = document.getElementById("id_crtf-TOTAL_FORMS").value;
    // add Project Form
    var newNode = document.createElement("div");
    newNode.className = "certification_container";
    newNode.innerHTML = document.getElementById("crtf_empty_form").innerHTML.replace(/__prefix__/g, form_idx);
    document.getElementById("crtf_form_set").appendChild(newNode);

    document.getElementById("id_crtf-TOTAL_FORMS").value = parseInt(form_idx) + 1;

    document.getElementById("del_crtf_").id = "del_crtf_"+(parseInt(form_idx)+1);
    document.getElementById("del_crtf_"+(parseInt(form_idx)+1)).addEventListener("click", function () {
        console.log("clicked");
        this.parentElement.remove();
    });
    var elem = document.querySelectorAll('select');
    var instance = M.FormSelect.getInstance(elem);
    addSelectBoxEventListener();
});

document.addEventListener('DOMContentLoaded', function() {
    var options = [
    opacity = 0.5,
    inDuration = 250,
    outDuration = 250,
    preventScrolling = true,
    dismissible = true,
    startingTop = '4%',
    endingTop = '10%'
  ];

  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems, options);

  addSelectBoxEventListener();
});

function addSelectBoxEventListener()  {
    var options = [
        classes = "",
        dropdownOptions = {}
    ];

    var elems = document.querySelectorAll('select');
    M.FormSelect.init(elems, options);
}
var opts = [
    classes = "",
    dropdownOptions = {}
];
