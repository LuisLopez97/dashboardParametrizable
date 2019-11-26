import React, { Component } from 'react';

class Tabla extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div className="table-responsive-md overflow-auto">
                <table className="table table-hover table-striped table-bordered table-sm">
                    <thead className="thead-dark">
                        <tr>
                            <th>Usuario</th>
                            <th>Texto</th>
                            <th>Fecha</th>
                            <th>Sentimiento</th>
                        </tr>
                    </thead>
                    <tbody className="p-5">
                        {this.props.datos.map(dato => (
                            <tr key={dato.id} className="p-5">
                                <td>{dato.Author}</td>
                                <td>{dato.Text}</td>
                                <td>{dato.Date}</td>
                                <td>{dato.Sentiment}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>)
    }
}

export default Tabla;