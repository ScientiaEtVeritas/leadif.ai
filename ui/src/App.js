import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Container, Form, Header, Image, Loader } from 'semantic-ui-react';
import './App.css';
import { getDataFromUrl } from './services/api';
import PageMenu from './components/PageMenu';
import { APP_NAME } from './config/constants';


class EmailInput extends Component {
  state = { value: 'timo@usertimes.io' };

  static propTypes = {
    onData: PropTypes.func,
    onLoading: PropTypes.func
  }

  static propTypes = {
    onData: () => {},
    onLoading: () => {}
  }

  onSubmit = async () => {
    const { value } = this.state;
    const { onData, onLoading } = this.props;
    if (!value) return;
    const domain = value.split('@').pop();
    if (!domain) return;
    this.setState({ loading: true });
    onLoading();
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
          // label='Enter an email address'
          action={{ icon: 'search', onClick: this.onSubmit }}
          fluid
          name='input'
          type='email'
          value={value}
          loading={loading}
          disabled={loading}
          onChange={this.onChange}
          placeholder='someone@company.org'
        />
      </Form>
    );
  }
}

class Footer extends Component {
  render() {
    return (
      <Container textAlign='center' style={{ marginTop: 80 }}>
        &copy; leadif.ai – originated from the AI challenge by
        <Image src='images/uniserve.png' centered />
      </Container>
    )
  }
}

class App extends Component {
  state = { loading: false };

  onData = data => {
    this.setState({ data, loading: false });
  }

  onLoading = () => {
    this.setState({ loading: false });
  }

  render() {
    const { data, loading } = this.state;

    return (
      <div className="App">
        <PageMenu />

        <Container style={{ marginTop: 80, marginBottom: 80 }} text>
          <Header as='h1' textAlign='center'>
            This is { APP_NAME }
            <Header.Subheader>
              Lead Management with AI and Open Data
            </Header.Subheader>
          </Header>

          <p style={{ marginTop: 40, marginBottom: 40, textAlign: 'center' }}>
            Someone entered an email address on your website?<br />
            Find out more about their company below.
          </p>

          <EmailInput
            onData={this.onData}
            onLoading={this.onLoading}
          />

          {
            loading &&
            <Loader active inline='centered' style={{ marginTop: 80 }} size='huge'>
              Loading lead data...
            </Loader>
          }

          {
            data && <pre>{ JSON.stringify(data) }</pre>
          }


        </Container>

        <Footer />

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
