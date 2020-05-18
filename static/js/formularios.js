function nuevaEtiqueta() {
    const divMainFrmData = document.getElementById("cajaLineas");
    const nLineas = document.getElementsByClassName("etiqueta").length;

    if (nLineas < 5) {
        var div = document.createElement("div");
        div.id = "etiqueta" + (nLineas + 1);
        div.className = "form-group";

        var lab = document.createElement("label");
        lab.innerHTML = "Etiqueta " + (nLineas + 1);
        lab.htmlFor = "etiqueta_" + (nLineas + 1);

        var input = document.createElement("input");
        input.type = "text";
        input.className = "form-control etiqueta";
        input.id = "etiqueta_" + (nLineas + 1);
        input.name = "etiqueta";
        input.placeholder = "Máximo 15 caracteres";
        input.maxLength = "15";
        input.onblur = function () {
            comprobarEtiqueta(nLineas + 1)
        };

        div.appendChild(lab);
        div.appendChild(input);
        divMainFrmData.appendChild(div);
    }
}

function quitarEtiqueta() {
    const nLineas = document.getElementsByClassName("etiqueta").length;
    if (nLineas > 0) {
        var div = document.getElementById("etiqueta" + nLineas);
        var padre = div.parentNode;
        padre.removeChild(div);
    }
}

function calcularEtiquetas() {
    document.getElementById("nEtiquetas").value = (document.getElementsByClassName("etiqueta").length) + "";
}

function abrirModal(header, body) {
    document.getElementById("modalHeader").innerHTML = header;
    document.getElementById("modalBody").innerHTML = body;
    $('#myModal').modal('show');
}

function fallido(campoID) {
    document.getElementById(campoID).style.border = "1px solid red";
}

function valido(campoID) {
    document.getElementById(campoID).style.border = "1px solid green";
}

function comprobarMensaje() {
    var toret = true;
    var id = "mensaje";
    var value = document.getElementById(id).value;

    if (value.trim().length <= 0) {
        toret = false;
        abrirModal("El mensaje no es válido", "El mensaje no puede estar vacío");
    }

    toret ? valido(id) : fallido(id);
    return toret;
}

function comprobarEtiqueta(i) {
    var toret = true;
    var id = "etiqueta_" + i;
    var value = document.getElementById(id).value;

    if (!/^[A-z0-9ñÑ]+$/.test(value)) {
        toret = false;
        abrirModal("La etiqueta " + i + " no es válida", "Las etiquetas no pueden estar vacías, no pueden contener espacios y solo se permiten números y letras sin acentos");
    }

    toret ? valido(id) : fallido(id);
    return toret;
}

function comprobarApodo() {
    var toret = true;
    var id = "user";
    var value = document.getElementById(id).value;

    if (!/^[^\s]*$/.test(value)) {
        toret = false;
        abrirModal("El apodo no es válido", "El apodo no pueden contener espacios");
    }

    toret ? valido(id) : fallido(id);
    return toret;
}

function comprobarFormSquab() {
    var toret = true;
    for (var i = document.getElementsByClassName("etiqueta").length; i > 0; i--) {
        if (!comprobarEtiqueta(i)) {
            toret = false;
        }
    }

    if (!comprobarMensaje()) {
        toret = false;
    }

    return toret;
}

function comprobarFormFiltro() {
    var toret = true;
    for (var i = document.getElementsByClassName("etiqueta").length; i > 0; i--) {
        if (!comprobarEtiqueta(i)) {
            toret = false;
        }
    }

    if (!comprobarApodo()) {
        toret = false;
    }

    return toret;
}


function mueveReloj() {
    const momentoActual = new Date();

    var dia = momentoActual.getDate();
    var mes = momentoActual.getMonth() + 1;
    var ano = momentoActual.getFullYear();

    var hora = momentoActual.getHours();
    var minuto = momentoActual.getMinutes();
    var segundo = momentoActual.getSeconds();

    var elemento = document.getElementById("reloj");
    const str_dia = String(dia);
    if (str_dia.length === 1)
        dia = "0" + dia;

    const str_mes = String(minuto);
    if (str_mes.length === 1)
        mes = "0" + mes;

    const str_hora = String(hora);
    if (str_hora.length === 1)
        hora = "0" + hora;

    const str_segundo = String(segundo);
    if (str_segundo.length === 1)
        segundo = "0" + segundo;

    const str_minuto = String(minuto);
    if (str_minuto.length === 1)
        minuto = "0" + minuto;

    elemento.innerHTML = dia + "/" + mes + "/" + ano + "  -  " + hora + " : " + minuto + " : " + segundo;

    setTimeout("mueveReloj()", 1000);
}