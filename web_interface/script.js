async function getJSON(url) {
  const response = await fetch(url);
  return await response.json();
}

async function update(selector, path) {
  const container = document.querySelector(selector);
  const value = container.querySelector(".value");
  const time = container.querySelector(".time");
  const data = await getJSON(path);
  value.textContent = data["value"].toFixed(2);
  let parsed_time = Date.parse(data["time"]);
  let date = new Date(parsed_time);

  time.textContent = date.toLocaleString();
}

function updateLoop() {
  update("#temperature", "/api/temperature");
  update("#humidity", "/api/humidity");
  update("#pressure", "/api/pressure");
  setTimeout(updateLoop, 3000);
}

addEventListener("DOMContentLoaded", () => {
  updateLoop();
});
