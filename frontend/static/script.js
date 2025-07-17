document.getElementById("resumeForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("resume");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload a PDF file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  const suggestionsList = document.getElementById("suggestionsList");
  suggestionsList.innerHTML = "";

  if (data.suggestions && data.suggestions.length > 0) {
    document.getElementById("results").classList.remove("hidden");
    data.suggestions.forEach(suggestion => {
      const li = document.createElement("li");
      li.textContent = suggestion;
      suggestionsList.appendChild(li);
    });
  } else {
    alert("No suggestions found.");
  }
});
