import Header from 'components/header/Header.tsx';
import Footer from 'components/footer/Footer.tsx';
import MainLeft from 'components/main/MainLeft.tsx';
import { BrowserRouter } from 'react-router-dom';
import MainRight from 'components/main/MainRight.tsx';
import Box from '@mui/material/Box';
import { useAppStyles } from 'styles/app/appStyles.tsx';
import { ThemeProvider, useTheme } from '@material-ui/core/styles';

function App() {
  const theme = useTheme();
  const classes = useAppStyles(theme);
  return (
    <>
      <BrowserRouter>
        <Header />
        <Box className={classes.main}>
          <Box className={classes.mainSide} />
          <Box className={classes.mainLeft}>
            <MainLeft />
          </Box>
          <Box className={classes.mainRight}>
            <MainRight />
          </Box>
          <Box className={classes.mainSide} />
        </Box>
        <Footer />
      </BrowserRouter>
      <ThemeProvider theme={theme} children={classes.root} />
    </>
  );
}

export default App;
