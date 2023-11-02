import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { MouseEvent } from 'react';

type NavMenuProps = {
  anchorElNav: null | HTMLElement;
  handleCloseNavMenu: () => void;
  pages: string[];
  handleOpenNavMenu: (event: MouseEvent<HTMLElement>) => void;
};

function NavMenu({ anchorElNav, handleCloseNavMenu, pages, handleOpenNavMenu }: NavMenuProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        '@media (max-width: 1200px)': {
          xs: 'flex',
          md: 'none',
          color: 'black',
        },
      }}
    >
      <IconButton
        size="large"
        aria-label="account of current user"
        aria-controls="menu-appbar"
        aria-haspopup="true"
        onClick={handleOpenNavMenu}
        color="inherit"
      >
        {window.innerWidth <= 1200 ? <MenuIcon /> : <Typography>Menu</Typography>}
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
