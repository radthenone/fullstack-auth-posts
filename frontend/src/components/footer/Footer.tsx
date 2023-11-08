import { Grid, Container } from '@mui/material';
import { footerStyles } from 'styles/app/footerStyles.tsx';
import { useTheme } from '@material-ui/core/styles';

function Footer() {
  const theme = useTheme();
  const classes = footerStyles(theme);
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
