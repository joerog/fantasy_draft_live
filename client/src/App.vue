<template>
  <div id="app">
    <div class="title-bar">
      <h2>Rogerson League 19/20</h2>
    </div>
    <div class="card-item">
      <router-view/>
    </div>
    <div class="card-item">
      <chart/>
    </div>
    <div class="card-item">
      <fixtures/>
    </div>
  </div>
</template>

<script>

import Chart from './components/Chart.vue';
import Fixtures from './components/Fixtures.vue';

export default {
  components: {
    Chart,
    Fixtures,
  },
  name: 'App',
};
</script>

<style>
#app {
  font-family: rubik, Bahnschrift, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.card-item {
  display: inline-block;
  width: 48%;
  min-width: 400px;
  min-height: 500px;
  border: solid;
  border-color: black;
  border-width: 1px;
  margin: 5px;
}
.card-title {
  background-color: #00ff87;
  color: #37003c;
  height: 60px;
  margin-bottom: 10px;
}
h2 {
  padding: 20px auto;
  line-height: 60px !important;
}
h3 {
  line-height: 60px !important;
}
h4 {
  background-color: #00ff87;
  color: #37003c;
  font-size: 16px !important;
  margin-top: 10px !important;
  margin-bottom: 0px !important;
}
h5 {
  background-color: #37003c;
  color: white;
  font-size: 14px !important;
}
.title-bar {
  background-color: #37003c;
  color: #00ff87;
  height: 60px;
  margin-bottom: 10px;
}
.btn-info {
  background-color: #37003c !important;
  border: none !important;
}
.p-1 {
  padding: 0 5px !important;
  border: none !important;
}
.btn {
  border-radius: 0px !important;
}
.card {
  border-radius: 0px !important;
}
</style>
