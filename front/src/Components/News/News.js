import React, { Component } from 'react';
import './News.css';

var API_KEY = 'c5e77b2452c7475b80e127915a27b790';

export default class News extends Component {
  constructor() {
    super();
    this.state = {
      articles: []
    };
    this.getNews();
  }

  componentDidMount() {
    setInterval( () => {
      this.getNews();
    }, 1000 * 60 * 30);
  }

  getNews() {
    fetch('https://newsapi.org/v2/top-headlines?country=us&apiKey=' + API_KEY)
      .then(response => response.json())
      .then(data => {
        this.setState({
          articles: [data.articles[0].title, data.articles[1].title, data.articles[2].title]
        });
      });
  }

  render() {
    return(
      <div style={{position: 'fixed', top: '1540px', width: '45%', fontSize: '25px'}}>
        <span style={{ fontSize: '60px'}}>NEWS</span>
        <br></br>
        <ul>
          <li>{this.state.articles[0]}</li>
          <li>{this.state.articles[1]}</li>
          <li>{this.state.articles[2]}</li>
        </ul>
      </div>
    );
  }

};