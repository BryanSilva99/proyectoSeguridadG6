import { createBrowserRouter, Navigate } from 'react-router-dom'

import {SideBar, loader as sidebarLoader} from '../Components/SideBar/SideBar';
import {LoginPage, loader as loginLoader} from '../Pages/LoginPage/LoginPage';
import {RegistrarsePage, loader as registerLoader} from '../Pages/RegistrarsePage/RegistrarsePage';
import { NotFoundPage } from '../Pages/NotFoundPage/NotFoundPage';
import {LibrosPage} from '../Pages/LibrosPage/LibrosPage';
import {LibroPage, loader as libroLoader} from '../Pages/LibroPage/LibroPage';
import {UsuariosPage, loader as loaderUsuarios} from '../Pages/UsuariosPage/UsuariosPage';
import {PerfilPage, loader as loaderPerfil} from '../Pages/PerfilPage/PerfilPage';
import {PrestamosPage, loader as loaderPrestamos} from '../Pages/PrestamosPage/PrestamosPage';
import {PrestamoPage, loader as loaderPrestamo} from '../Pages/PrestamoPage/PrestamoPage';
import {CanastaPage, loader as loaderCanasta} from '../Pages/CanastaPage/CanastaPage';
import {PanelAdministracionPage, loader as loaderPanel} from '../Pages/PanelAdministracionPage/PanelAdministracionPage';
import {UnauthorizedPage} from '../Pages/UnauthorizedPage/UnauthorizedPage';


const routes = createBrowserRouter([
    
    {
      // Redirect root to explicit login path
      path: "/",
      element: <Navigate to="/login" replace />
    },
    {
      path: "/login",
      element: <LoginPage />,
      loader: loginLoader
    },
    {
      path: "/register",
      element: <RegistrarsePage />,
      loader: registerLoader
    },
    {
      path: "/unauthorized",
      element: <UnauthorizedPage />
    },
    {
      // Authenticated app shell - no userId in URL; we read current user from localStorage
      path: "/app",
      element: <SideBar />,
      loader: sidebarLoader,
      children: [
        { path: "libros", element: <LibrosPage /> },
        { path: "libros/:libroId", element: <LibroPage />, loader: libroLoader },
        { path: "usuarios", element: <UsuariosPage />, loader: loaderUsuarios },
        { path: "perfil", element: <PerfilPage />, loader: loaderPerfil },
        { path: "prestamos", element: <PrestamosPage />, loader: loaderPrestamos },
        { path: "prestamos/:prestamoId", element: <PrestamoPage />, loader: loaderPrestamo },
        { path: "canasta", element: <CanastaPage />, loader: loaderCanasta },
        { path: "panel-administracion", element: <PanelAdministracionPage />, loader: loaderPanel }
      ]
    }
    ,
    {
      path: '*',
      element: <NotFoundPage />
    }
]);


export default routes;