import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import { Button, Menu, Input, Container, Form } from 'semantic-ui-react';
import { getDataFromUrl } from './services/api';
import PropTypes from 'prop-types';

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

  static propTypes = {
    onData: PropTypes.func
  }

  static propTypes = {
    onData: () => {}
  }

  onSubmit = async () => {
    const { value } = this.state;
    const { onData } = this.props;
    if (!value) return;
    const domain = value.split('@').pop();
    if (!domain) return;
    this.setState({ loading: true });
    const { data } = await getDataFromUrl(domain);
    onData(data);
    this.setState({ loading: false });
  }

  onChange = (evt, { value }) => {
    this.setState({ value });
  }

  render() {
    const { value, loading} = this.state;

    return (
      <Form>
        <Form.Input
          label='Enter an email address'
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
  state = {};

  onData = data => {
    this.setState({ data });
  }

  render() {
    const { data } = this.state;

    return (
      <div className="App">
        <PageMenu />

        <Container>
          <EmailInput onData={this.onData} />

          {
            data && <pre>{ JSON.stringify(data) }</pre>
          }


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
