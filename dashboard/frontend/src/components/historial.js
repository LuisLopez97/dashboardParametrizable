import React, { Component } from 'react';
import { connect } from 'react-redux';
import propTypes from 'prop-types';
import { getBusquedas } from '../actions/busquedas'
import Moment from 'react-moment';

export class Historial extends Component {
    static propTypes = {
        busquedas: propTypes.array.isRequired,
        getBusquedas: propTypes.func.isRequired,
    };

    componentDidMount() {
        this.props.getBusquedas();
    }
    render() {
        return (
            <div className="container">
                <div className="table-responsive-md overflow-auto pt-5">
                    <h1 className="text-center pb-4">Historial de Busquedas</h1>
                    <table className="table table-hover table-bordered table-sm">
                        <thead className="thead-dark">
                            <tr>
                                <th>Id</th>
                                <th>Idioma</th>
                                <th>Palabra</th>
                                <th>Cantidad de Tweets</th>
                                <th>Fecha de busqueda</th>
                            </tr>
                        </thead>
                        <tbody className="p-5">
                            {this.props.busquedas.map(busqueda => (
                                <tr key={busqueda.id} className="p-5">
                                    <td>{busqueda.id}</td>
                                    <td>{busqueda.lenguaje}</td>
                                    <td>{busqueda.palabraclave}</td>
                                    <td>{busqueda.cantidadtweets}</td>
                                    <td>
                                        <Moment format="DD/MM/YYYY">{busqueda.fechadebusqueda}</Moment>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
}

const mapStateToProps = state => ({
    busquedas: state.busquedas.busquedas
});

export default connect(mapStateToProps, { getBusquedas })(Historial);
