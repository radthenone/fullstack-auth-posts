import { Grid, Container } from '@mui/material';
import { footerStyles } from 'styles/app/footerStyles.tsx';

function Footer() {
  const { classes } = footerStyles();
  return (
    <>
      <footer className={classes.base}>
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
