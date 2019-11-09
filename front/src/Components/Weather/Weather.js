import React, { Component } from 'react';
import './Weather.css'

var API_KEY = 'deb5cfb37421aca2f2e614d3b2b125ee';
var ZIP = '07101';

export default class Weather extends Component {
  constructor() {
    super();
    this.state = {
      temp: -1,
      status: '',
      sunrise: -1,
      sunset: -1
    }
    this.getWeather();
  }

  componentDidMount() {
    setInterval( () => {
      this.getWeather();
    }, 1000 * 60 * 30);
  }

  getWeather() {
    fetch('http://api.openweathermap.org/data/2.5/weather?zip=' + ZIP + ',us&appid=' + API_KEY)
      .then(response => response.json())
      .then(data => {
        console.log(data);
        let t = data.main.temp;
        let weatherID = data.weather[0].id;
        let s = '';
        if (weatherID >= 200 && weatherID < 300) {
          s = 'thunder storm';
        }
        else if (weatherID >= 300 && weatherID < 600) {
          s = 'rain';
        }
        else if (weatherID >= 600 && weatherID < 700) {
          s = 'snow';
        }
        else if (weatherID >= 700 && weatherID < 800) {
          s = 'fog';
        }
        else if (weatherID === 800) {
          s = 'clear';
        }
        else if (weatherID > 800) {
          s = 'cloudy';
        }
        t = Math.round((t - 273.15) * 9/5 + 32);
        this.setState({
          status: s,
          temp: t,
          sunrise: data.sys.sunrise,
          sunset: data.sys.sunset
        });
      })
  }

  render() {
    return(
      <div className="weather">
        Temp: {this.state.temp} °F
        <br></br> 
        Status: {this.state.status}
        <br></br>
      </div>
    );
  }



};