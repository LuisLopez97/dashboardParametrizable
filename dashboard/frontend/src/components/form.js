import React, { Component } from 'react'
import Axios from 'axios'

export class Form extends Component {
    constructor(props) {
        super(props)
    }

    state = {
        keyword: '0',
        idioma: '0',
    }

    handleSubmit = event => {
        event.preventDefault()
        const palabra = this.state.keyword;
        const idiom = this.state.idioma;
        Axios.post(`/test`, {
            keyword: palabra,
            idioma: idiom,
        })
            .then(res => {
                console.log(res);
                console.log(res.data)
                this.props.resetDatos()
                this.props.getDatos()
            }).catch(err => console.log(err))
        document.getElementById("btnEnviar").disabled = true;
        document.getElementById("btnEnviar").innerHTML = "Enviado";
        document.getElementById("btnEnviar").className = "btn btn-success";
        document.getElementById("spinner").className = "";
        document.getElementById("inputKey").disabled = true;
    };

    handleKeyChange = event => {
        this.setState({ keyword: event.target.value })
        document.getElementById("btnEnviar").className = "btn btn-primary"
    };

    handleIdiomChange = event => {
        this.setState({ idioma: event.target.value })
    }

    render() {
        return (
            <div>
                <div className="align-middle">
                    <form onSubmit={this.handleSubmit}>
                        {/* <form action="/test" method="POST"> */}
                        <p className="display-4 py-4 text-center">Iniciar Recoleccion</p>
                        <div className="form-group">
                            <label>Seleccione el idioma</label>
                            <select
                                className="form-control border border-primary"
                                onChange={this.handleIdiomChange}>
                                <option selected value="0">Español</option>
                                <option value="1">Ingles</option>
                            </select>
                        </div>
                        <div className="form-group text-center py-3">
                            <label>Palabra a buscar:</label>
                            <div className="border border-primary">
                                <input
                                    type='text'
                                    name="keyword"
                                    className="form-control"
                                    onChange={this.handleKeyChange}
                                    id="inputKey"
                                />
                            </div>
                        </div>
                        <div className="d-flex justify-content-center py-5">
                            <button
                                type="submit"
                                value="Submit"
                                id="btnEnviar"
                                className="d-none btn btn-primary">
                                Enviar
                                    </button>
                        </div>
                    </form>
                    <div className="d-none" id="spinner">
                        <div className="d-flex justify-content-center">
                            <div className="spinner-border py-5 px-5" role="status">
                                <span className="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div >
        )
    }
}

export default Form
