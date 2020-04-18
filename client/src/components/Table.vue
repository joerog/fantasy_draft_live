<template>
  <div>
    <div class="card-title">
      <h3>Current Standings</h3>
    </div>
    <div>
      <b-table striped hover
        :items="getLiveTable"
        :fields="fields"
        :fixed="false"
        :small="!getTooSmall">
        <template v-slot:cell(team_and_manager)="data">
          <b>{{ data.item.team }}</b>
          <small v-if="getTooSmall">   {{ data.item.player }}</small>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Table',
  props: {
  },
  data() {
    return {
      fields: [
        { key: 'rank', sortable: true },
        'team_and_manager',
        { key: 'total_points', sortable: true },
        { key: 'live_points', sortable: true },
        { key: 'weekly_score', sortable: true },
      ],
    };
  },
  asyncComputed: {
    async getLiveTable() {
      const path = `${this.$hostname}/table/`;
      const res = await axios.get(path);
      return res.data;
    },
  },
  computed: {
    getTooSmall() {
      if (window.innerWidth < 500) {
        return false;
      }
      return true;
    },
  },
};
</script>

<style scoped>
table {
  display: table;
  text-align: left;
  margin: auto;
  width: 90%;
  font-size: 11px;
  border: solid;
  border-color: lightgrey;
  border-width: 1px;
}
table th {
  width: auto !important;
}
/deep/ th {
  background-color: #37003c;
  color: #00ff87;
}
/deep/ td {
  vertical-align: middle !important;
}
</style>
