import React, { Component } from 'react';
import Axios from 'axios';

// COMPONENTS
// import Tabla from "./tabla";
import Form from "./form";

class Section1 extends Component {
    state = {
        loading: true,
        datos: [],
    };

    resetDatos = () => {
        this.setState({ datos: [] })
    }

    getDatos = () => {
        this.setState({ loading: true }, () => {
            Axios.get('/static/tweetsp.json/', { timeout: 0 })
                .then(result => this.setState({
                    loading: false,
                    datos: [...result.data.slice(0, 10)],
                }));
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
                                <div className="col-md-6 bg-light my-4">
                                    <Form resetDatos={this.resetDatos} getDatos={this.getDatos} />
                                </div>
                                <div className="col-md-6 my-4">
                                    {this.state.loading ? <p>Loading...</p>
                                        : <ul>
                                            {this.state.datos.map(dato => (
                                                <li>{dato.name}</li>
                                            ))}
                                        </ul>}
                                    {/* <Tabla /> */}
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