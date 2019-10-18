import React, { Fragment } from 'react';
import Form from './Form';
import Searchs from './Searchs';

export default function Dashboard() {
    return (
        <div>
            <Fragment>
                <div className="container py-5">
                    <div className="row">
                        <div className="col-6">
                            <Form />
                        </div>
                        <div className="col-6">
                            <Searchs />
                        </div>
                    </div>
                </div>
            </Fragment>
        </div>
    )
}
