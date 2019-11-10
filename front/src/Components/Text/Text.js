import React, { Component } from 'react';
import './Text.css';

export default class Text extends Component {
  constructor() {
    super();
    this.state = {
      s: false,
      msg: ''
    };
  }

  componentDidMount() {
    setInterval( () => {
      this.ckText();
    }, 200);
  }

  showMsg(){
    this.setState({s: true})
    setTimeout(() => {
      this.setState({ s: false })
    }, 7000)
  }
  
  getText(){
    fetch('http://127.0.0.1:5000'+'/getMsg')
      .then(response=>response.json())
      .then(data => {
        this.setState({
          msg: data['msg']
        })
        this.showMsg()
      })
  }

  ckText() {
    fetch('http://127.0.0.1:5000'+'/checkMsg')
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if(data['status'] == true){
          this.getText()
        }
      });
  }

  render() {
    return(
      <div>
      {this.state.s &&
          <div style={{ position: "relative", top: "300px", width: '300px', left: "35%", display: "inline-block", fontSize: "30px", textAlign: 'center' }}>
          <span style={{ fontSize: '30px' }}>Confirm MSG</span>
          <br></br>
          <span style={{ fontSize: '20px' }}>Send out: {this.state.msg}</span>
          <br></br>
          <span style={{ fontSize: '20px' }}>is that ok?</span>
        </div>
      }
      </div>
    );
  }

};