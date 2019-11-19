import React, { Component } from 'react';
import Axios from 'axios';

class Tabla extends Component {
    state = {
        loading: true,
        searchs: [],
    }

    componentDidMount() {
        this.getData()
    }
    getData = () => {
        this.setState({ loading: true }, () => {
            Axios.get('/static/tweetsp.json/')
                .then(result => this.setState({
                    loading: false,
                    searchs: [...result.data.slice(0, 10)],
                }));
        });
    }
    render() {
        return (
            <div className="table-responsive-md overflow-auto">
                <table className="table table-hover table-striped table-bordered table-sm">
                    <thead className="thead-dark">
                        <tr>
                            <th>Sentimiento</th>
                            <th>Razón del sentimiento</th>
                            <th>Usuario</th>
                            <th>Texto</th>
                            <th>Ubicación</th>
                        </tr>
                    </thead>
                    <tbody className="p-5">
                        {this.state.searchs.map(search => (
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
            </div>)
    }
}

export default Tabla;