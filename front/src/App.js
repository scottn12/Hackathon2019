import React, { Component } from 'react';
import './App.css';
import Time from './Components/Time/Time';
import Weather from './Components/Weather/Weather';
import News from './Components/News/News'
import Calendar from './Components/Calendar/Calendar'
import Text from './Components/Text/Text'
import Email from './Components/Email/Email';

class App extends Component {
  constructor() {
    super();
    this.state = {
      showData: true,
      inScreen: [],
      greet: false,
      greetMsg: 'Hi null!'
    }
  }

  newPerson(pList){
    if(JSON.stringify(this.state.inScreen)==JSON.stringify(pList)){
      return false
    }else{
      return true
    }
  }

  showGreet(person){
    this.setState({greetMsg:'Hi, '+person[0]+'\n You look pretty '+person[1]})
    this.setState({greet: true})
    setTimeout(()=>{
      this.setState({greet: false})
    },5000)
  }

  // Check for person every second
  componentDidMount() {
    setInterval(() => {
      fetch('http://127.0.0.1:5000/checkForPerson')
        .then(response => response.json())
        .then(data => {
          if (data.person) {
            var names = []
            data.data.forEach(element => {
              names.push(element)
            });
            if (this.newPerson(names)) {
              this.showGreet(names[0])
            }
            this.setState({
              showData: true, // data.person
              inScreen: names,
            });
          } else {
            this.setState({
              showData: false,
              inScreen: [], // data.person
            });
          }

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
            <div style={{position:"relative",top:"300px",left:"35%",display:"inline-block"}} className={this.state.greet ? 'fadeInG' : 'fadeOutG'}>
              {this.state.greetMsg}
            </div>
            <Text></Text>
            <News></News>
            <Email></Email>
          </div>
        }
      </div>
    );
  }

}

export default App;
