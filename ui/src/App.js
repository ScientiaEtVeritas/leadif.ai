import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import { Button, Menu, Input, Container, Form } from 'semantic-ui-react';
import { getDataFromUrl } from './services/api';

class PageMenu extends Component {
  render() {
    return (
      <Menu stackable>
        <Menu.Item>
          {/* <img src='/images/logo.png' /> */}
          Leadif.ai
        </Menu.Item>
      </Menu>
    )
  }
}

class EmailInput extends Component {
  state = { value: 'timo@usertimes.io' };

  onSubmit = () => {
    const { value } = this.state;
    if (!value) return;
    const domain = value.split('@').pop();
    if (!domain) return;
    this.setState({ loading: true });
    const data = getDataFromUrl(domain);

    console.log('submit', domain, data);
    this.setState({ loading: false });
  }

  onChange = (evt, { value }) => {
    this.setState({ value });
  }

  render() {
    const { value, loading } = this.state;

    return (
      <Form>
        <Form.Input
          action={{ icon: 'search', onClick: this.onSubmit }}
          fluid
          name='input'
          type='email'
          value={value}
          loading={loading}
          disabled={loading}
          onChange={this.onChange}
        />
      </Form>
    );
  }
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <PageMenu />

        <Container>
          <EmailInput />

        </Container>

        {/* <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header> */}
      </div>
    );
  }
}

export default App;
