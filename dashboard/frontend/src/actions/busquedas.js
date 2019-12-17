import axios from 'axios';

import { GET_BUSQUEDAS, ADD_BUSQUEDAS } from './types';

// Metodo para obtener las busquedas
export const getBusquedas = () => dispatch => {
    axios.get('/db/busquedas/')
        .then(res => {
            dispatch({
                type: GET_BUSQUEDAS,
                payload: res.data
            });
        }).catch(err => console.log(err));
};

// Metodo para añadir una busqueda
export const addBusquedas = (busqueda) => dispatch => {
    axios.post('/db/busquedas/', busqueda)
        .then(res => {
            dispatch({
                type: ADD_BUSQUEDAS,
                payload: res.data
            });
        }).catch(err => console.log(err));
};