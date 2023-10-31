import Header from 'components/Header.tsx';
import Footer from 'components/Footer.tsx';
import MainLeft from 'components/MainLeft.tsx';
import './App.css';
import { BrowserRouter } from 'react-router-dom';
import MainRight from 'components/MainRight.tsx';
import Box from '@mui/material/Box';

function App() {
  return (
    <>
      <BrowserRouter>
        <Header />
        <Box
          className="main"
          sx={{
            display: 'flex',
            flexDirection: 'row',
            p: 1,
          }}
        >
          <Box sx={{ flexGrow: 1, m: 1, minWidth: 300 }} />
          <Box sx={{ flexGrow: 2, m: 1, minWidth: 800 }} className="main-left">
            <MainLeft />
          </Box>{' '}
          <Box sx={{ flexGrow: 1, m: 1, minWidth: 500 }} className="main-right">
            <MainRight />
          </Box>
          <Box sx={{ flexGrow: 1, m: 1, minWidth: 300 }} />
        </Box>
        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;
