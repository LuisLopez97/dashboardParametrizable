import { GET_SEARCHS, DELETE_SEARCHS, ADD_SEARCHS } from '../actions/types.js';

const initialState = {
    searchs: [],
}

export default function (state = initialState, action) {
    switch (action.type) {
        case GET_SEARCHS:
            return {
                ...state,
                searchs: action.payload
            };
        case DELETE_SEARCHS:
            return {
                ...state,
                searchs: state.searchs.filter(search => search.id !== action.payload)
            };
        case ADD_SEARCHS:
            return {
                ...state,
                searchs: [...state.searchs, action.payload]
            }
        default:
            return state;
    }
}