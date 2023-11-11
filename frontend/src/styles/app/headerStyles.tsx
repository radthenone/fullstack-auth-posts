import { makeStyles } from 'tss-react/mui';
import { theme } from 'styles/app/appStyles.tsx';

const headerStyles = makeStyles()(() => {
  return {
    navMenu: {
      display: 'flex',
      color: 'black',
      [theme.breakpoints.only('md')]: {
        display: 'none',
      },
    },
  };
});

export { headerStyles };
