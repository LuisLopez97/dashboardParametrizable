import React, { Component, Fragment } from 'react'
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getSearchs, deleteSearchs } from '../../actions/searchs';

export class Searchs extends Component {
    static PropTypes = {
        searchs: PropTypes.array.isRequired,
        getSearchs: PropTypes.func.isRequired,
        deleteSearchs: PropTypes.func.isRequired
    };

    componentDidMount() {
        this.props.getSearchs();
    }
    render() {
        return (
            <Fragment>
                <h2 className="py-5">Tweets</h2>
                <table className="table table-striped py-5">
                    <thead>
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
            </Fragment >
        )
    }
}

const mapStateToProps = state => ({
    searchs: state.searchs.searchs
});

export default connect(mapStateToProps, { getSearchs, deleteSearchs })(Searchs);
