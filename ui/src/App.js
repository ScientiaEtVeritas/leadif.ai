import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { Container, Form, Header, Image, Loader, Table, Icon, Flag } from 'semantic-ui-react';
import './App.css';
import { getDataFromUrl } from './services/api';
import PageMenu from './components/PageMenu';
import { APP_NAME } from './config/constants';
import SocialButtons from './components/SocialButtons';
import Tags from './components/Tags';

const DEBUG = false;


class EmailInput extends Component {
  state = { value: DEBUG ? 'timo@usertimes.io' : '' };

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
      <Container textAlign='center' style={{ marginTop: 80, marginBottom: 20 }}>
        &copy; leadif.ai – originated from the AI challenge by
        <Image src='images/uniserve.png' centered />
      </Container>
    )
  }
}

class WZ extends Component {
  render() {
    const { data } = this.props;

    const getTop3 = (code) => code.classes
      .map((c, idx) => ({
        probability: code.probabilities[idx],
        class: c
      }))
      .sort((a, b) => b.probability - a.probability)
      .filter((_, idx) => idx < 3);

    const sections = getTop3(data.section);
    const codes = getTop3(data.code);

    // return JSON.stringify(sections, null, 2)
    return (
      <Table celled collapsing basic='very' compact>
        <Table.Body>
          { sections.map((section, idx) => (
            <Table.Row key={idx}>
              <Table.Cell>
                <strong>{ section.class }</strong>
              </Table.Cell>
              <Table.Cell>
                { Math.round(section.probability * 100) }%
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    )
  }
}

class DataTable extends Component {
  static propTypes = {
    data: PropTypes.object.isRequired
  }

  render() {
    const { data } = this.props;
    let { company, url } = data;

    // Use the URL as fallback for the name.
    company = company || url;

    const rows = [
      {
        key: 'WZ',
        value: data.wz && <WZ data={data.wz} />
      },
      {
        key: 'Address',
        value: data.address[0] && (
          <span>
            { data.address[0].street } <br/>
            { data.address[0].city } <br/>
            { data.address[0].phone } <br/>
          </span>
        )
      },
      {
        key: 'Number of employees',
        value: data.size
      },
      {
        key: 'Language',
        value: data.language && (
          <span>
            <Flag name={data.language} style={{ marginRight: 8 }} />
            { data.language.toUpperCase() }
          </span>
        )
      },
      {
        key: 'Social',
        value: data.social && <SocialButtons accounts={data.social} />
      },
      {
        key: 'Tags',
        value: data.tags && <Tags tags={data.tags} />
      },
    ];

    return (
      <Table> 
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell colSpan='2'>
              { company }
              <a href={url} style={{ marginLeft: 8 }}>
                <Icon name='external' style={{ color: '#ddd' }} />
              </a>
            </Table.HeaderCell>
          </Table.Row>
        </Table.Header>  
        <Table.Body>

          {
            rows
              .filter(row => !!row.value)
              .map((row, idx) => (
                <Table.Row key={idx}>
                  <Table.Cell collapsing>
                    <strong>{ row.key }</strong>
                  </Table.Cell>
                  <Table.Cell>
                    { row.value }
                  </Table.Cell>
                </Table.Row>    
              ))
          }

        </Table.Body>
      </Table>
    );
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
            data && <DataTable data={data} />
          }

          {
            DEBUG && data && <pre>{ JSON.stringify(data, null, 2) }</pre>
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
