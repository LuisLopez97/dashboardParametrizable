import { GET_SEARCHS, DELETE_SEARCHS, ADD_SEARCHS } from './types';
import Axios from 'axios';

// GET SEARCHS
export const getSearchs = () => dispatch => {
    Axios.get('/static/tweetsp.json/')
        .then(res => {
            dispatch({
                type: GET_SEARCHS,
                payload: res.data.slice(0, 5),
            });
        })
        .catch(err => console.log(err));
};

export const getData = (loading) => dispatch => {
    Axios.get('/static/tweetsp.json/')
        .then(res => {
            loading = false;
            dispatch({
                type: GET_SEARCHS,
                payload: res.data, loading
            });
        })
        .catch(err => console.log(err));
};

// DELETE SEARCH
export const deleteSearchs = (id) => dispatch => {
    Axios.delete(`/api/keywords/${id}/`)
        .then(res => {
            dispatch({
                type: DELETE_SEARCHS,
                payload: id
            });
        })
        .catch(err => console.log(err));
};

//ADD SEARCH
export const addSearchs = search => dispatch => {
    Axios.post("/api/keywords/", search)
        .then(res => {
            dispatch({
                type: ADD_SEARCHS,
                payload: res.data
            });
        })
        .catch(err => console.log(err));
};