import React, { Component } from 'react';
import { Menu } from 'semantic-ui-react';
import { PRIMARY_COLOR } from '../config/style';
import { APP_NAME } from '../config/constants';

export default class PageMenu extends Component {
  render() {
    return (
      <Menu stackable size='large' inverted style={{
        background: PRIMARY_COLOR
      }}>
        <Menu.Item>
          {/* <img src='/images/logo.png' /> */}
          { APP_NAME }
        </Menu.Item>
      </Menu>
    )
  }
}
