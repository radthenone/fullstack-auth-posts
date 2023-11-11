import { makeStyles } from 'tss-react/mui';

const footerStyles = makeStyles()(() => {
  return {
    base: {
      color: 'black',
      minHeight: '25px',
      height: '50px',
      backgroundColor: 'white',
    },
  };
});

export { footerStyles };
