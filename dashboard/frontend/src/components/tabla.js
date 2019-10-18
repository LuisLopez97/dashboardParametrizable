import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getSearchs } from '../actions/searchs';

class Tabla extends Component {
    static PropTypes = {
        searchs: PropTypes.array.isRequired,
        getsearchs: PropTypes.array.isRequired
    }

    componentDidMount() {
        this.props.getSearchs();
    }

    render() {
        return (
            <div className="table-responsive-md overflow-auto">
                <table className="table table-hover table-striped table-bordered table-sm">
                    <thead className="thead-dark">
                        <tr>
                            <th>Sentimiento</th>
                            <th>Rason del sentimiento</th>
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
            </div>)
    }
}

const mapStateToProps = state => ({
    searchs: state.searchs.searchs
})

export default connect(mapStateToProps, { getSearchs })(Tabla);