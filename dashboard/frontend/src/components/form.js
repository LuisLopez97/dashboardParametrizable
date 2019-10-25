import React, { Component } from 'react'

export class Form extends Component {

    constructor(props) {
        super(props)

        this.state = {
            keyWord: ''
        }
    }

    handleSubmit = event => {
        console.log("hola")
        event.preventDefault()
        const { keyWord } = this.state;
        const search = { keyWord };
        const conf = {
            method: "post",
            body: JSON.stringify(search),
            headers: new Headers({ "Content-Type": "application/json" })
        };
        document.getElementById("btnEnviar").disabled = true;
        document.getElementById("btnEnviar").innerHTML = "Enviado";
        document.getElementById("btnEnviar").className = "btn btn-success";
        document.getElementById("spinner").className = "";
        document.getElementById("inputKey").disabled = true;
    };

    handlekeyWordChange = (event) => {
        this.setState({
            keyWord: event.target.value
        })
        document.getElementById("btnEnviar").className = "btn btn-primary"
    };

    render() {
        return (
            <div>
                <nav>
                    <div className="nav nav-tabs" id="nav-tab" role="tablist">
                        <a className="nav-item nav-link active" id="nav-home-tab" data-toggle="tab" href="#nav-home" role="tab" aria-controls="nav-home" aria-selected="true">Español</a>
                        <a className="nav-item nav-link" id="nav-profile-tab" data-toggle="tab" href="#nav-profile" role="tab" aria-controls="nav-profile" aria-selected="false">Ingles</a>
                    </div>
                </nav>
                <div className="tab-content" id="nav-tabContent">
                    <div className="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
                        <div className="align-middle">
                            <form onSubmit={this.handleSubmit}>
                                <p className="display-4 py-4 text-center">Iniciar Recoleccion</p>
                                <div className="form-group text-center py-3">
                                    <label>Palabra a buscar:</label>
                                    <div className="border border-primary">
                                        <input
                                            type='text'
                                            value={this.state.keyWord}
                                            onChange={this.handlekeyWordChange} className="form-control"
                                            id="inputKey"
                                            placeholder="#PalabraDeInteres"
                                        />
                                    </div>
                                </div>
                                <div className="d-flex justify-content-center py-5">
                                    <button
                                        type="submit"
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

                    </div>

                    <div className="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">

                        <div className="align-middle">
                            <form onSubmit={this.handleSubmit}>
                                <p className="display-4 py-4 text-center">Iniciar Recoleccion</p>
                                <div className="form-group text-center py-3">
                                    <label>Palabra a buscar:</label>
                                    <input
                                        type='text'
                                        value={this.state.keyWord}
                                        onChange={this.handlekeyWordChange} className="form-control"
                                        id="inputKey"
                                        placeholder="#PalabraDeInteres"
                                    />
                                </div>
                                <div className="d-flex justify-content-center py-5">
                                    <button
                                        type="submit"
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

                    </div>
                </div>

            </div>
        )
    }
}

export default Form
