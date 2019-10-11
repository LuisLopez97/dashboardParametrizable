import React, { Component } from 'react';

class Footer extends Component {
    render(){
        return(
            <div className="card text-center rounded-0 border-dark">
                <div className="card-body bg-dark text-light">
                    <h5 className="card-title">Special title treatment</h5>
                    <p className="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <a href="/" class="btn btn-warning">Go somewhere</a>
                </div>
            </div>
        )
    }
}

export default Footer;