import React, { Component } from 'react';
import './Email.css';

export default class Email extends Component {
  constructor() {
    super();
    this.state = {
      emails: [],
      d:false
    };
  }

  componentDidMount() {
    this.ckMail()
    setInterval(() => {
      this.ckMail()
    }, 1000)
  }

  ckMail(){
    fetch('http://127.0.0.1:5000/checkForEmail')
      .then(response => response.json())
      .then(data=>{
        console.log(data)
        if(data['email']==true){
          this.getMail()
        }
      })
  }

  showMail(){
    this.setState({d: true})
    setTimeout(() => {
      this.setState({ d: false })
    }, 15000)
  }

  getMail() {
    fetch('http://127.0.0.1:5000/readEmail')
      .then(response => response.json())
      .then(data =>{
        this.setState({emails:data['email']})
        this.showMail()
      })
      .catch((error) => {
        console.log(error);
      })
  }

  render() {
    return (
      <div>
        {this.state.d &&
          <div style={{ position: 'fixed', top: '1540px', width: '40%', fontSize: '25px', right: '40px' }} className="fadeIn">
            <span style={{ fontSize: '60px' }}>EMAILS</span>
            <br></br>
            <ul>
              {this.state.emails.map((mail, i) =>
                <li key={i}>{mail.Subject + ' From:' + mail.Sender}</li>
              )}
            </ul>
          </div>
        }

      </div>
    );
  }

};