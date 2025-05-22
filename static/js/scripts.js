// SIDEBAR TOGGLE

let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebarOpen = false;
  }
}

// ---------- CHARTS ----------

const barChartOptions = {
  series: [
    {
      data: [
        364000000,  // ADELA ZAMUDIO
        208000000,  // MOLLE
        182000000,  // ITOCTA
        416000000,  // VALLE HERMOSO
        468000000,  // TUNARI
        260000000   // ALEJO CALATAYUD
      ],
    },
  ],
  chart: {
    type: 'bar',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f', '#4f35a1' , '#8b55a2'],
  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 4,
      horizontal: false,
      columnWidth: '40%',
    },
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false,
  },
  xaxis: {
    categories: ['ADELA ZAMUDIO', 'MOLLE', 'ITOCTA', 'VALLE HERMOSO', 'TUNARI', 'ALEJO CALATAYUD'],
  },
  yaxis: {
    title: {
      text: 'Consumo de Agua (litros)',
    },
  },
};

const barChart = new ApexCharts(
  document.querySelector('#bar-chart'),
  barChartOptions
);
barChart.render();

// AREA CHART - Consumo de agua Cochabamba (cada 10 días)
const areaChartOptions = {
  series: [
    {
      name: 'Consumo Residencial (m³)',
      data: [12500, 13100, 12700, 13300, 13800, 13950],
    },
    {
      name: 'Consumo Comercial (m³)',
      data: [8200, 8600, 8450, 8800, 9100, 9300],
    },
  ],
  chart: {
    height: 350,
    type: 'area',
    toolbar: {
      show: false,
    },
  },
  colors: ['#4f35a1', '#246dec'],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth', // Hace que las líneas tengan forma de curva
    width: 3,
  },
  labels: ['01/Abr', '11/Abr', '21/Abr', '01/May', '11/May', '21/May'],
  markers: {
    size: 4,
  },
  yaxis: [
    {
      title: {
        text: 'Consumo Residencial (m³)',
      },
    },
    {
      opposite: true,
      title: {
        text: 'Consumo Comercial (m³)',
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
  },
  
};

const areaChart = new ApexCharts(
  document.querySelector('#area-chart'),
  areaChartOptions
);
areaChart.render();
