// Effects on change button
function changeButton(elemento) {
  document.getElementById("objetivo-input-choice").value = elemento.innerText
  var texto = elemento.innerText; // Obtém o texto do elemento clicado
  document.getElementById('objetivo-button').innerText = texto; // Atualiza o texto do botão
  var objetivoInput = document.getElementById("objetivo-input")
  if (texto == "Ao atingir magic number") {
    objetivoInput.disabled = true
  } else {
    objetivoInput.disabled = false
  }
}

// Add block to only acepts numbers in numeric fields
function patternNumber(event) {
  const sanitizedValue = event.target.value.replace(/[^0-9]/g, "")
  event.target.value = sanitizedValue;
}
const numberInput = document.getElementById("objetivo-input")
const aporteMensalInput = document.getElementById("aporte-mensal-input")
const montanteInicialInput = document.getElementById("montante-inicial-input")
numberInput.addEventListener("input", function(event) {
  patternNumber(event)
})
aporteMensalInput.addEventListener("input", function(event) {
  patternNumber(event)
})
montanteInicialInput.addEventListener("input", function(event) {
  patternNumber(event)
})

function validateForm() {
  const numberInput = document.getElementById("objetivo-input").value
  const aporteMensalInput = document.getElementById("aporte-mensal-input").value
  const objetivoButton = document.getElementById("objetivo-button").textContent.trim()
  const montanteInicialInput = document.getElementById("montante-inicial-input").value
  if (
    (numberInput === "" && objetivoButton !== "Ao atingir magic number") ||
    (aporteMensalInput === "") || 
    (montanteInicialInput === "") ||
    (objetivoButton === "Objetivo")) {
    window.alert('Preencha os campos corretamente')
    return false;
  }
  const cotaInput = document .getElementById("cota-input").value
  if (cotaInput === "") {
    window.alert('Preencha o campo cota, com um FII válido')
    return false
  }
  return true; 
}