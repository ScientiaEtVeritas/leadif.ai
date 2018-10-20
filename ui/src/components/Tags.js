
import React, { Component } from 'react';
import { Label } from 'semantic-ui-react';


export default class Tags extends Component {
  render() {
    const { tags } = this.props;
    return tags.map((tag, idx) => {
      return (
        <Label
          size='huge'
          key={idx}
          content={tag}
        />
      );
    });
  }
}
