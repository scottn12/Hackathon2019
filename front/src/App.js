import React, { Component } from 'react';
import './App.css';
import Time from './Components/Time/Time';
import Weather from './Components/Weather/Weather';
import News from './Components/News/News'

class App extends Component {
  constructor() {
    super();
    this.state = {
      showData: true
    }
  }

  // Check for person every second
  componentDidMount() {
    setInterval( () => {
      fetch('https://smartmirroryoo.azurewebsites.net/checkForPerson')
        .then(response => response.json())
        .then(data => {
          this.setState({
            showData: true // data.person
          });
        })
        .catch((error) => {
          console.log(error);
        })
    }, 1000);
  }

  render() {
    return (
      <div>
        {this.state.showData &&
          <div className="app">
            <Time></Time>
            <Weather></Weather>
            <News></News>
          </div>
        }
      </div>
    );
  }

}

export default App;
