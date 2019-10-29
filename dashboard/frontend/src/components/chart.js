import React, { Component } from 'react';
import Axios from 'axios';

import Bars from './graphs/bar'
import Pies from './graphs/pie'
import Dona from './graphs/dona';
import Hbar from './graphs/hbar';

class Chart extends Component {
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
                    searchs: [...result.data],
                }));
        });
    }
    render() {
        return (
            <div className="card container fluid my-5">
                <div className="card-body">
                    <div className="row">
                        <div className="col-xl-6 py-5">
                            <div className="card">
                                <div className="card-body">
                                    <Bars searchs={this.state.searchs} />
                                </div>
                            </div>
                        </div>
                        <div className="col-xl-6 py-5">
                            <div className="card">
                                <div className="card-body">
                                    <Pies searchs={this.state.searchs} />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="card-body">
                    <div className="row">
                        <div className="col-xl-6 py-5 d-none d-lg-block">
                            <div className="card">
                                <div className="card-body">
                                    <Dona searchs={this.state.searchs} />
                                </div>
                            </div>
                        </div>
                        <div className="col-xl-6 py-5">
                            <div className="card">
                                <div className="card-body">
                                    <Hbar searchs={this.state.searchs} />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        )
    }
}

export default Chart;