import { ComponentPreview, Previews } from '@react-buddy/ide-toolbox';
import { PaletteTree } from './palette';
import App from '../App';
import Header from 'components/header/Header.tsx';
import Footer from 'components/footer/Footer.tsx';
import Tags from 'pages/Tags/Tags.tsx';
import PostCard from 'pages/Posts/PostCard.tsx';
import { PostCreate } from 'pages/Posts/PostCreate.tsx';

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
      <ComponentPreview path="/Tags">
        <Tags />
      </ComponentPreview>
      <ComponentPreview path="/PostCard">
        <PostCard />
      </ComponentPreview>
      <ComponentPreview path="/PostCreate">
        <PostCreate />
      </ComponentPreview>
      <ComponentPreview path="/ComponentPreviews">
        <ComponentPreviews />
      </ComponentPreview>
    </Previews>
  );
};

export default ComponentPreviews;
