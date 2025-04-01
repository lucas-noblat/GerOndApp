const botaoAbrir = document.querySelector(".botao-abrir");
const botaoFechar = document.querySelector(".fechar");
const popup = document.querySelector(".popup");

botaoAbrir.addEventListener("click", () => {
  popup.classList.add("aberto");
});

botaoFechar.addEventListener("click", () => {
  popup.classList.remove("aberto");
});