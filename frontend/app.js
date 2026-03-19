const API_URL = "YOUR_AZURE_FUNCTION_URL_HERE";

document.getElementById("refreshBtn").addEventListener("click", loadData);

let barChart, pieChart, lineChart;

async function loadData() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    document.getElementById("meta").textContent =
      `Execution time: ${data.execution_time_ms ?? "--"} ms`;

    renderCharts(data);
  } catch (error) {
    console.error("Error loading data:", error);
  }
}

function renderCharts(data) {
  const labels = data.avg_macros?.map(x => x.Diet_type) || [];
  const protein = data.avg_macros?.map(x => x.Protein) || [];
  const carbs = data.avg_macros?.map(x => x.Carbs) || [];
  const fat = data.avg_macros?.map(x => x.Fat) || [];

  if (barChart) barChart.destroy();
  if (pieChart) pieChart.destroy();
  if (lineChart) lineChart.destroy();

  barChart = new Chart(document.getElementById("barChart"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Protein", data: protein },
        { label: "Carbs", data: carbs },
        { label: "Fat", data: fat }
      ]
    }
  });

  pieChart = new Chart(document.getElementById("pieChart"), {
    type: "pie",
    data: {
      labels,
      datasets: [
        { label: "Protein", data: protein }
      ]
    }
  });

  lineChart = new Chart(document.getElementById("lineChart"), {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Protein", data: protein }
      ]
    }
  });
}