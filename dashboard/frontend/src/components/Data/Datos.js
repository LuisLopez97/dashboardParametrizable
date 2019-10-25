import React, { Component } from 'react'

export class Datos extends Component {
    render() {
        return (
            <div>
                <div className="table-responsive-md overflow-auto">
                    <table className="table table-hover table-striped table-bordered table-sm">
                        <thead className="thead-dark">
                            <tr>
                                <th>Sentimiento</th>
                                <th>Razon del sentimiento</th>
                                <th>Usuario</th>
                                <th>Texto</th>
                                <th>Ubicacion</th>
                            </tr>
                        </thead>
                        <tbody className="p-5">
                            {this.props.searchs.map(search => (
                                <tr key={search.id} className="p-5">
                                    <td>{search.airline_sentiment}</td>
                                    <td>{search.negativereason}</td>
                                    <td>{search.name}</td>
                                    <td>{search.text}</td>
                                    <td>{search.tweet_location}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
}

export default Datos
