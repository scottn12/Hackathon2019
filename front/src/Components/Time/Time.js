import React, { Component } from 'react';
import './Time.css'

export default class Time extends Component{

  constructor() {
    super();
    this.state = {
      time: new Date().toLocaleTimeString()
    }
  }

  componentDidMount() {
    setInterval( () => {
      this.setState({
        time: new Date().toLocaleTimeString()
      })
    });
  }


  render() {
    return(
      <div style={{fontSize: '80px'}}>
        {this.state.time}
      </div>
    );
  }

};