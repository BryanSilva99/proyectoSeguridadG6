import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Box, Typography } from '@mui/material';
import BlockIcon from '@mui/icons-material/Block';

export const UnauthorizedPage = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        backgroundColor: '#f5f5f5',
        padding: 3,
      }}
    >
      <BlockIcon sx={{ fontSize: 120, color: '#d32f2f', marginBottom: 2 }} />
      <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: '#d32f2f' }}>
        403
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom sx={{ color: '#666', textAlign: 'center' }}>
        Acceso No Autorizado
      </Typography>
      <Typography variant="body1" sx={{ color: '#888', marginBottom: 4, textAlign: 'center', maxWidth: 500 }}>
        No tienes permisos para acceder a esta página. Si crees que esto es un error, contacta al administrador.
      </Typography>
      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          onClick={() => navigate('/app/libros')}
          sx={{
            backgroundColor: 'black',
            color: 'white',
            borderRadius: '50px',
            padding: '10px 30px',
            '&:hover': {
              backgroundColor: '#333',
            },
          }}
        >
          Ir a Inicio
        </Button>
        <Button
          variant="outlined"
          onClick={() => navigate(-1)}
          sx={{
            borderColor: 'black',
            color: 'black',
            borderRadius: '50px',
            padding: '10px 30px',
            '&:hover': {
              borderColor: '#333',
              backgroundColor: 'rgba(0,0,0,0.04)',
            },
          }}
        >
          Volver
        </Button>
      </Box>
    </Box>
  );
};
