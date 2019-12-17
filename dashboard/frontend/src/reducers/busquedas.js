import { GET_BUSQUEDAS, ADD_BUSQUEDAS } from '../actions/types.js';

const initialState = {
    busquedas: []
}

export default function (state = initialState, action) {
    switch (action.type) {
        case GET_BUSQUEDAS:
            return {
                ...state,
                busquedas: action.payload
            };
        case ADD_BUSQUEDAS:
            return {
                ...state,
                busquedas: [...state.busquedas, action.payload]
            };
        default:
            return state;
    }
}