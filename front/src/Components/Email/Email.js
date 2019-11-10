import React, { Component } from 'react';
import './Email.css';

export default class Email extends Component {
  constructor() {
    super();
    this.state = {
      emails: []
    };
  }

  componentDidMount() {
    this.getMail()
    
  }

  getMail() {
    fetch('http://127.0.0.1:5000/readEmail')
      .then(response => response.json())
      .then(data =>{
        this.setState({emails:data['email']})
        console.log(this.state.emails)
      })
  }

  render() {
    return (
      <div style={{ position: 'fixed', top: '1480px', width: '35%', fontSize: '25px', right: '20px' }}>
        <span style={{ fontSize: '60px' }}>EMAILS</span>
        <br></br>
        <ul>
          {this.state.emails.map((mail, i) =>
            <li>{mail.Subject + ' From:' + mail.Sender}</li>
          )}
        </ul>
      </div>
    );
  }

};