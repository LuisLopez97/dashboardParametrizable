import React, { Component } from 'react'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { addSearchs } from '../../actions/searchs';

export class Form extends Component {
    state = {
        keyWord: "",
    }

    static PropTypes = {
        addSearchs: PropTypes.func.isRequired
    };

    onChange = e => this.setState({ [e.target.name]: e.target.value });

    onSubmit = e => {
        e.preventDefault();
        const { keyWord } = this.state;
        const search = { keyWord };
        this.props.addSearchs(search);
    };

    render() {
        const { keyWord } = this.state;
        return (
            <div className="py-5">
                <h2 className="lead">Ingrese su Busqueda</h2>
                <form onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label>Palabra Clave</label>
                        <input
                            className="form-control"
                            type="text"
                            name="keyWord"
                            onChange={this.onChange}
                            value={keyWord}
                        />
                    </div>
                    <div className="form-group">
                        <button type="submit"
                            className="btn btn-primary">
                            Enviar
                        </button>
                    </div>
                </form>
            </div>
        )
    }
}

export default connect(null, { addSearchs })(Form);
