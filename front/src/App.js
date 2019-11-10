import React, { Component } from 'react';
import './App.css';
import Time from './Components/Time/Time';
import Weather from './Components/Weather/Weather';

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
        .then((response) => {
          if (response.ok) {
            this.setState({
              showData: true
            });
          }
          else {
            this.setState({
              showData: true // PUT BACK TO FALSE
            });
          }
        })
        .catch((error) => {
          //console.log(error);
        })

    }, 1000);
  }

  render() {
    return (
      <div>
        {this.state.showData &&
          <div className="app">
            <Time style={{float: 'left'}}></Time>
            <Weather style={{float: 'right'}}></Weather>
          </div>
        }
      </div>
    );
  }

}

export default App;
