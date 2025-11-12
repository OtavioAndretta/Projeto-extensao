// Abre/fecha o chat
document.getElementById("chat-toggle").onclick = () => {
  document.getElementById("chat-container").classList.toggle("hidden");
};

document.getElementById("close-chat").onclick = () => {
  document.getElementById("chat-container").classList.add("hidden");
};

// Envia mensagem com Enter ou clique
document.getElementById("send-btn").onclick = sendMessage;
document.getElementById("user-input").addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  // Mostra mensagem do usuário
  appendMessage("Você", message, "user");
  input.value = "";

  try {
    // Envia ao backend Flask
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error("Erro na resposta do servidor");
    }

    const data = await response.json();

    // Mostra resposta da IA
    appendMessage("Assistente", data.reply, "bot");
  } catch (error) {
    console.error(error);
    appendMessage("Sistema", "⚠️ Ocorreu um erro ao se comunicar com o servidor.", "bot");
  }
}

// Função para adicionar mensagens ao chat
function appendMessage(sender, text, type) {
  const chat = document.getElementById("chat-messages");

  const msgWrapper = document.createElement("div");
  msgWrapper.classList.add("chat-message", type);

  // Texto formatado (com quebras de linha seguras)
  const msgText = document.createElement("div");
  msgText.innerHTML = `<b>${sender}:</b> ${text.replace(/\n/g, "<br>")}`;

  msgWrapper.appendChild(msgText);
  chat.appendChild(msgWrapper);

  // Scroll automático para a última mensagem
  chat.scrollTop = chat.scrollHeight;
}
