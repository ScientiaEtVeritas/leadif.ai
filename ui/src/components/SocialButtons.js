
import React, { Component } from 'react';
import { Button } from 'semantic-ui-react';


export default class SocialButtons extends Component {
  render() {
    const { accounts } = this.props;
    return Object.keys(accounts).map((platform, idx) => {
      const allowedColors = ["red","orange","yellow","olive","green","teal","blue","violet","purple","pink","brown","grey","black","facebook","google plus","instagram","linkedin","twitter","vk","youtube"];
      const link = `https://${platform}.com/${accounts[platform]}`;
      const label = platform[0].toUpperCase() + platform.substring(1);
      const color = allowedColors.includes(platform) ? platform : null;
      return (
        <Button
          key={idx}
          as={'a'}
          href={link}
          target='_blank' rel='noopener'
          size='large'
          // circular
          color={color}
          icon={platform}
          aria-label={label}
        />
      );
    });
  }
}
