<template>
  <div role="tablist">
    <div class="card-title">
      <h3>Fixtures</h3>
    </div>
    <div class="gw-navigator">
      <span class="nav-left" @click="gwMinus(gw)">&lt;</span>
      <span class="nav-centre">GW {{ gw }}</span>
      <span class="nav-right" @click="gwPlus(gw)">&gt;</span>
    </div>
    <div v-if="gw > 0 && !loading">
      <b-card
        v-for="(fixture, index) in getFixtures"
        v-bind:key="fixture.code"
        no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button block href="#" v-b-toggle="'accordion-' + index" variant="info">
            {{ fixture.team_h }} <b>{{ fixture.team_h_score }}</b> v
            <b>{{ fixture.team_a_score }}</b> {{ fixture.team_a }}</b-button>
        </b-card-header>
        <b-collapse :id="'accordion-' + index" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text>
              <div v-for="stat in fixture.stats" v-bind:key="stat.s">
                <div v-if="stat.h.length != 0 || stat.a.length != 0">
                  <h4>{{ titleCase(stat.s).replace('Bps', 'Bonus Points') }}</h4>
                  <div class="stat-column">
                    <h5>{{ fixture.team_h }}</h5>
                    <div v-for="homeStat in stat.h" v-bind:key="homeStat">
                      {{ homeStat.name }} ({{ homeStat.value }})
                      <span v-b-tooltip.hover
                            v-if="homeStat.owner.short_name !== '--'"
                            class="owner-box"
                            :title="homeStat.owner.name">
                        {{ homeStat.owner.short_name }}</span>
                    </div>
                  </div>
                  <div class="stat-column">
                    <h5>{{ fixture.team_a }}</h5>
                    <div v-for="awayStat in stat.a" v-bind:key="awayStat">
                      {{ awayStat.name }} ({{ awayStat.value }})
                      <span v-b-tooltip.hover
                            v-if="awayStat.owner.short_name !== '--'"
                            class="owner-box"
                            :title="awayStat.owner.name">
                        {{ awayStat.owner.short_name }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
    <div v-else>
      <b-spinner label="Spinning"></b-spinner>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Fixtures',
  data() {
    return {
      gw: 0,
      current: 0,
      loading: true,
    };
  },
  asyncComputed: {
    async getFixtures() {
      if (this.gw > 0) {
        this.loading = true;
        const path = `${this.$hostname}/fixtures/${this.gw}/`;
        const res = await axios.get(path);
        this.loading = false;
        return res.data;
      }
      return [];
    },
  },
  methods: {
    titleCase(string) {
      const str = string.toLowerCase().split('_');
      for (let i = 0; i < str.length; i += 1) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
      }
      return str.join(' ');
    },
    condClass(owner) {
      if (owner === '--') {
        return '';
      }

      return 'owner-box';
    },
    gwMinus() {
      if (this.gw > 0) {
        this.gw -= 1;
      }
    },
    gwPlus() {
      if (this.gw < this.current) {
        this.gw += 1;
      }
    },
    async getCurrent() {
      const path = `${this.$hostname}/current/`;
      const res = await axios.get(path);
      this.current = res.data;
      return res.data;
    },
    async getOwner(id) {
      const path = `${this.$hostname}/owner/${id}`;
      const res = await axios.get(path);
      return res.data.short_name;
    },
  },
  async mounted() {
    this.gw = await this.getCurrent();
  },
};
</script>
<style scoped>
b {
  color: #00ff87;
}
.stat-column {
  width: 50%;
  display: inline-block;
  vertical-align: top;
  font-size: 12px;
}
.gw-navigator {
  background-color: lightgrey;
  margin-bottom: 10px;
}
.nav-left {
  float: left;
  padding: 0 5px;
}
.nav-right {
  float: right;
  padding: 0 5px;
}
.card-title {
  margin-bottom: 0px;
}
.owner-box {
  background-color: #37003c;
  color: white;
  padding: 1px;
  margin: 2px 0;
}
</style>
