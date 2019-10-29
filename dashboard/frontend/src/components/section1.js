import React, { Component } from 'react';

// COMPONENTS
import Tabla from "./tabla";
import Form from "./form";

class Section1 extends Component {
    render() {
        return (
            <div className="my-5">
                <div className="card">
                    <div className="card-body">
                        <div className="container-fluid">
                            <div className="row">
                                <div className="col-md-6 my-4">
                                    <Tabla />
                                </div>
                                <div className="col-md-6 bg-light my-4">
                                    <Form />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Section1;