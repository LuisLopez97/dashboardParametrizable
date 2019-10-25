import React, { Component } from 'react';
import Axios from 'axios';
import Datatable from 'react-data-table-component';

import Datos from './Data/Datos';


class DataTable extends Component {


    state = {
        loading: true,
        searchs: [],
    }

    componentDidMount() {
        this.getData();
    }
    getData = () => {
        this.setState({ loading: true }, () => {
            Axios.get('/static/tweetsp.json/')
                .then(result => this.setState({
                    loading: false,
                    searchs: [...result.data],
                    finalpage: false,
                }));
        });
    }


    render() {
        const columns = [
            {
                name: 'Sentimiento',
                selector: 'airline_sentiment',
                sortable: true,
            },
            {
                name: 'Razon del Sentimiento',
                selector: 'negativereason',
                sortable: true,
                wrap: true,
            },
            {
                name: 'Texto',
                selector: 'text',
                sortable: false,
                wrap: true,
            },
            {
                name: 'Usuario',
                selector: 'name',
                sortable: true,
            },
            {
                name: 'Ubicacion',
                selector: 'tweet_location',
                sortable: true,
            },
        ];

        return (
            <div className="text-center">
                <h2 className="mt-2">Tabla de Datos</h2>
                {this.state.loading ? <div className="d-flex justify-content-center">
                    <div className="spinner-border py-5 px-5" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
                    :
                    <Datatable
                        columns={columns}
                        data={this.state.searchs}
                        pagination
                    />
                }
            </div>
        )
    }
}


export default DataTable;