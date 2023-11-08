import { ComponentPreview, Previews } from '@react-buddy/ide-toolbox';
import { PaletteTree } from './palette';
import App from '../App';
import Header from 'components/header/Header.tsx';
import Footer from 'components/footer/Footer.tsx';

const ComponentPreviews = () => {
  return (
    <Previews palette={<PaletteTree />}>
      <ComponentPreview path="/App">
        <App />
      </ComponentPreview>
      <ComponentPreview path="/Header">
        <Header />
      </ComponentPreview>
      <ComponentPreview path="/Footer">
        <Footer />
      </ComponentPreview>
    </Previews>
  );
};

export default ComponentPreviews;
