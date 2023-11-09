import { makeStyles } from '@material-ui/core/styles';
import { theme } from 'styles/app/appStyles.tsx';

const headerStyles = makeStyles({
  navMenu: {
    display: 'flex',
    color: 'black',
    [theme.breakpoints.only('md')]: {
      display: 'none',
    },
  },
});

export { headerStyles };
