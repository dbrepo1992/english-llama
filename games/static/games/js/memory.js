let cards = [];
let flipped = [];
let score = 0;
let matchedPairs = 0;
let startTime;
let timerInterval;
let selectedDifficulty = "easy"; // default

const wordEmojiPairs = {
  "Cat": "😺", "Dog": "🐶", "Monkey": "🐵", "Pig": "🐷", "Panda": "🐼", "Fox": "🦊", "Cow": "🐮", "Rabbit": "🐰",
  "Tiger": "🐯", "Koala": "🐨", "Lion": "🦁", "Mouse": "🐭", "Frog": "🐸", "Bear": "🐻", "Chicken": "🐔", "Penguin": "🐧",
  "Elephant": "🐘", "Dolphin": "🐬", "Shark": "🦈", "Octopus": "🐙", "Crab": "🦀", "Fish": "🐟", "Bee": "🐝", "Butterfly": "🦋",
  "Spider": "🕷️", "Crocodile": "🐊", "Horse": "🐴", "Unicorn": "🦄", "Camel": "🐫", "Zebra": "🦓", "Giraffe": "🦒", "Kangaroo": "🦘"
};

function shuffle(array) {
  return array.sort(() => Math.random() - 0.5);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function getPairsForDifficulty(level) {
  const allPairs = Object.entries(wordEmojiPairs);
  let count = 8; // default easy
  if (level === "medium") count = 18;
  else if (level === "hard") count = 32;
  return shuffle(allPairs).slice(0, count);
}

function createCard(content, index) {
  const card = document.createElement("div");
  card.className = "card";
  card.dataset.index = index;
  card.innerHTML = "❓";
  card.onclick = () => flipCard(card, index);
  return card;
}

function startGame() {
  const board = document.getElementById("game-board");
  board.innerHTML = "";
  score = 0;
  matchedPairs = 0;
  flipped = [];

  const pairList = getPairsForDifficulty(selectedDifficulty);
  const flatList = [];

  pairList.forEach(([word, emoji], idx) => {
    const pairId = `pair-${idx}`;
    flatList.push({ type: "word", value: word, pairId });
    flatList.push({ type: "emoji", value: emoji, pairId });
  });


  cards = shuffle(flatList);
  setBoardGrid(pairList.length);

  cards.forEach((item, i) => {
    const card = createCard(item.value, i);
    board.appendChild(card);
  });

  startTime = Date.now();
  updateScore();

  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(updateScore, 1000);
}

function setBoardGrid(pairCount) {
  const board = document.getElementById("game-board");
  const total = pairCount * 2;
  let cols = Math.sqrt(total);
  if (selectedDifficulty === "easy") cols = 4;
  else if (selectedDifficulty === "medium") cols = 6;
  else if (selectedDifficulty === "hard") cols = 8;
  board.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
}

function flipCard(card, index) {
  if (flipped.length >= 2 || card.classList.contains("matched")) return;

  card.innerHTML = cards[index].value;
  flipped.push({ card, index });

  if (flipped.length === 2) {
    const [a, b] = flipped;
    const aVal = cards[a.index];
    const bVal = cards[b.index];

    if ((aVal.type !== bVal.type) && (aVal.pairId === bVal.pairId)) {
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
            time: timeTaken,
            difficulty: selectedDifficulty,
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

document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".difficulty-btn");
  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      selectedDifficulty = btn.dataset.level;
      startGame();
    });
  });

  document.getElementById("restart-btn").addEventListener("click", startGame);
  startGame(); // default
});
