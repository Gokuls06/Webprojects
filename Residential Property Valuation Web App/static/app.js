function uploadCSV() {
    const file = document.getElementById("fileInput").files[0];
    const formData = new FormData();
    formData.append("file", file);
  
    fetch("/upload", {
      method: "POST",
      body: formData
    }).then(res => res.json()).then(data => {
      if (data.error) {
        document.getElementById("uploadMessage").innerText = data.error;
        return;
      }
      document.getElementById("uploadMessage").innerText = data.message;
      const locationSelect = document.getElementById("locationSelect");
      locationSelect.innerHTML = "";
      data.locations.forEach(loc => {
        locationSelect.innerHTML += `<option value="${loc}">${loc}</option>`;
      });
      document.getElementById("formArea").classList.remove("hidden");
    });
  }
  
  function predictPrice() {
    const rooms = document.getElementById("rooms").value;
    const sqft = document.getElementById("sqft").value;
    const location = document.getElementById("locationSelect").value;
  
    fetch("/predict", {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ rooms, square_foot: sqft, location })
    }).then(res => res.json()).then(data => {
      document.getElementById("priceResult").innerText = `💵 USD Price Range: $${data.lower_usd} - $${data.upper_usd}`;
      window.usdPrices = data;
    });
  }
  
  