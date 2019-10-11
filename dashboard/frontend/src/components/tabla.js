import React, { Component } from 'react';

class Tabla extends Component {
    constructor(props) {
        super(props);
        this.getTitulo = this.getTitulo.bind(this);
        this.getDatos = this.getDatos.bind(this);
        this.getKeys = this.getKeys.bind(this);
    }

    getKeys = function () {
        return Object.keys(this.props.data[0]);
    }

    getTitulo = function () {
        var keys = this.getKeys();
        console.log(keys);
        return keys.map((key, index) => {
            return <th key={key}>{key.toUpperCase()}</th>
        })
    }

    getDatos = function () {
        var items = this.props.data;
        var keys = this.getKeys();
        return items.map(
            (row, index) => {
                return <tr key={index}> <RenderRow key={index} data={row} keys={keys} /> </tr>
            }
        )
    }
    getLoading = function () {
        if (this.props.loading) {
            return <h2>Loading...</h2>
        }
    }

    render() {
        console.log(this.props.data);
        return (
        <div className="table-responsive-md overflow-auto">
            {this.getLoading()}
                <table className="table table-hover table-striped table-bordered table-sm">
                <thead className="thead-dark">
                    <tr>{this.getTitulo()}</tr>
                </thead>
                <tbody>
                    {this.getDatos()}
                </tbody>
            </table>
        </div>)
    }
}

const RenderRow = (props) => {
    return props.keys.map((key, index) => {
        return <td key={props.data[key]}>{props.data[key]}</td>
    }
    )
}

export default Tabla;