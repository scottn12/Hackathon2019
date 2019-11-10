import React, { Component } from 'react';
import './Calendar.css';

var API_KEY = 'c5e77b2452c7475b80e127915a27b790';

export default class News extends Component {
  constructor() {
    super();
    this.state = {
      events: [],
      user: 'none'
    };
    this.getCalendar('jackson');
  }

  componentDidMount() {
    setInterval(() => {
      this.getCalendar('jackson');
    }, 1000 * 60 * 30);
  }

  getCalendar(user) {
    user='jackson'
    fetch('https://smartmirroryoo.azurewebsites.net/getSchedule?user='+user)
      .then(response => response.json())
      .then(data => {
        data.events.forEach(function(e){
          this.setState(state =>{
            const events = [...state.events,e] // data.person
          });
        })
        console.log(this.state.events)
      })
      .catch((error) => {
        console.log(error);
      })
  }

  render() {
    return (
      <div style={{ position: 'absolute', bottom: '100px', width: '45%', fontSize: '25px' }}>
        <span style={{ fontSize: '60px' }}>NEWS</span>
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