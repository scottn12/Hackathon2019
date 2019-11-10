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
    }, 1000);
  }

  showMsg(){
    this.setState({s: true})
    setTimeout(() => {
      this.setState({ s: false })
    }, 5000)
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
        if(data['status'] == true){
          this.getText()
        }
      });
  }

  render() {
    return(
      <div style={{ position: 'absolute', right: '200px', top: '100px', fontSize: '25px',width:'100px' }} className={this.state.s ? 'fadeIn' : 'fadeOut'} >
        <span style={{ fontSize: '30px'}}>Confirm MSG</span>
        <br></br>
        <span style={{ fontSize: '20px' }}>Send out: {this.state.msg}</span>
        <br></br>
        <span style={{ fontSize: '20px' }}>is that ok?</span>
      </div>
    );
  }

};