import { createTheme, makeStyles } from '@material-ui/core/styles';

const theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 640,
      md: 1024,
      lg: 1280,
      xl: 1920,
    },
  },
});

const useAppStyles = makeStyles({
  body: {
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#fcfcfc',
  },
  root: {
    height: '100%',
    width: '100%',
    margin: 0,
    padding: 0,
  },
  main: {
    display: 'flex',
    flexDirection: 'row',
    padding: 10,
    minHeight: '100vh',
    flex: 1,
    alignItems: 'stretch',
  },
  mainSide: {
    flexGrow: 1,
    margin: 1,
    minWidth: 300,
    [theme.breakpoints.between('xs', 'lg')]: {
      display: 'none',
    },
  },
  mainLeft: {
    flexGrow: 2,
    margin: 1,
    minWidth: 800,
    boxShadow:
      'rgba(0, 0, 0, 0.2) 0 2px 4px -1px, rgba(0, 0, 0, 0.14) 0 4px 5px 0, rgba(0, 0, 0, 0.12) 0 1px 10px 0',
    backgroundColor: 'white',
    color: 'black',
    borderRadius: 10,
    padding: 10,
    [theme.breakpoints.between('xs', 'md')]: {
      flexGrow: 1,
      minWidth: 0,
    },
  },
  mainRight: {
    flexGrow: 1,
    margin: 1,
    minWidth: 500,
    boxShadow:
      'rgba(0, 0, 0, 0.2) 0 2px 4px -1px, rgba(0, 0, 0, 0.14) 0 4px 5px 0, rgba(0, 0, 0, 0.12) 0 1px 10px 0',
    backgroundColor: 'white',
    color: 'black',
    borderRadius: 10,
    padding: 10,
    [theme.breakpoints.between('xs', 'md')]: {
      display: 'none',
    },
  },
});

export { useAppStyles };
