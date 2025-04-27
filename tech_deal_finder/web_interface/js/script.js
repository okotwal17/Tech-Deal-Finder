const queryInput = document.getElementById("queryInput");
const searchBtn = document.getElementById("searchBtn");
const resultsContainer = document.getElementById("results");

async function fetchDeals(query) {
  resultsContainer.innerHTML = "<p>Loading...</p>";
  const response = await fetch(`http://localhost:5000/api/deals?query=${query}`);
  const deals = await response.json();

  if (deals.length === 0) {
    resultsContainer.innerHTML = "<p class='text-gray-500'>No deals found.</p>";
    return;
  }

  resultsContainer.innerHTML = "";
  deals.forEach((deal) => {
    const card = document.createElement("div");
    card.className = "border p-4 rounded-md shadow-md";

    card.innerHTML = `
      <h2 class="text-lg font-semibold">${deal.title}</h2>
      <p class="text-gray-700">$${deal.price}</p>
      <a href="${deal.url}" target="_blank" class="text-blue-500 hover:underline">View Deal</a>
    `;
    resultsContainer.appendChild(card);
  });
}

searchBtn.addEventListener("click", () => {
  const query = queryInput.value.trim();
  if (query) fetchDeals(query);
});

queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") searchBtn.click();
});
