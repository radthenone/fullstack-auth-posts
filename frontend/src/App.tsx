import Header from 'components/Header.tsx';
import Footer from 'components/Footer.tsx';
import Main from 'components/Main.tsx';
import './App.css';
import { BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <>
      <BrowserRouter>
        <Header />
        <Main />
        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;
