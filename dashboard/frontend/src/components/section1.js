import React, { Component } from 'react';
import Axios from 'axios';

// COMPONENTS
// import Tabla from "./tabla";
import Form from "./form";
import Tabla from "./tabla";

class Section1 extends Component {
    state = {
        loading: false,
        datos: [],
    };

    resetDatos = () => {
        this.setState({
            datos: [],
            loading: true,
        })
    }


    getDatos = () => {
        this.setState({ loading: true },
            () => {
                Axios.get('/static/prediccion.json', { timeout: 0 })
                    .then(
                        result => this.setState({
                            loading: false,
                            datos: [...result.data.slice(0, 10)],
                        }
                        )
                    );
            });
    }

    componentDidMount() {
        this.getDatos();
    }

    render() {
        return (
            <div className="my-5">
                <div className="card">
                    <div className="card-body">
                        <div className="container-fluid">
                            <div className="row">
                                <div className="col-md-12 col-lg-6 bg-light my-4">
                                    <Form resetDatos={this.resetDatos} getDatos={this.getDatos} />
                                </div>
                                <div className="col-md-12 col-lg-6 my-4">
                                    {
                                        this.state.loading ? <div id="spinner">
                                            <div className="d-flex justify-content-center">
                                                <div className="spinner-border py-5 px-5" role="status">
                                                    <span className="sr-only">Loading...</span>
                                                </div>
                                            </div>
                                        </div>
                                            : <Tabla datos={this.state.datos.slice(0, 10)} />
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Section1;