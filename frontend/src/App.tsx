import Header from 'components/header/Header.tsx';
import Footer from 'components/footer/Footer.tsx';
import MainLeft from 'components/main/MainLeft.tsx';
import { BrowserRouter } from 'react-router-dom';
import MainRight from 'components/main/MainRight.tsx';
import Box from '@mui/material/Box';
import { useAppStyles } from 'styles/app/appStyles.tsx';
import { ThemeProvider } from '@mui/material';
import { StyledEngineProvider } from '@mui/material/styles';
import { useTheme } from '@emotion/react';

function App() {
  const theme = useTheme();
  const { classes } = useAppStyles();
  return (
    <StyledEngineProvider injectFirst>
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
      <ThemeProvider theme={theme} />
    </StyledEngineProvider>
  );
}

export default App;
