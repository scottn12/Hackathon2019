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
      greetMsg1: 'Hi null!',
      greeMsg2: '',
      emoji: '',
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
    let emotion = '';
    let emj = '';
    if (person[1] == 'happiness') {
      emotion = 'You look great! I love your smile!';
      emj = '😃';
    }
    else if (person[1] == 'neutral') {
      emotion = 'Looking good! Today will be aweosome!';
      emj = '😐';
    }
    else if (person[1] == 'sadness') {
      emotion = 'Cheer up! It will be a great day :)';
      emj = '😭';
    }
    this.setState({greetMsg1:'Hi '+person[0]+'!', greeMsg2: emotion, emoji: emj});
    this.setState({greet: true})
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
    }, 100);
  }

  render() {
    return (
      <div>
        {this.state.showData &&
          <div className="app">
            <Time></Time>
            <span className="emoji">{this.state.emoji}</span>
            <Weather></Weather>
            <div style={{position:"relative",top:"600px", width: '300px', left:"35%",display:"inline-block",fontSize:"30px", textAlign: 'center'}} className={this.state.greet ? 'fadeInG' : 'fadeOutG'}>
              <span style={{fontSize: '50px', fontWeight: '500'}}>{this.state.greetMsg1}</span>
              <br></br>
              {this.state.greeMsg2}
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
