import React, { Component } from 'react';

// COMPONENTS
import Tabla from "./tabla";

class Section1 extends Component {
    render(){
        return(
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-6 my-4">
                        <Tabla data={this.props.data.slice(0,5)}/>
                    </div>
                    <div className="col-md-6 bg-light my-4">
                        <div class="jumbotron">
                            <h1 class="display-4">Hello, world!</h1>
                            <p class="lead">This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p>
                            <hr class="my-4" />
                                <p>It uses utility classes for typography and spacing to space content out within the larger container.</p>
                                <a class="btn btn-primary btn-lg" href="/" role="button">Learn more</a>
                        </div>
                    </div>
                </div>
                <footer className="bg-light mt-5 py-4 text-center border-0">
                    <div className="text-dark">
                        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nobis enim soluta aut aliquid est. Amet alias repellat optio
                        quae. Consectetur impedit repellendus dignissimos doloremque libero ut commodi ratione soluta officia.
                        </div>
                </footer>
            </div>
        )
    }
}

export default Section1;