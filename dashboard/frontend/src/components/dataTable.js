import React, { Component } from 'react';
import Axios from 'axios';
import Datatable from 'react-data-table-component';



class DataTable extends Component {


    state = {
        loading: true,
        searchs: [],
    }

    componentDidMount() {
        this.getData()
    }
    getData = () => {
        this.setState({ loading: true }, () => {
            Axios.get('/static/prediccion.json')
                .then(result => this.setState({
                    loading: false,
                    searchs: [...result.data],
                }));
        });
    }


    render() {
        const columns = [
            {
                name: 'Usuario',
                selector: 'Author',
                sortable: true,
            },
            {
                name: 'Texto',
                selector: 'Text',
                sortable: false,
                wrap: true,
            },
            {
                name: 'Fecha',
                selector: 'Date',
                sortable: true,
            },
            {
                name: 'Sentimiento',
                selector: 'Sentiment',
                sortable: true,
            },
        ];

        return (
            <div className="">
                {this.state.loading ? <div className="d-flex justify-content-center">
                    <div className="spinner-border py-5 px-5" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
                    :
                    <div className="my-2 mx-4 p-0">
                        <div className="container">
                            <h2 className="text-center">Tabla de Datos</h2>
                            <Datatable
                                columns={columns}
                                data={this.state.searchs}
                                pagination
                                responsive
                                striped="true"
                                highlightOnHover="true"
                                noHeader
                                dense
                                paginationPerPage="10"
                            />
                        </div>
                    </div>
                }
            </div>
        )
    }
}


export default DataTable;