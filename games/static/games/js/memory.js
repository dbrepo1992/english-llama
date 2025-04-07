let cards = [];
let flipped = [];
let score = 0;
let matchedPairs = 0;
let startTime;
let timerInterval;

const emojis = ["🐶", "🐱", "🐶", "🐱", "🐵", "🐵"];

function shuffle(array) {
  return array.sort(() => Math.random() - 0.5);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

function startGame() {
  const board = document.getElementById("game-board");
  board.innerHTML = "";
  cards = shuffle([...emojis]);
  flipped = [];
  score = 0;
  matchedPairs = 0;
  startTime = Date.now();
  updateScore();

  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(updateScore, 1000);

  cards.forEach((emoji, index) => {
    const card = document.createElement("div");
    card.className = "card";
    card.dataset.index = index;
    card.innerHTML = "❓";
    card.onclick = () => flipCard(card, index);
    board.appendChild(card);
  });
}

function flipCard(card, index) {
  if (flipped.length >= 2 || card.classList.contains("matched")) return;

  card.innerHTML = cards[index];
  flipped.push({ card, index });

  if (flipped.length === 2) {
    const [a, b] = flipped;
    if (cards[a.index] === cards[b.index]) {
      a.card.classList.add("matched");
      b.card.classList.add("matched");
      matchedPairs++;
      score++;
      flipped = [];
      if (matchedPairs === cards.length / 2) {
        clearInterval(timerInterval);
        const timeTaken = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById("game-status").textContent = `🎉 You won! Score: ${score}, Time: ${timeTaken}s`;
        fetch("/games/memory/save/", {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            body: new URLSearchParams({
              score: score,
              time: Math.floor((Date.now() - startTime) / 1000),
              difficulty: "easy"
            }),
          });
      }
    } else {
      setTimeout(() => {
        a.card.innerHTML = "❓";
        b.card.innerHTML = "❓";
        flipped = [];
      }, 800);
    }
  }
  updateScore();
}

function updateScore() {
  const time = Math.floor((Date.now() - startTime) / 1000);
  document.getElementById("score-time").textContent = `Score: ${score} | Time: ${time}s`;
}

// window.onload = startGame;<---- inny sposób na załadowanie danych z Document Objects Model. Pod spodem kolejny sposób.
document.addEventListener("DOMContentLoaded", () => {
  startGame(); // or whatever your main setup function is
});

