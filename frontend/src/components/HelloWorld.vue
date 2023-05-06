<template>
    <div class="container">
      <button @click="prevPage">上一页</button>
        <div>
          {{page}}
        </div>
      <button @click="nextPage">下一页</button>
      <table>
        <thead>
          <tr>
            <th>发布日期</th>
            <th>分类</th>
            <th>标题</th>
            <th>下载</th>
            <th>大小</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(file, index) in data" :key="index">
            <td>{{ file.release_time }}</td>
            <td>{{ file.category }}</td>
            <td>{{ file.title }}</td>
            <td><a :href="file.download_link">下载</a></td>
            <td>{{ file.size }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="prevPage">上一页</button>
        <div>
          {{page}}
        </div>
      <button @click="nextPage">下一页</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    data() {
      return {
        data:[],
        totalPages:0,
        page:1
      }
    },
    mounted() {
      this.fetchAnimes()
    },
    methods: {
      fetchAnimes(){
        const url = 'http://47.242.179.219:81?page=' + this.page
        axios.get(url).then(response => {
          console.log(response.data)
          this.data = response.data["data"]
          this.totalPages = response.data["total_pages"]
        })
      },
      prevPage(){
        if(this.page > 1)this.page--, this.fetchAnimes();
      },
      nextPage(){
        if(this.page < this.totalPages)this.page++, this.fetchAnimes();
      }
    },
  }
  </script>
  
  <style>
  .container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  table {
    border-collapse: collapse;
    width: 100%;
  }
  
  thead {
    background-color: #eee;
  }
  
  th,
  td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
  }
  
  th {
    font-weight: bold;
  }
  
  tr:hover {
    background-color: #f5f5f5;
  }
  </style>