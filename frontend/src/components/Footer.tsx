import { Grid, Container } from '@mui/material';
import './global.css';

function Footer() {
  return (
    <>
      <footer>
        <Grid container justifyContent="center" textAlign="center">
          <Grid item xs={12}>
            <Container maxWidth="lg">
              <p>Copyright © 2023</p>
            </Container>
          </Grid>
        </Grid>
      </footer>
    </>
  );
}

export default Footer;
