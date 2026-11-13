// Scripts do Já Pod Quitar
// Nada aqui é obrigatório para o sistema funcionar, é só para deixar as telas mais práticas.

document.addEventListener("DOMContentLoaded", function () {
  confirmarFormularios();
  campoOutro();
  valorDoRange();
  contadorDeCaracteres();
  contarCliquesApoio();

  var caixaCronometro = document.getElementById("caixa-cronometro");
  if (caixaCronometro) {
    iniciarCronometro(caixaCronometro);
  }
});

// pede confirmação antes de enviar formulários importantes (excluir, interromper...)
function confirmarFormularios() {
  document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
    form.addEventListener("submit", function (evento) {
      if (!window.confirm(form.dataset.confirmar)) {
        evento.preventDefault();
      }
    });
  });
}

// mostra o campo de texto quando a pessoa escolhe "Outro" no select
function campoOutro() {
  document.querySelectorAll("select[data-campo-outro]").forEach(function (select) {
    var campo = document.getElementById(select.dataset.campoOutro);
    if (!campo) return;
    var grupo = campo.closest(".grupo-outro");

    function atualizar() {
      var mostrar = select.value === "Outro";
      grupo.classList.toggle("d-none", !mostrar);
      campo.required = mostrar;
    }

    select.addEventListener("change", atualizar);
    atualizar();
  });
}

// mostra o número escolhido na barrinha de intensidade
function valorDoRange() {
  document.querySelectorAll("input[type=range][data-saida]").forEach(function (range) {
    var saida = document.getElementById(range.dataset.saida);
    function atualizar() {
      saida.textContent = range.value;
    }
    range.addEventListener("input", atualizar);
    atualizar();
  });
}

function contadorDeCaracteres() {
  document.querySelectorAll("textarea[maxlength]").forEach(function (campo) {
    var aviso = document.createElement("div");
    aviso.className = "contador-caracteres";
    campo.insertAdjacentElement("afterend", aviso);

    function atualizar() {
      aviso.textContent = campo.value.length + " / " + campo.maxLength;
    }
    campo.addEventListener("input", atualizar);
    atualizar();
  });
}

// conta os cliques nos canais de apoio (indicador da seção 2.3 do documento).
// usa sendBeacon para não atrapalhar a abertura do link
function contarCliquesApoio() {
  var area = document.querySelector("[data-url-clique]");
  if (!area || !navigator.sendBeacon) return;

  var token = document.querySelector("meta[name=csrf-token]").content;

  area.querySelectorAll("a[data-canal]").forEach(function (link) {
    link.addEventListener("click", function () {
      var dados = new FormData();
      dados.append("canal", link.dataset.canal);
      dados.append("csrf_token", token);
      navigator.sendBeacon(area.dataset.urlClique, dados);
    });
  });
}

// cronômetro das missões práticas
function iniciarCronometro(caixa) {
  var total = parseInt(caixa.dataset.minutos, 10) * 60;
  var restante = total;
  var fim = null;
  var intervalo = null;

  var visor = caixa.querySelector(".cronometro");
  var botaoIniciar = caixa.querySelector("[data-acao=iniciar]");
  var botaoZerar = caixa.querySelector("[data-acao=zerar]");
  var avisoFim = caixa.querySelector(".aviso-fim");

  function formatar(segundos) {
    var h = Math.floor(segundos / 3600);
    var m = Math.floor((segundos % 3600) / 60);
    var s = segundos % 60;
    var mm = String(m).padStart(2, "0");
    var ss = String(s).padStart(2, "0");
    return h > 0 ? h + ":" + mm + ":" + ss : mm + ":" + ss;
  }

  function mostrar() {
    visor.textContent = formatar(restante);
  }

  function pausar() {
    clearInterval(intervalo);
    intervalo = null;
  }

  function passarTempo() {
    // calcula pelo relógio, porque o setInterval atrasa quando a aba fica em segundo plano
    restante = Math.max(0, Math.round((fim - Date.now()) / 1000));
    mostrar();
    if (restante === 0) {
      pausar();
      botaoIniciar.textContent = "Começar de novo";
      avisoFim.classList.remove("d-none");
    }
  }

  botaoIniciar.addEventListener("click", function () {
    if (intervalo) {
      pausar();
      botaoIniciar.textContent = "Continuar";
      return;
    }
    if (restante === 0) {
      restante = total;
    }
    avisoFim.classList.add("d-none");
    fim = Date.now() + restante * 1000;
    botaoIniciar.textContent = "Pausar";
    intervalo = setInterval(passarTempo, 500);
  });

  botaoZerar.addEventListener("click", function () {
    pausar();
    restante = total;
    botaoIniciar.textContent = "Iniciar";
    avisoFim.classList.add("d-none");
    mostrar();
  });

  mostrar();
}
