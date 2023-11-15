// import { ChangeEvent, useState, useRef } from 'react';
// import { useNavigate, Link } from 'react-router-dom';
// import {
//   Button,
//   CircularProgress,
//   Container,
//   Box,
//   Typography,
//   Grid,
//   TextField,
//   FormControlLabel,
//   Checkbox,
//   Alert,
// } from '@mui/material';
// // import { useLoginMutation } from 'app/services/old/authAPI.tsx';
//
// const LoginPage = () => {
//   const emailRef = useRef<HTMLInputElement>(null);
//   const passwordRef = useRef<HTMLInputElement>(null);
//   const [error, setError] = useState(false);
//   const navigate = useNavigate();
//   // const [login, { isLoading }] = useLoginMutation();
//
//   const loginRequest = {
//     email: emailRef.current?.value ?? '',
//     password: passwordRef.current?.value ?? '',
//   };
//
//   if (!loginRequest) {
//     setError(true);
//   }
//
//   const handleSubmit = async (event: ChangeEvent<HTMLFormElement>) => {
//     event.preventDefault();
//     login(loginRequest);
//     navigate('/');
//   };
//
//   return (
//     <>
//       <Container component="main" maxWidth="sm">
//         <Box
//           sx={{
//             display: 'flex',
//             flexDirection: 'column',
//             alignItems: 'center',
//           }}
//         >
//           <Typography component="h1" variant="h5">
//             Sign in
//           </Typography>
//           <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
//             <TextField
//               margin="normal"
//               required
//               fullWidth
//               id="email"
//               label="Email Address"
//               name="email"
//               autoComplete="email"
//               autoFocus
//               inputRef={emailRef}
//             />
//             <TextField
//               margin="normal"
//               required
//               fullWidth
//               name="password"
//               label="Password"
//               type="password"
//               id="password"
//               autoComplete="current-password"
//               inputRef={passwordRef}
//             />
//             <FormControlLabel
//               control={<Checkbox value="remember" color="primary" />}
//               label="Remember me"
//             />
//             <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
//               {isLoading ? <CircularProgress size={24} /> : 'Login'}
//             </Button>
//             <Grid container>
//               <Grid item xs>
//                 <Link to="#">Forgot password?</Link>
//               </Grid>
//               <Grid item>
//                 <Link to="/register">{"Don't have an account? Sign Up"}</Link>
//               </Grid>
//             </Grid>
//             {error && <Alert severity="error">Error: Invalid credentials</Alert>}
//           </Box>
//         </Box>
//       </Container>
//     </>
//   );
// };
//
// export default LoginPage;
