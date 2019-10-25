import React, { Component } from 'react';
import Axios from 'axios';

import Datos from './Data/Datos';
import Pagination from './Data/Pagination';

class DataTable extends Component {


    state = {
        loading: true,
        searchs: [],
        currentPage: 1,
        currentData: [],
        perpageData: 10,
    }

    componentDidMount() {
        this.getData();
        this.isLastPage();
    }
    getData = () => {
        this.setState({ loading: true }, () => {
            Axios.get('/static/tweetsp.json/')
                .then(result => this.setState({
                    loading: false,
                    searchs: [...result.data],
                    finalpage: false,
                }));
        });
    }

    setCurrentPage = (numberPage) => {
        this.setState({ currentPage: numberPage, });
    }

    setLastPage = (lastPage) => {
        this.setState({
            currentPage: lastPage,
            finalpage: true,
        });
    }

    isLastPage = () => {
        if (this.state.finalpage == true) {
            document.getElementById("second").innerHTML = "."
        }
    }


    render() {
        const numberPage = this.state.currentPage;
        const indexOfLastData = this.state.currentPage * this.state.perpageData;
        const indexOfFirstData = indexOfLastData - this.state.perpageData;
        const currentData = this.state.searchs.slice(indexOfFirstData, indexOfLastData);
        const lastPage = this.state.searchs.length / 10;
        return (
            <div className="mt-5 container text-center">
                <h1 className="mb-5 text-weight-bold">Tabla de Datos</h1>
                {this.state.loading ? <div className="d-flex justify-content-center">
                    <div className="spinner-border py-5 px-5" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
                    :
                    <Datos searchs={currentData} />
                }
                <nav aria-label="Page navigation example">
                    <ul className="pagination">
                        <li className="page-item">
                            <a className="btn page-link border" onClick={this.setCurrentPage.bind(this, 1)}>First</a>
                        </li>
                        <li className="page-item active" id="first">
                            <a className="btn page-link border">{numberPage}</a>
                        </li>
                        <li className="page-item">
                            <a className="btn page-link border" onClick={this.setCurrentPage.bind(this, numberPage + 1)} id="second">
                                {numberPage + 1}</a>
                        </li>
                        <li className="page-item">
                            <a className="btn page-link border" onClick={this.setCurrentPage.bind(this, numberPage + 2)} id="third">
                                {numberPage + 2}</a>
                        </li>
                        <li className="page-item">
                            <a className="btn page-link border" onClick={this.setLastPage.bind(this, lastPage)} id="last">
                                Last</a>
                        </li>
                    </ul>
                </nav>
            </div>
        )
    }
}


export default DataTable;