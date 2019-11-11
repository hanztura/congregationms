deleteButtonApp = new Vue({
  el: '#delete-button-app',
  delimiters: ['[[', ']]'],
  data: () => {
    return {
      disabled: false,
    }
  },

  methods: {
    confirmDelete: function (e) {
      let target = e.target;
      this.disabled = true;
      if (confirm('You sure you want to delete?')) {
        target.submit();
      }
      this.disabled = false;
    }
  }
});