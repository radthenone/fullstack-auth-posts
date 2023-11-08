import '../../App.css';
// import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';

import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AutoStories from '@mui/icons-material/AutoStories';
import NavMenu from 'components/header/NavMenu.tsx';
import SearchBar from 'components/header/SearchBar.tsx';

const pages = ['Products', 'Pricing', 'Blog'];
const userSettings = ['Profile', 'Account', 'Dashboard'];
const loginSettings = [...userSettings, 'Login'];
const logoutSettings = [...userSettings, 'Logout'];

type User = {
  name: string;
  avatar: string;
  email: string;
  password: string;
};

const initialUser: User = {
  name: 'Tom Cook',
  avatar: 'https://mui.com/static/images/avatar/2.jpg',
  email: 'X2MvD@example.com',
  password: '123456',
};

function Header() {
  const [user, setUser] = useState<null | User>();
  // const navigate = useNavigate();
  const [anchorElNav, setAnchorElNav] = useState<null | HTMLElement>(null);
  const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleLogin = (data: User) => {
    console.log('User zalogowany');
    setUser(data);
    // navigate('/');
  };

  const handleLogout = () => {
    console.log('User wylogowany');
    setUser(null);
    // navigate('/');
  };

  return (
    <header>
      <AppBar
        position="static"
        sx={{
          backgroundColor: 'white',
          display: 'flex',
          flexDirection: 'row',
        }}
      >
        <Container>
          <Toolbar disableGutters>
            <AutoStories
              sx={{
                display: { xs: 'none', md: 'flex', color: 'black' },
                mr: 1,
                fontSize: '42px',
              }}
            />
            <Typography
              variant="h6"
              noWrap
              component="a"
              sx={{
                mr: 2,
                display: { xs: 'none', md: 'flex' },
                fontFamily: 'monospace',
                fontWeight: 700,
                letterSpacing: '.3rem',
                color: 'inherit',
                textDecoration: 'none',
              }}
            ></Typography>
            <NavMenu
              anchorElNav={anchorElNav}
              handleCloseNavMenu={handleCloseNavMenu}
              pages={pages}
              handleOpenNavMenu={handleOpenNavMenu}
            />
            <SearchBar />
            <AutoStories sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
            <Typography
              variant="h5"
              noWrap
              // component={user ? 'a' : Link}
              // to={user ? '/login' : '/'}
              sx={{
                mr: 2,
                display: { xs: 'flex', md: 'none' },
                flexGrow: 1,
                fontFamily: 'monospace',
                fontWeight: 700,
                letterSpacing: '.3rem',
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              {user ? 'LOGOUT' : 'LOGO'}
            </Typography>
            <Box
              sx={{
                flexGrow: 1,
                display: { xs: 'none', md: 'flex', justifyContent: 'flex-start' },
              }}
            >
              {pages.map((page) => (
                <Button
                  key={page}
                  onClick={handleCloseNavMenu}
                  sx={{ my: 2, color: 'black', display: 'block' }}
                >
                  {page}
                </Button>
              ))}
            </Box>

            <Box sx={{ flexGrow: 0 }}>
              <Tooltip title="Open settings">
                {/*<IconButton onClick={user ? handleLogout : handleOpenUserMenu} sx={{ p: 0 }}>*/}
                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                  <Avatar alt="Remy Sharp" src={user ? user.avatar : ''} />
                </IconButton>
              </Tooltip>
              <Menu
                sx={{ mt: '45px' }}
                id="menu-appbar"
                anchorEl={anchorElUser}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}
              >
                {user
                  ? logoutSettings.map((setting) => (
                      <MenuItem
                        key={setting}
                        onClick={setting === 'Logout' ? () => handleLogout() : handleCloseUserMenu}
                      >
                        <Typography textAlign="center">{setting}</Typography>
                      </MenuItem>
                    ))
                  : loginSettings.map((setting) => (
                      <MenuItem
                        key={setting}
                        onClick={
                          setting === 'Login' ? () => handleLogin(initialUser) : handleCloseUserMenu
                        }
                      >
                        <Typography textAlign="center">{setting}</Typography>
                      </MenuItem>
                    ))}
              </Menu>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
    </header>
  );
}

export default Header;
