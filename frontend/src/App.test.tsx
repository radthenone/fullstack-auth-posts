import { render } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders Hello World', () => {
    const { getByText } = render(<App />);
    const helloWorldElement = getByText('Hello World');
    expect(helloWorldElement).toBeInTheDocument();
  });
});
