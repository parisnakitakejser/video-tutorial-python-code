<template>
  <div class="home">
    Welcom to API test!<br />
    api data: {{post_data}}

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',

  data () {
    return {
        'post_data': null
    }
  },

  components: {
  },

  computed: {
    api_url () {
        return 'http://localhost:8000'
    }
  },

  methods: {
    load_data () {
        axios.get(this.api_url + '/api/posts').then((resp) => {
            this.post_data = resp.data;
        });
    }
  },

  created () {
    this.load_data();
}
}
</script>
