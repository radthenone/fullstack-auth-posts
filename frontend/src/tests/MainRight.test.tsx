import { render } from '@testing-library/react';
import MainRight from 'components/main/MainRight.tsx';
import { expect, it, describe } from 'vitest';

describe('MainRight', () => {
  it('renders "Hello right" in MainRight component', () => {
    const xhtml = render(<MainRight />);
    xhtml.getByText('Hello right');
    expect(xhtml).toBeTruthy();
  });
});
