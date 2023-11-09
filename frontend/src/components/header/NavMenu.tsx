import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { MouseEvent } from 'react';
import { useTheme } from '@material-ui/core/styles';
import { headerStyles } from 'styles/app/headerStyles.tsx';

type NavMenuProps = {
  anchorElNav: null | HTMLElement;
  handleCloseNavMenu: () => void;
  pages: string[];
  handleOpenNavMenu: (event: MouseEvent<HTMLElement>) => void;
};

function NavMenu({ anchorElNav, handleCloseNavMenu, pages, handleOpenNavMenu }: NavMenuProps) {
  const theme = useTheme();
  const classes = headerStyles(theme);
  return (
    <Box className={classes.navMenu}>
      <IconButton
        size="large"
        aria-label="account of current user"
        aria-controls="menu-appbar"
        aria-haspopup="true"
        onClick={handleOpenNavMenu}
        color="inherit"
      >
        {window.innerWidth <= 1200 ? <MenuIcon /> : <Typography></Typography>}
      </IconButton>
      <Menu
        id="menu-appbar"
        anchorEl={anchorElNav}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
        open={Boolean(anchorElNav)}
        onClose={handleCloseNavMenu}
        sx={{
          display: { xs: 'block', md: 'none' },
        }}
      >
        {pages.map((page) => (
          <MenuItem key={page} onClick={handleCloseNavMenu}>
            <Typography textAlign="center">{page}</Typography>
          </MenuItem>
        ))}
      </Menu>
    </Box>
  );
}

export default NavMenu;
