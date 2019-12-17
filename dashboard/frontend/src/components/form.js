import React, { Component } from 'react';
import { connect } from 'react-redux';
import propTypes from 'prop-types';
import { addBusquedas } from '../actions/busquedas';
import Axios from 'axios';



export class Form extends Component {
    constructor(props) {
        super(props)
    }

    state = {
        keyword: '',
        keywordError: '',
        idioma: 'es',
        idiomaError: '',
        tweets: 100,
        tweetsError: '',
    }

    static propTypes = {
        addBusquedas: propTypes.func.isRequired
    }

    guardarDB = () => {
        const lenguaje = this.state.idioma;
        const palabraclave = this.state.keyword;
        const cantidadtweets = parseInt(this.state.tweets);
        const busqueda = { lenguaje, palabraclave, cantidadtweets };
        this.props.addBusquedas(busqueda);

    }
    handleSubmit = event => {
        event.preventDefault()
        const palabra = this.state.keyword;
        const idiom = this.state.idioma;
        const twets = this.state.tweets;
        let esValido = this.validacion();
        if (esValido) {
            this.setState({
                keywordError: '',
                idiomaError: '',
                tweetsError: '',
            })
            this.props.resetDatos()
            document.getElementById("Erroridioma").className = "d-none";
            document.getElementById("Errorkeyword").className = "d-none";
            document.getElementById("Errortweets").className = "d-none";
            this.guardarDB()
            Axios.post(`/test`, {
                keyword: palabra,
                idioma: idiom,
                tweets: twets,
            })
                .then(res => {
                    console.log(res);
                    console.log(res.data)
                    this.props.getDatos()
                    this.desbloquearBoton()
                }).catch(err => console.log(err))
            document.getElementById("btnEnviar").disabled = true;
            document.getElementById("btnEnviar").innerHTML = "Enviado";
            document.getElementById("btnEnviar").className = "btn btn-success";
            document.getElementById("inputKey").disabled = true;
        }
    };

    validacion = () => {
        let keyword = this.state.keyword
        let idioma = this.state.idioma
        let tweets = this.state.tweets
        if (idioma == "") {
            this.setState({ idiomaError: 'No puedes dejar vacio el idioma' })
            document.getElementById("Erroridioma").className = "alert alert-danger text-danger";
            return false
        }
        if (idioma !== 'es' && idioma !== 'en') {
            this.setState({ idiomaError: 'El idioma tiene que ser "es" o "en"' })
            document.getElementById("Erroridioma").className = "alert alert-danger text-danger"
            return false
        }
        if (keyword == "") {
            this.setState({ keywordError: 'No puede enviar palabras vacias', })
            document.getElementById("Errorkeyword").className = "alert alert-danger text-danger";
            return false
        }
        if (keyword.match(/^\s*$/)) {
            this.setState({ keywordError: 'No puede tener espacios en blanco', })
            document.getElementById("Errorkeyword").className = "alert alert-danger text-danger";
            return false
        }
        if (!parseInt(tweets)) {
            this.setState({ tweetsError: 'La cantidad de Tweets debe ser numerica' })
            document.getElementById("Errortweets").className = "alert alert-danger text-danger"
            return false
        }
        return true
    }

    handleKeyChange = event => {
        this.setState({ keyword: event.target.value })
    };

    handleIdiomChange = event => {
        this.setState({ idioma: event.target.value })
    }
    handleTweetChange = event => {
        this.setState({ tweets: event.target.value })
    }
    desbloquearBoton = () => {
        document.getElementById("btnEnviar").disabled = false;
        document.getElementById("btnEnviar").innerHTML = "Enviar";
        document.getElementById("btnEnviar").className = "btn btn-primary";
        document.getElementById("inputKey").disabled = false;
    }

    render() {
        return (
            <div>
                <div className="align-middle">
                    <form onSubmit={this.handleSubmit}>
                        <p className="display-4 py-4 text-center">Iniciar Recoleccion</p>
                        <div className="form-group">
                            <label>Seleccione el idioma</label>
                            <select
                                className="form-control border border-primary"
                                onChange={this.handleIdiomChange}>
                                <option value="es">Español</option>
                                <option value="en">Ingles</option>
                            </select>
                            <div className="d-none" id="Erroridioma">{this.state.idiomaError}</div>
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
                            <div className="d-none" id="Errorkeyword">{this.state.keywordError}</div>
                        </div>
                        <div className="form-group">
                            <label>Cantidad de Tweets a recolectar</label>
                            <select
                                className="form-control border border-primary"
                                onChange={this.handleTweetChange}>
                                <option type="number" value="100">100</option>
                                <option value="1000">1,000</option>
                                <option value="10000">10,000</option>
                                <option value="100000">100,000</option>
                            </select>
                            <div className="d-none" id="Errortweets">{this.state.tweetsError}</div>
                        </div>
                        <div className="d-flex justify-content-center py-5">
                            <button
                                type="submit"
                                value="Submit"
                                id="btnEnviar"
                                className="btn btn-primary">
                                Enviar
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
}

export default connect(null, { addBusquedas })(Form);
