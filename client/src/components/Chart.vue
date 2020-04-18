<template>
  <div v-if="loaded">
    <div class="card-title">
      <h3>League History</h3>
    </div>
    <line-chart
      :chartdata="chartdata"
      :options="options"
      :styles="styles"></line-chart>
  </div>
</template>

<script>
import axios from 'axios';
import LineChart from './LineChart.vue';

export default {
  name: 'Chart',
  components: {
    LineChart,
  },
  data() {
    return {
      loaded: false,
      chartdata: [],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          labels: {
            fontFamily: 'rubik',
          },
        },
        tooltips: {
          titleFontFamily: 'rubik',
          bodyFontFamily: 'rubik',
        },
      },
      styles: {
        height: '100%',
        position: 'relative',
        width: '90%',
        margin: '20px auto',
      },
    };
  },
  methods: {
    generateColour(string) {
      let hash = 0;
      if (string.length === 0) return hash;
      for (let i = 0; i < string.length; i += 1) {
        hash = string.charCodeAt(i) + ((hash << 5) - hash); // eslint-disable-line no-bitwise
        hash &= hash; // eslint-disable-line no-bitwise
      }
      let color = '#';
      for (let i = 0; i < 3; i += 1) {
        const value = (hash >> (i * 8)) & 255; // eslint-disable-line no-bitwise
        color += (`00${value.toString(16)}`).substr(-2);
      }
      return color;
    },
  },
  async mounted() {
    const path = `${this.$hostname}/history/`;
    const res = await axios.get(path);
    // this.chartdata = res.data;
    const dataset = [];

    for (let i = 0; i < res.data.length; i += 1) {
      dataset.push({
        label: res.data[i].player,
        fill: false,
        borderColor: this.generateColour(res.data[i].player),
        data: res.data[i].history_total,
      });
    }
    const labels = [];
    for (let i = 1; i <= res.data[0].history_total.length; i += 1) {
      labels.push(`GW ${i}`);
    }
    this.chartdata = {
      labels,
      datasets: dataset,
    };
    this.loaded = true;
  },
};
</script>
